def _give_position_in_parent_from_donor_components_to_container(
    donors, container):
    '''Do nothing when `donors` have no parent.

    Otherwise find `donors` parent;
    insert `container` contents in parent immediately before `donors`;
    remove `donors` from parent.

    Return none.

    Not composer-safe.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import selectiontools

    # check input
    assert isinstance(container, containertools.Container)
    assert componenttools.all_are_contiguous_components_in_same_parent(donors)

    # coerce input
    container_selection = selectiontools.Selection([container])
    if not isinstance(donors, selectiontools.Selection):
        donors = selectiontools.Selection(donors)

    # get donors' position in parent
    parent, start, stop = \
        componenttools.get_parent_and_start_stop_indices_of_components(donors)

    # do nothing when donors have no parent
    if parent is None:
        return

    # to avoid pychecker slice assignment error
    #parent._music[start:start] = container
    parent._music.__setitem__(slice(start, start), container_selection)
    container_selection._set_component_parents(parent)
    donors._set_component_parents(None)
