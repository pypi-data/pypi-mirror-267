#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2024  Florian Grethler

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import base64
import textwrap


class Sh2Py:
    """
    Convert a python script into a obfuscated shell script. \n
    If this shell script is run it will create the original python script. \n
    This can be used for obfuscation purposes or to hide the code
    when sharing it with others. \n
    """
    def __init__(self, path: str) -> None:
        self.python_script: str = open(path, "rb").read()
        self.custom_output_path: str = ""
        self.output_name: str = ""
        if not self.output_name:
            self.filename: str = f"{self.custom_output_path}{os.path.basename(path)}"
        else:
            self.filename: str = f"{self.custom_output_path}{self.output_name}"
        self.shell_script: str = "#!/bin/bash\n"

    def __fileout(self) -> None:
        """
        Writes the shell script to a file.
        """
        with open("shell_script.sh", "w") as file:
            file.write(self.shell_script)

    def base64_encode(self):
        """
        Encodes the python script into base64.
        """
        b64: str = base64.b64encode(self.python_script).decode()
        if len(b64) > 64:
            b64 = textwrap.wrap(b64, width=64)
            self.shell_script += f"b64='{b64[0]}'\n"
            for i in range(1, len(b64)):
                self.shell_script += f"b64+='{b64[i]}'\n"
        else:
            self.shell_script += f"b64={b64}"
        self.shell_script += f"\necho $b64 | base64 -d > {self.filename}"
        self.__fileout()
