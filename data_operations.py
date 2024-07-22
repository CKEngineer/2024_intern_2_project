import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd


def load_data():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            global df
            df = pd.read_csv(file_path)
            display_data(df)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading data: {e}")

def display_data(tree,dataframe):
    try:
        # Clear previous data
        for item in tree.get_children():
            tree.delete(item)
        
        # Set up the columns
        tree["column"] = list(dataframe.columns)
        tree["show"] = "headings"
        for column in tree["columns"]:
            tree.heading(column, text=column)
        
        # Insert data into the treeview
        for index, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying data: {e}")