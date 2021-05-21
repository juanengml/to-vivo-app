from voiceit2 import VoiceIt2
from console_logging.console import Console
console = Console()

console.log("Stating....")

# developerId : ff4a62e3f7014748b75085b17dde1f01

apiKey = "key_aaf0da565b3b41ac8f6de78213f93e52"
apiToken = "tok_d096d530e9374df481ffbe966dfdbd44"

my_voiceit = VoiceIt2(apiKey,apiToken)

id_user = 'usr_54fbb7f880214222958ce92aef0f22f2'

cadastro_img = "https://observatoriodocinema.uol.com.br/wp-content/uploads/2021/01/Renato-Aragao-1.jpg"

verifica_img = "https://stcotvfoco.com.br/2021/01/renato-aragao-didi-carreira-trapalhoes-filmes-1.jpg"

image_fake = "https://conexao.segurosunimed.com.br/wp-content/uploads/2021/01/Capa-idoso-2.0.jpg"

voz_url = "https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/output+(2).flac"
#print(my_voiceit.check_user_exists(id_user))

#print(my_voiceit.create_face_enrollment_by_url(id_user, cadastro_img))

console.info("Verifica...do......")

r = my_voiceit.face_verification_by_url(id_user, verifica_img)
console.info(r['faceConfidence'])

console.info("Verificando image fake...")

fake = my_voiceit.face_verification_by_url(id_user, image_fake)
console.info(fake['faceConfidence'])

console.info("Verificando voz......")
my_voiceit.voice_verification_by_url(id_user, "pt-BR", "Juan Manoel Marinho Nascimento", voz_url)

# -------------------------------------------------


job_uri = "s3://to-vivo-app/users/usr_54fbb7f880214222958ce92aef0f22f2/file.file-extension"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='wav',
    LanguageCode='en-US'
)

while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)

s3_url = "https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/rosto_original.jpg"

>>> from ldataflavor.Services.upload import upload_file
>>> upload_file('usr_54fbb7f880214222958ce92aef0f22f2','verifica.png','image')
users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png
verifica.png to-vivo-app users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png image
'https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png'
>>> upload_file('usr_54fbb7f880214222958ce92aef0f22f2','verifica.png','image')
users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png
verifica.png to-vivo-app users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png image
'https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/verifica.png'
>>> 