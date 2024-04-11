ZacrosIOTools
===========

This project is a collective of tools for the preparation of input files for Zacros.

### Installation

To complete

### Dependencies

To complete
 
### Example

To complete

#### 1. simulation_tags (dict)

This dictionary contains the keyords related to the frequency of sampling and stopping criteria.

#### 2. df_gas.csv 

This dataframe contains information about the gas-phase species. Each row corresponds to a gas-phase species, and the following columns are required:
- type (str): 'linear' or 'non_linear'
- gas_molec_weight (float): molecular weight in g/mol, e.g. 16.04
- sym_number (int): symmetry number, e.g. 1
- degeneracy (int): degeneracy of the ground state, for the calculation of the electronic partition function, e.g. 1
- inertia_list (list of floats): moments of intertia in amu*Å2 (1 or 3 elements for linear or non-linear molecules, respectively), e.g. [8.9]  # can be obtained from ase.Atoms.get_moments_of_inertia()
- gas_energy (float): formation energy in eV, e.g. -0.42

#### 3. df_mechanism.csv

This dataframe contains information about the steps included in the reaction model, where each row of corresponds to a reversible elementary step. The following columns are required:
- sites (int): number of sites involved, e.g. 2
- site_types (str): type of adsorption sites, e.g. tM tC
- neighboring (str): connectivity between sites involved, e.g. 1-2
- initial (list): initial configuration, e.g. ['1 * 1','2 CH3** 1','2 CH3** 2']
- final (list): final configuration, e.g. ['1 H_tC* 1','2 CH2** 1','2 CH2** 2']
- activ_eng (float): activation energy in eV, e.g. 1.02
- prox_factor (float): proximity factor, e.g. 0.2    # default is 0.5
- angles (str): angle between sites, e.g. 1-2-3:180  # default is None
- vib_list_is (list of floats): list of vibrational modes in meV for the initial state in meV, e.g. [332.7, 196.2, 70.5]
- vib_list_ts (list of floats): list of vibrational modes in meV for the transition state in meV, e.g. [332.7, 196.2]. For non-activated adsorption, define this as an empty list i.e. []
- vib_list_fs (list of floats): list of vibrational modes in meV for the final state in meV, e.g. [332.7, 196.2, 70.5]

Additional required columns for adsorption steps:
- molecule (str): gas-phase molecule involved, e.g. CO
- A_site (float): area of the adsoption site in Å, e.g. 4.28

#### 4. df_energetics.csv

This dataframe contains information about the clusters included in the cluster expansion, where each row of corresponds to a cluster. The entries corresponding to point clusters and pairwise lateral interactions must end in '_point' and '_pair', respectively (e.g. CH3_point, CH2+H_pair) and the following columns are required:
- cluster_eng (float): cluster formation energy, e.g. -1.23
- sites (int): number of sites involved, e.g. 2
- site_types (str): type of adsorption sites, e.g. top top
- neighboring (str): connectivity between sites involved, e.g. 1-2
- lattice_state (list): cluster configuration, e.g. ['1 CO* 1','2 CO* 1']
- angles (str): angle between sites, e.g. 1-2-3:180  # default is None
- graph_multiplicity (int): symmetry number of the cluster, e.g. 2  # default is 1


#### 5. lattice_path (str)

Path were the lattice_input.dat file is located. This file has to be generated manually in advance. 


