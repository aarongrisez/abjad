# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnotes'
    assert not wrangler._configuration.package_exists(string)
    filesystem_path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnotes',
        )

    try:
        wrangler._make_handmade_material_package(filesystem_path)
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not manager.has_output_material_module
        assert not os.path.isfile(manager.illustration_builder_module_path)
        assert manager.material_definition is None
        assert manager.output_material is None
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)


def test_MaterialPackageWrangler__make_handmade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.example_notes'
    assert wrangler._configuration.package_exists(string)
    statement = 'wrangler._make_handmade_material_package'
    statement += "('scoremanager.materials.example_notes')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler__make_handmade_material_package_03():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnotes'
    assert not wrangler._configuration.package_exists(string)
    filesystem_path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnotes',
        )

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_handmade_material_package(
            filesystem_path, 
            metadata=metadata,
            )
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(filesystem_path)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)