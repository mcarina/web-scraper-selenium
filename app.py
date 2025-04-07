from flask import Flask, request, jsonify, render_template
from search import buscar_google

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.json
    termo = data.get("q")

    if not termo:
        return jsonify({"erro": "Por favor, forneça um termo de busca."}), 400

    resultado = buscar_google(termo)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
