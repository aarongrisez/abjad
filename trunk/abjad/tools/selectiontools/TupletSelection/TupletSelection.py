from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.FreeSelection import FreeSelection


class TupletSelection(FreeSelection):
    '''Free selection of tuplets.
    '''

    ### PUBLIC METHODS ###

    def remove(self):
        r'''Remove tuplets in selection.

        Example 1. Remove trivial tuplets in selection:

        ::

            >>> tuplet_1 = Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = Tuplet((1, 1), "g'4 fs'4")
            >>> staff = Staff([tuplet_1, tuplet_2])

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }
                {
                    g'4
                    fs'4
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> selection = selectiontools.select_tuplets(
            ...     staff,
            ...     include_augmented_tuplets=False,
            ...     include_diminished_tuplets=False,
            ...     include_trivial_tuplets=True,
            ...     )

        ::

            >>> selection
            TupletSelection(Tuplet(1, [g'4, fs'4]),)

        ::

            >>> selection.remove()

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }
                g'4
                fs'4
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import componenttools
        for tuplet in self:
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])

    def set_denominator_to_at_least(self, n):
        r'''Set denominator of tuplets in selection to at least `n`.

        Example 1. Set denominator of tuplets to at least ``8``:

        ::

            >>> tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'4
                d'8
                e'8
                f'4
                g'2
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        ::

            >>> tuplets = selectiontools.select_tuplets(tuplet)
            >>> tuplets.set_denominator_to_at_least(8)

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 6/10 {
                c'4
                d'8
                e'8
                f'4
                g'2
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import tuplettools

        assert mathtools.is_nonnegative_integer_power_of_two(n)
        Duration = durationtools.Duration
        #for tuplet in iterationtools.iterate_tuplets_in_expr(expr):
        for tuplet in self:
            tuplet.force_fraction = True
            durations = [
                tuplet.contents_duration, 
                tuplet._preprolated_duration, 
                (1, n),
                ]
            duration_pairs = Duration.durations_to_nonreduced_fractions_with_common_denominator(
                durations)
            tuplet.preferred_denominator = duration_pairs[1].numerator
