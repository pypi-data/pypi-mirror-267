#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.04.10 05:00:00                  #
# ================================================== #

import copy
import os
from pathlib import Path
from uuid import uuid4

from PySide6.QtGui import QAction

from pygpt_net.utils import trans


class Profile:
    def __init__(self, window=None):
        """
        Profile controller

        :param window: Window instance
        """
        self.window = window
        self.dialog = False
        self.width = 500
        self.height = 500
        self.initialized = False
        self.dialog_initialized = False

    def setup(self):
        """Setup profile"""
        self.setup_menu()
        if not self.dialog_initialized:
            self.window.profiles.setup()  # widget dialog
            self.dialog_initialized = True

    def switch(self, uuid: str, force: bool = False):
        """
        Switch profile

        :param uuid: Profile UUID
        :param force: Force switch
        """
        current = self.window.core.config.profile.get_current()
        if uuid == current and not force:
            self.update_menu()
            return
        profile = self.window.core.config.profile.get(uuid)
        if profile is None:
            self.window.ui.dialogs.alert("Profile not found!")
            return
        self.window.ui.status("Please wait...")
        print("Saving all settings in current profile...")
        self.window.controller.settings.save_all(force=True)  # save all current settings
        self.window.core.config.profile.set_current(uuid)

        # switch to profile workdir
        path = self.window.core.config.profile.get_current_workdir()
        if path and os.path.exists(path):
            self.window.controller.settings.workdir.update(path, force=True)

        self.update_menu()
        self.update_list()
        self.window.ui.update_title()
        self.window.ui.status(trans("dialog.profile.status.changed") + ": " + profile['name'])
        self.select_current_on_list()

    def select_current_on_list(self):
        """Select current profile on list"""
        current = self.window.core.config.profile.get_current()
        profiles = self.get_profiles()
        idx = 0
        for uuid in profiles:
            if uuid == current:
                index = self.window.ui.models['profile.list'].index(idx, 0)
                self.window.ui.nodes['profile.list'].setCurrentIndex(index)
                break
            idx += 1

    def get_profiles(self) -> dict:
        """
        Get profiles

        :return: profiles dict
        """
        return self.window.core.config.profile.get_all()

    def new(self):
        """New profile dialog"""
        self.window.ui.dialog['profile.item'].id = 'profile'
        self.window.ui.dialog['profile.item'].uuid = None
        self.window.ui.dialog['profile.item'].mode = 'create'
        self.window.ui.dialog['profile.item'].path = ""
        self.window.ui.dialog['profile.item'].input.setText("")
        self.window.ui.dialog['profile.item'].prepare()
        self.window.ui.dialog['profile.item'].show()

    def edit(self, uuid: str):
        """
        Edit profile dialog

        :param uuid: profile UUID
        """
        profile = self.window.core.config.profile.get(uuid)
        if profile is None:
            self.window.ui.dialogs.alert("Profile not found!")
            return
        self.window.ui.dialog['profile.item'].id = 'profile'
        self.window.ui.dialog['profile.item'].uuid = uuid
        self.window.ui.dialog['profile.item'].mode = 'edit'
        self.window.ui.dialog['profile.item'].path = profile['workdir'].replace("%HOME%", str(Path.home()))
        self.window.ui.dialog['profile.item'].input.setText(profile['name'])
        self.window.ui.dialog['profile.item'].prepare()
        self.window.ui.dialog['profile.item'].show()

    def open(self, force: bool = False):
        """
        Open profiles editor

        :param force: force open
        """
        if not self.initialized:
            self.setup()
            self.initialized = True
        if not self.dialog or force:
            self.window.ui.dialogs.open(
                'profile.editor',
                width=self.width,
                height=self.height,
            )
            self.dialog = True
            self.select_current_on_list()

    def close(self):
        """Close profile dialog"""
        if self.dialog:
            self.window.ui.dialogs.close('profile.editor')
            self.dialog = False

    def toggle_editor(self):
        """Toggle profile dialog"""
        if self.dialog:
            self.close()
        else:
            self.open()

    def handle_update(self, mode: str, name: str, path: str, uuid: str = None):
        """
        Handle new/edit profile dialog

        :param mode: mode (create | update | duplicate)
        :param name: profile name
        :param path: profile workdir path
        :param uuid: profile UUID (update and duplicate only)
        """
        current = self.window.core.config.profile.get_current()
        if name.strip() == "":
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.name.empty"))
            return
        if path.strip() == "":
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.path.empty"))
            return
        if not os.path.exists(path) or not os.path.isdir(path):
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.path.not_exists"))
            return

        if not self.window.core.filesystem.is_directory_empty(path):
            if not self.window.core.filesystem.is_workdir_in_path(path):
                self.window.ui.dialogs.alert(trans("dialog.profile.alert.duplicate.not_empty"))
                return

        if mode == 'create':
            # create new profile
            self.window.core.config.profile.add(name, path)
            self.window.ui.status(trans("dialog.profile.status.created"))

        elif mode == 'edit':
            # update profile
            profile = self.window.core.config.profile.get(uuid)
            old_path = profile['workdir'].replace("%HOME%", str(Path.home()))
            self.window.core.config.profile.update_profile(uuid, name, path)
            self.window.ui.status(trans("dialog.profile.status.updated"))

            # if current profile and path was changed then reload:
            if uuid == current and old_path != path:
                self.switch(uuid, force=True)

        elif mode == 'duplicate':
            # duplicate profile (duplicate requires empty directory)
            if not self.window.core.filesystem.is_directory_empty(path):
                self.window.ui.dialogs.alert(trans("dialog.workdir.change.empty.alert"))
                return

            profiles = self.get_profiles()
            if uuid not in profiles:
                self.window.ui.dialogs.alert(trans("dialog.profile.alert.src.empty"))
                return
            profile = profiles[uuid]

            # check if not same path
            if profile['workdir'].replace("%HOME%", str(Path.home())) == path:
                self.window.ui.dialogs.alert(trans("dialog.profile.alert.path.same"))
                return

            # check free space
            src_path = profile['workdir'].replace("%HOME%", str(Path.home()))
            space_required = self.window.core.filesystem.get_directory_size(src_path, human_readable=False)
            space_free = self.window.core.filesystem.get_free_disk_space(path, human_readable=False)
            if space_required > space_free:
                self.window.ui.dialogs.alert(trans("dialog.workdir.result.no_free_space").format(
                    required=self.window.core.filesystem.get_directory_size(src_path),
                    free=self.window.core.filesystem.get_free_disk_space(path),
                ))
                return

            # make duplicate
            self.duplicate(uuid, name, path)
            self.window.ui.status(trans("dialog.profile.status.duplicated"))

        # close dialog and update list
        self.window.ui.dialogs.close('profile.item')
        self.update_menu()
        self.update_list()

    def dismiss_update(self):
        """Dismiss update dialog"""
        self.window.ui.dialogs.close('profile.item')

    def edit_by_idx(self, idx: int):
        """
        Rename profile by index

        :param idx: profile index
        """
        uuid = self.get_id_by_idx(idx)
        self.edit(uuid)

    def select_by_idx(self, idx: int):
        """
        Select profile by index

        :param idx: profile index
        """
        uuid = self.get_id_by_idx(idx)
        self.switch(uuid)

    def delete_by_idx(self, idx: int, force: bool = False):
        """
        Delete profile by index

        :param idx: profile index
        :param force: force delete
        """
        uuid = self.get_id_by_idx(idx)
        current = self.window.core.config.profile.get_current()
        if uuid == current:
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.delete.current"))
            return
        if not force:
            self.window.ui.dialogs.confirm(
                type='profile.delete',
                id=idx,
                msg=trans('confirm.profile.delete'),
            )
            return
        self.delete(uuid)

    def delete(self, uuid: str):
        """
        Delete profile (remove only)

        :param uuid: profile ID
        """
        profiles = self.get_profiles()
        if uuid in profiles:
            profile = profiles[uuid]
            name = profile['name']
            # remove profile
            if self.window.core.config.profile.remove(uuid):
                self.window.ui.status(trans("dialog.profile.status.removed") + ": " + name)
                self.update_list()
                self.update_menu()

    def delete_all_by_idx(self, idx: int, force: bool = False):
        """
        Delete profile with files by index

        :param idx: profile index
        :param force: force delete
        """
        uuid = self.get_id_by_idx(idx)
        current = self.window.core.config.profile.get_current()
        if uuid == current:
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.delete.current"))
            return
        if not force:
            self.window.ui.dialogs.confirm(
                type='profile.delete.all',
                id=idx,
                msg=trans('confirm.profile.delete_all'),
            )
            return
        self.delete_all(uuid)

    def delete_all(self, uuid: str):
        """
        Delete profile with files

        :param uuid: profile ID
        """
        profiles = self.get_profiles()
        if uuid in profiles:
            profile = profiles[uuid]
            name = profile['name']
            path = profile['workdir'].replace("%HOME%", str(Path.home()))
            # remove profile
            if self.window.core.config.profile.remove(uuid):
                if not os.path.exists(path) or not os.path.isdir(path):
                    self.window.ui.dialogs.alert(trans("dialog.profile.alert.path.not_exists"))
                    return
                print("Clearing workdir: ", path)
                self.window.core.filesystem.clear_workdir(path)
                self.window.ui.status(trans("dialog.profile.status.deleted") + ": " + name)
                self.update_list()
                self.update_menu()

    def duplicate(self, uuid: str, new_name: str, new_path: str):
        """
        Duplicate profile

        :param uuid: profile ID
        :param new_name: new profile name
        :param new_path: new profile path
        """
        profiles = self.get_profiles()
        if uuid not in profiles:
            self.window.ui.dialogs.alert("Profile not found!")
            return
        profile = profiles[uuid]

        # make copy
        duplicate = copy.deepcopy(profile)
        new_uuid = str(uuid4())
        duplicate['name'] = new_name
        duplicate['workdir'] = new_path
        self.window.core.config.profile.append(new_uuid, duplicate)

        # copy files from workdir
        path_from = profile['workdir'].replace("%HOME%", str(Path.home()))
        path_to = new_path
        print("Copying all files from {} to: {}".format(path_from, path_to))
        self.window.ui.status("Copying files...")
        result = self.window.core.filesystem.copy_workdir(path_from, path_to)
        if not result:
            self.window.ui.dialogs.alert("Error copying files!")
            self.window.ui.status("Error copying files!")
            return
        print("[OK] All files copied successfully.")
        self.window.ui.status("Files copied.")
        self.update_list()
        self.update_menu()

    def duplicate_by_idx(self, idx: int):
        """
        Duplicate profile by index

        :param idx: profile index
        """
        uuid = self.get_id_by_idx(idx)
        profile = self.window.core.config.profile.get(uuid)
        if profile is None:
            self.window.ui.dialogs.alert("Profile not found!")
            return
        self.window.ui.dialog['profile.item'].id = 'profile'
        self.window.ui.dialog['profile.item'].uuid = uuid
        self.window.ui.dialog['profile.item'].mode = 'duplicate'
        self.window.ui.dialog['profile.item'].path = ""
        self.window.ui.dialog['profile.item'].input.setText(profile['name'] + " - copy")
        self.window.ui.dialog['profile.item'].prepare()
        self.window.ui.dialog['profile.item'].show()

    def reset(self, uuid: str):
        """
        Reset profile

        :param uuid: profile ID
        """
        profiles = self.get_profiles()
        if uuid in profiles:
            profile = profiles[uuid]
            path = profile['workdir'].replace("%HOME%", str(Path.home()))
            if not os.path.exists(path) or not os.path.isdir(path):
                self.window.ui.dialogs.alert("Directory not exists!")
                return
            print("Clearing workdir: ", path)
            self.window.core.filesystem.clear_workdir(path)
            self.window.ui.status("Profile cleared: " + profile['name'])

    def reset_by_idx(self, idx: int, force: bool = False):
        """
        Reset profile by index

        :param idx: profile index
        :param force: force reset
        """
        uuid = self.get_id_by_idx(idx)
        current = self.window.core.config.profile.get_current()
        if uuid == current:
            self.window.ui.dialogs.alert(trans("dialog.profile.alert.delete.current"))
            return
        if not force:
            self.window.ui.dialogs.confirm(
                type='profile.reset',
                id=idx,
                msg=trans('confirm.profile.reset'),
            )
            return
        id = self.get_id_by_idx(idx)
        self.reset(id)

    def get_id_by_idx(self, idx: int) -> str:
        """
        Get profile id by index

        :param idx: profile index
        """
        profiles = self.get_profiles()
        if len(profiles) > idx:
            return list(profiles.keys())[idx]

    def update_list(self):
        """Reload profile list"""
        items = self.get_profiles()
        self.window.profiles.update_list("profile.list", items)

    def setup_menu(self):
        """Setup profile menu"""
        profiles = self.window.core.config.profile.get_all()
        current = self.window.core.config.profile.get_current()
        for uuid in profiles:
            if uuid not in self.window.ui.menu['config.profiles']:
                profile = profiles[uuid]
                name = profile['name']
                checked = False
                if uuid == current:
                    name = name + " " + trans("profile.current.suffix")
                    checked = True
                self.window.ui.menu['config.profiles'][uuid] = QAction(
                    name,
                    self.window,
                    checkable=True,
                )
                self.window.ui.menu['config.profiles'][uuid].setChecked(checked)
                self.window.ui.menu['config.profiles'][uuid].triggered.connect(
                    lambda checked=True, uuid=uuid: self.window.controller.settings.profile.switch(uuid))
                self.window.ui.menu['config.profile'].addAction(self.window.ui.menu['config.profiles'][uuid])

    def update_menu(self):
        """Update menu"""
        profiles = self.window.core.config.profile.get_all()
        current = self.window.core.config.profile.get_current()
        for uuid in list(self.window.ui.menu['config.profiles'].keys()):
            if uuid in profiles:
                name = profiles[uuid]['name']
                checked = False
                if uuid == current:
                    name = name + " " + trans("profile.current.suffix")
                    checked = True
                self.window.ui.menu['config.profiles'][uuid].setText(name)
                self.window.ui.menu['config.profiles'][uuid].setChecked(checked)

        # add new profiles
        for uuid in list(profiles.keys()):
            if uuid not in self.window.ui.menu['config.profiles']:
                profile = profiles[uuid]
                name = profile['name']
                checked = False
                if uuid == current:
                    name = name + " " + trans("profile.current.suffix")
                    checked = True
                self.window.ui.menu['config.profiles'][uuid] = QAction(
                    name,
                    self.window,
                    checkable=True,
                )
                self.window.ui.menu['config.profiles'][uuid].setChecked(checked)
                self.window.ui.menu['config.profiles'][uuid].triggered.connect(
                    lambda checked=True, uuid=uuid: self.window.controller.settings.profile.switch(uuid)
                )
                self.window.ui.menu['config.profile'].addAction(self.window.ui.menu['config.profiles'][uuid])

        # remove non-exist profiles
        for uuid in list(self.window.ui.menu['config.profiles'].keys()):
            if uuid not in profiles:
                self.window.ui.menu['config.profile'].removeAction(self.window.ui.menu['config.profiles'][uuid])
                del self.window.ui.menu['config.profiles'][uuid]

