# -*- encoding: utf-8 -*-
import collections
import os
from abjad.tools import stringtools
from scoremanager import predicates
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class MaterialPackageWrangler(PackageWrangler):
    r'''Material package wrangler.

    ..  container:: example

        ::

            >>> from scoremanager import wranglers
            >>> wrangler = wranglers.MaterialPackageWrangler()
            >>> wrangler
            MaterialPackageWrangler()

    ..  container:: example

        ::

            >>> wrangler_in_score = wranglers.MaterialPackageWrangler()
            >>> session = wrangler_in_score._session
            >>> session._current_score_snake_case_name = 'red_example_score'
            >>> wrangler_in_score
            MaterialPackageWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        superclass = super(MaterialPackageWrangler, self)
        superclass.__init__(session=session)
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(session=self._session)
        self.abjad_storehouse_directory_path = \
            self._configuration.abjad_material_packages_directory_path
        self.user_storehouse_directory_path = \
            self._configuration.user_library_material_packages_directory_path
        self.score_storehouse_path_infix_parts = ('materials',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'materials'
        else:
            return 'material library'

    @property
    def _user_input_to_action(self):
        superclass = super(MaterialPackageWrangler, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'd': self.make_data_package,
            'mtn': self._navigate_to_next_material,
            'mtp': self._navigate_to_previous_material,
            'nmh': self.make_handmade_material_package,
            'nmm': self.make_managermade_material_package,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _get_appropriate_material_package_manager(
        self,
        material_package_manager_class_name, 
        material_package_path,
        ):
        import scoremanager
        from scoremanager import managers
        if material_package_manager_class_name is None:
            material_package_manager = \
                managers.MaterialPackageManager(
                material_package_path, 
                session=self._session,
                )
        else:
            command = 'material_package_manager = '
            command += 'scoremanager.materialpackagemanagers.{}'
            command += '(material_package_path, session=self._session)'
            command = command.format(material_package_manager_class_name)
            try:
                exec(command)
            except AttributeError:
                command = 'from {0}.{1}.{1}'
                command += ' import {1} as material_package_manager_class'
                package_path = '.'.join([
                    self._configuration._user_library_directory_name,
                    'material_packages',
                    ])
                command = command.format(
                    package_path,
                    material_package_manager_class_name,
                    )
                exec(command)
                material_package_manager = material_package_manager_class(
                    material_package_path, 
                    session=self._session,
                    )
        return material_package_manager

    def _get_next_material_package_name(self):
        last_package_path = self._session.last_material_package_path
        menu_entries = self._make_asset_menu_entries()
        package_paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_name = self._session.current_score_snake_case_name
            package_paths = [
                x for x in package_paths 
                if x.startswith(score_name)
                ]
        if last_package_path is None:
            return package_paths[0]
        assert last_package_path in package_paths
        index = package_paths.index(last_package_path)
        next_index = (index + 1) % len(package_paths)
        next_package_name = package_paths[next_index]
        return next_package_name
        
    def _get_previous_material_package_name(self):
        last_package_path = self._session.last_material_package_path
        menu_entries = self._make_asset_menu_entries()
        package_paths = [x[-1] for x in menu_entries]
        if self._session.is_in_score:
            score_name = self._session.current_score_snake_case_name
            package_paths = [
                x for x in package_paths 
                if x.startswith(score_name)
                ]
        if last_package_path is None:
            return package_paths[-1]
        assert last_package_path in package_paths
        index = package_paths.index(last_package_path)
        previous_index = (index - 1) % len(package_paths)
        previous_package_name = package_paths[previous_index]
        return previous_package_name

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            material_package_manager = self._initialize_asset_manager(result)
            if os.path.exists(material_package_manager._filesystem_path):
                material_package_manager._run()

    def _initialize_asset_manager(self, package_path):
        wrangler = self._material_package_manager_wrangler
        manager = wrangler._initialize_asset_manager(package_path)
        return manager

    def _list_asset_filesystem_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad material package filesystem paths:

        ::

            >>> for x in wrangler._list_asset_filesystem_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/materialpackages/example_articulation_handler'
            '.../scoremanager/materialpackages/example_dynamic_handler'
            '.../scoremanager/materialpackages/example_markup_inventory'
            '.../scoremanager/materialpackages/example_notes'
            '.../scoremanager/materialpackages/example_numbers'
            '.../scoremanager/materialpackages/example_sargasso_measures'
            '.../scorepackages/red_example_score/materials/tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass._list_asset_filesystem_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_managers(
        self, 
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Lists abjad material package managers:

        ::

            >>> for x in wrangler._list_asset_managers(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            ArticulationHandlerMaterialPackageManager('.../scoremanager/materialpackages/example_articulation_handler')
            DynamicHandlerMaterialPackageManager('.../scoremanager/materialpackages/example_dynamic_handler')
            MarkupInventoryMaterialPackageManager('.../scoremanager/materialpackages/example_markup_inventory')
            MaterialPackageManager('.../scoremanager/materialpackages/example_notes')
            MaterialPackageManager('.../scoremanager/materialpackages/example_numbers')
            SargassoMeasureMaterialPackageManager('.../scoremanager/materialpackages/example_sargasso_measures')
            MaterialPackageManager('.../red_example_score/materials/magic_numbers')
            PitchRangeInventoryMaterialPackageManager('.../red_example_score/materials/pitch_range_inventory')
            TempoInventoryMaterialPackageManager('.../red_example_score/materials/tempo_inventory')

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_names(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset names.

        Lists abjad material package names:

        ::

            >>> for x in wrangler._list_asset_names(
            ...     user_library=False, user_score_packages=False):
            ...     x
            'example articulation handler'
            'example dynamic handler'
            'example markup inventory'
            'example notes'
            'example numbers'
            'example sargasso measures'
            'magic numbers'
            'pitch range inventory'
            'tempo inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass._list_asset_names(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_package_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Lists abjad material package paths:

        ::

            >>> for x in wrangler._list_asset_package_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            'scoremanager.materialpackages.example_articulation_handler'
            'scoremanager.materialpackages.example_dynamic_handler'
            'scoremanager.materialpackages.example_markup_inventory'
            'scoremanager.materialpackages.example_notes'
            'scoremanager.materialpackages.example_numbers'
            'scoremanager.materialpackages.example_sargasso_measures'
            'red_example_score.materials.magic_numbers'
            'red_example_score.materials.pitch_range_inventory'
            'red_example_score.materials.tempo_inventory'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass._list_asset_package_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_directory_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad material package storehouse filesystem paths:

        ::

            >>> for x in wrangler._list_storehouse_directory_paths(
            ...     user_library=False, 
            ...     user_score_packages=False):
            ...     x
            '.../scoremanager/materialpackages'
            '.../scoremanager/scorepackages/blue_example_score/materials'
            '.../scoremanager/scorepackages/green_example_score/materials'
            '.../scoremanager/scorepackages/red_example_score/materials'

        Returns list.
        '''
        superclass = super(MaterialPackageWrangler, self)
        return superclass._list_storehouse_directory_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    def _make_data_package(self, material_package_path, metadata=None):
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = False
        metadata['should_have_user_input_module'] = False
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_handmade_material_package(self, material_package_path, metadata=None):
        metadata = metadata or {}
        metadata['material_package_manager_class_name'] = None
        metadata['should_have_illustration'] = True
        metadata['should_have_user_input_module'] = False
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_main_menu(self, head=None):
        menu = self._io_manager.make_menu(where=self._where)
        section = menu.make_asset_section(name='assets')
        asset_menu_entries = self._make_asset_menu_entries(head=head)
        section.menu_entries = asset_menu_entries
        section = menu.make_command_section(name='new material')
        section.append(('new material - by hand', 'nmh'))
        section.append(('new material - with manager', 'nmm'))
        lilypond_section = menu['lilypond']
        index = menu.menu_sections.index(lilypond_section) + 1
        tour_menu_section = self._io_manager._make_material_tour_menu_section(
            menu)
        menu.menu_sections.insert(index, tour_menu_section)
        return menu

    def _make_managermade_material_package(
        self,
        material_package_path, 
        material_package_manager_class_name, 
        metadata=None,
        ):
        metadata = metadata or {}
        command = 'from scoremanager.materialpackagemanagers '
        command += 'import {} as material_package_manager_class'
        command = command.format(material_package_manager_class_name)
        try:
            exec(command)
        except ImportError:
            command = 'from {} import {} as material_package_manager_class'
            package_path = '.'.join([
                self._configuration._user_library_directory_name,
                'material_packages',
                ])
            command = command.format(
                package_path,
                material_package_manager_class_name,
                )
            exec(command)
        should_have_user_input_module = getattr(
            material_package_manager_class, 
            'should_have_user_input_module', 
            True,
            )
        should_have_illustration = hasattr(
            material_package_manager_class, 
            'illustration_builder',
            )
        metadata['material_package_manager_class_name'] = \
            material_package_manager_class_name
        metadata['should_have_illustration'] = \
            should_have_illustration
        metadata['should_have_user_input_module'] = \
            should_have_user_input_module
        self._make_material_package(material_package_path, metadata=metadata)

    def _make_material_package(
        self, 
        package_path, 
        prompt=False, 
        metadata=None,
        ):
        metadata = collections.OrderedDict(metadata or {})
        metadata['is_material_package'] = True
        directory_path = \
            self._configuration.package_path_to_filesystem_path(
            package_path)
        assert not os.path.exists(directory_path)
        os.mkdir(directory_path)
        string = 'material_package_manager_class_name'
        material_package_manager_class_name = metadata.get(string)
        pair = (material_package_manager_class_name, package_path)
        material_package_manager = self._get_appropriate_material_package_manager(
            *pair)
        material_package_manager._initializer_file_manager._write_stub()
        material_package_manager.rewrite_metadata_module(
            metadata, 
            prompt=False,
            )
        material_package_manager.conditionally_write_stub_material_definition_module()
        material_package_manager.conditionally_write_stub_user_input_module()
        message = 'material package {!r} created.'.format(package_path)
        self._io_manager.proceed(message=message, prompt=prompt)

    def _navigate_to_next_material(self):
        pass

    def _navigate_to_previous_material(self):
        pass

    ### PUBLIC METHODS ###

    def make_data_package(
        self, 
        metadata=None, 
        pending_user_input=None,
        ):
        r'''Makes data package.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            material_package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_data_package(material_package_path, metadata=metadata)

    def make_handmade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Makes handmade material package.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_handmade_material_package(package_path)

    def make_managermade_material_package(
        self, 
        pending_user_input=None,
        ):
        r'''Makes managermade material package.

        Returns none.
        '''
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            wrangler = self._material_package_manager_wrangler
            result = wrangler.select_asset_package_path(
                cache=True, clear=False)
        if self._session._backtrack():
            return
        material_package_manager_package_path = result
        material_package_manager_class_name = \
            material_package_manager_package_path.split('.')[-1]
        with self._backtracking:
            material_package_path = \
                self.get_available_package_path()
        if self._session._backtrack():
            return
        self._make_managermade_material_package(
            material_package_path, material_package_manager_class_name)
        manager = self._get_appropriate_material_package_manager(
            material_package_manager_class_name, material_package_path)
        manager._run_first_time()
