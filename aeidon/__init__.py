# Copyright (C) 2005-2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Reading, writing and manipulating text-based subtitle files.

:mod:`aeidon` is a Python package that provides classes and functions for
dealing with text-based subtitle files of many different formats. Functions
exist for reading and writing subtitle files as well as manipulating subtitle
data, i.e. positions (times or frames) and texts. Three examples of basic use
of the :mod:`aeidon` package follow below.

Converting a file from the SubRip format to the MicroDVD format::

    project = aeidon.Project()
    project.open_main("/path/to/file.srt", "utf_8")
    project.set_framerate(aeidon.framerates.FPS_23_976)
    project.save_main(aeidon.files.new(aeidon.formats.MICRODVD,
                                       "/path/to/file.sub",
                                       "utf_8"))

Making all subtitles in a file appear two seconds earlier::

    project = aeidon.Project()
    project.open_main("/path/to/file.srt", "utf_8")
    project.shift_positions(None, -2.0)
    project.save_main()

Removing all blank subtitles::

    project = aeidon.Project()
    project.open_main("/path/to/file.srt", "utf_8")
    indices = [i for i, x in enumerate(project.subtitles)
               if not x.main_text]

    project.remove_subtitles(indices)
    project.save_main()

:mod:`aeidon` handles positions as either times (as strings of form
``HH:MM:SS.SSS``), frames (as integers) or in some cases seconds (as floats).
All these can be used with functions that edit subtitle data regardless of what
the native position type of the file format used is.

:mod:`aeidon` handles two separate documents that comprise a project -- a main
and a translation document. These correspond to separate files, but the
subtitles are common since positions are shared.

:mod:`aeidon` includes an undo/redo-system. Any subtitle data-editing methods
of :class:`aeidon.Project` (ones marked with the :func:`aeidon.deco.revertable`
decorator) can be undone and redone. If using :mod:`aeidon` in a context where
reverting actions is never needed, greater flexibility can be achieved by
accessing the subtitles directly (via :attr:`aeidon.Project.subtitles`).

:var CONFIG_HOME_DIR: Path to the user's local configuration directory
:var DATA_DIR: Path to the global data directory
:var DATA_HOME_DIR: Path to the user's local data directory
:var LOCALE_DIR: Path to the global locale directory

:var align_methods: Enumerations for subtitle align methods
:var documents: Enumerations for document types
:var formats: Enumerations for subtitle file format types
:var framerates: Enumerations for framerate types
:var modes: Enumerations for position unit types
:var newlines: Enumerations for newline character types
:var players: Enumerations for video player application types
:var registers: Enumerations for action action reversion register types

:var debug: ``True`` to perform additional run-time checks

   `debug` is used in many cases at import time and should thus not be set
   directly, but rather by setting a non-blank value, e.g. "1", to either of
   environment variables ``AEIDON_DEBUG`` or ``GAUPOL_DEBUG``.

:var re_any_tag: Regular expression for markup tags of any format
"""

import os
import re

__version__ = "0.19"

debug = (bool(os.environ.get("AEIDON_DEBUG", "")) or
         bool(os.environ.get("GAUPOL_DEBUG", "")))

re_any_tag = re.compile(r"(^[/\\_]+|<.*?>|\{.*?\})")

from aeidon.paths import *
from aeidon import deco
from aeidon import i18n
from aeidon import util
from aeidon import temp
from aeidon.contractual import *
from aeidon.delegate import *
from aeidon.singleton import *
from aeidon.mutables import *
from aeidon.observable import *
from aeidon.errors import *
from aeidon.enum import *
from aeidon.enums.align import *
from aeidon.enums.documents import *
from aeidon.enums.formats import *
from aeidon.enums.framerates import *
from aeidon.enums.modes import *
from aeidon.enums.newlines import *
from aeidon.enums.players import *
from aeidon.enums.registers import *
from aeidon import encodings
from aeidon import languages
from aeidon import countries
from aeidon import locales
from aeidon import scripts
from aeidon.metadata import *
from aeidon.calculator import *
from aeidon.finder import *
from aeidon.parser import *
from aeidon.liner import *
from aeidon import containers
from aeidon.subtitle import *
from aeidon.file import *
from aeidon import files
from aeidon.markup import *
from aeidon import tags
from aeidon.converter import *
from aeidon.pattern import *
from aeidon.patternman import *
from aeidon.clipboard import *
from aeidon.revertable import *
from aeidon import agents
from aeidon.project import *
from aeidon.unittest import *
