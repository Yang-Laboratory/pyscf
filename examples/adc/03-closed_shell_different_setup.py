#!/usr/bin/env python

'''
IP/EA-ADC calculations for closed-shell N2
'''

from pyscf import gto, scf, adc

mol = gto.Mole()
r = 1.098
mol.atom = [
    ['N', ( 0., 0.    , -r/2   )],
    ['N', ( 0., 0.    ,  r/2)],]
mol.basis = {'N':'aug-cc-pvdz'}
mol.build()

mf = scf.RHF(mol)
mf.conv_tol = 1e-12
mf.kernel()

myadc = adc.ADC(mf)
myadc.kernel_gs()

#IP-ADC(2)
myadc.verbose = 4
myadcip = adc.radc.RADCIP(myadc)
eip,vip,pip = myadcip.kernel(nroots=3)

#EA-ADC(3)
myadc.method = "adc(3)"
myadc.kernel_gs()
myadcea = adc.radc.RADCEA(myadc)
eea,vea,pea = myadcea.kernel(nroots=3)

#IP/EA-ADC(3) for 1 root
eip,vip,pip = myadc.ip_adc()
eea,vea,pea = myadc.ea_adc()
