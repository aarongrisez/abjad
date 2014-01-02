# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Hairpin import Hairpin


class Crescendo(Hairpin):
    r'''A crescendo spanner that includes rests.

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> crescendo = spannertools.Crescendo(include_rests=True)
        >>> attach(crescendo, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            r4 \<
            c'8
            d'8
            e'8
            f'8
            r4 \!
        }

    Abjad crescendo spanner that does not include rests:

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> crescendo = spannertools.Crescendo(include_rests=False)
        >>> attach(crescendo, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            r4
            c'8 \<
            d'8
            e'8
            f'8 \!
            r4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_include_rests',
        '_shape',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        direction=None,
        include_rests=True, 
        overrides=None,
        ):
        Hairpin.__init__(
            self, 
            descriptor='<', 
            direction=direction,
            include_rests=include_rests,
            overrides=overrides,
            )
