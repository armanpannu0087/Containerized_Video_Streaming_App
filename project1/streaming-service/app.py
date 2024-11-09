import mysql.connector
from flask import Flask, jsonify, send_file

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'mysql-db',
    'user': 'root',
    'password': 'Passw0rd',
    'database': 'video_db'
}

@app.route('/videos', methods=['GET'])
def get_videos():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT name, path FROM videos")
    videos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(videos), 200

@app.route('/video/<filename>', methods=['GET'])
def stream_video(filename):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Query the database for the path of the requested file
    query = "SELECT path FROM videos WHERE name = %s"
    cursor.execute(query, (filename,))
    result = cursor.fetchone()  # Fetch the result
    
    cursor.close()
    conn.close()
    
    if result:
        video_path = result[0]  # Extract the file path from the result
        return send_file(video_path)
    else:
        return jsonify({"message": "Video not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
