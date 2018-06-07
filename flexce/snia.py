# @Author: Brett Andrews <andrews>
# @Date:   2018-06-06 12:06:40
# @Last modified by:   andrews
# @Last modified time: 2018-06-07 12:06:18

"""
FILE
    snia.py

DESCRIPTION
    Functions for computing the SNIa delay time distribution.
"""

import traceback

import numpy as np

import flexce.utils


def snia_dtd(func='exponential', kwargs=None):
    """Set SNIa delay time distribution.

    Args:
        func (str): functional form of DTD. Default is 'exponential'.
        kwargs (dict): keyword arguments to pass to individual DTD
            functions. Default is ``None``.

    Returns:
        dict: SNIa params
    """
    kwargs = flexce.utils.none_to_empty_dict(kwargs)
    snia_param = {'func': func, 'k': kwargs}
    try:
        # TODO use map
        if func == 'exponential':
            dtd_exp(**kwargs)
        elif func == 'power_law':
            dtd_powerlaw(**kwargs)
        elif func == 'prompt_delayed':
            dtd_prompt_delayed(**kwargs)
        elif func == 'single_degenerate':
            snia_dtd_single_degenerate(**kwargs)
    except TypeError:
        print(traceback.print_exc())
        print(
            '\nValid keywords:\n'
            'exponential: timescale, min_snia_time, snia_fraction\n'
            'power_law: min_snia_time, nia_per_mstar, slope\n'
            'prompt_delayed: A, B, min_snia_time\n'
            'single_degenerate: no keywords\n'
        )

    return snia_param


def dtd_exp(min_snia_time=150., timescale=1500., snia_fraction=0.078):
    """Implement exponential SNIa delay time distribution.

    If we adopt the SNIa prescription of Schoenrich & Binney (2009a)
    and a Salpeter IMF, 7.8% of the white dwarf mass formed form stars with
    initial mass between 3.2-8.0 Msun in a stellar population explodes as a
    SNIa (once we adjust to a mass range between 3.2-8.0 Msun instead of
    7.5% of the white dwarf mass that forms from stars of initial mass
    between 3.2-8.5 Msun).  For a Kroupa (2001) IMF, 5.5% of the white
    dwarf mass will explode as SNIa.

    Args:
        min_snia_time (float): Minimum delay time for SNIa in Myr.
            Default is 150.
        timescale (float): Exponential decay timescale of delay time
            distribution in Myr. Default is 1500.
        snia_fraction (float): Fraction of white dwarf mass formed from
           stars with initial mass M=3.2-8.0 Msun that will explode in
           SNIa (see extended description). Default is 0.078.
    """
    ind_min_t = (tstep -
                 np.ceil(self.min_snia_time / self.dt).astype(int))
    if ind_min_t > 0:
        Nia_stat = np.sum(self.Mwd_Ia[:ind_min_t+1] * self.dMwd /
                          snia_mass)
        self.Mwd_Ia[:ind_min_t+1] *= 1. - self.dMwd
    self.snia_fraction = snia_fraction
    self.min_snia_time = min_snia_time
    self.snia_timescale = timescale
    self.dMwd = self.dt / self.snia_timescale


def dtd_powerlaw(min_snia_time=40., nia_per_mstar=2.2e-3, slope=-1.):
    """Implement power-law SNIa delay time distribution.

    Args:
        min_snia_time (float): Minimum delay time for SNIa in Myr.
            Defaults to 150.
        nia_per_mstar (float): number of SNIa per stellar mass formed
            that explode within 10 Gyr. Defaults to 2.2e-3.
        slope (float): power law slope. Defaults to -1.
    """
    self.min_snia_time = min_snia_time
    ind_min = np.where(self.t >= min_snia_time)
    ind10000 = np.where(self.t <= 10000.)
    ria = np.zeros(len(self.t))
    ria[ind_min] = self.t[ind_min]**slope
    norm = nia_per_mstar / ria[ind10000].sum()
    self.ria = ria * norm


def dtd_prompt_delayed(A=4.4e-8, B=2.6e3, min_snia_time=40.):
    """Implement prompt plus delayed SNIa delay time distribution.

    Args:
        A (float): coefficient connected to stellar mass of galaxy
            (see extended description). Defaults to 4.4e-8.
        B (float): Defaults to 2.6e3.
        min_snia_time (float): Minimum delay time for SNIa in Myr.
            Defaults to 150.

    Scannapieco & Bildstein (2005) prompt + delayed components to SNIa
    rate Equation 1\:

    N_Ia / (100 yr)^-1 = A [Mstar / 10^10 Msun] +
    B [SFR / (10^10 Msun Gyr^-1)]

    A = 4.4e-2 (errors: +1.6e-2 -1.4e-2)

    B = 2.6 (errors: +/-1.1)

    In units useful for flexCE\:
    N_Ia per timestep = {4.4e-8 [Mstar / Msun] +
    2.6e3 [SFR / (Msun yr^-1)]} * (len of timestep in Myr)
    see also Mannucci et al. (2005)
    """
    self.prob_delay = A
    self.prob_prompt = B
    self.min_snia_time = min_snia_time
    return


def snia_dtd_single_degenerate(
    A=5e-4,
    gam=2.,
    eps=1.,
    normalize=False,
    nia_per_mstar=1.54e-3
):
    '''SNIa DTD for the single degenerate scenario (SDS).

    Solve for the SNIa rate (ria) according to Greggio (2005).  The minimum
    primary mass is either (1) the mass of the secondary, (2) the mass
    required to form a carbon-oxygen white dwarf (2 Msun), or (3) the mass
    needed such that the WD mass plus the envelope of the secondary
    (accreted at an efficiency [eps]) equals the Chandrasekhar limit (1.4
    Msun).
    '''
    t2 = np.arange(29., self.t[-1]+1., 1.)  # time in 1 Myr intervals
    m2 = invert_lifetime(t2)
    # mass_int2_tmp = self.integrate_multi_power_law(
    #     m2, self.alpha2 * -1, self.mass_breaks, self.mass_bins,
    #     self.normalize_imf() * -1)
    # num_int2_tmp = self.integrate_multi_power_law(
    #     m2, self.alpha1 * -1, self.mass_breaks, self.mass_bins,
    #     self.normalize_imf() * -1)
    # mass_ave2 = mass_int2_tmp / num_int2_tmp
    # a = 1. / self.mass_int.sum()
    # a2 = 1. / np.sum(mass_int2_tmp)
    # calculate the envelope mass of the secondary
    m2ca = 0.3 * np.ones(len(t2))
    m2cb = 0.3 + 0.1 * (m2 - 2.)
    m2cc = 0.5 + 0.15 * (m2 - 4.)
    m2c = np.max((m2ca, m2cb, m2cc), axis=0)  # secondary core mass
    m2e = m2 - m2c  # secondary envelope mass
    mwdn = 1.4 - (eps * m2e)  # minimum WD mass
    m1na = 2. * np.ones(len(t2))
    m1nb = 2. + 10. * (mwdn - 0.6)
    # min prim. mass set by min CO WD mass
    m1n = np.max((m1na, m1nb), axis=0)  # min prim. mass
    m1low1 = invert_lifetime(t2)
    m1low = np.max((m1low1, m1n), axis=0)  # min primary mass
    m1up = 8.
    k_alpha = self.num_int.sum() / self.mass_int.sum()
    nm2 = np.zeros(len(m1low))
    for i in range(len(self.alpha)):
        if i == 0:
            if len(self.mass_breaks) > 0:
                ind = np.where(np.around(m1low, decimals=5) <=
                               self.mass_breaks[0])[0]
            else:
                ind = np.arange(len(m1low), dtype=int)
            ind_int = ind[:-1]
        elif i != len(self.alpha) - 1:
            ind = np.where((m1low >= self.mass_breaks[i-1]) &
                           (m1low <= self.mass_breaks[i]))[0]
            ind_int = ind[:-1]
        else:
            ind = np.where(m1low >= self.mass_breaks[-1])[0]
            ind_int = ind
        nm2[ind_int] = ((m2[ind_int]**-self.alpha[i]) *
                        ((m2[ind_int]/m1low[ind_int])**(self.alpha[i]+gam) -
                         (m2[ind_int]/m1up)**(self.alpha[i] + gam)))
    # from Greggio (2005): t**-1.44 approximates log(dm/dt) = log(m) -
    # log(t), which works for either the Padovani & Matteucci (1993) or the
    # Greggio (2005)/Girardi et al. (2000) stellar lifetimes
    dm2dt = 10.**4.28 * t2**1.44
    fia2 = nm2 / dm2dt
    fia = fia2 / fia2.sum()
    ria1 = k_alpha * A * fia
    ind_tbin = np.where(t2 % self.dt == 0.)[0]
    self.ria = np.zeros(self.n_steps - 1)
    self.ria[0] = ria1[:ind_tbin[0]].sum()
    for i in range(1, self.n_steps - 1):
        self.ria[i] = ria1[ind_tbin[i-1]:ind_tbin[i]].sum()
    if normalize:
        ind10000 = np.where(self.t <= 10000.)
        self.ria = self.ria / self.ria[ind10000].sum() * nia_per_mstar


def snia_ev(params, tstep, dt, Mwd_Ia, dMwd, ria, mstar, snia_mass, mstar_tot, sfr):
    """Calculate the expected number of SNIa of a stellar population from
    a previous timestep.  The delay time distribution can be\:

    1. exponential
    2. empirical t^-1 power law
    3. empirical two component model with a prompt [~SFR] component and
       a delayed component [~Mstar]).
    4. theoretical DTD based on the single degenerate scenario

    Mannucci et al. (2005) find that the Rate SNIa / Rate SNII =
    0.35 +/- 0.08 in young stellar populations. Maoz et al. (2011) find
    that the time-integrated Rate SNII / Rate SNIa from a stellar
    population is about 5:1.

    snia_mass: mass of an individual SNIa

    min_snia_time: the minimum delay time from the birth of a stellar
    population
    """
    if params['snia']['func'] == 'exponential':
        ind_min_t = (tstep - np.ceil(params['snia']['min_time'] / dt).astype(int))
        if ind_min_t > 0:
            Nia_stat = np.sum(Mwd_Ia[:ind_min_t + 1] * dMwd / snia_mass)
            Mwd_Ia[:ind_min_t + 1] *= 1. - dMwd
            # TODO need to return Mwd_Ia
        else:
            Nia_stat = 0.

    elif params['snia']['func'] == 'power_law':
        Nia_stat = np.sum(ria[:tstep] * np.sum(mstar[1:tstep + 1], axis=1)[::-1])

    elif params['snia']['func'] == 'prompt_delayed':
        ind = tstep - np.ceil(params['snia']['min_time'] / dt)
        Nia_prompt = sfr[ind] * params['snia']['prob_prompt'] if ind > 0 else 0.
        Nia_delay = mstar_tot * params['snia']['prob_delay']
        Nia_stat = (Nia_prompt + Nia_delay) * dt

    elif params['snia']['func'] == 'single_degenerate':
        Nia_stat = np.sum(ria[:tstep] * np.sum(mstar[1:tstep + 1], axis=1)[::-1])

    return Nia_stat
