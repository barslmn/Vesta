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
    iii) Sibling line (Ls)
        Connects to a descent line from union line and

************
How it works
************
"""

from pedigree import Pedigree, Individual, Union
from features import Square, Circle, Line
from scipy.spatial.distance import cdist
import numpy as np
import sys


class PedigreeBuilder(object):
    ''' Build pedigree from set of given nodes and coordinates. '''

    def __init__(self, input_file):
        self.feature_types = ['node', 'edge']
        self.node_types = ['circle', 'square']
        self.edge_types = ['line']
        self.tolerance = .1
        self.created_nodes = {'as_parent': {}, 'as_child': {}}
        self.pedigree = Pedigree('foo')

        with open(input_file) as f:
            ls = f.read().splitlines()

        self.features = []
        for l in ls:
            feature_type = l.split('\t')[0]
            coordinates = [float(point)
                           for point in l.split('\t')[1].split(',')]
            name = l.split('\t')[2]
            if feature_type == 'circle':
                self.features.append(Circle(coordinates, name))
            elif feature_type == 'square':
                self.features.append(Square(coordinates, name))
            elif feature_type == 'line':
                self.features.append(Line(coordinates, name))
            else:
                sys.stdout.write('Feature type is not handled! O_o')

        for feature in self.features:
            self.get_connected_features(feature)

        # for f in self.features:
        #     if f.feature_type == 'edge':
        #         print(
        #             '*' * 50,
        #             '\n',
        #             f,
        #             '\n',
        #             '\t'.join([str(i) for i in f.connected]),
        #             '\n',
        #             '#' * 50
        #         )

    def min_distance(self, node, feature_types=False, dropped_features=False):
        'Get the distance of the two closest points between a feature and others'

        features = self.features
        # Drop features by types
        if feature_types:
            features = [
                feature for feature in self.features if feature.feature_type in feature_types]
        # Drop specific features
        if dropped_features:
            features = [
                feature for feature in self.features if feature not in dropped_features]

        cdists = {}
        for n in features:
            dist = cdist(node.junction_points, n.junction_points)
            cdists[n] = np.amin(dist)
        # print(
        #     '*' * 100,
        #     '\n',
        #     node,
        #     '\n',
        #     '\n'.join(['{}\t{}'.format(i, cdists[i]) for i in cdists]),
        #     '\n',
        #     '#' * 100
        # )
        return cdists

    def get_connected_features(self, node, distances=False):
        if not distances:
            distances = self.min_distance(node, dropped_features=(node,))
        connected_features = [
            f for f, d in distances.items() if d < self.tolerance]
        for feature in connected_features:
            node.append(feature)
        return connected_features

    def build_pedigree(self):
        ''' This function works recursively
        Stop condition is running out of
        union lines.
        '''
        edges = [f for f in self.features if f.feature_type == 'edge']
        union_lines = [line for line in edges if line.edge_type == 'lU']
        print('0')
        if not union_lines:
            print('1')
            pass
        else:
            print('2')
            lu = union_lines[0]

            parents = []
            for node in lu.get_connected('node'):
                print('3')
                parent = self.create_individual(node, 'as_parent')
                if parent:
                    parents.append(parent)

            union = self.create_union(parents)

            # lX because we don't know if its a lD or lUtS
            lX = lu.get_connected('edge')[0]
            ''' two possibilities for lX
                either LdUtS (multiple children) or LdUtC (single children)
                first hande for LdUtC '''
            # print(lX.name, lX.edge_type, '\n', [i.name for i in lX.connected], '\n' * 2)
            if lX.edge_type == 'lD':
                node = lX.get_connected('node')[0]
                self.create_individual(node, 'as_child', union)
                if node.count['edge'] > 1:
                    print('keep')
            # See feature.py Line.edge_types for explanation for line below.
            # In short, a lS wont be connected to a lU.
            elif lX.edge_type in ['lUtS', 'lS']:
                # find the lS
                lS = [line for line in lX.get_connected('edge') if line.edge_type == 'lS'][0]
                lDs = [line for line in lS.get_connected('edge') if line.edge_type == 'lD']
                print('#' * 20)
                for line in lS.get_connected('edge'):
                    print(line.name, line.edge_type, '\n', [f.name for f in line.connected], '\n' * 2)
                for lD in lDs:
                    node = lD.get_connected('node')[0]
                    self.create_individual(node, 'as_child', union)
                    if node.count['edge'] > 1:
                        print('keep')
            self.remove_feature(lu)
            self.build_pedigree()

    def create_individual(self, node, created_as, parents=None):
        if node.node_type == 'square':
            sex = 'male'
        if node.node_type == 'circle':
            sex = 'female'
        created_nodes = {node: indv for nodes in self.created_nodes.values()
                         for node, indv in nodes.items()}

        if node not in created_nodes:
            individual = Individual(node.name, parents=parents, sex=sex)
            self.created_nodes[created_as][node] = individual
            self.pedigree.append(individual)
            return individual
        else:
            return created_nodes[node]

    def create_union(self, nodes):
        A, B = nodes
        union = Union(A, B)
        return union

    def remove_feature(self, feature):
        self.features.remove(feature)
        pass


def test():
    input_file = 'test'
    pb = PedigreeBuilder(input_file)
    pb.build_pedigree()
    print(pb.pedigree.hapmap())


test()
