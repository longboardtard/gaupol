# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Audio actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n import _


class ShowAudioTrackMenuAction(gaupol.Action):

    """Show the audio track menu."""

    def __init__(self):
        """Initialize a :class:`ShowAudioTrackMenuAction` instance."""
        gaupol.Action.__init__(self, "show-audio-track-menu")
        self.set_label(_("_Language"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)
        languages = application.player.get_audio_languages()
        aeidon.util.affirm(languages is not None)


class VolumeDownAction(gaupol.Action):

    """Decrease volume."""

    def __init__(self):
        """Initialize a :class:`VolumeDownAction` instance."""
        gaupol.Action.__init__(self, "volume-down")
        self.set_label(_("Volume _Down"))
        self.set_tooltip(_("Decrease volume"))
        self.accelerator = "<Ctrl>minus"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


class VolumeUpAction(gaupol.Action):

    """Increase volume."""

    def __init__(self):
        """Initialize a :class:`VolumeUpAction` instance."""
        gaupol.Action.__init__(self, "volume-up")
        self.set_label(_("Volume _Up"))
        self.set_tooltip(_("Increase volume"))
        self.accelerator = "<Ctrl>plus"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.player is not None)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
