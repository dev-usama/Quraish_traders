from flask import Blueprint, render_template, request, flash, redirect,send_file, url_for
from pdf_to_json.text_from_pdf import ExtractTextInfoFromPDF
from pdf_to_json.text_info_with_char_bounds import ExtractTextInfoWithCharBoundsFromPDF
from io import BytesIO

project3 = Blueprint('pdf_to_json', __name__, template_folder='templates')

@project3.route('/')
def index():
    return render_template("pdf_to_json/index.html")

@project3.route("/switch", methods=["POST"])
def switch():
    option = request.form.get("options")
    if option == 1:
        redirect(url_for("pdf_to_json.text"))
    if option == 2:
        redirect(url_for("pdf_to_json.text2"))
    if option == 3:
        redirect(url_for("pdf_to_json.text3"))
    if option == 4:
        redirect(url_for("pdf_to_json.text4"))
    if option == 5:
        redirect(url_for("pdf_to_json.text5"))
    if option == 6:
        redirect(url_for("pdf_to_json.text6"))
    if option == 7:
        redirect(url_for("pdf_to_json.text7"))
    if option == 8:
        redirect(url_for("pdf_to_json.text8"))

@project3.route("/text_from_pdf", methods=["POST"])
def text():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\2.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_from_pdf.zip', mimetype='application/zip')

@project3.route("/text_with_char_bounds", methods=["POST"])
def text2():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\3.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_with_char_bounds.zip', mimetype='application/zip')

@project3.route("/text_table_info", methods=["POST"])
def text3():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\4.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info.zip', mimetype='application/zip')

@project3.route("/text_table_info_with_char", methods=["POST"])
def text4():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\5.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info.zip', mimetype='application/zip')

@project3.route("/6", methods=["POST"])
def text5():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\6.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info_with_figure.zip', mimetype='application/zip')

@project3.route("/7", methods=["POST"])
def text6():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\7.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info_with_renditions.zip', mimetype='application/zip')

@project3.route("/8", methods=["POST"])
def text7():
    if "PDF" not in request.files:
        return "File not attached", 400
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\8.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info_with_styling.zip', mimetype='application/zip')

@project3.route("/9", methods=["POST"])
def text8():
    if "PDF" not in request.files:
        return "File not attached"
    file = request.files["PDF"]
    file.save(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\static\temp.pdf")
    ExtractTextInfoFromPDF(file)
    buffer = BytesIO()
    with open(r"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\pdf_to_json\output\9.zip", "rb") as file:
        buffer.write(file.read())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='text_table_info_with_table_structure.zip', mimetype='application/zip')
