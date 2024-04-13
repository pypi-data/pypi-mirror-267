import numpy as np


def BV_gMod01(eta, c_sld, c_lyte, k0, E_A, T, act_R=None,
              act_lyte=None, lmbda=None, alpha=None):
    if act_R is None:
        act_R = c_sld/(1-c_sld)
    gamma_ts = (1./(c_sld*(1-c_sld)))
    ecd = (k0 * act_lyte**(1-alpha)
           * act_R**(alpha) / gamma_ts)
    Rate = ecd * np.exp(-E_A/T + E_A/1) * (np.exp(-alpha*eta/T) - np.exp((1-alpha)*eta/T))
    return Rate
