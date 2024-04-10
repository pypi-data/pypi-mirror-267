#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.04.09 23:00:00                  #
# ================================================== #

import os
import shutil

from datetime import datetime
from pathlib import PurePath

from PySide6.QtCore import QUrl

from .actions import Actions
from .editor import Editor
from .types import Types
from .url import Url

class Filesystem:
    def __init__(self, window=None):
        """
        Filesystem core

        :param window: Window instance
        """
        self.window = window
        self.actions = Actions(window)
        self.editor = Editor(window)
        self.types = Types(window)
        self.url = Url(window)
        self.workdir_placeholder = "%workdir%"
        self.styles = [
            "style.css",
            "style.dark.css",
            "style.light.css",
            "markdown.css",
            "markdown.dark.css",
            "markdown.light.css",
            "fix_windows.css",
        ]

    def install(self):
        """Install provider data"""
        # data directory
        data_dir = self.window.core.config.get_user_dir('data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)

        # upload directory
        upload_dir = self.window.core.config.get_user_dir('upload')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)

        self.install_css()  # install custom css styles

    def install_css(self, force: bool = False):
        """
        Install custom css styles

        :param force: force install
        """
        css_dir = os.path.join(self.window.core.config.path, 'css')
        if not os.path.exists(css_dir):
            os.mkdir(css_dir)

        src_dir = os.path.join(self.window.core.config.get_app_path(), 'data', 'css')
        dst_dir = os.path.join(self.window.core.config.path, 'css')

        try:
            for style in self.styles:
                src = os.path.join(src_dir, style)
                dst = os.path.join(dst_dir, style)
                if (not os.path.exists(dst) or force) and os.path.exists(src):
                    shutil.copyfile(src, dst)
        except Exception as e:
            print("Error while installing css files: ", e)

    def backup_custom_css(self):
        """Backup user custom css styles"""
        css_dir = os.path.join(self.window.core.config.path, 'css')
        backup_file_extension = '.backup'
        for style in self.styles:
            src = os.path.join(css_dir, style)
            dst = os.path.join(css_dir, style + backup_file_extension)
            if os.path.exists(src):
                shutil.copyfile(src, dst)

    def make_local(self, path: str) -> str:
        """
        Make local placeholder path

        :param path: path to prepare
        :return: local path with working dir placeholder
        """
        return path.replace(
            self.window.core.config.get_user_path(),
            self.workdir_placeholder
        )

    def make_local_list(self, paths: list) -> list:
        """
        Make local placeholder paths

        :param paths: list with paths to prepare
        :return: local paths with working dir placeholder
        """
        return [self.make_local(path) for path in paths]

    def make_local_list_img(self, paths: list) -> list:
        """
        Make local placeholder paths for images

        :param paths: list with paths to prepare
        :return: local paths with working dir placeholder
        """
        img_ext = self.types.get_img_ext()
        result = []
        for path in paths:
            if path.endswith(tuple(img_ext)):
                result.append(self.make_local(path))
        return result

    def get_url(self, url) -> QUrl:
        """
        Make current OS-specific URL to open file or directory

        :param url: URL to prepare
        :return: URL to open file or directory
        """
        if self.window.core.platforms.is_windows():
            if not url.startswith('file:///'):
                url = 'file:///' + url
            return QUrl(url, QUrl.TolerantMode)
        else:
            return QUrl.fromLocalFile(url)

    def get_path(self, path) -> str:
        """
        Prepare current OS-specific path from given path

        :param path: path to prepare
        :return: prepared OS-specific path
        """
        parts = PurePath(path).parts
        if len(parts) > 1:
            return os.path.join(*parts)  # rebuild OS directory separators
        return path

    def to_workdir(self, path) -> str:
        """
        Replace user path with current workdir

        :param path: path to fix
        :return: path with replaced user workdir
        """
        path = self.get_path(path)
        work_dir = self.window.core.config.get_user_path()  # current OS app workdir

        # try to find %workdir% placeholder in path
        if self.workdir_placeholder in path:
            return path.replace(
                self.workdir_placeholder,
                work_dir
            )

        # try to find workdir in path: old versions compatibility, < 2.0.113
        if work_dir.endswith('.config/pygpt-net'):
            work_dir = work_dir.rsplit('/.config/pygpt-net', 1)[0]
        elif work_dir.endswith('.config\\pygpt-net'):
            work_dir = work_dir.rsplit('\\.config\\pygpt-net', 1)[0]

        if self.window.core.platforms.is_windows():
            dir_index = path.find('\\.config\\pygpt-net\\') + 1
        else:
            dir_index = path.find('/.config/pygpt-net/') + 1

        parts = path[dir_index:]
        return os.path.join(work_dir, parts)

    def extract_local_url(self, path) -> (str, str):
        """
        Extract local url and path from url

        :param path: local path or url
        :return: url, path
        """
        if not self.is_schema(path):
            path = self.to_workdir(path)

        prefix = ''
        if not self.is_schema(path):
            if self.window.core.platforms.is_windows():
                prefix = 'file:///'
            else:
                prefix = 'file://'

        url = prefix + path
        return url, path

    def get_workdir_prefix(self) -> str:
        """
        Get workdir prefix

        :return: workdir prefix
        """
        prefix = ''
        if self.window.core.platforms.is_windows():
            prefix = 'file:///'
        else:
            prefix = 'file://'
        return prefix + self.window.core.config.get_user_path()

    def in_work_dir(self, path: str) -> bool:
        """
        Check if path is in work directory

        :param path: path to file
        :return: True if path is in work directory
        """
        work_dir = self.window.core.config.get_user_dir("data")
        return path.startswith(work_dir)

    def store_upload(self, path: str) -> str:
        """
        Store file in upload directory

        :param path: path to uploading file
        :return: path to stored uploaded file
        """
        upload_dir = self.window.core.config.get_user_dir("upload")
        file_name = os.path.basename(path)
        upload_path = os.path.join(upload_dir, file_name)
        # if file exists, add datetime prefix
        if os.path.exists(upload_path):
            upload_path = os.path.join(upload_dir, datetime.now().strftime("%Y-%m-%d_%H-%M-%S_") + file_name)
        shutil.copyfile(path, upload_path)
        return upload_path

    def remove_upload(self, path: str) -> None:
        """
        Delete uploaded file

        :param path: path to uploading file
        """
        upload_dir = self.window.core.config.get_user_dir("upload")
        if path.startswith(upload_dir):
            if os.path.exists(path):
                os.remove(path)

    def is_schema(self, path: str) -> bool:
        """
        Check if path has schema prefix (http, https, file)

        :param path: path to check
        :return: True if path has schema prefix
        """
        return path.startswith('file://') or path.startswith('http://') or path.startswith('https://')

    def sizeof_fmt(self, num: float, suffix='B') -> str:
        """
        Convert numbers to human-readable unit formats.

        :param num: number to convert
        :param suffix: suffix to add
        :return: human-readable format
        """
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    def get_directory_size(self, directory : str, human_readable: bool = True) -> str or int:
        """
        Calculate the total size of the given directory

        :param directory: directory path
        :param human_readable: return human-readable format
        :return: total size of the directory
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        if human_readable:
            return self.sizeof_fmt(total_size)
        return total_size

    def get_free_disk_space(self, directory: str, human_readable: bool = True) -> str or int:
        """
        Check free disk space in the given directory

        :param directory: directory path
        :param human_readable: return human-readable format
        :return: free disk space
        """
        total, used, free = shutil.disk_usage(os.path.dirname(directory))
        if human_readable:
            return self.sizeof_fmt(free)
        return free

    def copy_workdir(self, path: str, new_path: str) -> bool:
        """
        Copy working directory

        :param path: current working directory
        :param new_path: new working directory
        :return: True if working directory is copied
        """
        if os.path.isdir(path):
            for item in os.listdir(path):
                s = os.path.join(path, item)
                d = os.path.join(new_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks=False, ignore=None)
                else:
                    shutil.copy2(s, d)

        # put empty "path.cfg"
        lock_file = os.path.join(new_path, 'path.cfg')
        with open(lock_file, 'w', encoding='utf-8') as f:
            f.write('')

        # remove "profile.json" if exists
        profile_file = os.path.join(new_path, 'profile.json')
        if os.path.exists(profile_file):
            os.remove(profile_file)
        return True

    def clear_workdir(self, path: str) -> bool:
        """
        Clear working directory

        :param path: path to working directory
        :return: True if working directory is cleared
        """
        persist_files = ["app.log", "path.cfg", "profile.json"]
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                if item not in persist_files:
                    os.remove(item_path)
            else:
                shutil.rmtree(item_path)
        return True

    def is_workdir_in_path(self, path: str) -> bool:
        """
        Check if workdir is in path

        :param path: path to check
        :return: True if workdir is in path
        """
        files = ["config.json", "db.sqlite"]
        for file in files:
            if not os.path.exists(os.path.join(path, file)):
                return False
        return True

    def is_directory_empty(self, path: str) -> bool:
        """
        Check if directory is empty

        :param path: directory path
        :return: True if directory is empty
        """
        return len(os.listdir(path)) == 0

