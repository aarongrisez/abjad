from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class _RelativeConstraint(_Constraint):

    __slots__ = ('_index_span', '_indices', '_kind', '_predicate')

    def __init__(self, indices, predicate):
        object.__setattr__(self, '_kind', 'relative')

        if isinstance(indices, int):
            assert 1 < indices
            indices = range(indices)
        elif isinstance(indices, (list, tuple)):
            indices = sorted(set(indices))
            assert 1 < len(indices)
            min_indices = min(indices)
            indices = [x - min_indices for x in indices]
        else:
            raise Exception('Cannot determine indices from %s' % indices)
        object.__setattr__(self, '_indices', tuple(indices))
        object.__setattr__(self, '_index_span', max(indices) - min(indices) + 1)

        assert isinstance(predicate, type(lambda: None))
#        assert predicate.func_code.co_argcount == len(indices)
        object.__setattr__(self, '_predicate', predicate)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r, %r' % (self._indices, self._predicate)

    ### PUBLIC ATTRIBUTES ###

    @property
    def index_span(self):
        return self._index_span

    @property
    def indices(self):
        return self._indices

    @property
    def predicate(self):
        return self._predicate
