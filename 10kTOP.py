from flask import Flask, request, jsonify

app = Flask(__name__)

# Загружаем пароли при запуске
with open("10k-most-common.txt", "r", encoding="utf-8") as f:
    common_passwords = set(line.strip() for line in f)

@app.route("/check", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Password is required"}), 400

    is_common = password in common_passwords
    return jsonify({
        "password": password,
        "is_common": is_common,
        "message": "Your password is too common. Consider changing it." if is_common else "Your password is not in the top 10k."
    })

if __name__ == "__main__":
    app.run(debug=True)
