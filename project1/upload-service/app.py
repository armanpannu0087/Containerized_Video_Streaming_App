import os
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv


app = Flask(__name__)

UPLOAD_FOLDER = '/uploads'

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Database connection configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Save to MySQL
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videos (name, path) VALUES (%s, %s)", (file.filename, file_path))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")  # Log the error to the console
            return jsonify({"message": "Database error", "error": str(err)}), 500
        finally:
            cursor.close()
            conn.close()

        return jsonify({"message": "File uploaded successfully!"}), 201
    return jsonify({"message": "No file provided"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
