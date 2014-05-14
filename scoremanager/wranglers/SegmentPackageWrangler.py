# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import systemtools
from scoremanager.wranglers.Wrangler import Wrangler


class SegmentPackageWrangler(Wrangler):
    r'''Segment package wrangler.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> wrangler = score_manager._segment_package_wrangler
            >>> wrangler
            SegmentPackageWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(SegmentPackageWrangler, self)
        superclass.__init__(session=session)
        self._asset_identifier = 'segment package'
        self._basic_breadcrumb = 'segments'
        self._manager_class = managers.SegmentPackageManager
        self._score_storehouse_path_infix_parts = ('segments',)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superclass = super(SegmentPackageWrangler, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            '>': self.go_to_next_asset,
            '<': self.go_to_previous_asset,
            'cp': self.copy_package,
            'dpye*': self.edit_every_definition_py,
            'ino': self.open_initializer,
            'inws': self.write_stub_initializer,
            'lyi': self.interpret_lilypond_files,
            'mpyi*': self.interpret_every_make_py,
            'new': self.make_package,
            'pdfo': self.open_output_pdfs,
            'ren': self.rename_package,
            'rm': self.remove_packages,
            'ver': self.version_artifacts,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_segments = False

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            manager = self._initialize_manager(result)
            manager._run()

    def _is_valid_directory_entry(self, expr):
        superclass = super(SegmentPackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_all_segments_menu_section(self, menu):
        commands = []
        commands.append(('all segments - definition.py - edit', 'dpye*'))
        commands.append(('all segments - make.py - interpret', 'mpyi*'))
        commands.append(('all segments - interpret output.ly files', 'lyi'))
        commands.append(('all segments - open metadata pys', 'mdmo'))
        commands.append(('all segments - open output.pdf files', 'pdfo'))
        commands.append(('all segments - version artifacts', 'ver'))
        menu.make_command_section(
            commands=commands,
            is_hidden=True,
            name='all segments',
            )

    def _make_asset(self, path, metadata=None):
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.write_initializer()
        manager.write_definition_py()
        if not os.path.exists(manager._versions_directory_path):
            os.mkdir(manager._versions_directory_path)

    def _make_main_menu(self, name='segment wrangler'):
        superclass = super(SegmentPackageWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_all_segments_menu_section(menu)
        self._make_initializer_menu_section(menu)
        self._make_metadata_menu_section(menu)
        self._make_segments_menu_section(menu)
        self._make_sibling_asset_tour_menu_section(menu)
        return menu

    # TODO: migrate to SegmentPackageManager
    def _make_package(self, path, metadata=None):
        from scoremanager import managers
        assert os.path.sep in path
        metadata = collections.OrderedDict(metadata or {})
        assert not os.path.exists(path)
        os.mkdir(path)
        manager = self._initialize_manager(path)
        manager.write_stub_definition_py(confirm=False, display=False)
        manager.write_stub_make_py(confirm=False, display=False)

    def _make_segments_menu_section(self, menu):
        commands = []
        commands.append(('segments - copy', 'cp'))
        commands.append(('segments - new', 'new'))
        commands.append(('segments - rename', 'ren'))
        commands.append(('segments - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='segments',
            )

    def _set_is_navigating_to_sibling_asset(self):
        self._session._is_navigating_to_score_segments = True

    ### PUBLIC METHODS ###

    def copy_package(self):
        r'''Copies segment package.

        Returns none.
        '''
        self._copy_asset()

    def edit_every_definition_py(self):
        r'''Edits ``definition.py`` in every segment.

        Returns none.
        '''
        self._open_in_each_package('definition.py', verb='edit')
        self._session._hide_next_redraw = True

    def go_to_next_asset(self):
        r'''Goes to next asset.

        Returns none.
        '''
        self._go_to_next_asset()

    def go_to_previous_asset(self):
        r'''Goes to previous asset.

        Returns none.
        '''
        self._go_to_previous_asset()

    def interpret_lilypond_files(
        self,
        confirm=True,
        display=True,
        open_output_pdfs=True,
        ):
        r'''Reinterprets all current LilyPond files.

        Returns none.
        '''
        segments_directory = self._get_current_directory()
        entries = sorted(os.listdir(segments_directory))
        if confirm:
            messages = []
            messages.append('')
            messages.append('will interpret ...')
            messages.append('')
            segment_paths = self._list_visible_asset_paths()
            for segment_path in segment_paths:
                input_path = os.path.join(segment_path, 'output.ly')
                output_path = os.path.join(segment_path, 'output.pdf')
                messages.append('  INPUT: {}'.format(input_path))
                messages.append(' OUTPUT: {}'.format(output_path))
                messages.append('')
            self._io_manager.display(messages)
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
            self._io_manager.display('')
        for manager in self._list_visible_asset_managers():
            self._session._hide_next_redraw = False
            manager.interpret_lilypond_file(confirm=False, display=True)
        self._session._hide_next_redraw = True

    def interpret_every_make_py(self):
        r'''Interprets ``__make.py__`` in every segment.
        
        Makes ``output.ly`` and ``output.pdf`` in every segment.

        Returns none.
        '''
        with self._io_manager.make_interaction():
            managers = self._list_visible_asset_managers()
            make_py_paths = []
            output_ly_paths = []
            output_pdf_paths = []
            for manager in managers:
                make_py_paths.append(manager._make_py_path)
                output_ly_paths.append(manager._output_lilypond_file_path)
                output_pdf_paths.append(manager._output_pdf_file_path)
            # TODO: gather message with dry_run=True keyword
            messages = []
            messages.append('will interpret ...')
            triples = zip(make_py_paths, output_ly_paths, output_pdf_paths)
            for triple in triples:
                make_py_path = triple[0]
                output_ly_path = triple[1]
                output_pdf_path = triple[2]
                messages.append('  INPUT: {}'.format(make_py_path))
                messages.append(' OUTPUT: {}'.format(output_ly_path))
                messages.append(' OUTPUT: {}'.format(output_pdf_path))
            self._io_manager.display(messages)
            result = self._io_manager.confirm()
            if self._should_backtrack():
                return
            if not result:
                return
            for manager in managers:
                manager.interpret_make_py(confirm=False, display=False)
            if not managers:
                self._io_manager.display('')

    def make_package(self):
        r'''Makes segment package.

        Returns none.
        '''
        if self._session.is_in_score:
            storehouse_path = self._current_storehouse_path
        else:
            storehouse_path = self._select_storehouse_path()
        prompt_string = 'enter segment package name'
        path = self._get_available_path(
            prompt_string=prompt_string,
            storehouse_path=storehouse_path,
            )
        if self._should_backtrack():
            return
        if not path:
            return
        self._make_package(path)
        manager = self._get_manager(path)
        manager._run()

    def open_initializer(self):
        r'''Opens initializer.

        Returns none.
        '''
        self._current_package_manager.open_initializer()

    def open_output_pdfs(self):
        r'''Opens output.pdf file in each segment.

        Returns none.
        '''
        self._open_in_each_package('output.pdf')
        self._session._hide_next_redraw = True

    def remove_packages(self):
        r'''Removes one or more segment packages.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_package(self):
        r'''Renames segment package.

        Returns none.
        '''
        self._rename_asset()

    def version_artifacts(self, confirm=True, display=True):
        r'''Versions all segment packages.

        Returns none.
        '''
        self._version_artifacts(confirm=confirm, display=display)

    def write_stub_initializer(self):
        r'''Writes stub initializer.

        Returns none.
        '''
        self._current_package_manager.write_stub_initializer()