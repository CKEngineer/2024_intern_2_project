import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from main import filtered_df,root

def plot_data():
    if filtered_df is not None:
        plot_window = tk.Toplevel(root)
        plot_window.title("Plot Data")
        plot_window.geometry("400x600")

        tk.Label(plot_window, text="Select X Axis Column").pack(pady=5)
        x_column_entry = ttk.Combobox(plot_window, values=list(filtered_df.columns))
        x_column_entry.pack(pady=5)

        tk.Label(plot_window, text="Select Y Axis Column").pack(pady=5)
        y_column_entry = ttk.Combobox(plot_window, values=list(filtered_df.columns))
        y_column_entry.pack(pady=5)

        tk.Label(plot_window, text="Select Plot Type").pack(pady=5)
        plot_type_entry = ttk.Combobox(plot_window, values=["line", "bar", "scatter", "hist", "pie", "box", "area"])
        plot_type_entry.pack(pady=5)

        tk.Label(plot_window, text="Plot Title").pack(pady=5)
        title_entry = tk.Entry(plot_window)
        title_entry.pack(pady=5)

        tk.Label(plot_window, text="X Label").pack(pady=5)
        xlabel_entry = tk.Entry(plot_window)
        xlabel_entry.pack(pady=5)

        tk.Label(plot_window, text="Y Label").pack(pady=5)
        ylabel_entry = tk.Entry(plot_window)
        ylabel_entry.pack(pady=5)

        tk.Label(plot_window, text="Color").pack(pady=5)
        color_entry = tk.Entry(plot_window)
        color_entry.pack(pady=5)

        tk.Label(plot_window, text="Line Style").pack(pady=5)
        linestyle_entry = ttk.Combobox(plot_window, values=['-', '--', '-.', ':'])
        linestyle_entry.pack(pady=5)

        tk.Label(plot_window, text="Marker").pack(pady=5)
        marker_entry = ttk.Combobox(plot_window, values=['o', 's', '^', 'D', 'P', '*'])
        marker_entry.pack(pady=5)

        def apply_plot():
            x_column = x_column_entry.get()
            y_column = y_column_entry.get()
            plot_type = plot_type_entry.get()
            title = title_entry.get()
            xlabel = xlabel_entry.get()
            ylabel = ylabel_entry.get()
            color = color_entry.get()
            linestyle = linestyle_entry.get()
            marker = marker_entry.get()

            if x_column and y_column and plot_type:
                fig, ax = plt.subplots(figsize=(10, 6))
                if plot_type == "line":
                    ax.plot(filtered_df[x_column], filtered_df[y_column], color=color if color else 'b', linestyle=linestyle if linestyle else '-', marker=marker if marker else '')
                elif plot_type == "bar":
                    ax.bar(filtered_df[x_column], filtered_df[y_column], color=color if color else 'b')
                elif plot_type == "scatter":
                    ax.scatter(filtered_df[x_column], filtered_df[y_column], color=color if color else 'b', marker=marker if marker else 'o')
                elif plot_type == "hist":
                    ax.hist(filtered_df[y_column], color=color if color else 'b')
                elif plot_type == "pie":
                    ax.pie(filtered_df[y_column], labels=filtered_df[x_column], autopct='%1.1f%%', colors=[color] if color else None)
                    ax.axis('equal')
                elif plot_type == 'box':
                    ax.boxplot(filtered_df[y_column], patch_artist=True, boxprops=dict(facecolor=color if color else 'b'))
                elif plot_type == 'area':
                    ax.fill_between(filtered_df[x_column], filtered_df[y_column], color=color if color else 'b', alpha=0.5)

                ax.set_title(title if title else f'{plot_type.capitalize()} Plot of {x_column} vs {y_column}')
                ax.set_xlabel(xlabel if xlabel else x_column)
                ax.set_ylabel(ylabel if ylabel else y_column)
                ax.grid(True)

                mplcursors.cursor(ax, hover=True)

                plt.show()
            plot_window.destroy()

        apply_button = tk.Button(plot_window, text="Create Plot", command=apply_plot)
        apply_button.pack(pady=10)
