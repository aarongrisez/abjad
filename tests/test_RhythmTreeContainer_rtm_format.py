import abjad
import abjad.rhythmtrees


def test_RhythmTreeContainer_rtm_format_01():

    leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
    leaf_c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
    subcontainer = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=2, children=[leaf_b, leaf_c])
    leaf_d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
    container = abjad.rhythmtrees.RhythmTreeContainer(
        preprolated_duration=1, children=[leaf_a, subcontainer, leaf_d])

    assert subcontainer.rtm_format == '(2 (3 2))'
    assert container.rtm_format == '(1 (3 (2 (3 2)) 1))'
