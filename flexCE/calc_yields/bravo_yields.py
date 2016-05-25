"""Convert Eduardo Bravo (in prep.) SNIa yields to pickled arrays."""

from __future__ import print_function, division, absolute_import

import os
from os.path import join
import sys

import numpy as np
import pandas as pd
import string

# ---- Set Paths -----
path_calc_yields = join(os.path.abspath(os.path.dirname(__file__)), '')  # TODO Uncomment when done debugging
# path_calc_yields = '/Users/andrews/flexCE/flexCE/calc_yields/'  # Remove when down debugging.................
path_flexce = join('/'.join(path_calc_yields.split('/')[:-2]), '')
path_fileio = join(path_flexce, 'fileio')
path_data = join(path_flexce, 'data')
path_yields = join(path_data, 'yields')
path_yldgen = join(path_yields, 'general')
path_bravo = join(path_yields, 'bravo')
sys.path.append(path_fileio)
# -------------------

from pickle_io import pickle_write


# ---- Eduardo Bravo (in prep.) SNIa yields ----

# models: DDTa, DDTc, DDTe, DDTf

# Read in yields
ddt_in = join(path_bravo, 'DDT_Yields_Z.dat')
data = {}
bravo_el = None
with open(ddt_in, 'r') as infile:
    for line in infile:
        if 'DDT' in line:
            model_name, model_metallicity = line.strip().split()
            if model_name not in data.keys():
                data[model_name] = {}
                data[model_name][model_metallicity] = {}
        else:
            parsed = line.strip().split('   ')
            tmp_sym = []
            tmp_yld = []
            for it in parsed:
                tmp_sym_ind, tmp_yld_ind = it.split(': ')
                tmp_sym.append(tmp_sym_ind)
                tmp_yld.append(float(tmp_yld_ind))
            if bravo_el is None:
                bravo_el = tmp_sym
            data[model_name][model_metallicity] = tmp_yld

bravo_el = np.array(bravo_el)

# Read in isotopes
species_in = pd.read_csv(join(path_yldgen, 'species.txt'),
                         delim_whitespace=True, skiprows=1, usecols=[1],
                         names=['name'])
species = np.array(species_in['name'])
n_species = len(species)

# Solar abundances are prevalence "by mass"
solar_isotopes = pd.read_csv(join(path_yldgen, 'Solar_isotopes.txt'),
                             delim_whitespace=True, skiprows=1,
                             usecols=[0, 1], names=['name', 'ab'])

# Map elemental yields onto dominant isotope
snia_sym = []
for it in bravo_el:
    ind_tmp = []
    for ii, siso in enumerate(solar_isotopes.name):
        # remove numbers from isotope name
        elname = ''.join([i for i in siso if not i.isdigit()])
        if it == elname:
            ind_tmp.append(ii)
    ind_dominant = np.argmax(solar_isotopes.ab[ind_tmp])
    snia_sym.append(solar_isotopes.name[ind_dominant])

snia_sym = np.array(snia_sym)

DDTa = pd.DataFrame(data['DDTa'], index=snia_sym)
DDTc = pd.DataFrame(data['DDTc'], index=snia_sym)
DDTe = pd.DataFrame(data['DDTe'], index=snia_sym)
DDTf = pd.DataFrame(data['DDTf'], index=snia_sym)

# Metallicity independent yields
snia_yields = {}
models = [DDTa, DDTc, DDTe, DDTf]
model_names = ['DDTa', 'DDTc', 'DDTe', 'DDTf']
for mod, mname in zip(models, model_names):
    for met in mod.keys():
        mzname = '_z'.join((mname, met))
        snia_yields[mzname] = np.zeros(n_species)
        for j in range(n_species):
            if species[j] in snia_sym:
                snia_yields[mzname][j] = mod[met].ix[np.where(snia_sym == species[j])[0][0]]

# write to file
for k in snia_yields.keys():
    pickle_write(snia_yields[k], join(path_bravo, k + '_yields.pck'))

# Metallicity dependent yields
# array of shape (1001, 293) for each model