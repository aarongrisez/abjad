from experimental import *


def test_Menu_menu_entry_keys_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    section_1 = menu.make_section()
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    section_2 = menu.make_section()
    section_2.append(('add', 'add something'))
    section_2.append(('rm', 'delete something'))
    section_2.append(('mod', 'modify something'))
    assert menu.menu_entry_keys[-6:] == section_1.menu_entry_keys + section_2.menu_entry_keys
