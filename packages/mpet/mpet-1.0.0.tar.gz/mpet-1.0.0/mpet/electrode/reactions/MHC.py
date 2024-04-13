import numpy
import numpy as np
from .MHC_kfunc import MHC_kfunc


def MHC(eta, c_sld, c_lyte, k0, E_A, T, act_R=None,
        act_lyte=None, lmbda=None, alpha=None):
    # See Zeng, Smith, Bai, Bazant 2014
    # Convert to "MHC overpotential"
    k0 = k0/MHC_kfunc(0., lmbda)
    eta_f = eta + T*np.log(c_lyte/c_sld)
    gamma_ts = 1./(1. - c_sld)
    alpha = 0.5
    ecd_extras = act_lyte**(1-alpha) * act_R**(alpha) / (gamma_ts*np.sqrt(c_lyte*c_sld))
    if isinstance(eta, np.ndarray):
        Rate = np.empty(len(eta), dtype=object)
        for i, etaval in enumerate(eta):
            krd = k0*MHC_kfunc(-eta_f[i], lmbda)
            kox = k0*MHC_kfunc(eta_f[i], lmbda)
            Rate[i] = ecd_extras[i]*(krd*c_lyte - kox*c_sld[i])
    else:
        krd = k0*MHC_kfunc(-eta_f, lmbda)
        kox = k0*MHC_kfunc(eta_f, lmbda)
        Rate = np.exp(-E_A/T + E_A/1) * ecd_extras*(krd*c_lyte - kox*c_sld)
    return Rate
