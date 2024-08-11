from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_latex(text):
    latex_text = text.replace(" ", " ")
    latex_text = latex_text.replace("\n", "\\\\\n")
    latex_text = latex_text.replace("+", r"\+")
    latex_text = latex_text.replace("_", r"\_")
    latex_text = latex_text.replace("%", r"\%")
    latex_text = latex_text.replace("&", r"\&")
    latex_text = latex_text.replace("#", r"\#")
    latex_text = latex_text.replace("$", r"\$")
    latex_text = latex_text.replace("{", r"\{")
    latex_text = latex_text.replace("}", r"\}")
    latex_text = latex_text.replace("/", r"\frac")
    return latex_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                if filename.lower().endswith('.pdf'):
                    images = convert_from_path(file_path)
                    text = ""
                    for img in images:
                        text += pytesseract.image_to_string(img) + "\n"
                else:
                    img = Image.open(file_path)
                    text = pytesseract.image_to_string(img)
                
                latex_code = convert_to_latex(text)
                
            except Exception as e:
                flash(f"Error processing file: {e}")
                return redirect(request.url)
            
            return render_template('index.html', latex_code=latex_code)
    
    return render_template('index.html', latex_code=None)

if __name__ == '__main__':
    app.run(debug=True)
# Run the application
root.mainloop()

