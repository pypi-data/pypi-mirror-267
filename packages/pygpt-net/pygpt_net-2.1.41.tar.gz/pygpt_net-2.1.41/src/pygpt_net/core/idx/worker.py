#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.23 01:00:00                  #
# ================================================== #

from PySide6.QtCore import QObject, Signal, QRunnable, Slot


class IndexWorkerSignals(QObject):
    finished = Signal(str, object, object, bool)  # idx, result, errors, silent mode
    error = Signal(object)


class IndexWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(IndexWorker, self).__init__()
        self.signals = IndexWorkerSignals()
        self.window = None
        self.content = None
        self.from_ts = 0
        self.idx = None
        self.type = None
        self.silent = False

    @Slot()
    def run(self):
        """Indexer thread"""
        try:
            result = {}
            errors = []

            # log
            self.log("Indexing data...")
            self.log("Idx: {}, type: {}, content: {}, from_ts: {}".format(
                self.idx,
                self.type,
                self.content,
                self.from_ts,
            ))

            # execute indexing
            if self.type == "file":
                result, errors = self.window.core.idx.index_files(
                    self.idx,
                    self.content,
                )
            elif self.type == "db_meta":
                result, errors = self.window.core.idx.index_db_by_meta_id(
                    self.idx,
                    self.content,
                    self.from_ts,
                )
            elif self.type == "db_current":
                result, errors = self.window.core.idx.index_db_from_updated_ts(
                    self.idx,
                    self.content,
                )

            self.log("Finished indexing.")
            self.signals.finished.emit(
                self.idx,
                result,
                errors,
                self.silent,
            )
        except Exception as e:
            self.window.core.debug.error(e)
            self.signals.error.emit(e)

    def log(self, msg: str):
        """
        Log info message

        :param msg: message
        """
        is_log = False
        if self.window.core.config.has("log.llama") \
                and self.window.core.config.get("log.llama"):
            is_log = True
        self.window.core.debug.info(msg, not is_log)
        if is_log:
            print("[LLAMA-INDEX] {}".format(msg))
