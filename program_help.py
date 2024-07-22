import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from main import root


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