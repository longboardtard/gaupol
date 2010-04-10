# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Dialogs for applying linear tranfromations to positions."""

import aeidon
import gaupol
import gtk
_ = aeidon.i18n._

__all__ = ("FrameTransformDialog", "TimeTransformDialog")


class PositionTransformDialog(gaupol.BuilderDialog):

    """Base class for dialogs for transforming positions."""

    _widgets = ("correction_hbox_1",
                "correction_hbox_2",
                "correction_label_1",
                "correction_label_2",
                "current_radio",
                "input_entry_1",
                "input_entry_2",
                "preview_button_1",
                "preview_button_2",
                "selected_radio",
                "subtitle_spin_1",
                "subtitle_spin_2",
                "text_label_1",
                "text_label_2")

    def __init__(self, parent, application):
        """Initialize a :class:`PositionTransformDialog` object."""
        gaupol.BuilderDialog.__init__(self, "transform-dialog.ui")
        self.application = application
        self._init_input_labels()
        self._init_sensitivities()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_target(self):
        """Return the selected target."""
        if self._selected_radio.get_active():
            return gaupol.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        raise ValueError("Invalid target radio state")

    def _init_input_labels(self):
        """Initialize non-editable input entries."""
        style = self._correction_label_1.get_style()
        text_color = style.fg[gtk.STATE_NORMAL]
        base_color = style.bg[gtk.STATE_NORMAL]
        for entry in (self._input_entry_1, self._input_entry_2):
            entry.modify_text(gtk.STATE_NORMAL, text_color)
            entry.modify_base(gtk.STATE_NORMAL, base_color)

    def _init_sensitivities(self):
        """Initialize sensitivities of widgets."""
        page = self.application.get_current_page()
        if page.project.video_path is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button_1.set_sensitive(False)
            self._preview_button_2.set_sensitive(False)

    def _init_sizes(self):
        """Initialize widget sizes."""
        gaupol.util.scale_to_size(self._text_label_1, 40, -1)
        gaupol.util.scale_to_size(self._text_label_2, 40, -1)

    def _init_values(self):
        """Intialize default values for widgets."""
        page = self.application.get_current_page()
        self._subtitle_spin_1.set_value(1)
        self._subtitle_spin_2.set_value(len(page.project.subtitles))
        self._subtitle_spin_1.emit("value-changed")
        self._subtitle_spin_2.emit("value-changed")
        target = gaupol.conf.position_transform.target
        self._selected_radio.set_active(target == gaupol.targets.SELECTED)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)
        rows = page.view.get_selected_rows()
        if (not rows) and (target == gaupol.targets.SELECTED):
            self._current_radio.set_active(True)
        self._selected_radio.set_sensitive(bool(rows))

    def _init_widgets(self):
        """Initialize properties of widgets."""
        page = self.application.get_current_page()
        last_subtitle = len(page.project.subtitles)
        self._subtitle_spin_1.set_range(1, last_subtitle)
        self._subtitle_spin_2.set_range(1, last_subtitle)

    def _on_preview_button_1_clicked(self, *args):
        """Preview changes from the first point."""
        page = self.application.get_current_page()
        row = self._subtitle_spin_1.get_value_as_int() - 1
        doc = aeidon.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_preview_button_2_clicked(self, *args):
        """Preview changes from the second point."""
        page = self.application.get_current_page()
        row = self._subtitle_spin_2.get_value_as_int() - 1
        doc = aeidon.documents.MAIN
        method = page.project.transform_positions
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        args = (rows, point_1, point_2)
        self.application.preview_changes(page, row, doc, method, args)

    def _on_response(self, dialog, response):
        """Save target and transform positions."""
        gaupol.conf.position_transform.target = self._get_target()
        if response == gtk.RESPONSE_OK:
            self._transform_positions()

    def _transform_positions(self):
        """Transform positions in subtitles."""
        page = self.application.get_current_page()
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        point_1 = self._get_first_point()
        point_2 = self._get_second_point()
        page.project.transform_positions(rows, point_1, point_2)


class FrameTransformDialog(PositionTransformDialog):

    """Dialog for applying linear tranfromations to frames."""

    __metaclass__ = aeidon.Contractual

    def __init__(self, parent, application):
        """Initialize a :class:`FrameTransformDialog` object."""
        PositionTransformDialog.__init__(self, parent, application)
        self._output_spin_1 = gtk.SpinButton()
        self._output_spin_2 = gtk.SpinButton()
        self._init_widgets()
        self._init_values()

    def _get_first_point_ensure(self, value):
        assert isinstance(value[1], int)

    def _get_first_point(self):
        """Return row, output frame of the first sync point."""
        return (self._subtitle_spin_1.get_value_as_int() - 1,
                self._output_spin_1.get_value_as_int())

    def _get_second_point_ensure(self, value):
        assert isinstance(value[1], int)

    def _get_second_point(self):
        """Return row, output frame of the second sync point."""
        return (self._subtitle_spin_2.get_value_as_int() - 1,
                self._output_spin_2.get_value_as_int())

    def _init_widgets(self):
        """Initialize properties of widgets."""
        PositionTransformDialog._init_widgets(self)
        self._input_entry_1.set_width_chars(6)
        self._input_entry_2.set_width_chars(6)
        self._output_spin_1.set_digits(0)
        self._output_spin_2.set_digits(0)
        self._output_spin_1.set_increments(1, 10)
        self._output_spin_2.set_increments(1, 10)
        self._output_spin_1.set_range(0, 999999)
        self._output_spin_2.set_range(0, 999999)
        self._correction_hbox_1.pack_start(self._output_spin_1)
        self._correction_hbox_2.pack_start(self._output_spin_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_spin_1)
        self._correction_label_2.set_mnemonic_widget(self._output_spin_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_1.set_text(str(subtitle.start_frame))
        self._output_spin_1.set_value(subtitle.start_frame)
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.re_any_tag.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.props.adjustment.props.lower = row + 2

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_2.set_text(str(subtitle.start_frame))
        self._output_spin_2.set_value(subtitle.start_frame)
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.re_any_tag.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.props.adjustment.props.upper = row


class TimeTransformDialog(PositionTransformDialog):

    """Dialog for applying linear tranfromations to times."""

    __metaclass__ = aeidon.Contractual

    def __init__(self, parent, application):
        """Initialize a :class:`TimeTransformDialog` object."""
        PositionTransformDialog.__init__(self, parent, application)
        self._output_entry_1 = gaupol.TimeEntry()
        self._output_entry_2 = gaupol.TimeEntry()
        self._init_widgets()
        self._init_values()

    def _get_first_point_ensure(self, value):
        assert isinstance(value[1], basestring)

    def _get_first_point(self):
        """Return row, output time of the first sync point."""
        return (self._subtitle_spin_1.get_value_as_int() - 1,
                self._output_entry_1.get_text())

    def _get_second_point_ensure(self, value):
        assert isinstance(value[1], basestring)

    def _get_second_point(self):
        """Return row, output time of the second sync point."""
        return (self._subtitle_spin_2.get_value_as_int() - 1,
                self._output_entry_2.get_text())

    def _init_widgets(self):
        """Initialize properties of widgets."""
        PositionTransformDialog._init_widgets(self)
        self._input_entry_1.set_width_chars(13)
        self._input_entry_2.set_width_chars(13)
        self._correction_hbox_1.pack_start(self._output_entry_1)
        self._correction_hbox_2.pack_start(self._output_entry_2)
        self._correction_hbox_1.show_all()
        self._correction_hbox_2.show_all()
        self._correction_label_1.set_mnemonic_widget(self._output_entry_1)
        self._correction_label_2.set_mnemonic_widget(self._output_entry_2)

    def _on_subtitle_spin_1_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_1.set_text(subtitle.start_time)
        self._output_entry_1.set_text(subtitle.start_time)
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.re_any_tag.sub("", text)
        self._text_label_1.set_text(text)
        self._text_label_1.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_2.props.adjustment.props.lower = row + 2
        # Allow the glib.idle_add-using TimeEntry to update.
        gaupol.util.iterate_main()

    def _on_subtitle_spin_2_value_changed(self, spin_button):
        """Update subtitle data in widgets."""
        page = self.application.get_current_page()
        row = spin_button.get_value_as_int() - 1
        subtitle = page.project.subtitles[row]
        self._input_entry_2.set_text(subtitle.start_time)
        self._output_entry_2.set_text(subtitle.start_time)
        text = subtitle.main_text.replace("\n", " ")
        text = aeidon.re_any_tag.sub("", text)
        self._text_label_2.set_text(text)
        self._text_label_2.set_tooltip_text(subtitle.main_text)
        self._subtitle_spin_1.props.adjustment.props.upper = row
        # Allow the glib.idle_add-using TimeEntry to update.
        gaupol.util.iterate_main()