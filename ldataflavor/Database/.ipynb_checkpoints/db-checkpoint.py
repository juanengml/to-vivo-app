import dataset
from voiceit2 import VoiceIt2

from console_logging.console import Console
import os
console = Console()

console.log("Stating....")


apiKey = "key_aaf0da565b3b41ac8f6de78213f93e52" # os.getenv("API_KEY") 
apiToken = "tok_d096d530e9374df481ffbe966dfdbd44" #os.getenv("API_TOKEN") 

my_voiceit = VoiceIt2(apiKey,apiToken)

try: 
    #ENDPOINT_DB = os.getenv('ENDPOINT_DB')
    #db = dataset.connect(ENDPOINT_DB)
    db = dataset.connect('mysql://dbmasteruser:$ArM(R*u6TWM8[T_w]|=v|hR{nXvwU&E@ls-d3897fabf406022697bd50f2f95b05b3ee52c9f3.cx8982sx1pw5.us-east-1.rds.amazonaws.com/Heimdall_DB')
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
        


    
    
