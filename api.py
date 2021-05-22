import werkzeug
from flask import Flask
from flask_restful import Resource, Api,reqparse
from flask import Flask, request, redirect, url_for

from console_logging.console import Console
from flask_cors import CORS
from ldataflavor.Model.engine import ProvaDeVida
from ldataflavor.Database.db import CRUD, Verificacao
from ldataflavor.Services.upload import upload_file
from ldataflavor.Services.Rule import Opec

console = Console()

app = Flask(__name__)
api = Api(app)
#CORS(app, origins="*", allow_headers=[
#    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"])
CORS(app)


class verificacao(Resource):
   
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('url') 
        argumentos.add_argument('tipo')          
        argumentos.add_argument('cpf')  
        dados  = argumentos.parse_args()
        check = None
        if dados['tipo'] == 'facial':
            check = ProvaDeVida.facial(dados['url'])
        if dados['tipo'] == 'vocal':
            check = ProvaDeVida.vocal(dados['url'])
        if dados['tipo'] == 'pose':
            check = ProvaDeVida.pose(dados['url'])
            
        return {"dados":dados,"check":check}
    
class user(Resource):
    def post(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('data_nascimento')
        argumentos.add_argument('sexo')
        argumentos.add_argument('celular')
        argumentos.add_argument('cpf')
        argumentos.add_argument('numero_inss')
        argumentos.add_argument('email')
        argumentos.add_argument('senha')
        dados  = argumentos.parse_args()
        result = CRUD.cadastrar(dados)
        return result
    
    def get(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('cpf')
        dados  = argumentos.parse_args()
        result = CRUD.checar(dados)
        return result
    
    def put(self):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome')
        argumentos.add_argument('data_nascimento')
        argumentos.add_argument('sexo')
        argumentos.add_argument('celular')
        argumentos.add_argument('cpf')
        argumentos.add_argument('numero_inss')
        argumentos.add_argument('email')
        argumentos.add_argument('senha')
        dados  = argumentos.parse_args()
        result = CRUD.update(dados)
        return result


class upload_image(Resource): ## recebe os dados de pose e face
   def post(self):
     parse = reqparse.RequestParser()
     parse.add_argument('files', type=werkzeug.datastructures.FileStorage, location='files')         
     parse.add_argument('cpf')
     parse.add_argument('tipo')     # "pose", "facial" # apenas esses 
     parse.add_argument('operacao') # cadastrar ou apenas upar no s3 para verificação
 
     args = parse.parse_args()
     print(args)
     result = Opec.check(args)
     return result 


        
class upload_audio(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('audio', type=werkzeug.FileStorage, location='files')

        args = parse.parse_args()

        stream = args['audio'].stream
        wav_file = wave.open(stream, 'rb')
        signal = wav_file.readframes(-1)
        signal = np.fromstring(signal, 'Int16')
        fs = wav_file.getframerate()
        wav_file.close()
        
        
class show_db(Resource):
    def get(self):
        return CRUD.lista_all()    
         
    
class healthcheck(Resource):
    def get(self):
        return {"healthcheck":"WORK"},200

api.add_resource(verificacao, '/api/v1/verificacao/')

api.add_resource(healthcheck, '/')

api.add_resource(user, '/api/v1/user/')

api.add_resource(show_db, '/api/v1/admin/db')

api.add_resource(upload_image, '/api/v1/upload/image')

api.add_resource(upload_audio, '/api/v1/upload/audio')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5004,debug=True)
