import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import df,root


def filter_data():
    try:
        if df is not None:
            filter_window = tk.Toplevel(root)
            filter_window.title("Filter Data")
            filter_window.geometry("400x300")
            
            tk.Label(filter_window, text="Select Column").pack(pady=5)
            column = ttk.Combobox(filter_window, values=list(df.columns))
            column.pack(pady=5)

            tk.Label(filter_window, text="Condition (e.g. >, <, ==)").pack(pady=5)
            condition = ttk.Combobox(filter_window, values=['>', '<', '==', '!=', '>=', '<='])
            condition.pack(pady=5)

            tk.Label(filter_window, text="Value").pack(pady=5)
            value = tk.Entry(filter_window)
            value.pack(pady=5)

            def apply_filter():
                try:
                    col = column.get()
                    cond = condition.get()
                    val = value.get()
                    if col and cond and val:
                        query = f"{col} {cond} {val}"
                        try:
                            global filtered_df
                            filtered_df = df.query(query)
                            display_filtered_data(filtered_df)
                            filter_window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error", f"An error occurred while applying filter: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred in filter function: {e}")

            apply_button = tk.Button(filter_window, text="Apply Filter", command=apply_filter)
            apply_button.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in filter_data function: {e}")

def display_filtered_data(dataframe):
    try:
        filtered_window = tk.Toplevel(root)
        filtered_window.title("Filtered Data")
        filtered_window.geometry("800x600")

        filtered_frame = ttk.Frame(filtered_window)
        filtered_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        filtered_tree = ttk.Treeview(filtered_frame)

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(filtered_frame, orient="vertical", command=filtered_tree.yview)
        vsb.pack(side='right', fill='y')
        filtered_tree.configure(yscrollcommand=vsb.set)

        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(filtered_frame, orient="horizontal", command=filtered_tree.xview)
        hsb.pack(side='bottom', fill='x')
        filtered_tree.configure(xscrollcommand=hsb.set)

        # Set up the columns
        filtered_tree["column"] = list(dataframe.columns)
        filtered_tree["show"] = "headings"
        for column in filtered_tree["columns"]:
            filtered_tree.heading(column, text=column)
        
        # Insert data into the treeview
        for index, row in dataframe.iterrows():
            filtered_tree.insert("", "end", values=list(row))
        
        # Pack the treeview widget
        filtered_tree.pack(fill=tk.BOTH, expand=True)

        # Add Save button
        save_button = tk.Button(filtered_window, text="Save Filtered Data", command=save_filtered_data)
        save_button.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying filtered data: {e}")

def save_filtered_data():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            filtered_df.to_csv(file_path, index=False)
            messagebox.showinfo("File Saved", f"Filtered data has been saved as {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving filtered data: {e}")
