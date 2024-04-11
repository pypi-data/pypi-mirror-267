#
# This file is part of the magnum.np distribution
# (https://gitlab.com/magnum.np/magnum.np).
# Copyright (c) 2023 magnum.np team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from magnumnp.common import logging, timedmethod, constants, DecoratedTensor
from .ode_solvers import RKF45
import torch

__all__ = ["LLGSolver"]

class LLGSolver(object):
    def __init__(self, terms, solver = RKF45, no_precession = False, **kwargs):
        self._terms = terms
        self._solver = solver(self.dm, **kwargs)
        self._no_precession = no_precession

    def dm(self, state, alpha = None):
        alpha = alpha or state.material["alpha"]

        gamma_prime = constants.gamma / (1. + alpha**2)
        alpha_prime = alpha * gamma_prime

        h = sum([term.h(state) for term in self._terms])

        dm = -alpha_prime * torch.linalg.cross(state.m, torch.linalg.cross(state.m, h))
        if not self._no_precession:
            dm -= gamma_prime * torch.linalg.cross(state.m, h)

        return dm

    def E(self, state):
        return sum([term.E(state) for term in self._terms])

    @timedmethod
    def step(self, state, dt, **kwargs):
        self._solver.step(state, dt, **kwargs)
        logging.info_blue("[LLG] step: dt= %g  t=%g" % (dt, state.t))

    @timedmethod
    def solve(self, state, tt, **kwargs):
        logging.info_blue("[LLG] solve: t0=%g  t1=%g Integrating ..." % (tt[0].cpu().numpy(), tt[-1].cpu().numpy()))
        res = self._solver.solve(state, tt, **kwargs)
        logging.info_green("[LLG] solve: t0=%g  t1=%g Finished" % (tt[0].cpu().numpy(), tt[-1].cpu().numpy()))
        return res

    @timedmethod
    def relax(self, state, maxiter = 500, rtol = 1e-6, dt = 1e-11):
        t0 = state.t
        E0 = self.E(state)

        for i in range(maxiter):
            self._solver.step(state, dt, alpha = 1.0) #, no_precession = True) # no_precession requires more iterations for SP4 demo!?

            # dm = f(state, t, m, alpha = 1.0)
            # |dm|.max()
            E = self.E(state)
            dE = torch.linalg.norm(((E - E0)/E).reshape(-1), ord = float("Inf"))
            logging.info_blue("[LLG] relax: t=%g dE=%g E=%g" % (state.t-t0, dE, E))
            if dE < rtol:
                break
            E0 = E

        state.t = t0
