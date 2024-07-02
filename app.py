import pandas as pd
import json
import numpy as np
import cohere
from flask import Flask, request, jsonify,render_template
import requests
from pymongo import MongoClient
import os
from flask_cors import CORS

""" TABLA USERS"""
from flask import Flask, jsonify


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# Definir la función para descargar la colección desde MongoDB
def download_collection_from_mongodb(uri, db_name, collection_name):
    # Conectar a MongoDB
    client = MongoClient(uri)
    try:
        # Seleccionar la base de datos y la colección
        db = client[db_name]
        collection = db[collection_name]

        # Descargar los datos de la colección
        data = list(collection.find())

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data)
    finally:
        # Cerrar la conexión
        client.close()
    
    return df

# Datos de conexión a MongoDB
uri = "mongodb+srv://Cluster78620:uuMda3E0UnvIPzdi@cluster786∫20.jcfu9lt.mongodb.net"  # Cambia la URL según sea necesario
db_name = "Samoo"  # Cambia 'nombre_de_la_base_de_datos' por el nombre de tu base de datos
collection_name = "users"  # Cambia 'nombre_de_la_coleccion' por el nombre de tu colección

# Descargar la colección y convertirla en un DataFrame
dff_users = download_collection_from_mongodb(uri, db_name, collection_name)

# Mostrar el DataFrame
# dff_users



@app.route('/chatbot', methods=['POST'])
def chat():
    # co = cohere.Client(api_key=os.environ["COHERE_API_KEY"]) 
    co = cohere.Client(api_key="lOGO9JDezVva0OyZAzvPOQUjlq8fUw0nJ0WeL0fS")
    question = request.form.get("chat", None)
    prompt = f"""En base al siguiente Dataframe {dff_users}, quiero que respondas a la pregunta registrada en {question}. En la respuesta, intenta ser los más conciso posible, y pon solo texto normal, nada parecido a "\n" o similar """
    response = co.generate(
                        model = "command-nightly",
                        prompt = prompt,
                        max_tokens = 200,
                        temperature = 0.01,
                        k=0,
                        p = 0.75,
                        stop_sequences = [],
                        return_likelihoods = "NONE"
                        )

    # nav = response.generations[0].text
    # nav
    nav = response.generations[0].text.strip()

    # return render_template("result.html",prediction=nav)
    return jsonify({"response": nav})
    # return render_template({msg:"chat bot answer",answer:respuestadelchatbot})
if __name__ == '__main__':
    app.run(debug=True)
