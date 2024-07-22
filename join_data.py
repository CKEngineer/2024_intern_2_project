import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from main import df,root
from filter_operations import display_filtered_data



def join_data():
    if df is not None:
        join_window = tk.Toplevel(root)
        join_window.title("Join Data")
        join_window.geometry("400x300")
        
        tk.Label(join_window, text="Join with another CSV file").pack(pady=5)
        file_button = tk.Button(join_window, text="Select File", command=load_join_file)
        file_button.pack(pady=10)

def load_join_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global join_df
        join_df = pd.read_csv(file_path)

        join_window = tk.Toplevel(root)
        join_window.title("Join Data")
        join_window.geometry("400x300")

        tk.Label(join_window, text="Select Join Key (Column)").pack(pady=5)
        key_entry = ttk.Combobox(join_window, values=list(df.columns))
        key_entry.pack(pady=5)

        tk.Label(join_window, text="Select Join Type").pack(pady=5)
        join_type = ttk.Combobox(join_window, values=["inner", "outer", "left", "right"])
        join_type.pack(pady=5)

        def apply_join():
            key = key_entry.get()
            join_t = join_type.get()
            if key and join_t:
                global filtered_df
                filtered_df = df.merge(join_df, on=key, how=join_t)
                display_filtered_data(filtered_df)
                join_window.destroy()

        apply_button = tk.Button(join_window, text="Apply Join", command=apply_join)
        apply_button.pack(pady=10)