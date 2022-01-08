#!/usr/bin/env python
""" Simple pomadoro timer for Linux.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Oleg Papka"
__contact__ = "olegpapka2@gmail.com"
__copyright__ = "Copyright 2022, Oleg Papka"
__date__ = "2022/01/06"
__deprecated__ = False
__email__ =  "olegpapka2@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "OlegPapka2"
__status__ = "Production"
__version__ = "0.1.0"

# ---------------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GLib, Gdk, GdkPixbuf, Notify

import os 
import chime
from datetime import datetime, timedelta
from playsound import playsound

# ---------------------------------------------------------------------------

timer_running_flag = False
focus_running_flag = None

focus_time = 25
break_time = 5

alarm_flag = True

dir_path = os.path.dirname(os.path.realpath(__file__))

icon_path = f'{dir_path}/src/icon.png'
sound_path = f'{dir_path}/src/1.mp3'

APP_NAME = 'pomodoro_timer'

# ---------------------------------------------------------------------------

class Main_window(Gtk.Window):

    def __init__(self) -> None:
        super().__init__(title=APP_NAME, default_width=300, default_height=270)
        self.set_border_width(15)
        self.set_resizable(False)

        self.duration = 0
        self.end_time = 0
        self.start_time = 0
        self.state = ''
        self.notification = None
        

        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = APP_NAME
        self.set_titlebar(hb)

        mbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        pmenu = Gtk.Menu()

        self.settings_btn = Gtk.MenuItem(label='Settings')
        self.settings_btn.connect('activate', self.settings_clicked)
        self.settings_btn.show()
        pmenu.append(self.settings_btn)

        self.info_btn = Gtk.MenuItem(label='Info')
        self.info_btn.connect('activate', self.info_clicked)
        self.info_btn.show()
        pmenu.append(self.info_btn)

        mb = Gtk.MenuButton(popup=pmenu)
        mbox.add(mb)
        hb.pack_start(mbox)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        screen = Gdk.Screen.get_default()
        gtk_provider = Gtk.CssProvider()
        gtk_context = Gtk.StyleContext()
        gtk_context.add_provider_for_screen(screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        css =b"""
        #timer-lbl { 
                font-weight: bold;
                font-size: 34px
                } """

        gtk_provider.load_from_data(css)

        self.timer_lbl = Gtk.Label()
        self.timer_lbl.set_text('00:00')
        self.timer_lbl.set_name('timer-lbl')
        box.pack_start(self.timer_lbl, True, True, 0)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(0.0)
        box.pack_start(self.progressbar, False, False, 0)

        self.duration_lbl = Gtk.Label()
        self.duration_lbl.set_text('00:00 - 00:00')
        box.pack_start(self.duration_lbl, True, True, 0)

        self.button = Gtk.Button.new_with_label("Start")
        self.button.connect("clicked", self.on_start_clicked)
        box.pack_start(self.button, True, True, 0)


    def send_notification(self):
        global alarm_flag
        
        Notify.init('pomadoro_timer')

        self.notification = Notify.Notification.new('Pomodoro', f'{self.state} pomo ended! Choose action:', icon_path)
        self.notification.set_timeout(20000)
        self.notification.set_urgency(2)

        if focus_running_flag:
            self.notification.add_action(
                "break", "Break", self.notification_callback)
        else:
            self.notification.add_action(
                "focus", "Focus", self.notification_callback)

        self.notification.add_action(
            "snooze", "Snooze", self.notification_callback)

        if alarm_flag:
            playsound(sound_path)
        else:
            chime.theme('material')
            chime.info()
        
        self.notification.show()
    

    def notification_callback(self, notification, action_name):
        global timer_running_flag

        if not timer_running_flag:
            if action_name == "snooze":
                GLib.timeout_add_seconds(60, self.send_notification)
            else:
                self.on_start_clicked(button=self.button)


    def change_time(self):
        global timer_running_flag, focus_running_flag

        if not timer_running_flag:
            return False

        t_delta = self.end_time - datetime.now()
        minutes, seconds = divmod(t_delta.seconds, 60)
        out = f'{minutes:02d}:{seconds:02d}'

        self.timer_lbl.set_text(out)
        fr = self.progressbar.get_fraction() + self.n_seconds_in_timer
        self.progressbar.set_fraction(fr)
        
        if out == '00:00':

            if focus_running_flag:
                st = 'break'
                dur = break_time
            else:
                st = 'focus'
                dur = focus_time

            timer_running_flag = False

            self.timer_lbl.set_text('00:00')
            self.duration_lbl.set_text(f'Start {st} pomo({dur}m)?')
            self.button.set_label('Start')

            self.send_notification()
            return False
        
        return True


    def start_timer(self):
        self.change_time()
        GLib.timeout_add_seconds(1, self.change_time)
           

    def on_start_clicked(self, button):
        global timer_running_flag, focus_running_flag, focus_time, break_time
        
        if timer_running_flag:
            # Stops timer
            timer_running_flag = False
            focus_running_flag = None
            self.timer_lbl.set_text('00:00')
            self.duration_lbl.set_text('00:00 - 00:00')
            self.progressbar.set_fraction(0.0)
            button.set_label('Start')

        else:
            # Starts timer
            timer_running_flag = True
            self.progressbar.set_fraction(0.0)

            if focus_running_flag:
                # Start break timer
                focus_running_flag = False
                self.state = 'Break'
                self.duration = break_time
            else:
                # Start focus timer
                focus_running_flag = True
                self.state = 'Focus'
                self.duration = focus_time

            self.start_time = datetime.now()
            self.end_time = self.start_time + timedelta(minutes=self.duration)

            start_time_str = self.start_time.strftime("%H:%M")
            end_time_str = self.end_time.strftime("%H:%M")
            
            self.duration_lbl.set_text(f'{self.state} pomo:  {start_time_str} - {end_time_str}')

            button.set_label('Stop')

            tdelta = self.end_time - self.start_time
            self.n_seconds_in_timer = 1/tdelta.total_seconds()
            self.start_timer()


    def settings_clicked(self, button):
        win_s = Settings_window()
        win_s.show_all()


    def info_clicked(self, button):
        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_border_width(15)
        dialog.set_resizable(False)
        dialog.set_logo_icon_name(APP_NAME)
        dialog.set_program_name(APP_NAME)
        dialog.set_version(__version__)
        dialog.set_website('https://olegpapka.de')
        dialog.set_authors(['Oleg Papka <olegpapka2@gmail.com> (Maintainer)'])
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 100, 100))
        dialog.set_comments('Simple pomadoro timer')
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.run()
        dialog.destroy()


class Settings_window(Gtk.Window):

    def __init__(self) -> None:
        super().__init__(title=APP_NAME)
        self.set_border_width(15)
        self.set_resizable(False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        hbox = Gtk.Box(spacing=15)
        box.pack_start(hbox, True, True, 0)

        self.focus_lbl = Gtk.Label()
        self.focus_lbl.set_text('Focus time (minutes): ')
        hbox.pack_start(self.focus_lbl, True, True, 0)

        focus_adj = Gtk.Adjustment(upper=90, step_increment=1, page_increment=10)
        self.focus_sbtn = Gtk.SpinButton()
        self.focus_sbtn.set_adjustment(focus_adj)
        self.focus_sbtn.set_numeric(True)
        self.focus_sbtn.set_range(1, 90)
        self.focus_sbtn.set_value(focus_time)
        self.focus_sbtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.focus_sbtn.connect("value-changed", self.on_focus_sbtn_change)
        hbox.pack_start(self.focus_sbtn, False, False, 0)

        hbox2 = Gtk.Box(spacing=10)
        box.pack_start(hbox2, True, True, 0)

        self.break_lbl = Gtk.Label()
        self.break_lbl.set_text('Break time (minutes): ')
        hbox2.pack_start(self.break_lbl, True, True, 0)

        break_adj = Gtk.Adjustment(upper=30, step_increment=1, page_increment=10)
        self.break_sbtn = Gtk.SpinButton()
        self.break_sbtn.set_adjustment(break_adj)
        self.break_sbtn.set_numeric(True)
        self.break_sbtn.set_range(1, 90)
        self.break_sbtn.set_value(break_time)
        self.break_sbtn.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.break_sbtn.connect("value-changed", self.on_break_sbtn_change)
        hbox2.pack_start(self.break_sbtn, False, False, 0)

        self.check_alarm = Gtk.CheckButton(label="Allow alarm instead of notification")
        self.check_alarm.connect("toggled", self.on_alarm_toggled)
        
        if alarm_flag:
            self.check_alarm.set_active(True)

        box.pack_start(self.check_alarm, False, False, 0)


    def on_focus_sbtn_change(self, scroll):
        global focus_time
        val = scroll.get_value_as_int()
        scroll.set_value(val)
        focus_time = val

    def on_break_sbtn_change(self, scroll):
        global break_time
        val = scroll.get_value_as_int()
        scroll.set_value(val)
        break_time = val

    def on_alarm_toggled(self, button):
        global alarm_flag     

        if button.get_active():
            alarm_flag = True
        else:
            alarm_flag = False        
        
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    win = Main_window()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
