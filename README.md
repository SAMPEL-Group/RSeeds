# RSeeds
# Tim Yuan
# Sarupria Group
# Clemson University
# Created on 13th April, 2019

To perform the RSeed procedure, python3 and GROMACS (2018 preferred) are required.

The src folder contains two subfolders, and each subfolder has one python script.

combine-grofile: this script takes 2 gro files as input and outputs a combined gro file

rigid-generator: this script takes a gro file with ice seed and generates harmonic bond and angle potentials accordingly

seed-generator: this folder contains a script and necessary files to creat the seeds. A NOTES file is also available in the folder


The general folder contains files for the kaolinite-based kao_m surface, the ice seed, and a water slab.
A NOTES file is available for each subfolder under the general folder.


The test-case folder contains a working example to perform RSeed procedure on kao_m surface
To run this, cd into the run folder and use the command:

    source run.sh

Once the script finishes, check the configurations and trajectories in each folder (step1, step2, step3, and step4).

Detailed description of each step is avaiable in the corresponding run.sh file.

Hope you find this helpful.
