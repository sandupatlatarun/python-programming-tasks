import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE
# ============================================================

connection = sqlite3.connect("bmi_history.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL,
    date_time TEXT NOT NULL
)
""")

connection.commit()


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        # Validate input
        if weight <= 0 or height_cm <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than 0."
            )
            return

        # Convert centimeters to meters
        height_m = height_cm / 100

        # Calculate BMI
        bmi = weight / (height_m * height_m)

        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
            result_color = "orange"

        elif bmi < 25:
            category = "Normal Weight"
            result_color = "green"

        elif bmi < 30:
            category = "Overweight"
            result_color = "orange"

        else:
            category = "Obese"
            result_color = "red"

        # Current date and time
        date_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save result to database
        cursor.execute("""
        INSERT INTO bmi_records
        (weight, height, bmi, category, date_time)
        VALUES (?, ?, ?, ?, ?)
        """, (
            weight,
            height_m,
            bmi,
            category,
            date_time
        ))

        connection.commit()

        # Display result
        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        messagebox.showinfo(
            "Saved",
            "BMI result saved successfully!"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers."
        )


# ============================================================
# CLEAR INPUTS
# ============================================================

def clear_inputs():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    result_label.config(
        text="BMI: --\nCategory: --",
        fg="black"
    )

    weight_entry.focus()


# ============================================================
# CLEAR DATABASE HISTORY
# ============================================================

def clear_history():
    answer = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all BMI history?"
    )

    if answer:
        cursor.execute("DELETE FROM bmi_records")
        connection.commit()

        messagebox.showinfo(
            "History Cleared",
            "All BMI history has been deleted."
        )


# ============================================================
# VIEW HISTORY
# ============================================================

def view_history():
    history_window = tk.Toplevel(root)

    history_window.title("BMI History")
    history_window.geometry("800x450")

    title = tk.Label(
        history_window,
        text="BMI HISTORY",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=15)

    # Table columns
    columns = (
        "Date",
        "Weight",
        "Height",
        "BMI",
        "Category"
    )

    table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    # Column headings
    for column in columns:
        table.heading(
            column,
            text=column
        )

    # Column widths
    table.column("Date", width=180)
    table.column("Weight", width=120)
    table.column("Height", width=120)
    table.column("BMI", width=100)
    table.column("Category", width=150)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # Get records
    cursor.execute("""
    SELECT date_time, weight, height, bmi, category
    FROM bmi_records
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    # Display records
    for record in records:
        table.insert(
            "",
            "end",
            values=(
                record[0],
                f"{record[1]:.2f} kg",
                f"{record[2]:.2f} m",
                f"{record[3]:.2f}",
                record[4]
            )
        )


# ============================================================
# SHOW BMI GRAPH
# ============================================================

def show_graph():

    cursor.execute("""
    SELECT date_time, bmi
    FROM bmi_records
    ORDER BY id
    """)

    records = cursor.fetchall()

    if not records:
        messagebox.showinfo(
            "No Data",
            "No BMI records available for the graph."
        )
        return

    # Extract data
    dates = [record[0] for record in records]
    bmi_values = [record[1] for record in records]

    # Create graph
    plt.figure(figsize=(10, 5))

    plt.plot(
        dates,
        bmi_values,
        marker="o",
        label="BMI"
    )

    # BMI reference lines
    plt.axhline(
        y=18.5,
        linestyle="--",
        label="Underweight limit"
    )

    plt.axhline(
        y=25,
        linestyle="--",
        label="Normal limit"
    )

    plt.axhline(
        y=30,
        linestyle="--",
        label="Overweight limit"
    )

    plt.title("BMI History")
    plt.xlabel("Date and Time")
    plt.ylabel("BMI")

    plt.xticks(rotation=45)

    plt.legend()

    plt.tight_layout()

    plt.show()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Advanced BMI Calculator")

root.geometry("500x750")

root.resizable(False, False)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=25)


# ============================================================
# WEIGHT INPUT
# ============================================================

weight_label = tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial", 12)
)

weight_label.pack()

weight_entry = tk.Entry(
    root,
    font=("Arial", 13),
    width=25
)

weight_entry.pack(pady=8)


# ============================================================
# HEIGHT INPUT
# ============================================================

height_label = tk.Label(
    root,
    text="Height (cm)",
    font=("Arial", 12)
)

height_label.pack()

height_entry = tk.Entry(
    root,
    font=("Arial", 13),
    width=25
)

height_entry.pack(pady=8)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    width=20,
    command=calculate_bmi
)

calculate_button.pack(pady=15)


# ============================================================
# RESULT
# ============================================================

result_label = tk.Label(
    root,
    text="BMI: --\nCategory: --",
    font=("Arial", 16, "bold")
)

result_label.pack(pady=10)


# ============================================================
# BMI RANGE GUIDE
# ============================================================

range_title = tk.Label(
    root,
    text="BMI RANGE GUIDE",
    font=("Arial", 13, "bold")
)

range_title.pack(pady=(15, 5))


range_label = tk.Label(
    root,
    text=(
        "Below 18.5  → Underweight\n"
        "18.5 - 24.9 → Normal Weight\n"
        "25.0 - 29.9 → Overweight\n"
        "30.0+       → Obese"
    ),
    font=("Arial", 11),
    justify="left"
)

range_label.pack(pady=5)


# ============================================================
# CLEAR INPUT BUTTON
# ============================================================

clear_input_button = tk.Button(
    root,
    text="Clear Inputs",
    font=("Arial", 11),
    width=20,
    command=clear_inputs
)

clear_input_button.pack(pady=8)


# ============================================================
# HISTORY BUTTON
# ============================================================

history_button = tk.Button(
    root,
    text="View BMI History",
    font=("Arial", 11),
    width=20,
    command=view_history
)

history_button.pack(pady=8)


# ============================================================
# GRAPH BUTTON
# ============================================================

graph_button = tk.Button(
    root,
    text="Show BMI Graph",
    font=("Arial", 11),
    width=20,
    command=show_graph
)

graph_button.pack(pady=8)


# ============================================================
# CLEAR HISTORY BUTTON
# ============================================================

clear_history_button = tk.Button(
    root,
    text="Clear BMI History",
    font=("Arial", 11),
    width=20,
    command=clear_history
)

clear_history_button.pack(pady=8)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()