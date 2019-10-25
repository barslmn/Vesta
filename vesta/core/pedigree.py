class Sex(object):

    """Docstring for Sex. """

    def __init__(self, sex='unknown'):
        sexes = ['male', 'female', 'unknown']
        if sex in sexes:
            self.sex = sex
        else:
            raise ValueError(f'acceptable options are {", ".join(sexes)}')

    def __str__(self):
        return self.sex

    def __eq__(self, other):
        return self.sex == other

    @property
    def numeric(self):
        if self.sex == 'unknown':
            return 0
        if self.sex == 'male':
            return 1
        if self.sex == 'female':
            return 2


class Condition(object):
    """Docstring for Condition. """

    def __init__(self, condition):
        conditions = ['normal', 'obligatory', 'asymptomatic', 'affected']
        """TODO: to be defined. """
        if condition in conditions:
            self.condition = condition
        else:
            raise ValueError(
                f'acceptable conditions are {", ".join(conditions)}')

    @property
    def numeric(self):
        if self.condition == 'normal':
            return 1
        if self.condition == 'affected':
            return 2


class Pedigree:

    """Holds family name Individuals, Unions.
    This class has methods for counting marriages, founders etc."""

    def __init__(self, name, individuals=None):
        """TODO: to be defined. """
        self.name = name
        if individuals:
            self._individuals = individuals
        else:
            self._individuals = []

    def __str__(self):
        return self.name

    ##################
    # Attributes    #
    ##################
    @property
    def individuals(self):
        return self._individuals

    def append(self, individual):
        self.individuals.append(individual)
        self.proband = self.set_proband()

    def remove(self, individual):
        self.individuals.remove(individual)
        self.proband = self.set_proband()

    # @individuals.setter
    # def add_individual(self, Individual):
    #     self.individuals.append(Individual)

    def set_proband(self):
        proband = None
        for i in self.individuals:
            if proband is None and i.proband is True:
                proband = i
            elif proband is not None and i.proband is True:
                raise ValueError(f'Two probands found:{proband}, {i}')
            else:
                proband = None
        return proband

    @property
    def proband(self):
        return self.set_proband()

    @proband.setter
    def proband(self, individual):
        return self.set_proband()

    @property
    def unions(self):
        return [i.parents for i in self.individuals]

    #########################
    # Basic Stat Methods    #
    #########################
    def generations(self):
        pass

    def founders(self):
        pass

    #####################
    # Export Methods    #
    #####################
    def hapmap(self):
        hapmap_str = ''
        for individual in self.individuals:
            hapmap_str += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                self.name,
                individual.name,
                individual.parents.A,
                individual.parents.B,
                individual.sex.numeric,
                individual.condition.numeric,
            )
        return hapmap_str


class Individual(object):

    """Holds attributes for an individual.
    name, sex, DoB, DoD,
    siblings, twins, parents"""

    def __init__(self, name, parents=None, sex='unknown', condition='normal', proband=False):
        self.name = name

        if parents is not None:
            self._parents = parents
        # If there are no parents set it to 0
        else:
            null_individual = Individual(name='0', parents='0')
            null_union = Union(null_individual, null_individual)
            self._parents = null_union

        self.sex = Sex(sex)
        self.condition = Condition(condition)
        self.proband = proband

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, union):
        self._parents = union

    def add_siblings(self):
        """ List of Individual objects """
        pass

    def add_twins(self):
        """ Dictionary object"""
        pass


class Union(object):

    """Holds two individuals and union type"""

    def __init__(self, A, B):
        if A.name != '0' and B.name != '0':
            if A.sex == 'unknown' or B.sex == 'unknown':
                raise AttributeError(
                    'Individuals in a union expected to have their sex assigned.')
            if (A.sex == 'male' and B.sex == 'male') or (A.sex == 'female' and B.sex == 'female'):
                raise AttributeError(
                    'Individuals in a union expected to have opposite sex assigned.')

        if B.sex == 'male' and A.sex == 'female':
            self.A = B
            self.B = A
        else:
            self.A = A
            self.B = B

    def __str__(self):
        return f'Union between {self.A} and {self.B}'

    def __repr__(self):
        return f'Union between {self.A} and {self.B}'


def test():
    a = Individual('a', sex='male')
    b = Individual('b', sex='female')
    i = Individual('i', sex='female')
    j = Individual('j', sex='male')

    m = Union(a, b)
    n = Union(i, j)

    c = Individual('c', parents=m)
    f = Pedigree('abc', [a, b, c, i, j])
    print(f.unions)
    print(f.hapmap())
    c.parents = n
    print(f.hapmap())


# a = Individual('a', sex='male')
# p = Pedigree('foo')
# p.append(a)
# test()
