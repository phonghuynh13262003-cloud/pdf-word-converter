"""
PDF ↔ Word Converter - Public Web App
Dùng CloudConvert API để giữ nguyên layout + ảnh + bảng
"""

import os, uuid, threading, time, requests
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024  # 20MB

UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED = {".pdf", ".docx", ".doc"}
CLOUDCONVERT_API_KEY = os.environ.get("CLOUDCONVERT_API_KEY", "")

def auto_delete(path, delay=600):
    def _del():
        time.sleep(delay)
        try: os.remove(path)
        except: pass
    threading.Thread(target=_del, daemon=True).start()


def convert_via_cloudconvert(input_path, output_path, input_fmt, output_fmt):
    """Dùng CloudConvert API — giữ nguyên layout, ảnh, bảng."""
    headers = {
        "Authorization": f"Bearer {CLOUDCONVERT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Bước 1: Tạo job
    job_payload = {
        "tasks": {
            "upload-file": {
                "operation": "import/upload"
            },
            "convert-file": {
                "operation": "convert",
                "input": "upload-file",
                "input_format": input_fmt,
                "output_format": output_fmt,
            },
            "export-file": {
                "operation": "export/url",
                "input": "convert-file"
            }
        }
    }

    r = requests.post("https://api.cloudconvert.com/v2/jobs",
                      json=job_payload, headers=headers, timeout=30)
    if r.status_code != 201:
        return False, f"Tạo job thất bại: {r.text}"

    job = r.json()["data"]
    job_id = job["id"]

    # Lấy upload task
    upload_task = next(t for t in job["tasks"] if t["name"] == "upload-file")
    upload_url = upload_task["result"]["form"]["url"]
    upload_params = upload_task["result"]["form"]["parameters"]

    # Bước 2: Upload file
    with open(input_path, "rb") as f:
        files = {"file": (os.path.basename(input_path), f)}
        ur = requests.post(upload_url, data=upload_params, files=files, timeout=60)
    if ur.status_code not in (200, 201, 204):
        return False, f"Upload thất bại: {ur.text}"

    # Bước 3: Chờ convert xong (tối đa 3 phút)
    for _ in range(36):
        time.sleep(5)
        jr = requests.get(f"https://api.cloudconvert.com/v2/jobs/{job_id}",
                          headers=headers, timeout=30)
        job_status = jr.json()["data"]
        status = job_status["status"]

        if status == "finished":
            export_task = next(t for t in job_status["tasks"] if t["name"] == "export-file")
            download_url = export_task["result"]["files"][0]["url"]

            # Bước 4: Tải file về server
            dr = requests.get(download_url, timeout=60)
            with open(output_path, "wb") as f:
                f.write(dr.content)
            return True, "CloudConvert"

        if status == "error":
            return False, "CloudConvert báo lỗi khi convert"

    return False, "Timeout — convert quá lâu"


def pdf_to_word(pdf_path, docx_path):
    if CLOUDCONVERT_API_KEY:
        return convert_via_cloudconvert(pdf_path, docx_path, "pdf", "docx")

    # Fallback: pdfplumber
    try:
        import pdfplumber
        from docx import Document
        doc = Document()
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i > 0: doc.add_page_break()
                text = page.extract_text() or ""
                for line in text.split("\n"):
                    doc.add_paragraph(line)
                for tbl_data in page.extract_tables():
                    if not tbl_data: continue
                    rows = len(tbl_data)
                    cols = max(len(r) for r in tbl_data)
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
    if CLOUDCONVERT_API_KEY:
        return convert_via_cloudconvert(docx_path, pdf_path, "docx", "pdf")

    # Fallback: reportlab
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
                story.append(Spacer(1, 0.3*cm)); continue
            sname = para.style.name
            if "Heading 1" in sname: story.append(Paragraph(text, styles["Heading1"]))
            elif "Heading 2" in sname: story.append(Paragraph(text, styles["Heading2"]))
            else: story.append(Paragraph(text, styles["Normal"]))
        pdf_doc = SimpleDocTemplate(pdf_path, pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
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
        return jsonify({"error": "Không có file."}), 400
    file = request.files["file"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        return jsonify({"error": "Chỉ hỗ trợ .pdf hoặc .docx"}), 400

    uid = uuid.uuid4().hex[:8]
    safe = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{safe}")
    file.save(input_path)
    auto_delete(input_path)

    if ext == ".pdf":
        out_name = os.path.splitext(safe)[0] + ".docx"
        out_path = os.path.join(OUTPUT_FOLDER, f"{uid}_{out_name}")
        ok, method = pdf_to_word(input_path, out_path)
        label = "Word (.docx)"
    else:
        out_name = os.path.splitext(safe)[0] + ".pdf"
        out_path = os.path.join(OUTPUT_FOLDER, f"{uid}_{out_name}")
        ok, method = word_to_pdf(input_path, out_path)
        label = "PDF"

    if not ok:
        return jsonify({"error": f"Thất bại: {method}"}), 500

    auto_delete(out_path)
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
        return "File không còn tồn tại (đã tự xóa sau 10 phút).", 404
    return send_file(path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
