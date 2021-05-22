
from console_logging.console import Console
from flask_cors import CORS
from ldataflavor.Model.engine import ProvaDeVida
from ldataflavor.Database.db import CRUD, Verificacao
from ldataflavor.Services.upload import upload_file

console = Console()

class Opec:
    
    @staticmethod
    def check(args):
         if args['operacao'] == 'check':
                result = CRUD.checar({"cpf":args['cpf']})
                console.info("SAVING..IMAGE...")
                user = dict(result)['userId']
                tipo = "image"
                path = args['tipo']+".jpg"
                #print(path)
                image_file = args['files']
                image_file.save(path)
                url = upload_file(user,path,tipo)     # url do s3 
                if args['tipo'] == 'pose':
                    return {'url':url, "tipo":args['tipo']}
                if args['tipo'] == 'facial':
                    return {'url':url, "tipo":args['tipo']}

         if args['operacao'] == 'cadastro':
                result = CRUD.checar({"cpf":args['cpf']})
                user = dict(result)['userId']
                nome = dict(result)['nome']
                data = {}
                if user == None:
                    console.info("GERANDO USER ID")
                    user = Verificacao.cadastrar_user_id()
                    data['userId'] = user

                tipo = "image"
                path = args['tipo']+".jpg"
                #print(path)
                image_file = args['files']
                image_file.save(path)
                url = upload_file(user,path,tipo) 

                data['cpf'] = args['cpf'] 
                data['link_'+args['tipo']] =  url
                data["nome"] = nome
                if args['tipo'] == 'facial':
                     console.log(Verificacao.cadastrar_face(user, url))

                status = CRUD.update(data)
                status['data'] = data
                return status
