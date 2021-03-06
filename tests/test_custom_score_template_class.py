import abjad


# TODO: Move to doctests
def test_custom_score_template_class_01():
    """
    Score template with named contexts.
    """

    class NamedContextScoreTemplate(abjad.ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            voice = abjad.Voice(name='Blue_Voice')
            staff = abjad.Staff(name='Red_Staff')
            score = abjad.Score(name='Green_Score')
            staff.append(voice)
            score.append(staff)
            return score

    named_context_score_template = NamedContextScoreTemplate()
    score = named_context_score_template()

    assert format(score) == abjad.String.normalize(
        r"""
        \context Score = "Green_Score"
        <<
            \context Staff = "Red_Staff"
            {
                \context Voice = "Blue_Voice"
                {
                }
            }
        >>
        """
        )


def test_custom_score_template_class_02():
    """
    Score template with custom (voice and staff) contexts.

    CAUTION: always use built-in LilyPond score context; do not rename.
    """

    class CustomContextScoreTemplate(abjad.ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = abjad.Voice(lilypond_type='CustomVoice')
            custom_staff = abjad.Staff(lilypond_type='CustomStaff')
            score = abjad.Score()
            custom_staff.append(custom_voice)
            score.append(custom_staff)
            return score

    custom_context_score_template = CustomContextScoreTemplate()
    score = custom_context_score_template()

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new CustomStaff
            {
                \new CustomVoice
                {
                }
            }
        >>
        """
        )

    # here's how to properly override with externalized layout

    score = custom_context_score_template()
    score[0][0].extend("c'4 ( d'4 e'4 f'4 )")
    lilypond_file = abjad.LilyPondFile.new(score)

    context_block = abjad.ContextBlock(
        source_lilypond_type='Voice',
        type_='Engraver_group',
        name='CustomVoice',
        alias='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    abjad.override(context_block).note_head.color = 'green'
    abjad.override(context_block).stem.color = 'green'

    context_block = abjad.ContextBlock(
        source_lilypond_type='Staff',
        type_='Engraver_group',
        name='CustomStaff',
        alias='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomVoice')
    abjad.override(context_block).staff_symbol.color = 'red'

    context_block = abjad.ContextBlock(
        source_lilypond_type='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomStaff')

    assert format(lilypond_file.layout_block) == abjad.String.normalize(
        r"""
        \layout {
            \context {
                \Voice
                \name CustomVoice
                \type Engraver_group
                \alias Voice
                \override NoteHead.color = #green
                \override Stem.color = #green
            }
            \context {
                \Staff
                \name CustomStaff
                \type Engraver_group
                \alias Staff
                \accepts CustomVoice
                \override StaffSymbol.color = #red
            }
            \context {
                \Score
                \accepts CustomStaff
            }
        }
        """
        )

    assert format(lilypond_file.score_block) == abjad.String.normalize(
        r"""
        \score {
            \new Score
            <<
                \new CustomStaff
                {
                    \new CustomVoice
                    {
                        c'4
                        (
                        d'4
                        e'4
                        f'4
                        )
                    }
                }
            >>
        }
        """
        )
