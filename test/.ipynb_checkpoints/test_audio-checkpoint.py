




"""

from ldataflavor.Model.engine import ProvaDeVida
from uuid import uuid4

frase = "Abóbora enquadrada roxa, laranja azul."
url = "https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/record.wav"

print(ProvaDeVida.vocal(url))

import time
import boto3
from requests import get


def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        LanguageCode='pt-BR'
    )

    max_tries = 60
    url = ""
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                #print(
                #    f"Download the transcript from\n"
                #    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
                url = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    return list(get(url).json()['results']['transcripts'][0].values())[0]
        
def main():
    transcribe_client = boto3.client('transcribe')
    file_uri = 's3://to-vivo-app/users/usr_54fbb7f880214222958ce92aef0f22f2/record.wav'
    text = transcribe_file('Example-job'+str(uuid4()), file_uri, transcribe_client)
    print(text," == ", frase,"\tRESULT:",text == frase)
    
if __name__ == '__main__':
    main()
    
"""