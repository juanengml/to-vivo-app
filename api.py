from flask import Flask
from flask_restful import Resource, Api,reqparse
from console_logging.console import Console
from flask_cors import CORS
from ldataflavor.Model.engine import ProvaDeVida
from ldataflavor.Database.db import CRUD


console = Console()

app = Flask(__name__)
api = Api(app)
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"])


class verificacao(Resource):
   
    def post(self):
        argumentos = reqparse.RequestParser()
       ## argumentos.add_argument('id') # id do cliente
        argumentos.add_argument('url') # url do s3 
        argumentos.add_argument('tipo') # tipo de autenticacao ("facial","vocal","motor") 
        dados  = argumentos.parse_args()
        check = None
        if dados['tipo'] == 'facial':
            check = ProvaDeVida.facial(dados['url'])
        if dados['tipo'] == 'vocal':
            check = ProvaDeVida.vocal(dados['url'])
        return {"dados":dados,"check":check}
    

class healthcheck(Resource):
    def get(self):
        return {"healthcheck":"WORK"}

api.add_resource(verificacao, '/api/v1/verificacao/')

api.add_resource(healthcheck, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5003,debug=True)
