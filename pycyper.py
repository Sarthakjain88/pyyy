import tkinter as tk
from tkinter import messagebox
from tkinter import ttk # Import themed tkinter widgets for tabs
import math

#Standard Calculator Functions

def on_button_click(char):
    
   #Appends the clicked character (number or operator) to the display.

    current_text = display.get()
    
    if char in "+-*/":
        # Don't start with an operator
        if not current_text:
            return
        
        # If last char is already an operator, replace it
        if current_text[-1] in "+-*/":
            display.delete(len(current_text) - 1, tk.END)
    
    # Add the new character to the display
    display.insert(tk.END, str(char))


def calculate_result():
    #Evaluates the expression in the display when '=' is clicked.
    #Uses eval() for simplicity, with error handling.

    try:
        expression = display.get()
        
        # Prevent calculation if display is empty or ends with an operator
        if not expression or expression[-1] in "+-*/":
            show_error("Invalid Expression", "Incomplete expression.")
            return

        # Use eval() to compute the result
        # Note: eval() can be a security risk with untrusted input
        result = eval(expression)
        
        # Format result to integer if it's a whole number (e.g., 5.0 -> 5)
        if result == int(result):
            result = int(result)
            
        clear_display()
        display.insert(0, str(result))
        
    except ZeroDivisionError:
        show_error("Division by Zero", "Error: Cannot divide by zero.")
    except SyntaxError:
        show_error("Invalid Expression", "Error: The calculation is invalid.")
    except Exception as e:
        show_error("Error", f"An unexpected error occurred: {e}")

def clear_display():
    """
    Clears the display entry widget.
    """
    display.delete(0, tk.END)

def show_error(title, message):
    """
    Displays a popup error message.
    """
    messagebox.showerror(title, message)
    # Only clear the display if the error is from the main calculator (tab 0)
    if notebook.index(notebook.select()) == 0:
         clear_display()

#NEW BMI Calculator Function
def calculate_bmi():

   # Calculates Body Mass Index (BMI) based on user input.

    try:
        # Get weight and height from the entry fields
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        
        # Validate input
        if weight <= 0 or height_cm <= 0:
            show_error("Invalid Input", "Weight and height must be positive numbers.")
            return
            
        # Calculate BMI (Weight in kg / (Height in m)^2)
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        
        # Update the result label
        bmi_result_label.config(text=f"Your BMI is: {bmi:.2f}")
        
        # Determine the BMI category
        category = ""
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Healthy Weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        
        # Update the category label
        bmi_category_label.config(text=f"Category: {category}")
        
    except ValueError:
        show_error("Invalid Input", "Please enter valid numbers for weight and height.")
    except ZeroDivisionError:
        show_error("Invalid Input", "Height cannot be zero.")

#Main Application Setup 
window = tk.Tk()
window.title("Aesthetic Calculator")
window.geometry("320x480") # Set window size (Increased height for tabs)
window.resizable(False, False) # Prevent window from being resized

# Define colors for the UI for a consistent look
BG_COLOR = "#f5f5f5"
DISPLAY_BG = "#f5f5f5"
DISPLAY_FG = "#000000"
BTN_BG = "#ffffff"
BTN_FG = "#000000"
BTN_OP_BG = "#f59e0b" # Operator buttons (amber)
BTN_OP_FG = "#ffffff"
BTN_EQ_BG = "#f59e0b" # Equals button (amber)
BTN_EQ_FG = "#ffffff"
BTN_CLR_BG = "#d4d4d4" # Clear button (light grey)

window.configure(bg=BG_COLOR)

#Style for TTK Widgets (Tabs & BMI controls)
style = ttk.Style()
style.theme_use('clam') # 'clam' theme allows for more style customization

# Configure the Notebook (tab container)
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
# Configure the tabs themselves
style.configure("TNotebook.Tab", background=BTN_CLR_BG, foreground=BTN_FG, borderwidth=0, padding=[10, 5], font=("Arial", 10, "bold"))
# Style for the *selected* tab
style.map("TNotebook.Tab", background=[("selected", BTN_BG)])
# Configure the frame *inside* each tab
style.configure("TFrame", background=BG_COLOR)

#Create Notebook (Tabs)
notebook = ttk.Notebook(window, style="TNotebook")
notebook.pack(expand=True, fill='both', pady=5, padx=5)

#Tab 1: Standard Calculator
calculator_tab = ttk.Frame(notebook, style="TFrame")
notebook.add(calculator_tab, text='Calculator')

# Create the display screen
display_frame = tk.Frame(calculator_tab, bg=BG_COLOR)
display_frame.pack(pady=20)

display = tk.Entry(
    display_frame, 
    font=("Arial", 28), 
    borderwidth=0, 
    relief="flat", 
    justify="right",
    bg=DISPLAY_BG,
    fg=DISPLAY_FG,
    width=14,
    insertbackground=BTN_OP_BG # Set cursor color
)
display.pack(ipady=10, padx=5, pady=5)


# Create the frame for calculator buttons
button_frame = tk.Frame(calculator_tab, bg=BG_COLOR)
button_frame.pack(padx=10, pady=10)

# Configure the grid rows and columns to be equally sized
for i in range(1, 6): # 5 rows (1-5)
    button_frame.grid_rowconfigure(i, weight=1, minsize=60)
for i in range(4): # 4 columns (0-3)
    button_frame.grid_columnconfigure(i, weight=1, minsize=70)

# Button specifications: (text, row, col, columnspan, color_type)
button_specs = [
    ('C', 1, 0, 1, 'clear'),
    ('7', 1, 1, 1, 'num'),
    ('8', 1, 2, 1, 'num'),
    ('9', 1, 3, 1, 'num'),
    ('4', 2, 0, 1, 'num'),
    ('5', 2, 1, 1, 'num'),
    ('6', 2, 2, 1, 'num'),
    ('/', 2, 3, 1, 'op'),
    ('1', 3, 0, 1, 'num'),
    ('2', 3, 1, 1, 'num'),
    ('3', 3, 2, 1, 'num'),
    ('*', 3, 3, 1, 'op'),
    ('0', 4, 0, 1, 'num'),
    ('.', 4, 1, 1, 'num'),
    ('+', 4, 2, 1, 'op'),
    ('-', 4, 3, 1, 'op'),
    ('=', 5, 0, 4, 'equals') # Spans all 4 columns
]

# Create and place buttons in the grid by looping through the specs
for (text, row, col, span, type) in button_specs:
    # Determine color based on button type
    if type == 'op':
        bg_color = BTN_OP_BG
        fg_color = BTN_OP_FG
    elif type == 'num':
        bg_color = BTN_BG
        fg_color = BTN_FG
    elif type == 'clear':
        bg_color = BTN_CLR_BG
        fg_color = BTN_FG
    elif type == 'equals':
        bg_color = BTN_EQ_BG
        fg_color = BTN_EQ_FG
    
    # Define common button style properties
    btn_style = {
        'text': text,
        'font': ("Arial", 16, "bold"),
        'bg': bg_color,
        'fg': fg_color,
        'relief': "flat",
        'borderwidth': 0,
        'activebackground': "#ececec", # Color when pressed
        'activeforeground': "#000000"
    }

    # Assign the correct function to each button
    if text == '=':
        btn_style['command'] = calculate_result
    elif text == 'C':
        btn_style['command'] = clear_display
    else:
        # Use lambda to pass the button's text to the click function
        btn_style['command'] = lambda t=text: on_button_click(t)

    # Create the button and add it to the grid
    button = tk.Button(button_frame, **btn_style)
    button.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=6, pady=6) # sticky="nsew" makes button fill its cell

# --- Tab 2: BMI Calculator ---
bmi_tab = ttk.Frame(notebook, style="TFrame", padding=20)
notebook.add(bmi_tab, text='BMI')

# Configure grid layout for the BMI tab
bmi_tab.columnconfigure(0, weight=1)
bmi_tab.columnconfigure(1, weight=2)
for i in range(6):
    bmi_tab.rowconfigure(i, weight=1)

# Style for BMI tab widgets (using ttk)
style.configure("TLabel", background=BG_COLOR, foreground=BTN_FG, font=("Arial", 12))
style.configure("TEntry", fieldbackground=BTN_BG, foreground=BTN_FG, borderwidth=0, font=("Arial", 12))
style.configure("TButton", background=BTN_OP_BG, foreground=BTN_OP_FG, font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
style.map("TButton", background=[('active', BTN_EQ_BG)]) # Color when pressed

# Weight widgets
weight_label = ttk.Label(bmi_tab, text="Weight (kg):")
weight_label.grid(row=0, column=0, sticky="w", pady=5)
weight_entry = ttk.Entry(bmi_tab, width=15, font=("Arial", 14))
weight_entry.grid(row=0, column=1, sticky="ew", pady=5, ipady=5)

# Height widgets
height_label = ttk.Label(bmi_tab, text="Height (cm):")
height_label.grid(row=1, column=0, sticky="w", pady=5)
height_entry = ttk.Entry(bmi_tab, width=15, font=("Arial", 14))
height_entry.grid(row=1, column=1, sticky="ew", pady=5, ipady=5)

# Calculate button
calc_bmi_btn = ttk.Button(bmi_tab, text="Calculate BMI", command=calculate_bmi, style="TButton")
calc_bmi_btn.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=20, ipady=10)

# Result labels
bmi_result_label = ttk.Label(bmi_tab, text="Your BMI is: -", font=("Arial", 16, "bold"), anchor="center")
bmi_result_label.grid(row=3, column=0, columnspan=2, sticky="n", pady=10)

bmi_category_label = ttk.Label(bmi_tab, text="Category: -", font=("Arial", 14), anchor="center")
bmi_category_label.grid(row=4, column=0, columnspan=2, sticky="n", pady=5)


# Start the Application 
window.mainloop()