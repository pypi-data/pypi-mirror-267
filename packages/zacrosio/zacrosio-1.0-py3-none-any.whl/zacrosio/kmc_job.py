import os
from random import randint
from zacrosio.input_files.energetics_input import EnergeticModel
from zacrosio.input_files.mechanism_input import ReactionModel
from zacrosio.input_files.lattice_input import LatticeModel
from zacrosio.input_functions import write_header


class NewKMCJob:
    """A class that represents a new KMC job with ZACROS.

    Parameters:

    df_gas: Pandas dataframe
        Informaton about the gas molecules (see README.md)
    df_mechanism: Pandas dataframe
        Informaton on the reaction model (see README.md)
    df_energetics: Pandas dataframe
        Informaton on the energetic model (see README.md)
    lattice_path: str
        The path of the lattice_input.dat (previously created).

    Example:
    >>> import numpy as np
    >>> import pandas as pd
    >>> from zacrosio.kmc_job import NewKMCJob
    >>>
    >>> job = NewKMCJob(
    >>>    df_gas=pd.read_csv(f'gas_data.csv', index_col=0),
    >>>    df_mechanism=pd.read_csv(f'mechanism.csv', index_col=0),
    >>>    df_energetics=pd.read_csv(f'energetics.csv', index_col=0),
    >>>    lattice_path="lattice_input.dat")
    >>>
    >>>for T in np.linspace(500, 1000, 6):
    >>>    for pCO in np.logspace(-4, 0, 10):
    >>>        for pO in np.logspace(-4, 0, 10):
    >>>            job.create_job_dir(path=f"./co_oxidation_T_{T}_pCO_{pCO}_pO_{pO}",
    >>>                               T=T,
    >>>                               dict_pressure={'CO': pCO, 'O': pO},
    >>>                               reporting='on time 5.0e-1',
    >>>                               stopping={'max_steps': 'infinity', 'max_time': 'infinity', 'wall_time': 36000},
    >>>                               repeat_cell=[10, 10],
    >>>                               list_auto_scaling=['O_diffusion'])
    """

    def __init__(self, df_gas, df_mechanism, df_energetics, lattice_path):
        self.path = None
        self.df_gas = df_gas
        self.reaction_model = ReactionModel(df=df_mechanism)
        self.energetic_model = EnergeticModel(df=df_energetics)
        self.lattice_model = LatticeModel(path=lattice_path)

    def create_job_dir(self, path, T, dict_pressure, reporting=None, stopping=None, repeat_cell=None, dict_manual_scaling=None,
                       list_auto_scaling=None, scaling_tags=None):
        """Creates a new directory and writes there the ZACROS input files"""
        if scaling_tags is None:
            scaling_tags = {}
        if list_auto_scaling is None:
            list_auto_scaling = []
        if dict_manual_scaling is None:
            dict_manual_scaling = {}
        self.path = path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            self.write_simulation(T=T, reporting=reporting, stopping=stopping, dict_pressure=dict_pressure,
                                  list_auto_scaling=list_auto_scaling, scaling_tags=scaling_tags)
            self.reaction_model.write(path=self.path, T=T, df_gas=self.df_gas, dict_manual_scaling=dict_manual_scaling,
                                      list_auto_scaling=list_auto_scaling)
            self.energetic_model.write(path=self.path)
            if repeat_cell is not None:
                self.lattice_model.update_size(size=repeat_cell)
            self.lattice_model.write(path=self.path)
        else:
            print(f'{self.path} already exists (nothing done)')

    def write_simulation(self, T, reporting, stopping, dict_pressure, list_auto_scaling, scaling_tags):
        """Writes the simulation_input.dat file"""
        gas_specs_names = [x for x in self.df_gas.index]
        surf_specs_names = [x.replace('_point', '') for x in self.energetic_model.df.index if '_point' in x]
        surf_specs_names = [x + '*' * int(self.energetic_model.df.loc[f'{x}_point', 'sites']) for x in surf_specs_names]
        surf_specs_dent = [x.count('*') for x in surf_specs_names]
        write_header(f"{self.path}/simulation_input.dat")
        with open(f"{self.path}/simulation_input.dat", 'a') as infile:
            infile.write('random_seed\t'.expandtabs(26) + str(randint(100000, 999999)) + '\n')
            infile.write('temperature\t'.expandtabs(26) + str(float(T)) + '\n')
            p_tot = sum(dict_pressure.values())
            infile.write('pressure\t'.expandtabs(26) + str(p_tot) + '\n')
            infile.write('n_gas_species\t'.expandtabs(26) + str(len(gas_specs_names)) + '\n')
            infile.write('gas_specs_names\t'.expandtabs(26) + " ".join(str(x) for x in gas_specs_names) + '\n')
            tags_dict = ['gas_energy', 'gas_molec_weight']
            tags_zacros = ['gas_energies', 'gas_molec_weights']
            for tag1, tag2 in zip(tags_dict, tags_zacros):
                tag_list = [self.df_gas.loc[x, tag1] for x in gas_specs_names]
                infile.write(f'{tag2}\t'.expandtabs(26) + " ".join(str(x) for x in tag_list) + '\n')
            gas_molar_frac_list = [dict_pressure[x] / p_tot for x in gas_specs_names]
            infile.write(f'gas_molar_fracs\t'.expandtabs(26) + " ".join(str(x) for x in gas_molar_frac_list) + '\n')
            infile.write('n_surf_species\t'.expandtabs(26) + str(len(surf_specs_names)) + '\n')
            infile.write('surf_specs_names\t'.expandtabs(26) + " ".join(str(x) for x in surf_specs_names) + '\n')
            infile.write('surf_specs_dent\t'.expandtabs(26) + " ".join(str(x) for x in surf_specs_dent) + '\n')
            for tag in ['snapshots', 'process_statistics', 'species_numbers']:
                infile.write((tag + '\t').expandtabs(26) + reporting + '\n')
            for tag in ['max_steps', 'max_time', 'wall_time']:
                infile.write((tag + '\t').expandtabs(26) + str(stopping[tag]) + '\n')
            if len(list_auto_scaling) > 0:
                infile.write(f"enable_stiffness_scaling\n")
                for tag in scaling_tags:
                    infile.write((tag + '\t').expandtabs(26) + str(scaling_tags[tag]) + '\n')
            infile.write(f"finish\n")
