#!/bin/bash

#------------------------------------------------------------------------
#This file performs the RSeed precedure on kaom surface
#------------------------------------------------------------------------

for folder in step1 step2 step3 step4
do
    cd $folder
    source run.sh
    cd ../
done
