from voiceit2 import VoiceIt2
from __future__ import print_function
import time
import boto3
from console_logging.console import Console
console = Console()

apiKey = "key_aaf0da565b3b41ac8f6de78213f93e52"
apiToken = "tok_d096d530e9374df481ffbe966dfdbd44"

class ProvaDeVida(object):
    
    @statichmethod
    def facial(url): # s3 data
         # --------
         id_user = url.split("users")[1].split('/')[1]
         my_voiceit = VoiceIt2(apiKey,apiToken)
         r = my_voiceit.face_verification_by_url(id_user, url)
         return {"facial": "aprovado" } if r['faceConfidence'] > 95 else {"facial":"reprovado"}
    
    @statichmethod
    def vocal(url, frase): # s3 data ## TESTAR ESSA POHA 
         id_user = url.split("users")[1].split('/')[1]          
         # usar api do aws para validar isso  
         transcribe = boto3.client('transcribe')
         job_name = "job_user_"+id_user
         file_wav = url.split("users")[1].split("/")[2]
         job_uri = "s3://to-vivo-app/users/"+id_user+"/"+file_wav
         
         transcribe.start_transcription_job( TranscriptionJobName=job_name,  Media={'MediaFileUri': job_uri},
                                             MediaFormat='wav', LanguageCode='pt-BR' )
         status = None
         while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
         return  {"vocal": "aprovado" } if status['results']['transcripts'][0]['transcript'] == frase else  {"vocal": "reprovado" }
    
    @staticmethod
    def pose(url):
        id_user = url.split("users")[1].split('/')[1]  
        
         
        
         