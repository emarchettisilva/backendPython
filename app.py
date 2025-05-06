# app.py
from flask import Flask
from flask_cors import CORS
from routes import login_bp, cadastro_bp

app = Flask(__name__)
# Delimita para qual porta irá responder
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173"
]}})


# Registrando as rotas
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(cadastro_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

