from flask import Flask
from flask_cors import CORS
from api.generate import generate_bp
from api.upload import upload_bp
from api.templates import templates_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(generate_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(templates_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
