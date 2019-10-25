class Feature:

    """Docstring for Feature. """

    def __init__(self, name):
        self._connected = []
        self._name = name
        """TODO: to be defined. """

    def __str__(self):
        return 'Feature object'

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        self._name = _name

    @property
    def connected(self):
        return self._connected

    def get_connected(self, feature_type):
        return [f for f in self.connected if f.feature_type == feature_type]

    @property
    def count(self):
        f_types = [f.feature_type for f in self.connected]
        f_types = {
            'node': f_types.count('node'),
            'edge': f_types.count('edge'),
        }
        return f_types

    def append(self, connected):
        self.connected.append(connected)

    def remove(self, connected):
        self.connected.remove(connected)


class Edge(Feature):

    def __init__(self, name):
        super().__init__(name)
        pass

    @property
    def feature_type(self):
        return 'edge'


class Node(Feature):

    def __init__(self, name):
        super().__init__(name)
        pass

    @property
    def feature_type(self):
        return 'node'


class Line(Edge):

    def __init__(self, coordinates, name):
        super().__init__(name)
        self.x1 = coordinates[0]
        self.y1 = coordinates[1]
        self.x2 = coordinates[2]
        self.y2 = coordinates[3]

    def __str__(self):
        return f'Line at {self.x1, self.y1, self.x2, self.y2}'

    def __repr__(self):
        return f'Line at {self.x1, self.y1, self.x2, self.y2}'

    @property
    def edge_type(self):
        if self.count['node'] == 2 and self.count['edge'] == 1:
            return 'lU'
        if self.count['node'] == 1 and self.count['edge'] == 1:
            return 'lD'
        if self.count['node'] == 1 and self.count['edge'] == 2:
            ''' lD of middle child below connects to a node (middle child)
                and two lines; Ls and lUtS.
            '''
            return 'lD'
        if self.count['edge'] >= 3:
            return 'lS'
        if self.count['edge'] == 2:
            ''' This line may connect to just lU and lS

                  O---lU
                    |
                  -----lS
                  |   |
                  O   O

                or it also bind to a lD with lU, lS.

                  O---lU
                    |
                  -----lS
                  | | |lD
                  O O O    Middle child's lD connects to lUtS too.

                Second case makes this line classified as lS :((
            '''
            return 'lUtS'

    @property
    def junction_points(self):
        '''
            *-----*-----*

            *--*--*--*--*
        '''
        junction_points = [
            [self.x1, self.y1],
            [self.x2, self.y2],
            [(self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2],
        ]

        if self.orientation == 'horizontal':
            junction_points += [
                [self.x1 + self.width / 2, (self.y1 + self.y2) / 2],
                [self.x1 + self.width / 3, (self.y1 + self.y2) / 2],
                [self.x1 + self.width / 4, (self.y1 + self.y2) / 2],
            ]

        return junction_points

    @property
    def width(self):
        return abs(self.x2 - self.x1)

    @property
    def length(self):
        return abs(self.y2 - self.y1)

    @property
    def orientation(self):
        if self.length > self.width:
            return 'vertical'
        if self.width > self.length:
            return 'horizontal'


class Circle(Node):

    def __init__(self, coordinates, name):
        super().__init__(name)
        self.x1 = coordinates[0]
        self.y1 = coordinates[1]
        self.r = coordinates[2]

    def __str__(self):
        return f'Circle at {self.x1, self.y1, self.r}'

    def __repr__(self):
        return f'Circle at {self.x1, self.y1, self.r}'

    @property
    def node_type(self):
        return 'circle'

    @property
    def junction_points(self):
        r'''
              __*__
             /     \
            /       \
           |         |
           *         *
           |         |
            \       /
             \__*__/
        '''

        return [
            [self.x1 + self.r, self.y1],
            [self.x1 - self.r, self.y1],
            [self.x1, self.y1 + self.r],
            [self.x1, self.y1 - self.r],
        ]

    @property
    def diameter(self):
        return self.r * 2


class Square(Node):

    def __init__(self, coordinates, name):
        super().__init__(name)
        self.x1 = coordinates[0]
        self.y1 = coordinates[1]
        self.x2 = coordinates[2]
        self.y2 = coordinates[3]

    def __str__(self):
        return f'Square at {self.x1, self.y1, self.x2, self.y2}'

    def __repr__(self):
        return f'Square at {self.x1, self.y1, self.x2, self.y2}'

    @property
    def node_type(self):
        return 'square'

    @property
    def junction_points(self):
        ''' junction points marked with *
                   ___*___
                  |       |
                  |       |
                  *       *
                  |       |
                  |___*___|
        '''

        return [
            [self.x2 - abs(self.x2 - self.x1) / 2, self.y1],
            [self.x2 - abs(self.x2 - self.x1) / 2, self.y2],
            [self.x1, self.y2 - abs(self.y2 - self.y1) / 2],
            [self.x2, self.y2 - abs(self.y2 - self.y1) / 2],
        ]

    @property
    def width(self):
        return abs(self.x2 - self.x1)

    @property
    def length(self):
        return abs(self.y2 - self.y1)
