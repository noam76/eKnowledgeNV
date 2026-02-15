from flask import Flask, request, jsonify
import os
import PyPDF2
import docx
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'mp4', 'jpg', 'jpeg', 'png'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Indexing PDF Files
def index_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Indexing Word Documents
def index_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

# Indexing Text Files
def index_text(file_path):
    with open(file_path, 'r') as f:
        return f.read()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('/path/to/upload', filename)  # Update with your upload path
        file.save(file_path)

        if filename.endswith('.pdf'):
            text = index_pdf(file_path)
        elif filename.endswith('.docx'):
            text = index_docx(file_path)
        elif filename.endswith('.txt'):
            text = index_text(file_path)
        
        # Store the indexed text and return response
        return jsonify({'message': 'File uploaded and indexed', 'text': text})
    
    return jsonify({'error': 'File type not allowed'})

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '')
    # Implement search logic across indexed documents
    return jsonify({'message': 'Search results for query: ' + query})

@app.route('/admin/config', methods=['POST'])
def admin_configuration():
    settings = request.json
    # Handle admin configuration
    return jsonify({'message': 'Configuration updated', 'settings': settings})

if __name__ == '__main__':
    app.run(debug=True)