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


"""Cell renderer for cells containing integer data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gtk.cellrend.text import CellRendererText


class CellRendererInteger(CellRendererText):

    """Cell renderer for cells containing integer data."""

    def on_start_editing(self, event, widget, row, background_area, cell_area,
                         flags):
        """
        Initiate editing of the cell.

        Return gtk.Entry.
        """
        editor = gtk.Entry()
        editor.set_has_frame(False)
        editor.set_activates_default(True)
        editor.set_size_request(-1, cell_area.height)
        editor.modify_font(self.font_description)

        editor.set_text(self.text or u'')

        editor.connect('editing-done'   , self.on_editing_done, row)
        editor.connect('insert-text'    , self.on_insert_text      )
        editor.connect('key-press-event', self.on_key_press_event  )

        editor.grab_focus()
        editor.show()
        return editor

    def on_insert_text(self, editor, text, length, pointer):
        """
        Insert text to the cell.

        text must consist solely of digits to be inserted.
        """
        if not text.isdigit():
            editor.emit_stop_by_name('insert-text')

    def on_key_press_event(self, editor, event):
        """
        Respond to key press events.

        Cancel editing if Escape pressed.
        """
        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == 'Escape':
            editor.remove_widget()
            self.emit('editing-canceled')
            return True