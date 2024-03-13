# main.py
import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import create_table, insert_entry, search_database, delete_entry
import pathlib, os


# Create the main window
root = tk.Tk()
root.title("Fishing Log")
root.geometry("800x600")
#root.maxsize(800,800)

img_file_name = "picfish.ico"
current_dir = pathlib.Path(__file__).parent.resolve() # current directory
img_path = os.path.join(current_dir, img_file_name)
img= PhotoImage(file=img_path)
root.iconphoto(False,img)


#frames for left & right sides==================NEW ================CHANGES========21FEB
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for search box and button
search_frame = tk.Frame(right_frame)
search_frame.pack(pady=5)

# Labels for the entry boxes
entry_labels = ["Fish Species","Weight (LBs)", "Lure Type", "Location", "Date"]

# Initialize the list to hold the entry widgets
entries = []

#Create text boxes with labels
label_width = max(len(text) for text in entry_labels)

for i in range(5):
    entry_frame = tk.Frame(left_frame)
    entry_frame.pack(pady=2, fill=tk.X)

    label = tk.Label(entry_frame, text=entry_labels[i], width=label_width, anchor='w')
    label.grid(row=0, column=0, sticky=tk.W, padx=(10, 5))

    entry = tk.Entry(entry_frame)
    entry.grid(row=0, column=1, sticky=tk.EW, padx=(5, 10))
    entries.append(entry)

    # Configure the column weights to allocate extra space to the entry widget
    entry_frame.grid_columnconfigure(1, weight=1)

def submit_action():
    # Collect data from all text boxes
    data = [entry.get() for entry in entries]
    # Insert the data into the database
    insert_entry(*data)
    print("Saved to database:", data)

# Create a single submit button
submit_button = tk.Button(left_frame, text="Submit", command=submit_action)#CHANGED ROOT TO LEFT_FRAME
submit_button.pack(pady=10)

# Initialize the database table
create_table()

# Add a label before the search box
search_label = tk.Label(search_frame, text="Search by keyword:")
search_label.pack(side=tk.LEFT, padx=(0,5))

# Create and configure style
style = ttk.Style()
style.theme_use("default")

# Style for Treeview
style.configure("Treeview",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

# Style for Treeview Header
style.configure("Treeview.Heading",
                background="#B0B0B0",
                foreground="black",
                font=('Arial', 10, 'bold'))



# Grid lines in Treeview
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) # Remove borders
style.configure("Treeview", grid_lines="both") # "both", "vertical" or "horizontal"

#header names in display box
column_headers = ["Fish Species","Weight (LBs)", "Lure Type", "Location", "Date"]

#use Treeview to incorporate headers on displayed columns
result_tree = ttk.Treeview(right_frame, columns=column_headers, show='headings')

for col in column_headers:
    result_tree.heading(col, text=col)

result_tree.pack(padx=(1,1), pady=5, fill=tk.BOTH,expand= True)

def search_action(event=None):
    global entry_ids
    entry_ids = []  # Clear the previous ids
    search_query = search_entry.get()
    results = search_database(search_query)
    result_tree.delete(*result_tree.get_children())  # Clear existing results
    for row in results:
        entry_ids.append(row[0])  # Store the id
        result_tree.insert('', tk.END, values=row[1:])  # Insert row

#ensure table fits within the display box size
total_width = 500  # Width of the Treeview
column_width = total_width // len(column_headers)  # Divide equally among columns

for col in column_headers:
    result_tree.column(col, width=column_width, anchor='w')


# Add a search box
search_entry = tk.Entry(search_frame)  # Add it to search_frame instead of right_frame
search_entry.pack(side=tk.LEFT, padx=(0,5)) 

# Bind the Enter key to the search_action function
search_entry.bind("<Return>", search_action)

# Add a search button
search_button = tk.Button(search_frame, text="Search", command=search_action)
search_button.pack(side=tk.LEFT)

# Add a list box to display the results
#result_list = tk.Listbox(right_frame)#CHANGED ROOT TO RIGHT_FRAME
#result_list.pack(padx=(10,10), pady=5, fill=tk.BOTH, expand=True)

def delete_action():
    global entry_ids
    selection = result_tree.selection()  # Get the selected items

    if selection:
        for selected_item in selection:
            # Get the index of the selected item
            index = result_tree.index(selected_item)
            entry_id = entry_ids[index]  # Get the ID from the stored list
            delete_entry(entry_id)  # Pass the ID to delete_entry
            result_tree.delete(selected_item)  # Remove from Treeview

# Add a delete button
delete_button = tk.Button(right_frame, text="Delete", command=delete_action)#CHANGED ROOT TO RIGHT_FRAME
delete_button.pack(pady=5)

# Start the GUI event loop
root.mainloop()
