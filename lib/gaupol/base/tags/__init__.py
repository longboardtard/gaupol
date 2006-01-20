# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Base class for subtitle tag libraries."""


try:
    from psyco.classes import *
except ImportError:
    pass


class TagLibrary(object):

    """
    Base class for subtitle tag libraries.

    In the special case that a format does not contain any tags, this class can
    simply be subclassed with a pass statement.

    decode_tags is a list of regular expressions that convert tags to the
    Gaupol internal format. encode_tags convert from the Gaupol internal format
    to the class's format.

    pre- and post-decode and -encode functions can be used to perform arbitrary
    tasks in tag conversion. pre-methods are run before regular exressions
    and post-methods after.

    Gaupol internal tags are:
    <b></b>
    <i></i>
    <u></u>
    <color="#rrggbb"></color>
    <font="name"></font>
    <size="int"></size>
    """

    # Pattern, Flags
    tag        = '', None
    italic_tag = '', None

    # List of tuples (pattern, flags, replacement)
    decode_tags = []
    encode_tags = [
        (
            # Remove all tags.
            r'<.*?>', None,
            r''
        )
    ]

    @staticmethod
    def pre_decode(text):
        return text

    @staticmethod
    def post_decode(text):
        return text

    @staticmethod
    def pre_encode(text):
        return text

    @staticmethod
    def post_encode(text):
        return text

    @staticmethod
    def italicize(text):
        """Italicize text."""
        return text