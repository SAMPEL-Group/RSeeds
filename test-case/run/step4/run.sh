#!/bin/bash

#--------------------Step 4----------------------------------------------
#The bond and angle potentials are removed, therefore a new topology file is used
#First we generate an index file
gmx grompp -f ../../general/mdp_file/em_index.mdp -p ../../general/topology/kao-slab.top -c ../step3/anneal_300-240_kao.gro -o em_index_3.tpr  -maxwarn 100
gmx make_ndx -f em_index_3.tpr -o kao-slab_pre.ndx <<EOF
q
EOF
cat kao-slab_pre.ndx   ../../general/index/kao-s2_f0.97-12x7x2_solv.ndx > kao-slab.ndx

#Production run
gmx grompp -f ../../general/mdp_file/nvtprod-t240.mdp -p ../../general/topology/kao-slab.top -n kao-slab.ndx -c ../step3/anneal_300-240_kao.gro -o nvt_240_kao_prod_50ns.tpr -maxwarn 100
gmx mdrun -s  nvt_240_kao_prod_50ns.tpr -v -deffnm  nvt_240_kao_prod_50ns


