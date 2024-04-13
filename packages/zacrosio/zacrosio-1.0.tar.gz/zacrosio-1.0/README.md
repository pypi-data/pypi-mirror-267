ZacrosIO
===========

This project is a collective of tools for the preparation of input files for Zacros.

## Installation

`pip install zacrosio`

`git clone https://github.com/hprats/ZacrosIO.git`

## Dependencies

Pandas, Scipy
 
## Example

In this example, we create the ZACROS input files for many KMC simulations scanning a wide range of partial pressures and temperatures for the CO oxidation.

    import numpy as np
    import pandas as pd
    from zacrosio.kmc_job import NewKMCJob

    job = NewKMCJob(df_gas=pd.read_csv(f'gas_data.csv', index_col=0),
                    df_mechanism=pd.read_csv(f'mechanism.csv', index_col=0),
                    df_energetics=pd.read_csv(f'energetics.csv', index_col=0),
                    lattice_path="lattice_input.dat")
    
    for T in np.linspace(500, 1000, 6):
        for pCO in np.logspace(-4, 0, 10):
            for pO in np.logspace(-4, 0, 10):
                job.create_job_dir(path=f"./co_oxidation_T_{T}_pCO_{pCO}_pO_{pO}",
                                   T=T,
                                   dict_pressure={'CO': pCO, 'O': pO},
                                   reporting='on time 5.0e-1',
                                   stopping={'max_steps': 'infinity', 'max_time': 'infinity', 'wall_time': 36000},
                                   repeat_cell=[10, 10],
                                   list_auto_scaling=['O_diffusion'])


## Dataframes required

The user must prepare three following Pandas dataframes in advance:

### 1. df_gas.csv 

This dataframe contains information about the gas-phase species. Each row corresponds to a gas-phase species, and the following columns are required:
- type (str): 'linear' or 'non_linear'
- gas_molec_weight (float): molecular weight in g/mol, e.g. 16.04
- sym_number (int): symmetry number, e.g. 1
- degeneracy (int): degeneracy of the ground state, for the calculation of the electronic partition function, e.g. 1
- inertia_list (list of floats): moments of intertia in amu*Å2 (1 or 3 elements for linear or non-linear molecules, respectively), e.g. [8.9]  # can be obtained from ase.Atoms.get_moments_of_inertia()
- gas_energy (float): formation energy in eV, e.g. -0.42

### 2. df_mechanism.csv

This dataframe contains information about the steps included in the reaction model, where each row of corresponds to a reversible elementary step. The following columns are required:
- site_types (str): type of adsorption sites, e.g. tM tC
- neighboring (str): connectivity between sites involved, e.g. 1-2. Optional (default: None)
- initial (list): initial configuration, e.g. ['1 * 1','2 CH3** 1','2 CH3** 2']
- final (list): final configuration, e.g. ['1 H_tC* 1','2 CH2** 1','2 CH2** 2']
- activ_eng (float): activation energy in eV, e.g. 1.02
- prox_factor (float): proximity factor, e.g. 0.2. Optional (default: 0.5)
- angles (str): angle between sites, e.g. 1-2-3:180. Optional (default: None)
- vib_list_is (list of floats): list of vibrational modes in meV for the initial state in meV, e.g. [332.7, 196.2, 70.5]
- vib_list_ts (list of floats): list of vibrational modes in meV for the transition state in meV, e.g. [332.7, 196.2]. For non-activated adsorption, define this as an empty list i.e. []
- vib_list_fs (list of floats): list of vibrational modes in meV for the final state in meV, e.g. [332.7, 196.2, 70.5]

Additional required columns for adsorption steps:
- molecule (str): gas-phase molecule involved, e.g. CO
- A_site (float): area of the adsoption site in Å, e.g. 4.28

### 3. df_energetics.csv

This dataframe contains information about the clusters included in the cluster expansion, where each row of corresponds to a cluster. The entries corresponding to point clusters and pairwise lateral interactions must end in '_point' and '_pair', respectively (e.g. CH3_point, CH2+H_pair) and the following columns are required:
- cluster_eng (float): cluster formation energy, e.g. -1.23
- site_types (str): type of adsorption sites, e.g. top top
- neighboring (str): connectivity between sites involved, e.g. 1-2
- lattice_state (list): cluster configuration, e.g. ['1 CO* 1','2 CO* 1']
- angles (str): angle between sites, e.g. 1-2-3:180. Optional (default: None)
- graph_multiplicity (int): symmetry number of the cluster, e.g. 2. Optional (default: None)

### 4. lattice_path (str)

Path were the lattice_input.dat file is located. This file has to be generated manually in advance. 

## Contributors

Hector Prats Garcia
