import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import df,root
from filter_operations import display_filtered_data


def sort_data():
    if df is not None:
        sort_window = tk.Toplevel(root)
        sort_window.title("Sort Data")
        sort_window.geometry("400x300")

        tk.Label(sort_window, text="Select Column to Sort By").pack(pady=5)
        column_entry = ttk.Combobox(sort_window, values=list(df.columns))
        column_entry.pack(pady=5)

        tk.Label(sort_window, text="Select Sort Order").pack(pady=5)
        order_entry = ttk.Combobox(sort_window, values=["Ascending", "Descending"])
        order_entry.pack(pady=5)

        def apply_sort():
            column = column_entry.get()
            order = order_entry.get()
            ascending = True if order == "Ascending" else False
            if column:
                global filtered_df
                filtered_df = df.sort_values(by=column, ascending=ascending)
                display_filtered_data(filtered_df)
                sort_window.destroy()

        apply_button = tk.Button(sort_window, text="Apply Sort", command=apply_sort)
        apply_button.pack(pady=10)

def groupby_data():
    if df is not None:
        groupby_window = tk.Toplevel(root)
        groupby_window.title("Group By Data")
        groupby_window.geometry("400x300")

        tk.Label(groupby_window, text="Select Column to Group By").pack(pady=5)
        column_entry = ttk.Combobox(groupby_window, values=list(df.columns))
        column_entry.pack(pady=5)

        tk.Label(groupby_window, text="Select Aggregation Function").pack(pady=5)
        agg_entry = ttk.Combobox(groupby_window, values=["sum", "mean", "min", "max", "count"])
        agg_entry.pack(pady=5)

        def apply_groupby():
            column = column_entry.get()
            agg_func = agg_entry.get()
            if column and agg_func:
                global filtered_df
                grouped_df = df.groupby(column).agg(agg_func).reset_index()
                filtered_df = grouped_df
                display_filtered_data(filtered_df)
                groupby_window.destroy()

        apply_button = tk.Button(groupby_window, text="Apply Group By", command=apply_groupby)
        apply_button.pack(pady=10)
