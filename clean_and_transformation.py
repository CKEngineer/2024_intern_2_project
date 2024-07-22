import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import root
from data_operations import display_data
from helpers import save_data


def clean_and_transform_function():
    if df is not None:
        combined_window = tk.Toplevel(root)
        combined_window.title("Data Cleaning and Transformation")
        combined_window.geometry("400x400")

        tk.Label(combined_window, text="Select Operation").pack(pady=5)
        operation = ttk.Combobox(combined_window, values=[
            "Clean Data", 
            "Fill Missing Values", 
            "Remove Duplicates", 
            "Change Data Type",
            "Rename Column",
            "Add New Column",
            "Manipulate Column"
        ])
        operation.pack(pady=5)

        tk.Label(combined_window, text="Column (if applicable)").pack(pady=5)
        column = ttk.Combobox(combined_window, values=list(df.columns) + ["None"])
        column.pack(pady=5)

        tk.Label(combined_window, text="Value / Data Type / New Name (if applicable)").pack(pady=5)
        value_entry = tk.Entry(combined_window)
        value_entry.pack(pady=5)

        def apply_combined_function():
            op = operation.get()
            col = column.get()
            val = value_entry.get()
            global df

            try:
                if op == "Clean Data":
                    initial_rows = len(df)
                    initial_na = df.isna().sum().sum()

                    df.fillna(0, inplace=True)  # Replace NaN values with 0
                    df.drop_duplicates(inplace=True)  # Remove duplicate rows

                    final_rows = len(df)
                    final_na = df.isna().sum().sum()

                    rows_removed = initial_rows - final_rows
                    na_filled = initial_na - final_na

                    report = f"Data Cleaning Report:\n\nRows removed: {rows_removed}\nMissing values filled: {na_filled}"

                    display_data(df)
                    messagebox.showinfo("Data Cleaning Complete", report)

                elif op == "Fill Missing Values" and col:
                    df[col].fillna(val, inplace=True)

                elif op == "Remove Duplicates":
                    df.drop_duplicates(inplace=True)

                elif op == "Change Data Type" and col and val:
                    df[col] = df[col].astype(val)
                
                elif op == "Rename Column" and col and val:
                    df.rename(columns={col: val}, inplace=True)

                elif op == "Add New Column" and val:
                    df[val] = None  # Add new column with default None values

                elif op == "Manipulate Column" and col:
                    if val:
                        df[col] = val  # Set all values in the column to the specified value
                    else:
                        messagebox.showwarning("Warning", "Please enter a value to set for the column.")

                display_data(df)
                
                if messagebox.askyesno("Save Data", "Do you want to save the changes?"):
                    save_data(df)
                
                combined_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        apply_button = tk.Button(combined_window, text="Apply", command=apply_combined_function)
        apply_button.pack(pady=10)
