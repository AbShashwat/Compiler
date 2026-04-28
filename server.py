from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app)


@app.route("/compile", methods=["POST"])
def compile_code():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({
            "status": "error",
            "message": "No input provided"
        }), 400

    text = data.get("input", "")

    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(text)

    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({
            "status": "error",
            "message": result.stderr or result.stdout
        }), 500

    return jsonify({
        "status": "success",
        "message": "Compilation successful"
    })


@app.route("/download/md")
def download_md():
    path = os.path.join("output", "output.md")

    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    return send_file(path, as_attachment=True)


@app.route("/download/html")
def download_html():
    path = os.path.join("output", "output.html")

    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    return send_file(path, as_attachment=True)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)