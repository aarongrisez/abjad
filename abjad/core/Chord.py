import copy
import typing
from abjad import instruments
from abjad import mathtools
from abjad import pitch as abjad_pitch
from abjad import typings
from abjad.indicators.Tremolo import Tremolo
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.top.inspect import inspect
from abjad.top.parse import parse
from abjad.utilities.Duration import Duration
from .DrumNoteHead import DrumNoteHead
from .Leaf import Leaf
from .NoteHead import NoteHead
from .NoteHeadList import NoteHeadList


class Chord(Leaf):
    """
    Chord.

    ..  container:: example

        >>> chord = abjad.Chord("<e' cs'' f''>4")
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <e' cs'' f''>4

    ..  container:: example

        REGRESSION. Initializes from other chord:

        >>> chord = abjad.Chord("<e' cs'' f''>4", multiplier=(1, 2))
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            <e' cs'' f''>4 * 1/2

        >>> new_chord = abjad.Chord(chord)
        >>> abjad.show(new_chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(new_chord)
            <e' cs'' f''>4 * 1/2

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Leaves'

    __slots__ = (
        '_note_heads',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments,
        multiplier: typings.DurationTyping = None,
        tag: str = None,
        ) -> None:
        from abjad.ly import drums
        assert len(arguments) in (0, 1, 2)
        self._note_heads = NoteHeadList(client=self)
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f'{{ {arguments[0]} }}'
            parsed = parse(string)
            assert len(parsed) == 1 and isinstance(parsed[0], Leaf)
            arguments = tuple([parsed[0]])
        are_cautionary: typing.List[typing.Optional[bool]] = []
        are_forced: typing.List[typing.Optional[bool]] = []
        are_parenthesized: typing.List[typing.Optional[bool]] = []
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            leaf = arguments[0]
            written_pitches = []
            written_duration = leaf.written_duration
            if multiplier is None:
                multiplier = leaf.multiplier
            if 'written_pitch' in dir(leaf):
                written_pitches.append(leaf.note_head.written_pitch)
                are_cautionary = [leaf.note_head.is_cautionary]
                are_forced = [leaf.note_head.is_forced]
                are_parenthesized = [leaf.note_head.is_parenthesized]
            elif 'written_pitches' in dir(leaf):
                written_pitches.extend(
                    x.written_pitch for x in leaf.note_heads
                    )
                are_cautionary = [x.is_cautionary for x in leaf.note_heads]
                are_forced = [x.is_forced for x in leaf.note_heads]
                are_parenthesized = [
                    x.is_parenthesized for x in
                    leaf.note_heads
                    ]
        elif len(arguments) == 2:
            written_pitches, written_duration = arguments
            if isinstance(written_pitches, str):
                written_pitches = [x for x in written_pitches.split() if x]
            elif isinstance(written_pitches, type(self)):
                written_pitches = written_pitches.written_pitches
        elif len(arguments) == 0:
            written_pitches = [0, 4, 7]
            written_duration = Duration(1, 4)
        else:
            raise ValueError(f'can not initialize chord from {arguments!r}.')
        Leaf.__init__(
            self,
            written_duration,
            multiplier=multiplier,
            tag=tag,
            )
        if not are_cautionary:
            are_cautionary = [None] * len(written_pitches)
        if not are_forced:
            are_forced = [None] * len(written_pitches)
        if not are_parenthesized:
            are_parenthesized = [None] * len(written_pitches)
        for written_pitch, is_cautionary, is_forced, is_parenthesized in zip(
            written_pitches, are_cautionary, are_forced, are_parenthesized):
            if not is_cautionary:
                is_cautionary = None
            if not is_forced:
                is_forced = None
            if not is_parenthesized:
                is_parenthesized = None
            if written_pitch not in drums:
                note_head = NoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
            else:
                note_head = DrumNoteHead(
                    written_pitch=written_pitch,
                    is_cautionary=is_cautionary,
                    is_forced=is_forced,
                    is_parenthesized=is_parenthesized,
                    )
            self._note_heads.append(note_head)
        if len(arguments) == 1 and isinstance(arguments[0], Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        """
        Shallow copies chord.

        Returns new chord.
        """
        new_chord = Leaf.__copy__(self, *arguments)
        new_chord.note_heads[:] = []
        for note_head in self.note_heads:
            note_head = copy.copy(note_head)
            new_chord.note_heads.append(note_head)
        return new_chord

    def __getnewargs__(self):
        """
        Gets new chord arguments.

        Returns pair.
        """
        return self.written_pitches, self.written_duration

    ### PRIVATE METHODS ###

    def _format_before_slot(self, bundle):
        result = []
        result.append(self._format_grace_body())
        result.append(('comments', bundle.before.comments))
        commands = bundle.before.commands
        if inspect(self).has_indicator(Tremolo):
            tremolo_command = self._format_repeat_tremolo_command()
            commands = list(commands)
            commands.append(tremolo_command)
            commands = tuple(commands)
        result.append(('commands', commands))
        result.append(('indicators', bundle.before.indicators))
        result.append(('grob overrides', bundle.grob_overrides))
        result.append(('context settings', bundle.context_settings))
        result.append(('spanners', bundle.before.spanners))
        return result

    def _format_close_brackets_slot(self, bundle):
        result = []
        if inspect(self).has_indicator(Tremolo):
            brackets_close = ['}']
            result.append([('close brackets', ''), brackets_close])
        return result

    def _format_leaf_nucleus(self):
        indent = LilyPondFormatManager.indent
        result = []
        note_heads = self.note_heads
        if any('\n' in format(x) for x in note_heads):
            for note_head in note_heads:
                current_format = format(note_head)
                format_list = current_format.split('\n')
                format_list = [indent + x for x in format_list]
                result.extend(format_list)
            result.insert(0, '<')
            result.append('>')
            result = '\n'.join(result)
            result += str(self._get_formatted_duration())
        elif inspect(self).has_indicator(Tremolo):
            reattack_duration = self._get_tremolo_reattack_duration()
            duration_string = reattack_duration.lilypond_duration_string
            durated_pitches = []
            for note_head in note_heads:
                durated_pitch = format(note_head) + duration_string
                durated_pitches.append(durated_pitch)
            tremolo = inspect(self).indicator(Tremolo)
            if tremolo.is_slurred:
                durated_pitches[0] = durated_pitches[0] + r' \('
                durated_pitches[-1] = durated_pitches[-1] + r' \)'
            result = ' '.join(durated_pitches)
        else:
            result.extend([format(_) for _ in note_heads])
            result = '<%s>%s' % (
                ' '.join(result),
                self._get_formatted_duration(),
                )
        # single string, but wrapped in list bc contribution
        return ['nucleus', [result]]

    def _format_open_brackets_slot(self, bundle):
        result = []
        if inspect(self).has_indicator(Tremolo):
            brackets_open = ['{']
            result.append([('open brackets', ''), brackets_open])
        return result

    def _format_repeat_tremolo_command(self):
        tremolo = inspect(self).indicator(Tremolo)
        reattack_duration = self._get_tremolo_reattack_duration()
        repeat_count = self.written_duration / reattack_duration / 2
        if not mathtools.is_integer_equivalent(repeat_count):
            message = f'can not tremolo duration {self.written_duration}'
            message += f' with {tremolo.beam_count} beams.'
            raise Exception(message)
        repeat_count = int(repeat_count)
        command = r'\repeat tremolo {}'.format(repeat_count)
        return command

    def _get_compact_representation(self):
        return f'<{self._get_summary()}>{self._get_formatted_duration()}'

    def _get_compact_representation_with_tie(self):
        logical_tie = self._get_logical_tie()
        if 1 < len(logical_tie) and self is not logical_tie[-1]:
            return f'{self._get_compact_representation()} ~'
        else:
            return self._get_compact_representation()

    def _get_sounding_pitches(self):
        if 'sounding pitch' in inspect(self).indicators(str):
            return self.written_pitches
        else:
            instrument = self._get_effective(instruments.Instrument)
            if instrument:
                sounding_pitch = instrument.middle_c_sounding_pitch
            else:
                sounding_pitch = abjad_pitch.NamedPitch('C4')
            interval = abjad_pitch.NamedPitch('C4') - sounding_pitch
            sounding_pitches = [
                interval.transpose(pitch)
                for pitch in self.written_pitches
                ]
            return tuple(sounding_pitches)

    def _get_summary(self):
        return ' '.join([str(x) for x in self.note_heads])

    def _get_tremolo_reattack_duration(self):
        tremolos = inspect(self).indicators(Tremolo)
        if not tremolos:
            return
        tremolo = tremolos[0]
        exponent = 2 + tremolo.beam_count
        denominator = 2 ** exponent
        reattack_duration = Duration(1, denominator)
        return reattack_duration

    ### PUBLIC PROPERTIES ###

    @property
    def note_heads(self):
        r"""
        Gets note-heads in chord.

        ..  container:: example

            Gets note-heads in chord:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> abjad.f(chord.note_heads)
            abjad.NoteHeadList(
                [
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("g'"),
                        ),
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("c''"),
                        ),
                    abjad.NoteHead(
                        written_pitch=abjad.NamedPitch("e''"),
                        ),
                    ]
                )

        ..  container:: example

            Sets note-heads with pitch names:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.note_heads = "c' d' fs'"
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <c' d' fs'>4

        ..  container:: example

            Sets note-heads with pitch numbers:

                >>> chord = abjad.Chord("<g' c'' e''>4")
                >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.note_heads = [16, 17, 19]
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <e'' f'' g''>4

        Set note-heads with any iterable.

        Returns note-head list.
        """
        return self._note_heads

    @note_heads.setter
    def note_heads(self, note_heads):
        self._note_heads[:] = []
        if isinstance(note_heads, str):
            note_heads = note_heads.split()
        self.note_heads.extend(note_heads)

    @property
    def written_duration(self):
        """
        Gets written duration of chord.

        ..  container:: example

            Get written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_duration
            Duration(1, 4)

        ..  container:: example

            Set written duration:

            >>> chord = abjad.Chord("<e' cs'' f''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_duration = abjad.Duration(1, 16)
            >>> abjad.show(chord) # doctest: +SKIP

        Set duration.

        Returns duration.
        """
        return Leaf.written_duration.fget(self)

    @written_duration.setter
    def written_duration(self, argument):
        Leaf.written_duration.fset(self, argument)

    @property
    def written_pitches(self):
        """
        Written pitches in chord.

        ..  container:: example

            Get written pitches:

            >>> chord = abjad.Chord("<g' c'' e''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_pitches
            PitchSegment("g' c'' e''")

        ..  container:: example

            Set written pitches with pitch names:

            >>> chord = abjad.Chord("<e' g' c''>4")
            >>> abjad.show(chord) # doctest: +SKIP

            >>> chord.written_pitches = "f' b' d''"
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                <f' b' d''>4

            >>> chord.written_pitches
            PitchSegment("f' b' d''")

        Set written pitches with any iterable.

        Returns tuple.
        """
        return abjad_pitch.PitchSegment(
            items=(note_head.written_pitch for note_head in self.note_heads),
            item_class=abjad_pitch.NamedPitch,
            )

    @written_pitches.setter
    def written_pitches(self, pitches):
        self.note_heads = pitches
