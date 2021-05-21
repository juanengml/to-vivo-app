import gradio as gr
from requests import get,post 
from ldataflavor.Services.upload import upload_file
from PIL import Image

endpoint = "http://172.31.70.217:5003/api/v1/verificacao/"
#upload_file('usr_54fbb7f880214222958ce92aef0f22f2','verifica.png','image')

def autentica( tipo, url):
    data = {
     "tipo":tipo,
      "url":url
    }
    return post(endpoint,data).json()['check']['facial']


def verificacao_facial(cpf_user,img):
    im = Image.fromarray(img)
    im.save("verifica.jpeg")
    result = upload_file(cpf_user,'verifica.jpeg','image')
    print(result)
    verifica = autentica(tipo='facial',url=result) 
    print(verifica)
    value = {"verifica":verifica,"result":result} #'usr_54fbb7f880214222958ce92aef0f22f2'
    return value

iface = gr.Interface(
  fn=verificacao_facial, 
  inputs=["text", gr.inputs.Image(shape=(200, 200))],
  outputs=["text",'image'],server_port=8521, server_name="0.0.0.0")
          
iface.launch(debug=True)