# Filaments

Filaments is a simple Windows 11 desktop application that helps 3D printing enthusiasts keep track of their filament collection. If you've ever lost important filament information—like brand, color, material, flushing volume, or calibration data—after a firmware update (especially from Bambu Lab printers), this app is for you.

With Filaments, you can:
 - Store detailed information about each filament spool
 - View and manage your entire collection in one place
 - Preserve important data that might otherwise be deleted by printer software updates

To get started, simply download the latest setup.exe from the Releases page, install it on your Windows 11 machine, and launch the app—no technical experience needed.

# For Contributers

## Introduction

This project is a simple GUI application designed to manage filament data using the MVP (Model-View-Presenter) architecture. It allows users to store, view, and update information about various filaments in a SQLite3 database. The requirement for this project came from the Bambulabs updates etc deleting or removing my filament data including calibration values and flushing volume values that are calibrated.

If you are interested in helping to expand on this project, I welcome anyone with interest to reach out to me at [scottc.filaments@gmail.com](scottc.filaments@gmail.com)

## Project Structure

```
filament_gui_app
├── src
│   ├── main.py               # Entry point of the application
│   ├── model
│   │   ├── database.py       # Handles database operations
│   │   └── filament.py       # Defines the Filament data model
│   ├── view
│   │   ├── main_screen.py     # Main screen of the GUI
│   │   └── components
│   │       └── form.py       # Form components for inputting data
│   └── presenter
│       └── main_presenter.py  # Intermediary between model and view
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Features

- Add new filament records with attributes such as:
  - Brand
  - Color
  - Material
  - Weight
  - Purchase Link
  - Cost
- View existing filament records
- Update filament information

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd filament_gui_app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Use the main screen to navigate through the application.
- Fill out the form to add new filament data.
- Access existing records to view or update information as needed.

## License

This project is licensed under the MIT License.
