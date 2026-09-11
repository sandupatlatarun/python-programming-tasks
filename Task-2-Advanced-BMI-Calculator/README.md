# Advanced BMI Calculator

A Python-based Advanced BMI Calculator with a graphical user interface, SQLite database storage, BMI history, and BMI progress graph.

## Features

- Graphical User Interface using Tkinter
- Calculate BMI using weight and height
- Height input in centimeters
- Automatic BMI category detection
- BMI range guide
- SQLite database for storing BMI records
- View previous BMI records
- BMI history graph using Matplotlib
- Clear input fields
- Clear BMI history
- Input validation
- Date and time saved with each BMI record

## BMI Formula

BMI is calculated using:

BMI = Weight (kg) / Height² (m)

The calculator converts height from centimeters to meters automatically.

## BMI Categories

| BMI | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 - 24.9 | Normal Weight |
| 25.0 - 29.9 | Overweight |
| 30.0 and above | Obese |

These categories are intended for adults and BMI is a screening measure, not a medical diagnosis.

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## Requirements

- Python 3
- Matplotlib

Install the required package:

```bash
pip install -r requirements.txt