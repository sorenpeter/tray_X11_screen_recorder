#!/usr/bin/env python3

#  _____                 __  ___ _   ____
# |_   _| __ __ _ _   _  \ \/ / / | / ___|  ___ _ __ ___  ___ _ __
#   | || '__/ _` | | | |  \  /| | | \___ \ / __| '__/ _ \/ _ \ '_ \
#   | || | | (_| | |_| |  /  \| | |  ___) | (__| | |  __/  __/ | | |
#   |_||_|  \__,_|\__, | /_/\_\_|_| |____/ \___|_|  \___|\___|_| |_|
#                 |___/
#  ____                        _
# |  _ \ ___  ___ ___  _ __ __| | ___ _ __
# | |_) / _ \/ __/ _ \| '__/ _` |/ _ \ '__|
# |  _ <  __/ (_| (_) | | | (_| |  __/ |
# |_| \_\___|\___\___/|_|  \__,_|\___|_|
#
#
# A simple and easy way to video record your desktop
# Author: Andrianos Papamarkou
#



import sys
import os
import logging
import datetime
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QSettings, QRect, Qt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setFixedSize(400, 400)  # Set the size of the dialog

        # Create a layout
        layout = QVBoxLayout()

        # Create a label with information
        title_label = QLabel(
            "<h1 style='text-align: center;'>Tray X11 Screen Recorder</h1>"
            "<h2 style='text-align: center;'>Version 1.0</h2>"
            "<p>A system tray icon to record your desktop</p>"
            "<p>Author <b>Andrianos Papamarkou</b></p>"
            "<p><a href='https://github.com/apapamarkou/tray_X11_screen_recorder'>Visit on GitHub</a></p>"
        )

        title_label.setAlignment(Qt.AlignCenter)
        title_label.setOpenExternalLinks(True)

        # Add the labels to the layout
        layout.addWidget(title_label)

        # Set the layout for the dialog
        self.setLayout(layout)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

class ScreenRecorderTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(ScreenRecorderTray, self).__init__(parent)

        # Load settings
        self.settings = QSettings('ScreenRecorder', 'TrayApp')
        self.load_settings()

        # Set initial recording state
        self.recording = False

        # Set tray icon
        self.set_icon(self.recording)

        # Create context menu
        self.menu = QMenu(parent)
        self.create_menu()

        # Set the tray icon context menu
        self.setContextMenu(self.menu)

        # Connect click events
        self.activated.connect(self.on_tray_icon_activated)

        # Initialize recording state
        self.is_recording = False
        self.recording_process = None

        # Create a timer to update tooltip
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tooltip)
        self.timer.start(1000)  # Update every second

        # Initialize the about dialog
        self.about_dialog = AboutDialog()

    def set_icon(self, is_recording):
        if is_recording:
            self.setIcon(QIcon.fromTheme("media-playback-stoped"))
        else:
            self.setIcon(QIcon.fromTheme("media-record-symbolic"))

    def create_menu(self):
        # Area submenu
        self.area_menu = QMenu("Area", self.menu)
        self.full_screen_action = QAction("Full Screen", self.area_menu, checkable=True)
        self.full_screen_action.setChecked(self.area == "Full Screen")
        self.full_screen_action.triggered.connect(self.update_area)
        self.area_menu.addAction(self.full_screen_action)

        self.active_window_action = QAction("Active Window", self.area_menu, checkable=True)
        self.active_window_action.setChecked(self.area == "Active Window")
        self.active_window_action.triggered.connect(self.update_area)
        self.area_menu.addAction(self.active_window_action)

        self.menu.addMenu(self.area_menu)

        # Framerate submenu
        self.framerate_menu = QMenu("Framerate", self.menu)
        self.framerate_actions = []
        for framerate in [15, 24, 30, 60]:
            action = QAction(f"{framerate} FPS", self.framerate_menu, checkable=True)
            action.setChecked(self.framerate == framerate)
            action.triggered.connect(self.update_framerate)
            self.framerate_menu.addAction(action)
            self.framerate_actions.append(action)

        self.menu.addMenu(self.framerate_menu)

        # Add sound checkbox
        self.sound_action = QAction("With Sound", self, checkable=True)
        self.sound_action.setChecked(self.with_sound)
        self.sound_action.triggered.connect(self.update_with_sound)
        self.menu.addAction(self.sound_action)

        # Add start and stop actions
        self.start_action = QAction("Start Recording", self)
        self.start_action.triggered.connect(self.start_recording)
        self.menu.addAction(self.start_action)

        self.stop_action = QAction("Stop Recording", self)
        self.stop_action.triggered.connect(self.stop_recording)
        self.menu.addAction(self.stop_action)

        # Add about and quit actions
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)
        self.menu.addAction(self.about_action)

        self.quit_action = QAction("Quit", self)
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)

    def load_settings(self):
        self.area = self.settings.value("area", "Full Screen")
        self.framerate = int(self.settings.value("framerate", 30))
        self.with_sound = self.settings.value("with_sound", True, type=bool)

    def save_settings(self):
        self.settings.setValue("area", self.area)
        self.settings.setValue("framerate", self.framerate)
        self.settings.setValue("with_sound", self.with_sound)

    def update_tooltip(self):
        tooltip = f"Tray Screen Recorder\nArea: {self.area}\nFramerate: {self.framerate}\nWith Sound: {'Yes' if self.with_sound else 'No'}"
        self.setToolTip(tooltip)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            if not self.is_recording:
                self.start_recording()
            else:
                self.stop_recording()

    def update_area(self):
        action = self.sender()
        if action.isChecked():
            self.area = action.text()
            self.save_settings()

    def update_framerate(self):
        action = self.sender()
        if action.isChecked():
            self.framerate = int(action.text().split()[0])
            self.save_settings()

    def update_with_sound(self):
        self.with_sound = self.sound_action.isChecked()
        self.save_settings()

    def start_recording(self):
        self.set_icon(True)
        self.is_recording = True

        # Ensure no authentication failures
        subprocess.run(['xhost', '+SI:localuser:{}'.format(os.getlogin())])

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_file = os.path.expanduser(f"~/Videos/{timestamp}_recording.mp4")
        self.video_dimensions = "1920x1080"  # Default dimensions for full screen
        command = ["ffmpeg", "-y"]

        if self.area == "Full Screen":
            command += ["-f", "x11grab", "-framerate", str(self.framerate), "-i", ":0.0"]
        elif self.area == "Active Window":
            active_window_geom = subprocess.check_output(
                ["xdotool", "getactivewindow", "getwindowgeometry", "--shell"]
            ).decode().strip().split('\n')
            x = active_window_geom[1].split('=')[1]
            y = active_window_geom[2].split('=')[1]
            width = active_window_geom[3].split('=')[1]
            height = active_window_geom[4].split('=')[1]
            self.video_dimensions = f"{width}x{height}"
            command += ["-f", "x11grab", "-video_size", self.video_dimensions, "-framerate", str(self.framerate), "-i", f":0.0+{x},{y}"]

        if self.with_sound:
            command += ["-f", "pulse", "-ac", "2", "-i", "default"]

        command.append(self.output_file)

        self.recording_process = subprocess.Popen(command)

    def stop_recording(self):
        self.set_icon(False)
        self.is_recording = False
        if self.recording_process:
            self.recording_process.terminate()
            self.recording_process = None

            # Notify user about the recording
            self.show_notification()

    def show_notification(self):
        notification = QSystemTrayIcon.MessageIcon(QSystemTrayIcon.Information)
        self.showMessage(
            "Recording Stopped",
            f"File saved: {self.output_file}\n"
            f"Location: {os.path.dirname(self.output_file)}\n"
            f"Dimensions: {self.video_dimensions}\n"
            f"Framerate: {self.framerate} FPS\n"
            f"With Sound: {'Yes' if self.with_sound else 'No'}",
            notification
        )

    def show_about(self):
        self.about_dialog.show()

    def quit_app(self):
        self.save_settings()
        sys.exit()

def main():
    app = QApplication(sys.argv)
    tray = ScreenRecorderTray()
    tray.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
