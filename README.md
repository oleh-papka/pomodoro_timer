# Pomodoro Timer

## Description
This Pomodoro Timer is a simple project to recreate simple but usable time management tool to boost productivity by using the Pomodoro Technique.  
It allows users to work in focused intervals, known as "pomodoros," followed by short breaks to rest.

## Overview
https://github.com/Oleh-Papka/pomodoro_timer/assets/60508074/72b04ef6-af87-42e3-93d2-48b44fee3acf

## Features
- Customizable focus and break intervals
- Desktop notifications to alert the start and end of each interval
- Simple and user-friendly interface

## Prerequisites
Before installing the Pomodoro Timer, ensure you have Python installed on your system. Additionally, the application requires PyGObject for the GUI, which may need to be installed through your system's package manager.

## Installation

**1. Clone the repository:**  
  `git clone https://github.com/Oleh-Papka/pomadoro_timer.git`

**2. Navigate to the project directory:**  
  `cd pomadoro_timer`

**3. Install PyGObject**  
PyGObject is required for the application's GUI. Depending on your operating system, you can install PyGObject using the following commands:
- Ubuntu/Debian  
  `sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0`

- Fedora  
  `sudo dnf install python3-gobject gtk3`

- Arch Linux  
  `sudo pacman -S python-gobject gtk3`

- macOS (using Homebrew)  
  `brew install pygobject3 gtk+3`

**4. Install Python dependencies:**  
  `pip install -r requirements.txt`

## Usage
To run the Pomodoro Timer, execute the following command in the terminal from the project directory:  
`python main.py`

## Contributing
Contributions to the Pomodoro Timer are welcome. Feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the GNU General Public License v3.0. For more information, see the LICENSE file in the repository.
