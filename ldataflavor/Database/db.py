import dataset
from voiceit2 import VoiceIt2

from console_logging.console import Console
import os
console = Console()

console.log("Stating....")


apiKey ="   " #
apiToken = "  " 

my_voiceit = VoiceIt2(apiKey,apiToken)

try: 
    #ENDPOINT_DB = os.getenv('ENDPOINT_DB')
    #db = dataset.connect(ENDPOINT_DB)
    db = dataset.connect('sqlite:///tovivo.db')

except:
    db = dataset.connect('sqlite:///tovivo.db')

class CRUD:
    
    @staticmethod
    def cadastrar(data):
        table = db['user']
        user = my_voiceit.create_user()
        print(user)
        data['userId'] = user['userId']
        table.insert(data)
        user_data = table.find_one(cpf=data['cpf'])
        return user_data

    
    @staticmethod
    def checar(data):
        table = db['user']
        user_data = table.find_one(cpf=data['cpf'])
        return user_data
    
    @staticmethod
    def update(data):
        table = db['user']
        status = table.update(data, ['nome'])
        return {"status":"atualizado com sucesso !" if status == 1 else "falha ao salvar"}
    
    @staticmethod 
    def lista_all():
        table = db['user']
        todo_db = list()
        for user in table:
           value = dict(user) 
           todo_db.append(value)
        return todo_db    
            
class Verificacao:
    @staticmethod
    def cadastrar_face(userId, fileUrl):
        return my_voiceit.create_face_enrollment_by_url(userId, fileUrl)

    
    @staticmethod
    def cadastrar_user_id():
        user = my_voiceit.create_user()
        return user['userId']
        


    
    
