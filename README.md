# Tray X11 Screen Recorder

Tray X11 Screen Recorder is a system tray application to record your desktop using `ffmpeg`. It provides options to record the full screen or the active window with customizable framerate and sound settings.

## Features

- Record Full Screen or Active Window
- Select Framerate (15, 24, 30, 60 FPS)
- Record with or without sound
- Easy access from the system tray
- Notifications for recording status
- About dialog with author information and GitHub link

## Dependencies

Before running the application, you need to install the following dependencies:

- Python 3
- PyQt5
- ffmpeg
- xdotool (for capturing active window geometry)

### Installation on Various Distributions

#### Arch/Manjaro/Garuda
```sh
sudo pacman -Syu python python-pyqt5 ffmpeg xdotool
```

#### Redhat/Fedora
```sh
sudo dnf install python3 python3-qt5 ffmpeg xdotool
```

#### openSUSE
```sh
sudo zypper install python3 python3-qt5 ffmpeg xdotool
```

#### Ubuntu/Mint/Debian
```sh
sudo apt update
sudo apt install python3 python3-pyqt5 ffmpeg xdotool
```

#### Solus
```sh
sudo eopkg install python3 python3-pyqt5 ffmpeg xdotool
```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/apapamarkou/tray_X11_screen_recorder.git ~/Applications/tray_X11_screen_recorder
   chmod +x ~/Applications/tray_X11_screen_recorder/tray_X11_screen_recorder.py
   ```

## Adding to Startup Programs

### KDE

1. Open `System Settings`.
2. Go to `Startup and Shutdown` -> `Autostart`.
3. Click `Add Login Script...` and browse to the location of `~/Applications/tray_X11_screen_recorder/tray_X11_screen_recorder.py`.
4. Select the script and click `OK`.

### Gnome

1. Open `Startup Applications` from the application menu.
2. Click `Add`.
3. Enter a name for the application (e.g., `Tray X11 Screen Recorder`).
4. In the `Command` field, enter the path to `~/Applications/tray_X11_screen_recorder/tray_X11_screen_recorder.py`.
5. Click `Add`.

### XFCE

1. Open `Settings Manager`.
2. Go to `Session and Startup`.
3. In the `Application Autostart` tab, click `Add`.
4. Enter a name for the application (e.g., `Tray X11 Screen Recorder`).
5. In the `Command` field, enter the path to `~/Applications/tray_X11_screen_recorder/tray_X11_screen_recorder.py`.
6. Click `OK`.

### i3wm

1. Open your i3 configuration file (usually located at `~/.config/i3/config`).
2. Add the following line:
   ```sh
   exec --no-startup-id ~/Applications/tray_X11_screen_recorder/tray_X11_screen_recorder.py
   ```
3. Save the file and reload i3 (usually `Mod+Shift+R`).

## Usage

Once the application is running, you can access it from the system tray. Right-click the tray icon to access the menu options. Left-click the tray icon to start or stop recording.

Copy and paste this into a `README.md` file in your GitHub repository. This should provide all the necessary information for users to install and use your application.

