from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class CounttimeComponentSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components in `reference` container
    restricted according to keywords.

        >>> from experimental import *

    Select the first five counttime components::

        >>> selectortools.CounttimeComponentSliceSelector(stop_identifier=5)
        CounttimeComponentSliceSelector(stop_identifier=5)

    Select the last five counttime components::

        >>> selectortools.CounttimeComponentSliceSelector(start_identifier=-5)
        CounttimeComponentSliceSelector(start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5``::

        >>> selectortools.CounttimeComponentSliceSelector(start_identifier=5, stop_identifier=-5)
        CounttimeComponentSliceSelector(start_identifier=5, stop_identifier=-5)

    Select all counttime components::

        >>> selectortools.CounttimeComponentSliceSelector()
        CounttimeComponentSliceSelector()

    Select counttime measure ``3`` to starting during segment ``'red'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.CounttimeComponentSliceSelector(
        ... inequality=inequality, klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet_selector = selectortools.CounttimeComponentSliceSelector(
        ... selector=measure_selector, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaf_slice_selector = selectortools.CounttimeComponentSliceSelector(
        ... selector=tuplet_selector, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaf_slice_selector)
        selectortools.CounttimeComponentSliceSelector(
            klass=leaftools.Leaf,
            selector=selectortools.CounttimeComponentSliceSelector(
                klass=tuplettools.Tuplet,
                selector=selectortools.CounttimeComponentSliceSelector(
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4
                    ),
                start_identifier=-1
                ),
            start_identifier=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, klass=None, predicate=None, selector=None,
        start_identifier=None, stop_identifier=None):
        from experimental import helpertools
        assert selector is None or self._interprets_as_sliceable_selector(selector), repr(selector)
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._selector = selector
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def klass(self):
        '''Class of counttime component selector specified by user.

        Return counttime component class or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user.

        Return callback or none.
        '''
        return self._predicate

    @property
    def selector(self):
        '''To allow selectors to reference each other recursively.
        '''
        return self._selector
