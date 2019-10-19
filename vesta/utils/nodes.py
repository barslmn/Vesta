class Node(object):

    """Docstring for Node. """

    def __init__(self):
        """TODO: to be defined. """

    def __eq__(self, other):
        return self.node_type == other

    def neighbours(self):
        pass


class Line(Node):

    def __init__(self, coordinates):
        self.x1 = coordinates[0]
        self.y1 = coordinates[1]
        self.x2 = coordinates[2]
        self.y2 = coordinates[3]

    def __str__(self):
        return f'Line at {self.x1, self.y1, self.x2, self.y2}'

    def __repr__(self):
        return f'Line at {self.x1, self.y1, self.x2, self.y2}'

    @property
    def node_type(self):
        return 'line'

    @property
    def junction_points(self):
        return [
            [self.x1, self.y1],
            [self.x2, self.y2],
        ]

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

    def __init__(self, coordinates):
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
        return [
            [self.x1 + self.r, self.y1],
            [self.x1 + self.r, self.y1],
            [self.x1, self.y1 + self.r],
            [self.x1, self.y1 + self.r],
        ]

    @property
    def diameter(self):
        return self.r * 2


class Square(Node):

    def __init__(self, coordinates):
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
