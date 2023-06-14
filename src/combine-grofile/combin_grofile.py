#This code is written by Tim Yuan
#Last time modified 6th August, 2018
#This code combine two .gro files into 1
#Sarupria Group
#Clemson University

code ="combine_grofile.py"
modified = "6th August, 2018"

import sys
import os.path
import numpy as np
import argparse


def parseargs():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                            description="Tim Yuan\nSarupria Research Group\n"+modified+"\n\n"
                            "This code combine two .gro files:"
                            )
    parser.add_argument("-i1", "--inputfile_gro1", help="specify the first .gro file",
                       default="out.gro", metavar='')

    parser.add_argument("-i2", "--inputfile_gro2", help="specify the second gro file",
                       default="out.gro", metavar='')
    parser.add_argument("-o", "--outputfile", help="specify the name of the output file",
                       default="combined.gro", metavar='')

    parser.add_argument("-d", "--dimension", help="which .gro file has the correct dimension at the end(1/2)?",
                        default="1", metavar='')


    args = parser.parse_args()
    return args

args=parseargs()


def main():
    args = parseargs()
    f_gro1 = args.inputfile_gro1
    f_gro2 = args.inputfile_gro2
    f_o = args.outputfile
    dim = args.dimension
    gro_stored1 = []
    gro_stored2 = []


    if os.path.isfile(f_gro1):
        f_gro1_hand = open(f_gro1, 'r')
        grofile1 = f_gro1_hand.readlines()
        for line in grofile1[2:(len(grofile1)-1)]:
            gro_stored1.append(line)
            firstline_1 = grofile1[0]
            secondline_1 = grofile1[1]
            endline_1 = grofile1[-1]
            f_gro1_hand.close()
    else:
        print("First input gro file not found, please specify the correct name of the file")
        exit()


    if os.path.isfile(f_gro2):
        f_gro2_hand = open(f_gro2, 'r')
        grofile2 = f_gro2_hand.readlines()
        for line in grofile2[2:(len(grofile2)-1)]:
            gro_stored2.append(line)
            firstline_2 = grofile2[0]
            secondline_2 = grofile2[1]
            endline_2 = grofile2[-1]
            f_gro2_hand.close()

    else:
        print("Second input gro file not found, please specify the correct name of the file")
        exit()

    if dim=="1":
        endline = endline_1
    elif dim == "2":
        endline = endline_2
    else:
        print("Error in choosing the dimension of the final grofile, please choose 1 for the first grofile or 2 for the second grofile")

    f_o_hand = open(f_o, 'w')
    f_o_hand.write("Combine grofile of "+f_gro1+" "+f_gro1+"\n")
    f_o_hand.write(str(int(secondline_1)+int(secondline_2))+"\n")
    for line in gro_stored1:
        f_o_hand.write(line)
    for line in gro_stored2:
        f_o_hand.write(line)
    f_o_hand.write(endline)


# Boilerplate code to call main() function
if __name__ == '__main__':
    main()



