#!/bin/bash

#--------------------Step 2----------------------------------------------
#This step generate the .itp file to hold the seed rigid
python ../../../src/rigid-generator/ice_forcefield_public.py -i ../../general/ice/Ih100_162.gro -nameHW HWT4

#Now we place the seed on the surface
python ../../../src/combine-grofile/combin_grofile.py -i1 ../step1/kao-1stlayer.gro -i2 ../../general/ice/Ih100_162.gro -o seed-kao.gro

#Since there are frozen atoms on the surface, we need to generate an index file
gmx grompp -f ../../general/mdp_file/em_index.mdp -p ../../general/topology/seed-surf.top -c seed-kao.gro  -o em-seed-kao-index.tpr -maxwarn 100
gmx make_ndx -f em-seed-kao-index.tpr -o seed-kao_pre.ndx <<EOF
q
EOF
#The ../../general/index/kao-s2_f0.97-12x7x2_solv.ndx contains index for the frozen atoms in kaom surface 
cat seed-kao-slab_pre.ndx ../../general/index/kao-s2_f0.97-12x7x2_solv.ndx >seed-kao.ndx

#Now we will perform the first energy minimization, surface + interfacial water + seed
gmx grompp -f ../../general/mdp_file/em.mdp -p ../../general/topology/seed-surf.top -c seed-kao.gro -n seed-kao.ndx -o em-seed-kao.tpr -maxwarn 100
gmx mdrun -s em-seed-kao.tpr -v -deffnm em-seed-kao

#Once the energy minimization is done, we place the slab on the system
python ../../../src/combine-grofile/combin_grofile.py -i1 em-seed-kao.gro -i2 ../../general/slab/slab.gro -o seed-kao-slab.gro

#Another index file is required
gmx grompp -f ../../general/mdp_file/em_index.mdp -p ../../general/topology/seed-kao-slab.top -c seed-kao-slab.gro -o em-seed-kao-slab-index.tpr -maxwarn 100
gmx make_ndx -f em-seed-kao-slab-index.tpr -o seed-kao-slab_pre.ndx <<EOF
q
EOF
cat seed-kao-slab_pre.ndx   ../../general/index/kao-s2_f0.97-12x7x2_solv.ndx >seed-kao-slab.ndx

#Final energy minimization
gmx grompp -f ../../general/mdp_file/em.mdp -p ../../general/topology/seed-kao-slab.top -c  seed-kao-slab.gro -n seed-kao-slab.ndx -o em-seed-kao-slab.tpr -maxwarn 100
gmx mdrun -s em-seed-kao-slab.tpr -v -deffnm em-seed-kao-slab 


