import abjad
import abjad.rhythmtrees


def test_RhythmTreeNode_parentage_ratios_01():

    string = '(1 (1 (2 (3 4)) 2))'
    tree = abjad.rhythmtrees.RhythmTreeParser()(string)[0]

    assert tree.parentage_ratios == (1,)
    assert tree[0].parentage_ratios == (1, (1, 5))
    assert tree[1].parentage_ratios == (1, (2, 5))
    assert tree[1][0].parentage_ratios == (1, (2, 5), (3, 7))
    assert tree[1][1].parentage_ratios == (1, (2, 5), (4, 7))
    assert tree[2].parentage_ratios == (1, (2, 5))
