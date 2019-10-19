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
"""

from nodes import Square, Circle, Line
from scipy.spatial.distance import cdist

# from vesta.pedigree import Pedigree, Individual, Union

# create a family
# family = pedigree.Pedigree('Test')
# create individual
# inda = Individual('A')
# indb = Individual('B')
# unionab = Union(inda, indb)
# family.add_individual(inda)
# family.append(indb)
# family.append(unionab)


class PedigreeBuilder(object):
    ''' Build pedigree from set of given nodes and coordinates. '''

    def __init__(self, input_file):
        with open(input_file) as f:
            lines = f.read().splitlines()

        self.nodes = []
        for line in lines:
            node_type = line.split('\t')[0]
            coordinates = [int(point)
                           for point in line.split('\t')[1].split(',')]
            if node_type == 'circle':
                self.nodes.append(Circle(coordinates))
            if node_type == 'square':
                self.nodes.append(Square(coordinates))
            if node_type == 'line':
                self.nodes.append(Line(coordinates))

    def find_neighbours(self, node):
        lines = [node for node in self.nodes if node == 'line']
        print('*' * 100)
        print('*' * 100)
        print('*' * 100)
        print(node, '\n', node.junction_points)
        for n in lines:
            dist = cdist(node.junction_points, n.junction_points)
            print('#' * 100)
            print(n)
            print('#' * 50)
            print(n.junction_points)
            print('#' * 50)
            print(dist)

    def build_pedigree(self):
        individuals = [node for node in self.nodes if node in ['square', 'circle']]
        for individual in individuals:
            self.find_neighbours(individual)
        # for individual find the closest line (L)
        # than find the closest thing(X) to that line
        # if X is a line that means X is either a LdUtC or LdStC
        # again find other node X connects to if its another individual X is a Lu
        # if X connects to another line that means X is Ls


input_file = 'test'
pb = PedigreeBuilder(input_file)
pb.build_pedigree()
