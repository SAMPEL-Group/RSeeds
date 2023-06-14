# This python code is written by Tim Yuan
# Last time modified 30th July, 2018
# This code creates index according to z direction
# Sarupria Group
# Clemson University


code = "cut_cap_slab.py" 
modified = "31st July, 2018"

import sys
import os.path
import numpy as np
import argparse


def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                            description="Tim Yuan\nSarupria Research Group\n"+modified+"\n\n"
                            "cut a spherical cap from a water slab:"
                            )
    parser.add_argument("-i", "--inputfile", help="specify the correct input file for water slab",
                       default="water_slab.gro", metavar='')

    parser.add_argument("-x", "--x_dimen", help="specify the x of the sphere origin",
                       default="0", metavar='')

    parser.add_argument("-y", "--y_dimen", help="specify the y of the sphere origin",
                       default="0", metavar='')

    parser.add_argument("-z", "--z_dimen", help="specify the z of the sphere origin",
                       default="0", metavar='')

    parser.add_argument("-r", "--radius", help="specify the radius of the sphere ",
                       default="0", metavar='')

    parser.add_argument("-o1", "--outputfile1", help="specify the name of the output file",
                       default="cut1.gro", metavar='')

    parser.add_argument("-o2", "--outputfile2", help="specify the name of the output2 file",
                       default="cut2.gro", metavar='')



    args = parser.parse_args()
    return args

args=parseargs()


def main():
    args = parseargs()
    f_in = args.inputfile
    f_out = args.outputfile1
    f_out2 = args.outputfile2
    ori_x = float(args.x_dimen)
    ori_y = float(args.y_dimen)
    ori_z = float(args.z_dimen)
    rcut = float(args.radius)
    listofatoms=[]    
    mol_list = {}

    if os.path.isfile(f_in):
        fin = open(f_in, 'r')
        fin_line=fin.readlines()
        for i in fin_line[2:len(fin_line)-1]:
            x = [i[0:5].strip(), i[5:10].strip(),i[10:15].strip(),i[15:20].strip(),i[20:28].strip(),i[28:36].strip(),i[36:44].strip()]
#This read the grofile line by line
#In case where there is no velocities in the grofile
#            print(x)
            if x[1]=="SOL":                                                        #Check if it is water molecules
                num=int(x[0])                                                      #get the molecule number
                listofatoms.append(i)
                if x[2] =="OW":
                    mol_list[num]=(x)
        dimension = fin_line[-1]
        x = dimension.split()
        boxx = float(x[0])
        boxy = float(x[1])
        boxz = float(x[2])
        fin.close()
    else:
        print("Input file not found")

#Now we have got the molecules information, we start to calculate the distances
    mol_list_cp=mol_list.copy()
    for i in list(mol_list):
        dx = (float(mol_list[i][4])-ori_x)
        dx = dx - boxx*np.round(dx/boxx) 
        dy = (float(mol_list[i][5])-ori_y)
        dy = dy - boxy*np.round(dy/boxy) 
#Note that I applied PBC for x and y direction but not z direction
        dist2 = dx**2+dy**2+(float(mol_list[i][6])-ori_z)**2
        if dist2<rcut**2:
            del mol_list[i]
        if dist2>=rcut**2:
            del mol_list_cp[i]
        
    fout=open(f_out, 'w')
    fout.write("cutted gro file\n")
    fout.write(str(len(mol_list)*4)+"\n")

    for i in range(len(listofatoms)):
        key=int(listofatoms[i][0:5].split()[0])
        if key in mol_list:
            fout.write(listofatoms[i])

    fout.write(fin_line[-1])
    fout.close()

    fout=open(f_out2, 'w')
    fout.write("cutted gro file\n")
    fout.write(str(len(mol_list_cp)*4)+"\n")

    for i in range(len(listofatoms)):
        key=int(listofatoms[i][0:5].split()[0])
        if key in mol_list_cp:
            fout.write(listofatoms[i])

    fout.write(fin_line[-1])
    fout.close()


# Boilerplate code to call main() function
if __name__ == '__main__':
    main()








