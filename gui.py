import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

from classes import State, Machine
from funcs import getMachine

# Define initial states and transitions for the machine
states_list = getMachine("sample.txt")

# Create State objects
states = [State(state) for state in states_list]

# Create the Machine
dfa = Machine(states)

def displayFile(path):
    with open(path, 'r') as fptr:
        stream = fptr.read()
        machineDef_text_widget.insert(tk.END, stream)

def open_file():
    global states, states_list, dfa

    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if file_path:
        try:
            states_list = getMachine(file_path)
            states = [State(state) for state in states_list]
            dfa = Machine(states)

            with open(file_path, "r") as file:
                file_contents = file.read()
                machineDef_text_widget.config(state=tk.NORMAL)
                machineDef_text_widget.delete("1.0", tk.END)  # Clear any existing text in the text widget
                machineDef_text_widget.insert(tk.END, file_contents)
                machineDef_text_widget.config(state=tk.DISABLED)

            print("File uploaded and variables updated successfully.")
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"File '{file_path}' not found.")
        except IOError as e:
            tk.messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

def change_text(text_widget, new_text):
    """Change the text in the given Text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, new_text)
    text_widget.tag_configure("center", justify='center')
    text_widget.tag_add("center", "1.0", "end")
    text_widget.config(state=tk.DISABLED)

def change_label_text(label_widget, new_text):
    """Change the text of the given Label widget."""
    label_widget.config(text=new_text)

def change_character_color(text_widget, char_index, color):
    """Change the color of a specific character and set all other characters to a different color in the given Text widget."""
    text_widget.config(state=tk.NORMAL)
    text_widget.tag_configure("colored", foreground=color)
    text_widget.tag_add("colored", f"1.{char_index}")
    text_widget.config(state=tk.DISABLED)

def remove_color(text_widget):
    text_widget.config(state=tk.NORMAL)
    text_widget.tag_remove("colored", "1.0","end")
    text_widget.config(state=tk.DISABLED)

def run_button_clicked():
    step_button.config(state=tk.DISABLED)
    run_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.DISABLED)

    global input_string, righthandedge, index, steps
    while not (dfa.isFinal() and index==righthandedge):
        step_button_clicked()
        root.update_idletasks()
        root.after(100)
    step_button.config(state=tk.ACTIVE)
    run_button.config(state=tk.ACTIVE)
    reset_button.config(state=tk.ACTIVE)

def step_button_clicked():
    global input_string, righthandedge, index, steps
    if not (dfa.isFinal() and index==righthandedge):
        char = input_string[index]
        print(char, index, righthandedge)
        current_state = dfa.read_char(char)
        currStateLabel = current_state[0].label

        remove_color(header_value_text)
        if index < 0:
            index = len(input_string) + index
        change_character_color(header_value_text, index, "red")
        
        match current_state[1]:
            case 'L':
                index -= 1
            case 'R':
                index += 1
        print(f"Read Character: {char}, Current State: {current_state[0].label}, Direction: {current_state[1]}")
        steps += 1 

        if currStateLabel[0] == "t" and index==righthandedge:
            currStateLabel = "halt-accept"
        elif currStateLabel == "r" and index==righthandedge:
            currStateLabel = "halt-reject"

        change_label_text(left_value_label, currStateLabel)
        change_label_text(right_value_label, steps)

    else:
        step_button.config(state=tk.DISABLED)
    
def reset_button_clicked():
    global input_string, righthandedge, index, steps
    input_str = '<'+input_field.get()+'>'
    change_text(header_value_text, input_str)
    input_string = header_value_text.get("1.0", tk.END).strip()
    righthandedge = len(input_str)-1
    print("Input: ", input_string)
    index = 0
    steps = 0
    left_value_label.configure(text=0)
    right_value_label.configure(text=0)
    step_button.config(state=tk.ACTIVE)
    dfa.reset()

# Create the main application window
root = tk.Tk()
root.title("2FA GUI")
root.geometry("1080x720")
root.configure(bg='salmon')

# Container for the header text (outside the bigger container)
header_container = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RAISED)
header_container.pack(padx=10, pady=5, fill=tk.BOTH)

# Text for the header container
header_label = tk.Label(header_container, text="Input String", bg="lightgray", font=("Helvetica", 16))
header_label.pack()
header_value_text = tk.Text(header_container, font=("Arial", 14), fg="darkblue", bg="lightyellow", height=1)
header_value_text.pack(fill=tk.BOTH)
header_value_text.insert(tk.END, "<aaabb>")
# Center the text in the Text widget
header_value_text.tag_configure("center", justify='center')
header_value_text.tag_add("center", "1.0", "end")


# Container for the two side-by-side containers
side_by_side_container = tk.Frame(root, bg="salmon")
side_by_side_container.pack(fill=tk.X, expand=True)

# First side-by-side container
left_container = tk.Frame(side_by_side_container, bg="lightgray", bd=2, relief=tk.RAISED)
left_container.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add widgets to the left container (if needed)
left_label = tk.Label(left_container, text="Current State", bg="lightgray", font=("Helvetica", 14))
left_label.pack()
left_value_label = tk.Label(left_container, text="0", font=("Arial", 14), fg="darkblue", bg="lightyellow", width=25, height=1)
left_value_label.pack(fill=tk.BOTH)

# Second side-by-side container
right_container = tk.Frame(side_by_side_container, bg="lightgray", bd=2, relief=tk.RAISED)
right_container.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add widgets to the right container (if needed)
right_label = tk.Label(right_container, text="Steps", bg="lightgray", font=("Helvetica", 14))
right_label.pack()
right_value_label = tk.Label(right_container, text="0", font=("Arial", 14), fg="darkblue", bg="lightyellow", width=25, height=1)
right_value_label.pack(fill=tk.BOTH)

# Bottom container with light gray background
bottom_container = tk.Frame(root, bg="salmon")
bottom_container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Bottom container with light gray background
bottom_left_container = tk.Frame(bottom_container, bg="salmon")
bottom_left_container.pack(padx=10, pady=10, fill=tk.NONE, side = tk.LEFT)

# Controls container with light gray background
controls_container = tk.Frame(bottom_left_container, bg="lightgray", bd=2, relief=tk.RAISED)
controls_container.pack(padx=10, pady=10, fill=tk.NONE, expand=True)

# Label for the controls container
controls_label = tk.Label(controls_container, text="Controls", bg="lightgray", font=("Helvetica", 16))
controls_label.pack()

# Container for buttons (inside the controls container)
buttons_container = tk.Frame(controls_container, bg="lightgray", bd=2, relief=tk.RAISED)
buttons_container.pack(padx=10, pady=10, fill=tk.NONE, expand=True)

# Label for the buttons container
buttons_label = tk.Label(buttons_container, text="Buttons", bg="lightgray", font=("Helvetica", 12))
buttons_label.pack()

# Buttons
run_button = tk.Button(buttons_container, text="Run", command=run_button_clicked)
run_button.pack(side=tk.LEFT, padx=5, pady=5)

step_button = tk.Button(buttons_container, text="Step", command=step_button_clicked)
step_button.pack(side=tk.LEFT, padx=5, pady=5)

reset_button = tk.Button(buttons_container, text="Reset", command=reset_button_clicked)
reset_button.pack(side=tk.LEFT, padx=5, pady=5)

# Container for input (inside the controls container)
input_container = tk.Frame(controls_container, bg="lightgray", bd=2, relief=tk.RAISED)
input_container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label for the input container
input_label = tk.Label(input_container, text="Input String:", bg="lightgray", font=("Helvetica", 12))
input_label.pack()
input_secondlabel = tk.Label(input_container, text="DO NOT INCLUDE ENDMARKERS <,>", bg="lightgray", font=("Helvetica", 9))
input_secondlabel.pack()
# Input field
input_field = tk.Entry(input_container)
input_field.pack(pady=10)

# Container for upload file 
upload_container = tk.Frame(bottom_left_container, bg="lightgray", bd=2, relief=tk.RAISED)
upload_container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label for the upload file container
upload_label = tk.Label(upload_container, text="Machine Definition File:", bg="lightgray", font=("Helvetica", 12))
upload_label.pack()
# Label for the upload file container
upload_file = tk.Button(upload_container, text="Open File", command=open_file,bg="lightyellow")
upload_file.pack(fill=tk.BOTH)

# Container for the scrollable text (inside the controls container)
machineDef_container = tk.Frame(bottom_container, bg="lightgray", bd=2, relief=tk.RAISED)
machineDef_container.pack(padx=5, pady=5, fill=tk.BOTH, expand=True, side=tk.LEFT)

# Label for the text container
machineDef_label = tk.Label(machineDef_container, text="Machine Definition:", bg="lightgray", font=("Helvetica", 14))
machineDef_label.pack()

# Multi-line Text widget with scrollbars
machineDef_text_widget = scrolledtext.ScrolledText(machineDef_container, wrap=tk.WORD, width=50, height=20)
machineDef_text_widget.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
# Display the initial machine definition
displayFile("sample.txt")
machineDef_text_widget.config(state=tk.DISABLED)

input_string = header_value_text.get("1.0", tk.END).strip()
righthandedge = len(input_string)-1
print("Input: ", input_string)
index = 0
steps = 1

# Start the main event loop
root.mainloop()

