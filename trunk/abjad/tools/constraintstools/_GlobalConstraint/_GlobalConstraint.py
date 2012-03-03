from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class _GlobalConstraint(_Constraint):

    def __init__(self, predicate):
        object.__setattr__(self, '_kind', 'global')
        assert isinstance(predicate, type(lambda: None))
        assert predicate.func_code.co_argcount == 1
        object.__setattr__(self, '_predicate', predicate)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r' % self._predicate
