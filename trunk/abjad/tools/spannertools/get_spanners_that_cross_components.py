# -*- encoding: utf-8 -*-
from abjad.tools import componenttools


def get_spanners_that_cross_components(components):
    r'''Assert logical-voice-contiguous components.
    Collect spanners that attach to any component in 'components'.
    Return unordered set of crossing spanners.
    A spanner P crosses a list of logical-voice-contiguous components C
    when P and C share at least one component and when it is the
    case that NOT ALL of the components in P are also in C.
    In other words, there is some intersection -- but not total
    intersection -- between the components of P and C.

    Compare 'crossing' spanners with 'covered' spanners.
    Compare 'crossing' spanners with 'dominant' spanners.
    Compare 'crossing' spanners with 'contained' spanners.
    Compare 'crossing' spanners with 'attached' spanners.

    Return spanners.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    Selection = selectiontools.Selection

    assert Selection._all_are_contiguous_components_in_same_logical_voice(
        components)

    all_components = set(iterationtools.iterate_components_in_expr(components))
    contained_spanners = set()
    for component in iterationtools.iterate_components_in_expr(components):
        contained_spanners.update(component._get_spanners())
    crossing_spanners = set([])
    for spanner in contained_spanners:
        spanner_components = set(spanner[:])
        if not spanner_components.issubset(all_components):
            crossing_spanners.add(spanner)

    return crossing_spanners
