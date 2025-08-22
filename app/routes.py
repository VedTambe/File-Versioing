from flask import request, jsonify, render_template
import os
from .models import add_file, get_files, get_file_versions

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_app(app):
    @app.route('/')
    def home():
        files = get_files()
        return render_template('index.html', files=files)

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        original_name = file.filename
        # Check existing versions
        versions = get_file_versions(original_name)
        version = 1
        if versions:
            version = max([v[1] for v in versions]) + 1

        filename = f"{original_name}_v{version}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(save_path)

        # Add to DB
        add_file(filename, original_name, version)

        return jsonify({'message': f"{original_name} uploaded as v{version}"}), 200
