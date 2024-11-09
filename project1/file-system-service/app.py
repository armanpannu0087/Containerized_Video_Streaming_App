from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/uploads'

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully!"}), 201
    return jsonify({"message": "No file provided"}), 400

@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
