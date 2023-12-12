import numpy as np


def jacobi_sn(k_or_u, time, timeperiod):
    """
    Jacobi elliptic functions
    :param k_or_u:
    :param time:
    :param timeperiod:
    :return:
    """
    # Based on the article "https://doi.org/10.1016/j.jfluidstructs.2019.01.020"
    import scipy.special as sci
    # A(m) complete elliptic integral of first kind
    if 0 <= k_or_u < 1:
        # sn(4*A(sqr(K)*t/T, sqr(K))
        a_elliptic_integral = sci.ellipk(np.sqrt(k_or_u), out=None)
        sn = sci.ellipj(4 * a_elliptic_integral * time / timeperiod, np.sqrt(k_or_u))[0]
        angle_amplitude = sn
    elif -1 < k_or_u < 0:
        a_elliptic_integral = sci.ellipk(np.sqrt(np.abs(k_or_u)), out=None)
        cn = sci.ellipj(4 * a_elliptic_integral * time / timeperiod - a_elliptic_integral, np.sqrt(np.abs(k_or_u)))[1]
        angle_amplitude = cn
    else:
        angle_amplitude = "Error"
    return angle_amplitude
