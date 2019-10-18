"""
pb -stands for pedigree builder-
This program takes input formated as following

    node_type    coordinates
    square       0,1,2,3
    circle       1,2,3
    line         1,1,2,2

for the square; the first 2 integers denotes the bottom left corner
and the last 2 two integers the top right corner.

for the circle, the first 2 integers denotes the circle's center
and the last integer denotes circles radius.

for the line, the first 2 integers denotes the starting point
and the last 2 two integers denotes the end point.

***********
Definitions
***********
An individual can have two lines attached
that shows either descent or union.

There can be three types of lines:
    i) Union line (Lu)
        Shows marriage between two individuals.
    ii) Descent line (Ld)
        a) if there is single child
            Links individual to union line. (LdUtC)
        b) if there is multiple child
            Links sibling line to union line. (LdUtS)
            Links individual to sibling line. (LdStC)
    iii) Sibling line (Ls)
        Connects to a descent line from union line and

************
How it works
************
1. Pick a random square or circle.
2. Find linked lines. (Let's assume there can be two)
    2.1. For one line
        2.1.1. One can be descent or can be union.
        2.1.2. if line is linked to an another individual, its a union line.
                    * create a Union between two individuals.
                    * and go to union line function.
        2.1.3 if line is linked to an another line(Lx) its a Ld.
                    * Lx that Ld is linked to can be either LdUtS or Lu.
                    * If there node(s) connected to Lx then its a Lu.
                    * If there are other lines linked to Lx than its a LdUtS.
to be continued...
"""

# from vesta.pedigree import Pedigree, Individual, Union

# create a family
# family = pedigree.Pedigree('Test')
# create individual
# inda = Individual('A')
# indb = Individual('B')
# unionab = Union(inda, indb)
# family.add_individual(inda)
# family.add_individual(indb)
# family.add_union(unionab)
