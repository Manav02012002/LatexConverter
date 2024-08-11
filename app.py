import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, messagebox
from pdf2image import convert_from_path

# Function to open and process the file (image or PDF)
def open_file():
    try:
        file_path = filedialog.askopenfilename(
            initialdir="/", title="Select File", filetypes=(("Image files", "*.png;*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")))

        if not file_path:
            return

        print(f"Selected file: {file_path}")

        # Determine if the file is a PDF or an image
        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)
        else:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

        latex_code = convert_to_latex(text)

        # Clear the text widget and insert the LaTeX code
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, latex_code)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")

# Function to convert text to LaTeX format
def convert_to_latex(text):
    latex_text = text.replace(" ", " ")  # Preserve spaces
    latex_text = latex_text.replace("\n", "\\\\\n")  # New lines to LaTeX line breaks
    latex_text = latex_text.replace("+", r"\+")  # Escape LaTeX-specific characters
    latex_text = latex_text.replace("_", r"\_")
    latex_text = latex_text.replace("%", r"\%")
    latex_text = latex_text.replace("&", r"\&")
    latex_text = latex_text.replace("#", r"\#")
    latex_text = latex_text.replace("$", r"\$")
    latex_text = latex_text.replace("{", r"\{")
    latex_text = latex_text.replace("}", r"\}")
    
    # Handle fractions
    latex_text = latex_text.replace("/", r"\frac")
    
    # You can add more rules here to handle other LaTeX commands
    return latex_text

# Set up the main window
root = tk.Tk()
root.title("Handwritten to LaTeX Converter")
root.geometry("600x400")
root.configure(bg="#f0f0f0")  # Set a light background color

# Create a frame for the button and instructions
frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff", borderwidth=2, relief="sunken")
frame.pack(padx=20, pady=10, fill=tk.X)

# Add a title label
title_label = tk.Label(frame, text="Handwritten to LaTeX Converter", font=("Arial", 16, "bold"), bg="#ffffff", fg="#004d00")
title_label.pack(pady=(0, 10))

# Add instructions label
instructions_label = tk.Label(frame, text="Click 'Open File' to select an image or PDF file containing handwritten text.", font=("Arial", 12), bg="#ffffff", fg="#333333")
instructions_label.pack(pady=(0, 10))

# Add a button to open a file
open_button = tk.Button(frame, text="Open File", padx=10, pady=5, fg="white", bg="#0056b3", font=("Arial", 12), command=open_file)
open_button.pack()

# Create a frame for the text widget
text_frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff", borderwidth=2, relief="sunken")
text_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Add a scrollable text widget to display the LaTeX code
text_widget = Text(text_frame, wrap=tk.WORD, undo=True, width=70, height=15, font=("Arial", 12), bg="#f5f5f5", fg="#000000")
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar
scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Run the application
root.mainloop()

