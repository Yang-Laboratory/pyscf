#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

"""
DIIS
"""

from functools import reduce
import numpy
import pyscf.lib.diis
from pyscf.lib import logger


# J. Mol. Struct. 114, 31-34
# PCCP, 4, 11
# GEDIIS, JCTC, 2, 835
# C2DIIS, IJQC, 45, 31
# SCF-EDIIS, JCP 116, 8255
# error vector = SDF-FDS
# error vector = F_ai ~ (S-SDS)*S^{-1}FDS = FDS - SDFDS ~ FDS-SDF in converge
class DIIS(pyscf.lib.diis.DIIS):
    def update(self, s, d, f):
        sdf = reduce(numpy.dot, (s,d,f))
        errvec = sdf.T.conj() - sdf
        logger.debug1(self, 'diis-norm(errvec)=%g', numpy.linalg.norm(errvec))
        return pyscf.lib.diis.DIIS.update(self, f, xerr=errvec)

SCFDIIS = SCF_DIIS = DIIS
