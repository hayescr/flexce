# @Author: Brett Andrews <andrews>
# @Date:   2018-06-06 12:06:40
# @Last modified by:   andrews
# @Last modified time: 2018-06-06 12:06:18

"""
FILE
    snia.py

DESCRIPTION
    Functions for computing the SNIa delay time distribution.
"""

import traceback

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
        if func == 'exponential':
            snia_dtd_exp(**kwargs)
        elif func == 'power_law':
            snia_dtd_powerlaw(**kwargs)
        elif func == 'prompt_delayed':
            snia_dtd_prompt_delayed(**kwargs)
        elif func == 'single_degenerate':
            snia_dtd_single_degenerate(**kwargs)
    except TypeError:
        print(traceback.print_exc())
        print(
            '\nValid keywords:\n'
            'exponential: timescale, min_snia_time, snia_fraction\n'
            'power_law: min_snia_time, nia_per_mstar, slope\n'
            'prompt_delayed: A, B,  min_snia_time\n'
            'single_degenerate: no keywords\n'
        )

    return snia_param
