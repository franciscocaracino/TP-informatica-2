from flask import Flask, request, jsonify
from crm_model import CRMModel

app = Flask(__name__)
crm = CRMModel("clientes.db")

@app.route("/")
def inicio():
    return "API funcionando. Usá /clientes para comenzar."

# GET all clientes
@app.route("/clientes", methods=["GET"])
def obtener_clientes():
    datos = crm.obtener_clientes()
    clientes = [
        {
            "id": fila[0],
            "nombre": fila[1],
            "telefono": fila[2],
            "ultima_compra": fila[3],
            "frecuencia": fila[4]
        } for fila in datos
    ]
    return jsonify(clientes), 200


# GET cliente por ID
@app.route("/clientes/<int:id>", methods=["GET"])
def obtener_cliente(id):
    cliente = crm.obtener_por_id(id)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"error": "Cliente no encontrado"}), 404

# POST - Agregar cliente
@app.route("/clientes", methods=["POST"])
def agregar_cliente():
    data = request.json
    campos = ["nombre", "telefono", "ultima_compra", "frecuencia"]
    if not all(campo in data for campo in campos):
        return jsonify({"error": "Faltan datos"}), 400
    crm.agregar_cliente(data["nombre"], data["telefono"], data["ultima_compra"], int(data["frecuencia"]))
    return jsonify({"mensaje": "Cliente agregado correctamente"}), 201

# PUT - Actualizar cliente
@app.route("/clientes/<int:id>", methods=["PUT"])
def actualizar_cliente(id):
    data = request.json
    campos = ["nombre", "telefono", "ultima_compra", "frecuencia"]
    if not all(campo in data for campo in campos):
        return jsonify({"error": "Faltan datos"}), 400

    crm.actualizar_cliente(id, data["nombre"], data["telefono"], data["ultima_compra"], int(data["frecuencia"]))
    return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200


# DELETE - Eliminar cliente
@app.route("/clientes/<int:id>", methods=["DELETE"])
def eliminar_cliente(id):
    crm.eliminar_cliente(id)
    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200



# GET - Filtrar por estado (usando parámetros opcionales)
@app.route("/clientes/filtrar", methods=["GET"])
def filtrar_por_estado():
    estado = request.args.get("estado")
    if estado not in ["al_dia", "vencido"]:
        return jsonify({"error": "Parámetro estado inválido. Usá 'al_dia' o 'vencido'."}), 400
    clientes = crm.filtrar_por_estado(estado)
    return jsonify(clientes), 200

if __name__ == '__main__':
    app.run(debug=True)
