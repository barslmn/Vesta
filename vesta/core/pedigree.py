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


class Pedigree(object):

    """Holds family name Individuals, Unions.
    This class has methods for counting marriages, founders etc."""

    def __init__(self, name, individuals):
        """TODO: to be defined. """
        self.name = name
        self._individuals = individuals
        pass

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
            hapmap_str += f'{self.name}\t{individual.name}\t{individual.parents.A}\t{individual.parents.B}\t{individual.sex.numeric}\t{individual.condition.numeric}\n'
        return hapmap_str


class Individual(object):

    """Holds attributes for an individual.
    name, sex, DoB, DoD,
    siblings, twins, parents"""

    def __init__(self, name, parents=None, sex='unknown', condition='normal', proband=False):
        self.name = name

        if parents is not None:
            self.parents = parents
        # If there are no parents set it to 0
        else:
            null_individual = Individual(name='0', parents='0')
            null_union = Union(null_individual, null_individual)
            self.parents = null_union

        self.sex = Sex(sex)
        self.condition = Condition(condition)
        self.proband = proband

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_siblings():
        """ List of Individual objects """
        pass

    def add_twins():
        """ Dictionary object"""
        pass


class Union(object):

    """Holds two individuals and union type"""

    def __init__(self, A, B):
        self.A = A
        self.B = B

    def __str__(self):
        return f'Union between {self.A} and {self.B}'

    def __repr__(self):
        return f'Union between {self.A} and {self.B}'


a = Individual('a')
b = Individual('b')
u = Union(a, b)
c = Individual('c', parents=u)
f = Pedigree('abc', [a, b, c])
print(f.unions)
print(f.hapmap())
