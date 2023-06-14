# This python code is written by Tim Yuan
# Last time modified 9th Nov, 2018
# Modified by Ryan 18th April, 2019
# This code creates topology (.itp) file for a given ice nucleus
# Sarupria Group
# Clemson University


code = "ice_force_field.py" 
modified = "9th Nov, 2018"

import sys
import os.path
import numpy as np
import argparse
import datetime

def main():
    args = parseargs()
    f_i = args.inputfile
    f_o = args.outputfile
    fc_bond = args.fc_bond
    fc_angle = args.fc_angle
    dcut=args.cutoff_distance
    cutoff2=dcut**2
    ow_pos=[]
    bond=[]
    angle=[]
    name_OW=args.nameOW
    name_HW=args.nameHW
    name_MW=args.nameMW

    #There is 1 type of bond length for O-O roughly 0.278nm
    #There is 1 type of angle for O-O-O roughly 109 degree
    if os.path.isfile(f_i):
        f_i_hand = open(f_i,'r')
        grofile=f_i_hand.readlines()
        # Assumes four point water model
        # Insert a assert statement here which requires
        # Divisibility by four.
        assert (int(grofile[1]) % 4) == 0, \
                "Error, number of atoms in gro file not consistent with four point water model."
        n=int(int(grofile[1])/4)
        for line in grofile[2:len(grofile)-1]:
            x = [line[0:5].strip(), line[5:10].strip(),line[10:15].strip(),line[15:20].strip(),line[20:28].strip(),line[28:36].strip(),line[36:44].strip()]
            assert x[2] == 'OW' or x[2] == 'HW1' or x[2] == 'HW2' or x[2] == 'MW', \
                    """ Error, name other than OW, HW1, HW2, MW in gro file. This may 
                        or may not cause problems. Modify code at your own risk. """

            if x[2]=='OW':
                pos_vec=[float(x[4]),float(x[5]),float(x[6]),int(x[3])]
                ow_pos.append(pos_vec)
    else:
        print("No file found, please input the correct name of the ice gro file")
        exit()
    np_ow_pos=np.asarray(ow_pos)

    #--------------------------------------------------------------------------------------------------------
    # Since we do not know the order or the water molecules and its ice structure, we have to 
    # identify it using the input gro file, this requires bond calculation, angle calculation
    #--------------------------------------------------------------------------------------------------------
    
    for i in range(len(np_ow_pos)):
        for j in range(i+1,len(np_ow_pos)):
            dis2=(np_ow_pos[i][0]-np_ow_pos[j][0])**2+(np_ow_pos[i][1]-np_ow_pos[j][1])**2+(np_ow_pos[i][2]-np_ow_pos[j][2])**2
            if dis2<cutoff2:
                bond.append([int(np_ow_pos[i][3]),int(np_ow_pos[j][3])])

    print('Successfully constructed the bonds in the ice')

    for i in range(len(bond)):
        bnd1 = bond[i]
        at1_1 = bnd1[0]
        at1_2 = bnd1[1]
        for j in range(i+1,len(bond)):
            bnd2 = bond[j]
            at2_1 = bnd2[0] 
            at2_2 = bnd2[1]
            if bnd1 != bnd2:
                if at1_1 == at2_1:
                    angle.append([at1_2,at1_1,at2_2])
                elif at1_1 == at2_2:
                    angle.append([at1_2,at1_1,at2_1])
                elif at1_2 == at2_1:
                    angle.append([at1_1,at1_2,at2_2])
                elif at1_2 == at2_2:
                    angle.append([at1_1,at1_2,at2_1])

    print('Successfully constructed the angles in the ice')
#--------------------------------------blablabla---------------------------------------------------------
    f_o_hand = open(f_o, 'w')
    f_o_hand.write('; Tim Yuan\n; Sarupria Research Group\n; Clemson University\n; ' +str(datetime.datetime.now())+'\n\n')
#--------------------------------------Molecule Type-----------------------------------------------------
    f_o_hand.write('[ moleculetype ]\n')
    f_o_hand.write('; molname   nrexcl\n')
    f_o_hand.write('SIL         0\n\n')
#--------------------------------------Atoms-------------------------------------------------------------
    f_o_hand.write('[ atoms ]\n')
    f_o_hand.write(';   id  at type     resnr   resname     atname      cgnr    charge      mass\n')
    for i in range(n):
        f_o_hand.write("\t{:7s}{:11s}{:9s}{:12s}{:12s}{:9s}{:12s}{:12s}\n".format(str(4*i+1),name_OW,'1','SIL','OWI',str(i+1),'0.0', '15.9994'))
        f_o_hand.write("\t{:7s}{:11s}{:9s}{:12s}{:12s}{:9s}{:12s}{:12s}\n".format(str(4*i+2),name_HW,'1','SIL','HW1I',str(i+1),'0.5897', '1.008'))
        f_o_hand.write("\t{:7s}{:11s}{:9s}{:12s}{:12s}{:9s}{:12s}{:12s}\n".format(str(4*i+3),name_HW,'1','SIL','HW2I',str(i+1),'0.5897', '1.008'))
        f_o_hand.write("\t{:7s}{:11s}{:9s}{:12s}{:12s}{:9s}{:12s}{:12s}\n".format(str(4*i+4),name_MW,'1','SIL','MWI',str(i+1),'-1.1794', '0.000'))
#--------------------------------------Constraints-------------------------------------------------------
    f_o_hand.write('\n[ constraints ]\n')
    f_o_hand.write(';     ai        aj      funct       length\n')
    for i in range(n):
        f_o_hand.write("{:7s}{:7s}{:7s}{:12s}\n".format(str(4*i+1),str(4*i+2),'1','0.09572'))
        f_o_hand.write("{:7s}{:7s}{:7s}{:12s}\n".format(str(4*i+1),str(4*i+3),'1','0.09572'))
        f_o_hand.write("{:7s}{:7s}{:7s}{:12s}\n".format(str(4*i+2),str(4*i+3),'1','0.15139'))
#---------------------------------------Exclusions-------------------------------------------------------       
    f_o_hand.write('\n[ exclusions ]\n')
    for i in range(n):
        f_o_hand.write("{:7s}{:7s}{:7s}{:7s}\n".format(str(4*i+1),str(4*i+2),str(4*i+3),str(4*i+4)))
        f_o_hand.write("{:7s}{:7s}{:7s}{:7s}\n".format(str(4*i+2),str(4*i+1),str(4*i+3),str(4*i+4)))
        f_o_hand.write("{:7s}{:7s}{:7s}{:7s}\n".format(str(4*i+3),str(4*i+1),str(4*i+2),str(4*i+4)))
        f_o_hand.write("{:7s}{:7s}{:7s}{:7s}\n".format(str(4*i+4),str(4*i+1),str(4*i+2),str(4*i+3)))

#---------------------------------------Virtual Sites----------------------------------------------------
    f_o_hand.write('\n[ virtual_sites3 ]\n')
    f_o_hand.write(';  Vsite from                   funct           a         b   \n')
    for i in range(n):
        f_o_hand.write("{:9s}{:9s}{:9s}{:9s}{:9s}{:13s}{:13s}\n".format(str(i*4+4),str(i*4+1),str(i*4+2),str(i*4+3),'1','0.134583351', '0.134583351'))

#----------------------------------------Bonds----------------------------------------------------------- 
    f_o_hand.write('\n[ bonds ]\n')
    f_o_hand.write(';      ai      aj      funct       c0      c1      c2      c3\n')
    for bnd in bond:
        f_o_hand.write("{:<7d}{:<7d}{:7s}{:12s}{:15s}\n".format(bnd[0],bnd[1],'1','0.27800',str(fc_bond)))
 
#----------------------------------------Angles---------------------------------------------------------- 
    f_o_hand.write('\n[ angles ]\n')
    f_o_hand.write(";   ai      aj      ak      funct       c0      c1      c2      c3\n")
    for ang in angle:
        f_o_hand.write("{:<7d}{:<7d}{:<7d}{:7s}{:12s}{:15s}\n".format(ang[2],ang[1],ang[0],'1','108.6',str(fc_angle)))
 
#----------------------------------------Dihedrals-------------------------------------------------------
# None used

#----------------------------------------Close the file handle-------------------------------------------

    f_o_hand.close()

def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                            description="Tim Yuan & Ryan DeFever\nSarupria Research Group\n"+modified+"\n\n"
                            "This code generate a .itp file according to an input gro file.\n"  
                            "This code assumes the input file is a perfect ice lattice and uses 4 site water model.\n"
                            "The name for oxygen, hydrogen, and vitural site should be 'OW', 'HW1', 'HW2', and 'MW'."
                            )
    parser.add_argument("-i", "--inputfile", help="The name of input file, note that the input gro file must be an ice nucleus",
                       default="nucleus.gro", metavar='')
    parser.add_argument("-o", "--outputfile", help="specify the name of the output file",
                       default="nucleus.itp", metavar='')
    parser.add_argument("-fcb", "--fc_bond", help="force constant for artificial bond (kJ/nm^2*mol)",
                        default="7000.0", type=float, metavar='')
    parser.add_argument("-fca", "--fc_angle", help="force constant for artificial angle (kJ/rad^2*mol)",
                        default="20.0", type=float, metavar='')
    parser.add_argument("-dcut", "--cutoff_distance", help="O-O bond cutoff distance, default 0.33nm",
                        default="0.33", type=float, metavar='')
    parser.add_argument("-nameOW", "--nameOW", help="atom type for OW",
                        default="OWT4", metavar='')
    parser.add_argument("-nameHW", "--nameHW", help="atom type for HW",
                        default="HW", metavar='')
    parser.add_argument("-nameMW", "--nameMW", help="atom type for MW",
                        default="MWW", metavar='')

    args = parser.parse_args()
    return args


# Boilerplate code to call main() function
if __name__ == '__main__':
    main()


