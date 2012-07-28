from abc import abstractmethod, abstractproperty
from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from experimental.quantizationtools import QGrid
import copy


class SearchTree(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_definition',)

    ### INITIALIZER ###

    def __init__(self, definition=None):
        if definition is None:
            definition = self.default_definition
        else:
            assert self.is_valid_definition(definition)
        self._definition = definition

    ### SPECIAL METHODS ###

    def __call__(self, q_grid):
        assert isinstance(q_grid, QGrid)
        indices, subdivisions = self.find_divisible_leaf_indices_and_subdivisions(q_grid)
        combinations = [x for x in sequencetools.yield_outer_product_of_sequences(subdivisions)]
        new_q_grids = []
        for combo in combinations:
            zipped = zip(indices, combo)
            q_events = copy.copy(q_grid).subdivide_leaves(zipped)
        return new_q_grids, q_events

    def __eq__(self, other):
        if type(self) == type(other):
            if self.definition == other.definition:
                return True
        return False

    def __getnewargs__(self):
        return self.definition

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @abstractproperty
    def default_definition(self):
        raise NotImplemented

    @property
    def definition(self):
        return copy.deepcopy(self._definition)

    ### PUBLIC METHODS ###

    def find_divisible_leaf_indices_and_subdivisions(self, q_grid):
        indices, subdivisions = [], []
        for i, leaf in enumerate(q_grid.leaves[:-1]):
            if leaf.q_events and leaf.is_divisible:
                parentage_rations = leaf.parentage_ratios
                leaf_subdivisions = self.find_leaf_subdivisions(parentage_ratios)
                if leaf_subdivisions:
                    indices.append(i)
                    subdivisions.append(leaf_subdivisions)
        return indices, subdivisions

    @abstractmethod
    def find_leaf_subdivisions(self, leaf):
        raise NotImplemented

    @abstractmethod
    def is_valid_definition(self, definition):
        raise NotImplemented
