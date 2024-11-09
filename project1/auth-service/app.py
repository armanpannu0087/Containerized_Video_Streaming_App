from flask import Flask, Flask, request, jsonify, send_from_directory
app = Flask(__name__)

# test user data
users = {"user1": "password1", "user2": "password2"}




@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
