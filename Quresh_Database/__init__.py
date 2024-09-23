import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas as pd
from PIL import Image
from io import BytesIO
import os
from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import base64
from sqlalchemy.exc import IntegrityError
import logging
import pandas as pd
from __main__ import app, db

project1 = Blueprint('excel_to_db', __name__, template_folder='templates', static_folder='static')

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data is None:
        return ''
    return base64.b64encode(data).decode('utf-8')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, unique=True, nullable=False)
    unique_model_code = db.Column(db.String(100), nullable=True)
    image = db.Column(db.BLOB, nullable=False)
    product_name = db.Column(db.String(200), nullable=True)
    specification = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)

@project1.route('/')
def index():
    products = Product.query.all()
    return render_template('Quresh_Database/index.html', products=products)

@project1.route('/upload_excel', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            process_excel(file_path)
            os.remove(file_path)  # Remove the file after processing
            flash('Excel file processed successfully')
            return redirect(url_for('excel_to_db.index'))
    return render_template('Quresh_Database/upload_excel.html')

@project1.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    product_ids = request.json.get('product_ids', [])
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    for product in products:
        elements.append(Paragraph(f"Product: {product.product_name}", styles['Heading2']))
        data = [
            ["No.", str(product.no)],
            ["Unique Model Code", product.unique_model_code],
            ["Specification", product.specification],
            ["Price", f"${product.price:.2f}"],
        ]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (1, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (1, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

        if product.image:
            img = Image(BytesIO(product.image))
            img.drawHeight = 200
            img.drawWidth = 200
            elements.append(img)

        elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='selected_products.pdf', mimetype='application/pdf')

@project1.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Product(
            no=request.form.get('no'),
            unique_model_code=request.form.get('unique_model_code'),
            product_name=request.form.get('product_name'),
            specification=request.form.get('specification'),
            price=float(request.form.get('price', 0)),
            # additional_info removed
        )
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                new_product.image = file.read()
        
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully')
        return redirect(url_for('excel_to_db.index'))
    return render_template('Quresh_Database/add_product.html')

@project1.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.no = request.form.get('no')
        product.unique_model_code = request.form.get('unique_model_code')
        product.product_name = request.form.get('product_name')
        product.specification = request.form.get('specification')
        product.price = float(request.form.get('price', 0))
        # additional_info removed
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                product.image = file.read()
        
        db.session.commit()
        flash('Product updated successfully')
        return redirect(url_for('excel_to_db.index'))
    return render_template('Quresh_Database/edit_product.html', product=product)

@project1.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return redirect(url_for('excel_to_db.index'))

@project1.route('/update_image/<int:product_id>', methods=['POST'])
def update_image(product_id):
    product = Product.query.get_or_404(product_id)
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            product.image = file.read()
            db.session.commit()
            flash('Image updated successfully')
    return redirect(url_for('excel_to_db.index'))



def process_excel(file_path):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        # Skip the first 2 rows (headers) and use the 3rd row as column names
        df = pd.read_excel(file_path, skiprows=2, header=0)
        logger.debug(f"DataFrame columns: {df.columns}")
        logger.debug(f"First few rows:\n{df.head()}")

        # Rename columns to match your model
        df = df.rename(columns={
            'Unnamed: 0': 'no',
            'Unnamed: 1': 'unique_model_code',
            'Unnamed: 2': 'product_name',
            'Unnamed: 4': 'specification',
            'USD': 'price'
        })

        workbook = load_workbook(file_path)
        sheet = workbook.active
        image_loader = SheetImageLoader(sheet)
        
        skipped_rows = 0
        processed_rows = 0
        i = 4
        for _, row in df.iterrows():
            try:
                # Convert 'no' to integer, skip if not possible
                try:
                    no = int(row['no']) # no means number
                except (ValueError, TypeError):
                    skipped_rows += 1
                    i+=1
                    logger.warning(f"Skipping row with invalid No.: {row['no']}")
                    continue
                try:
                    image = image_loader.get(f"D{i}")
                except:
                    i+=1
                    continue
                i += 1
                path = fr"C:\Users\Usama Ahmed\Documents\Quresh_Kitchen\Quresh_Database\static\dummy.{image.format}"
                image.save(path)
                with open(path, "rb") as x:
                    file = x.read()
                product = Product(
                    no=no,
                    unique_model_code=str(row['unique_model_code']),
                    product_name=str(row['product_name']),
                    image=file,
                    specification=str(row['specification']),
                    price=float(row['price']),
                )
                db.session.add(product)
                try:
                    db.session.flush()
                    processed_rows += 1
                except IntegrityError:
                    db.session.rollback()
                    skipped_rows += 1
                    logger.warning(f"Skipping row with duplicate No. {no}: {row}")
                    continue
            except Exception as e:
                logger.error(f"Error processing row: {row}")
                logger.error(f"Error details: {str(e)}")
                db.session.rollback()
                skipped_rows += 1
                continue

        db.session.commit()
        flash(f'Excel file processed successfully. Processed {processed_rows} rows, skipped {skipped_rows} rows.', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing Excel file: {str(e)}")
        flash(f'Error processing Excel file: {str(e)}', 'error')