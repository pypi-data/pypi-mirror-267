#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.03.12 06:00:00                  #
# ================================================== #

import json

from llama_index.core.readers.base import BaseReader

from .hub.google.calendar import GoogleCalendarReader
from .base import BaseLoader


class Loader(BaseLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = "google_calendar"
        self.name = "Google Calendar"
        self.type = ["web"]
        self.instructions = [
            {
                "google_calendar": {
                    "description": "read and index files from Google Calendar",
                    "args": {
                        "number_of_results": {
                            "type": "int",
                        },
                        "start_date": {
                            "type": "str",
                        },
                    },
                }
            }
        ]
        self.init_args = {
            "credentials_path": "credentials.json",
            "token_path": "token.json",
        }

    def get(self) -> BaseReader:
        """
        Get reader instance

        :return: Data reader instance
        """
        args = self.get_args()
        return GoogleCalendarReader(**args)

    def get_external_id(self, args: dict = None) -> str:
        """
        Get unique web content identifier

        :param args: load_data args
        :return: unique content identifier
        """
        unique = {}
        if "start_date" in args and args.get("start_date"):
            unique["start_date"] = args.get("start_date")
        return json.dumps(unique)

    def prepare_args(self, **kwargs) -> dict:
        """
        Prepare arguments for load_data() method

        :param kwargs: keyword arguments
        :return: args to pass to reader
        """
        args = {}
        if "number_of_results" in kwargs and kwargs.get("number_of_results"):
            if isinstance(kwargs.get("number_of_results"), int):
                args["number_of_results"] = kwargs.get("number_of_results")  # number of results

        if "start_date" in kwargs and kwargs.get("start_date"):
            if isinstance(kwargs.get("start_date"), str):
                args["start_date"] = kwargs.get("start_date")  # start date
        return args
