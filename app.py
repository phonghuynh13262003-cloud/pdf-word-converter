"""
Web App chuyển đổi PDF ↔ Word
==============================
Cài thư viện:
    pip install flask pdf2docx python-docx pdfplumber reportlab

Chạy:
    python app.py

Mở trình duyệt tại: http://localhost:5000
"""

import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED = {".pdf", ".docx", ".doc"}


def pdf_to_word(pdf_path, docx_path):
    try:
        from pdf2docx import Converter
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        return True, "pdf2docx"
    except ImportError:
        pass

    try:
        import pdfplumber
        from docx import Document
        from docx.shared import Pt
        doc = Document()
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i > 0:
                    doc.add_page_break()
                text = page.extract_text() or ""
                for line in text.split("\n"):
                    doc.add_paragraph(line)
                for tbl_data in page.extract_tables():
                    if not tbl_data:
                        continue
                    rows, cols = len(tbl_data), max(len(r) for r in tbl_data)
                    tbl = doc.add_table(rows=rows, cols=cols)
                    tbl.style = "Table Grid"
                    for r_i, row in enumerate(tbl_data):
                        for c_i, cell in enumerate(row):
                            if c_i < cols:
                                tbl.cell(r_i, c_i).text = str(cell or "")
        doc.save(docx_path)
        return True, "pdfplumber"
    except Exception as e:
        return False, str(e)


def word_to_pdf(docx_path, pdf_path):
    import subprocess
    for cmd in ["libreoffice", "soffice"]:
        try:
            r = subprocess.run(
                [cmd, "--headless", "--convert-to", "pdf",
                 "--outdir", OUTPUT_FOLDER, docx_path],
                capture_output=True, timeout=60
            )
            if r.returncode == 0:
                generated = os.path.join(
                    OUTPUT_FOLDER,
                    os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
                )
                if generated != pdf_path and os.path.exists(generated):
                    os.rename(generated, pdf_path)
                return True, "LibreOffice"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    try:
        from docx2pdf import convert
        convert(docx_path, pdf_path)
        return True, "docx2pdf"
    except Exception:
        pass

    try:
        from docx import Document as DocxDoc
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm

        doc_word = DocxDoc(docx_path)
        styles = getSampleStyleSheet()
        story = []
        for para in doc_word.paragraphs:
            text = para.text.strip()
            if not text:
                story.append(Spacer(1, 0.3 * cm))
                continue
            sname = para.style.name
            if "Heading 1" in sname:
                story.append(Paragraph(text, styles["Heading1"]))
            elif "Heading 2" in sname:
                story.append(Paragraph(text, styles["Heading2"]))
            else:
                story.append(Paragraph(text, styles["Normal"]))
        pdf_doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
        pdf_doc.build(story)
        return True, "reportlab"
    except Exception as e:
        return False, str(e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "Không có file nào được gửi lên."}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Tên file trống."}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        return jsonify({"error": f"Chỉ hỗ trợ: .pdf, .docx"}), 400

    uid = uuid.uuid4().hex[:8]
    safe_name = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{safe_name}")
    file.save(input_path)

    if ext == ".pdf":
        out_name = os.path.splitext(safe_name)[0] + ".docx"
        out_path = os.path.join(OUTPUT_FOLDER, f"{uid}_{out_name}")
        ok, method = pdf_to_word(input_path, out_path)
        label = "Word (.docx)"
    else:
        out_name = os.path.splitext(safe_name)[0] + ".pdf"
        out_path = os.path.join(OUTPUT_FOLDER, f"{uid}_{out_name}")
        ok, method = word_to_pdf(input_path, out_path)
        label = "PDF"

    if not ok:
        return jsonify({"error": f"Chuyển đổi thất bại: {method}"}), 500

    return jsonify({
        "success": True,
        "download_url": f"/download/{uid}_{out_name}",
        "filename": out_name,
        "method": method,
        "label": label,
    })


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(path):
        return "File không tồn tại.", 404
    return send_file(path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    print("\n🚀  Mở trình duyệt tại: http://localhost:5000\n")
    app.run(debug=True, port=5000)
