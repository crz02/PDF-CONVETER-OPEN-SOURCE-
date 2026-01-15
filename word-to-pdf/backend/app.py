from flask import Flask, request, send_file
from flask_cors import CORS
from docx import Document
from reportlab.pdfgen import canvas
import os 
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def word_to_pdf(docx_path, pdf_path):
    doc = Document(docx_path)
    c = canvas.Canvas(pdf_path)

    y = 800
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            c.drawString(50, y, text)
            y -= 15
            if y < 50:
                c.showPage()
                y = 800

    c.save()

@app.route("/convert", methods=["POST"])
def convert_word_to_pdf():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "Empty filename"}, 400

    if not file.filename.endswith(".docx"):
        return {"error": "Only .docx files allowed"}, 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_filename = file.filename.rsplit(".", 1)[0] + ".pdf"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    word_to_pdf(input_path, output_path)

    if not os.path.exists(output_path):
        return {"error": "PDF generation failed"}, 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)