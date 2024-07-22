import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from helpers import *

df = None
filtered_df = None

def load_data():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            global df
            df = pd.read_csv(file_path)
            display_data(df)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading data: {e}")

def display_data(dataframe):
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


def add_scrollbars(frame, widget):
    try:
        vsb = ttk.Scrollbar(frame, orient="vertical", command=widget.yview)
        vsb.pack(side='right', fill='y')
        widget.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=widget.xview)
        hsb.pack(side='bottom', fill='x')
        widget.configure(xscrollcommand=hsb.set)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding scrollbars: {e}")

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


def analyze_data():
    try:
        if filtered_df is not None:
            analysis_window = tk.Toplevel(root)
            analysis_window.title("Data Analysis")
            analysis_window.geometry("800x600")

            # Create a notebook widget
            notebook = ttk.Notebook(analysis_window)
            notebook.pack(fill=tk.BOTH, expand=True)

            # Create frames for each tab
            head_frame = ttk.Frame(notebook)
            describe_frame = ttk.Frame(notebook)
            detailed_stats_frame = ttk.Frame(notebook)
            columns_frame = ttk.Frame(notebook)

            notebook.add(head_frame, text="First 5 Rows")
            notebook.add(describe_frame, text="Summary Statistics")
            notebook.add(detailed_stats_frame, text="Detailed Stats")
            notebook.add(columns_frame, text="Column Names")

            # Create a canvas widget to enable scrolling for each frame
            def create_scrollable_canvas(parent_frame):
                try:
                    canvas = tk.Canvas(parent_frame)
                    vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
                    hsb = ttk.Scrollbar(parent_frame, orient="horizontal", command=canvas.xview)
                    scroll_frame = ttk.Frame(canvas)

                    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
                    vsb.pack(side=tk.RIGHT, fill=tk.Y)
                    hsb.pack(side=tk.BOTTOM, fill=tk.X)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

                    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                    return scroll_frame
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while creating scrollable canvas: {e}")

            # Display df.head()
            head_scroll_frame = create_scrollable_canvas(head_frame)
            head_tree = ttk.Treeview(head_scroll_frame)
            head_tree["columns"] = list(filtered_df.columns)
            head_tree["show"] = "headings"
            for column in head_tree["columns"]:
                head_tree.heading(column, text=column)
            for index, row in filtered_df.head().iterrows():
                head_tree.insert("", "end", values=list(row))
            head_tree.pack(pady=5, fill=tk.BOTH, expand=True)

            # Display df.describe()
            describe_scroll_frame = create_scrollable_canvas(describe_frame)
            describe_tree = ttk.Treeview(describe_scroll_frame)
            describe_data = filtered_df.describe()
            describe_tree["columns"] = list(describe_data.columns)
            describe_tree["show"] = "headings"
            for column in describe_tree["columns"]:
                describe_tree.heading(column, text=column)
            for index, row in describe_data.iterrows():
                describe_tree.insert("", "end", values=list(row))
            describe_tree.pack(pady=5, fill=tk.BOTH, expand=True)

            # Display more detailed summary statistics
            detailed_stats_scroll_frame = create_scrollable_canvas(detailed_stats_frame)
            numeric_df = filtered_df.select_dtypes(include=[float, int])  # Select only numeric columns
            detailed_stats = {
                "Mean": numeric_df.mean(),
                "Median": numeric_df.median(),
                "Mode": numeric_df.mode().iloc[0],  # Mode can have multiple values, taking the first one
                "Standard Deviation": numeric_df.std(),
                "Variance": numeric_df.var(),
                "Min": numeric_df.min(),
                "Max": numeric_df.max(),
                "25th Percentile": numeric_df.quantile(0.25),
                "50th Percentile (Median)": numeric_df.quantile(0.5),
                "75th Percentile": numeric_df.quantile(0.75)
            }

            for stat_name, stat_values in detailed_stats.items():
                stat_label = tk.Label(detailed_stats_scroll_frame, text=f"{stat_name}:\n{stat_values}\n")
                stat_label.pack(pady=5, anchor="w")

            # Display column names
            columns_scroll_frame = create_scrollable_canvas(columns_frame)
            columns_label = tk.Label(columns_scroll_frame, text="Column Names:\n" + "\n".join(filtered_df.columns))
            columns_label.pack(pady=5, anchor="w")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred in analyze_data function: {e}")

def project_columns():
    if df is not None:
        project_window = tk.Toplevel(root)
        project_window.title("Project Columns")
        project_window.geometry("400x300")
        
        tk.Label(project_window, text="Select Columns (comma separated)").pack(pady=5)
        column_entry = tk.Entry(project_window)
        column_entry.pack(pady=5)

        def apply_projection():
            columns = column_entry.get().split(',')
            columns = [col.strip() for col in columns]
            if columns:
                global filtered_df
                filtered_df = df.loc[:, columns]
                display_filtered_data(filtered_df)
                project_window.destroy()

        apply_button = tk.Button(project_window, text="Apply Projection", command=apply_projection)
        apply_button.pack(pady=10)

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




def show_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("500x400")

    notebook = ttk.Notebook(help_window)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create frames for each tab
    usage_frame = ttk.Frame(notebook)
    feedback_frame = ttk.Frame(notebook)
    development_frame = ttk.Frame(notebook)

    notebook.add(usage_frame, text="Usage")
    notebook.add(feedback_frame, text="Feedback")
    notebook.add(development_frame, text="Development")

    # Usage tab content
    usage_text = tk.Text(usage_frame, wrap="word")
    usage_text.insert("1.0", """
    Usage Instructions:

    - Load Data: Load a CSV file into the application.
    - Analyze Data: Display basic statistics and information about the data.
    - Clean/Transform Data: Apply cleaning and transformation operations to the data.
    - Filter Data: Filter the data based on specific conditions.
    - Project Columns: Select specific columns to display.
    - Join Data: Join the loaded data with another CSV file.
    - Sort Data: Sort the data based on a selected column.
    - Group By Data: Group the data by a specific column and apply aggregation functions.
    - Plot Data: Create various types of plots based on the data.
    """)
    usage_text.config(state=tk.DISABLED)
    usage_text.pack(fill=tk.BOTH, expand=True)

    # Feedback tab content
    feedback_text = tk.Text(feedback_frame, wrap="word")
    feedback_text.insert("1.0", """
    Feedback:

    We value your feedback to improve this application. Please let us know if you encounter any issues or have suggestions for new features.

    You can provide feedback through the following methods:

    - Email: cankarakuzu3@gmail.com
    - GitHub: https://github.com/CKEngineer/2024_intern_2_project/issues
    """)
    feedback_text.config(state=tk.DISABLED)
    feedback_text.pack(fill=tk.BOTH, expand=True)

    # Development tab content
    development_text = tk.Text(development_frame, wrap="word")
    development_text.insert("1.0", """
    Development Information:
                            
    Developed by: CKEngineer

    This application was developed using Python and the Tkinter library for the graphical user interface. It also uses pandas for data manipulation and matplotlib for data visualization.

    For more information about the development process or to contribute to the project, please visit our GitHub repository:

    GitHub: https://github.com/CKEngineer/2024_intern_2_project

    If you are interested in contributing, please follow the guidelines in the repository and feel free to submit pull requests.
    """)
    development_text.config(state=tk.DISABLED)
    development_text.pack(fill=tk.BOTH, expand=True)


# Create the main window
root = tk.Tk()
root.title("Data Analyse and Visualization Application")
root.geometry("900x600")

# Create a frame to contain the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Add buttons to the button frame
load_button = tk.Button(button_frame, text="Load Data", command=load_data)
load_button.pack(side=tk.LEFT, padx=5)

analyze_button = tk.Button(button_frame, text="Analyze Data", command=analyze_data)
analyze_button.pack(side=tk.LEFT, padx=5)

clean_button = tk.Button(button_frame, text="Clean/Transform Data", command=clean_and_transform_function)
clean_button.pack(side=tk.LEFT, padx=5)

filter_button = tk.Button(button_frame, text="Filter Data", command=filter_data)
filter_button.pack(side=tk.LEFT, padx=5)

project_button = tk.Button(button_frame, text="Project Columns", command=project_columns)
project_button.pack(side=tk.LEFT, padx=5)

join_button = tk.Button(button_frame, text="Join Data", command=join_data)
join_button.pack(side=tk.LEFT, padx=5)

sort_button = tk.Button(button_frame, text="Sort Data", command=sort_data)
sort_button.pack(side=tk.LEFT, padx=5)

groupby_button = tk.Button(button_frame, text="Group By Data", command=groupby_data)
groupby_button.pack(side=tk.LEFT, padx=5)

plot_button = tk.Button(button_frame, text="Plot Data", command=plot_data)
plot_button.pack(side=tk.LEFT, padx=5)

help_button = tk.Button(button_frame, text="Help", command=show_help)
help_button.pack(side=tk.LEFT, padx=5)

# Add a frame for the data display
tree_frame = ttk.Frame(root)
tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Add the Treeview widget
tree = ttk.Treeview(tree_frame)
tree.pack(side='left', fill=tk.BOTH, expand=True)

# Add scrollbars to the treeview
add_scrollbars(tree_frame, tree)

# Run the main loop
root.mainloop()
