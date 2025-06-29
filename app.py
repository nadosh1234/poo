# app.py

from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import cv2
import os
from analysis import analyze_custom_data


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clean_text(text):
    lines = text.split('\n')
    cleaned = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned)

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    processed_path = os.path.join(UPLOAD_FOLDER, "processed.png")
    cv2.imwrite(processed_path, thresh)
    return processed_path

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    image_url = None
    error = None
    analysis = []

    if request.method == 'POST':
        if 'image' not in request.files:
            error = "لم يتم تحميل أي صورة"
        else:
            file = request.files['image']
            if file.filename == '':
                error = "لم يتم اختيار صورة"
            else:
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                image_url = filepath

                processed = preprocess_image(filepath)
                custom_config = r'--oem 3 --psm 4'
                text_eng = pytesseract.image_to_string(Image.open(processed), config=custom_config, lang='eng')

                extracted_text = clean_text(text_eng)
                analysis = analyze_custom_data(extracted_text)

    return render_template('index.html', text=extracted_text, image=image_url, error=error, analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)
