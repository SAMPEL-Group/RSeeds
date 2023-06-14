#!/bin/bash

#--------------------Step 3----------------------------------------------
gmx grompp -f ../../general/mdp_file/anneal-300-240.mdp -c ../step2/em-seed-kao-slab.gro -p ../../general/topology/seed-kao-slab.top -n ../step2/seed-kao-slab.ndx -o anneal_300-240_kao.tpr -maxwarn 100
gmx mdrun -s anneal_300-240_kao.tpr -v -deffnm anneal_300-240_kao -ntmpi 4


