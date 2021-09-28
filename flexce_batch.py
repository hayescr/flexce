import os


class ChemevoModel:
    def __init__(self, filename, init_param=None):
        self.filename = filename
        self.initialize_model(**init_param)

    def initialize_model(self, radius=10., time_tot=12000., dt=30.,
                         imf='kroupa', mbins_low=0.1, mbins_high=100.,
                         dm_low=0.1, dm_high=1., dtd_func='exponential',
                         dtd_min_time=150., dtd_time=1500.,
                         dtd_snia_frac=0.135, inflow='exp',
                         m_init=2e10, M1=4e11, b1=6000.,
                         inflow_ab_pattern='bbns', inflow_met=1.0,
                         outflow_source='ism', outflow=2.5, warmgas='False',
                         sf_func='constant', sf_nu1=1e-9, sf_f1=0., sf_tau1=0.,
                         sf_tau2=0., N_kslaw=1.):

        self.radius = radius
        self.time_tot = time_tot
        self.dt = dt
        self.imf = imf
        self.mbins_low = mbins_low
        self.mbins_high = mbins_high
        self.dm_low = dm_low
        self.dm_high = dm_high
        self.dtd_func = dtd_func
        self.dtd_min_time = dtd_min_time
        self.dtd_time = dtd_time
        self.dtd_snia_frac = dtd_snia_frac
        self.inflow = inflow
        self.m_init = m_init
        self.M1 = M1
        self.b1 = b1
        self.inflow_ab_pattern = inflow_ab_pattern
        self.inflow_met = inflow_met
        self.outflow_source = outflow_source
        self.outflow = outflow
        self.warmgas = warmgas
        self.sf_func = sf_func
        self.sf_nu1 = sf_nu1
        self.sf_f1 = sf_f1
        self.sf_tau1 = sf_tau1
        self.sf_tau2 = sf_tau2
        self.N_kslaw = N_kslaw

    def write_config(self):
        outfile = open('./config/' + self.filename, 'w')
        print('# Simulation', file=outfile)
        print('# Fiducial', file=outfile)
        print('', file=outfile)
        print('# Yields', file=outfile)
        print('yields_snii_dir = limongi06/iso_yields/', file=outfile)
        print('yields_agb_dir = karakas10/iso_yields/', file=outfile)
        print('yields_snia_dir = iwamoto99/', file=outfile)
        print('yields_rprocess_dir = cescutti06/', file=outfile)
        print('yields_sprocess_dir = busso01/', file=outfile)
        print('yields_snia_model = w70', file=outfile)
        print('yields_r_elements = Ba, Eu', file=outfile)
        print('yields_s_elements = Ba,', file=outfile)
        print('', file=outfile)
        print('# Basic parameters', file=outfile)
        print('initialize_radius = {}'.format(self.radius), file=outfile)
        print('initialize_time_tot = {}'.format(self.time_tot), file=outfile)
        print('initialize_dt = {}'.format(self.dt), file=outfile)
        print('initialize_imf = {}'.format(self.imf), file=outfile)
        print('', file=outfile)
        print('# Mass bins', file=outfile)
        print('mass_bins_low = {}'.format(self.mbins_low), file=outfile)
        print('mass_bins_high = {}'.format(self.mbins_high), file=outfile)
        print('mass_bins_dm_low = {}'.format(self.dm_low), file=outfile)
        print('mass_bins_dm_high = {}'.format(self.dm_high), file=outfile)
        print('', file=outfile)
        print('# SNIa DTD', file=outfile)
        print('snia_dtd_func = {}'.format(self.dtd_func), file=outfile)
        print('snia_dtd_min_snia_time = {}'.format(
            self.dtd_min_time), file=outfile)
        print('snia_dtd_timescale = {}'.format(self.dtd_time), file=outfile)
        print('snia_dtd_snia_fraction = {}'.format(
            self.dtd_snia_frac), file=outfile)
        print('', file=outfile)
        print('# Inflow', file=outfile)
        print('inflows_func = {}'.format(self.inflow), file=outfile)
        print('inflows_mgas_init = {}'.format(self.m_init), file=outfile)
        print('inflows_M1 = {}'.format(self.M1), file=outfile)
        print('inflows_b1 = {}'.format(self.b1), file=outfile)
        print('inflows_inflow_ab_pattern = {}'.format(
            self.inflow_ab_pattern), file=outfile)
        print('inflows_inflow_metallicity = {}'.format(
            self.inflow_met), file=outfile)
        print('', file=outfile)
        print('# Outflow', file=outfile)
        print('outflows_outflow_source = {}'.format(
            self.outflow_source), file=outfile)
        print('outflows_eta_outflow = {}'.format(self.outflow), file=outfile)
        print('', file=outfile)
        print('# Warm ISM', file=outfile)
        print('warmgasres_warmgas = {}'.format(self.warmgas), file=outfile)
        print('', file=outfile)
        print('# Star Formation Law', file=outfile)
        print('sf_func = {}'.format(self.sf_func), file=outfile)
        print('sf_nu1 = {}'.format(self.sf_nu1), file=outfile)
        if self.sf_func == 'sf_gauss':
            print('sf_f1 = {}'.format(self.sf_f1), file=outfile)
            print('sf_tau1 = {}'.format(self.sf_tau1), file=outfile)
            print('sf_tau2 = {}'.format(self.sf_tau2), file=outfile)
        print('sf_N_kslaw = {}'.format(self.N_kslaw), file=outfile)
        print('', file=outfile)

    def run(self):
        self.write_config()
        os.chdir('./flexCE/')
        os.system('python flexce.py {}'.format('../config/' + self.filename))
        os.chdir('../')


class DwarfModel(ChemevoModel):
    '''
    Implementation:

    import flexce_batch as fb
    fb.DwarfModel('batch_dwarf.txt')
    '''

    def __init__(self, filename, time_tot=13000., inflow='te-t', m_init=3e9,
                 M1=6e10, b1=2500., outflow=10, sf_func='constant',
                 sf_nu1=1e-11, sf_f1=0., sf_tau1=0., sf_tau2=0.):
        self.filename = filename
        self.initialize_model(time_tot=time_tot, inflow=inflow, m_init=m_init,
                              M1=M1, b1=b1, outflow=outflow, sf_func=sf_func,
                              sf_nu1=sf_nu1, sf_f1=sf_f1, sf_tau1=sf_tau1,
                              sf_tau2=sf_tau2)
        self.run()
