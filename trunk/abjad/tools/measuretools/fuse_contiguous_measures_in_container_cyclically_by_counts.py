from abjad.components.Container import Container
from abjad.tools.measuretools.fuse_measures import fuse_measures
from abjad.tools.measuretools.get_next_measure_from_component import get_next_measure_from_component


def fuse_contiguous_measures_in_container_cyclically_by_counts(container, counts, mark = False):
   r'''Fuse `container` measures cyclically by `counts`::

      abjad> staff = Staff(RigidMeasure((2, 8), notetools.make_repeated_notes(2)) * 5)
      abjad> pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 2/8
            e'8
            f'8
         }
         {
            \time 2/8
            g'8
            a'8
         }
         {
            \time 2/8
            b'8
            c''8
         }
         {
            \time 2/8
            d''8
            e''8
         }
      }
      
   ::
      
      abjad> counts = (2, 1)
      abjad> measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(staff, counts)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
         }
         {
            \time 2/8
            g'8
            a'8
         }
         {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
         }
      }

   Return none.

   Set `mark` to true to mark fused measures for later reference.

   .. todo:: rename `counts` to `counts`.

   .. versionchanged:: 1.1.2
      renamed ``fuse.measures_by_counts_cyclic( )`` to
      ``measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts( )``.
   '''

   assert isinstance(container, Container)
   assert isinstance(counts, (tuple, list))

   try:
      if not container._update._current:
         container._update._update_all( )
      container._update._forbid_update( )
      len_parts = len(counts)
      part_index = 0
      cur_measure = get_next_measure_from_component(container)
      while True:
         part_count = counts[part_index % len_parts]
         #print cur_measure, part_count
         if 1 < part_count:
            measures_to_fuse = [ ]
            measure_to_fuse = cur_measure
            for x in range(part_count):
               measures_to_fuse.append(measure_to_fuse)
               measure_to_fuse = get_next_measure_from_component(measure_to_fuse)
               if measure_to_fuse is None:
                  break
            meter_sum_str = ' + '.join([
               str(x.meter.effective) for x in measures_to_fuse])
            meter_sum_str = '"%s"' % meter_sum_str
            new = fuse_measures(measures_to_fuse)
            if mark:
               new.leaves[0].markup.up.append(meter_sum_str)
            cur_measure = new
         cur_measure = get_next_measure_from_component(cur_measure)
         if cur_measure is None:
            break
         part_index += 1 
   finally:
      container._update._allow_update( )
