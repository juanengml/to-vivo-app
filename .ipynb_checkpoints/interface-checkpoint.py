import streamlit as st
from random import choice
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from PIL import Image
    
import cv2
import time
import altair as alt
import datetime
import streamlit.components.v1 as stc
from requests import post,get,put 
from pydub import AudioSegment
from ldataflavor.Services.upload import upload_file
from ldataflavor.Database.db import CRUD, Verificacao

def status():
    return choice(range(100))


def save_image(img_file_buffer,name):
    image = Image.open(img_file_buffer)
    img_array = np.array(image)
    filename = "{}.jpeg".format(name)
    cv2.imwrite(filename, img_array)
    return filename

def save_audio(uploaded_file_audio, name):
    filename = "{}.wav".format(name)
    with open("{}.wav".format(name), "wb") as f:
           f.write(uploaded_file_audio.getbuffer())  

    return filename

def form():
     
    with st.form("my_form"):
       st.write("Envie os seguintes dados abaixo")
       with col1:
            st.write("""
            ## João da silva 
            (aposentado/funcionario publico)""")
       
       with col2:
            date = st.date_input('Data de nascimento', datetime.date.today())
       
       st.write("## Foto")
       uploaded_file_foto = st.file_uploader("Choose a file" , key=1)
          
       st.write("## Audio")
       uploaded_file_audio = st.file_uploader("Choose a file", key=2)
       
       st.write("## Video")
       uploaded_file_video = st.file_uploader("Choose a file", key=3)

       # Every form must have a submit button.
       submitted = st.form_submit_button("Submit")
       if submitted:
         st.write( "data", date)
         st.write(date)
         st.balloons()
         ## enviar para api de autenticação 
         ## enciar para s3 e rodar sagemaker para validação 
         ## usar ec2 para hosting
         st.write(" ")



def main():
    image = Image.open('banner.jpg')
    st.image(image, caption='Construido por Data Flavor')
    
    st.write("""
    ----
    """)
    col1,col2,col3=st.beta_columns(3)
    
    menu = st.sidebar.selectbox(
    "Funcionalidade",
    ("Acompanhar processo","Prova de Vida","Minhas informações")) 
    
    #st.write(menu)
    if menu == "Acompanhar processo":
        with st.form("process"):
            col5,col6=st.beta_columns(2)
            with col5:
                st.write("## Digite Seu CPF")
            with col6:
                cpf = st.text_input('CPF')
                
            submitted = st.form_submit_button("Buscar") 
            if submitted:
              st.write( "data", cpf)
              endpoint_search = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/user/"
              data = {
                 "cpf":cpf
              }
              r = get(endpoint_search,data).json()
              st.write("### Olá Senhor(a) ",r['nome'])   
              if r['prova_de_vida'] == 'aprovado':
                    st.success("Sua Prova de Vida está como \n### CONCLUÍDA 🥳" )
                    st.balloons()

              else:
                    st.warning("Sua Prova de Vida está como \n###NÃO CONCLUIDA ☹️")
              st.write("Data da Realização : ",r['data'])
             
                
            
              
    if menu == "Prova de Vida":
        with st.form("my_form"):
           st.write("Envie os seguintes dados abaixo")
           with col1:
                st.write("""
                ## Preencha com suas informações abaixo 
                EX: (CPF) 
                """)   

           with col2:
                cpf = st.text_input('CPF')
           st.write("## Reconhecimento Facial \nEnviar foto com Rosto")
           uploaded_file_foto = st.file_uploader("Choose a file" , key=1)

           st.write("## Reconhecimento de Marcha(Andando)\nEnviar uma Foto andando ")
           uploaded_file_video = st.file_uploader("Choose a file", key=2)

           st.write("## Reconhecimento de Voz\nGrave um audio lendo a frase a baixo ")
           st.write("### Doce de abóbora e laranja com gengibre ")
           uploaded_file_audio = st.file_uploader("Choose a file", key=3)
            

           # Every form must have a submit button.
           submitted = st.form_submit_button("Submit")
           if submitted:
              
              st.write( "cpf", cpf)
              #st.write(date,uploaded_file_foto,uploaded_file_video, uploaded_file_audio)
              
              endpoint_image = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/upload/image"

                      # -------------------------------------------------
                      # valida face regontion 
              path_face = save_image(uploaded_file_foto ,"facial") 

              files = {'files': open(path_face,'rb')}                      
              data = {"cpf":cpf,"tipo":"facial","operacao":"check"}                    
                    
              data_face = post(url=endpoint_image,data=data,files=files).json()
              data_face['cpf'] = cpf  
              #st.write("data_face",data_face)  
                      # -------------------------------------------  
                      ## valida pose estimation    
              path_pose = save_image(uploaded_file_video,"pose")
                      
              files = {'files': open(path_pose,'rb')}
              data = {"cpf":cpf,"tipo":"pose","operacao":"check"}
                    
              data_pose = post(url=endpoint_image,data=data,files=files).json()
              data_pose['cpf'] = cpf  
              #st.write("data_pose",data_pose)  
  
                      # ----------------------------------------------  
                      # valida audio recognition   
              path_audio = save_audio(uploaded_file_audio,"voz")  
              endpoint_search = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/user/"
              data = {
                 "cpf":cpf
              }
              r = get(endpoint_search,data).json()       
              user = r['userId']  
              link_voz = upload_file(user,path_audio,"voz")     # url do s3 
                    
              data_voz = {"cpf":cpf,"tipo":"vocal","url":link_voz}
              #st.write("data_voz",data_voz)
                      # -----------------------------------------------
                      # verificacao 
              endpoint_verificacao = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/verificacao/"
              r_face = post(endpoint_verificacao,data_face).json()

              if r_face['check']['facial'] == 'aprovado':
                    st.info('Reconhecimento Facial Verificada com Sucesso !')
                    
              r_pose = post(endpoint_verificacao,data_pose).json()

              if r_pose['check']['pose'] == 'aprovado':
                    st.info('Reconhecimento Pose Verificada com Sucesso !')
                    
              r_voz = post(endpoint_verificacao,data_voz).json()
 
              if r_voz['check']['vocal'] == 'aprovado':
                    st.info('Reconhecimento Vocal Verificada com Sucesso !')
              dados = {"cpf":cpf,'nome':r['nome'],"prova_de_vida":"aprovado","data":"05-04-2021"}  
              result = CRUD.update(dados)
              #st.write(result)
                
              st.success('Prova de Vida Verificada com Sucesso !')
              st.balloons()
              
                      #st.error("FALHA AO CADASTRAR DADOS ! TENTE NOVAMENTE MAIS TARDE !")  
   
              st.write(" ")

    
        
    if menu == "Minhas informações" :
        option = st.selectbox(
       'Primeiro Acesso ?',
        ('Sim', 'Não'))
        if option == "Sim":
          with st.form("info"):
             col5,col6=st.beta_columns(2)
                
             with col5:
                   nome = st.text_input('NOME COMPLETO')
                   data_nascimento = st.date_input( "Data de Nascimento", datetime.date(1958, 7, 6))
                   inss = st.text_input("NÚMERO INSS")
                   email = st.text_input("EMAIL") 
                   
             with col6:
                   cpf = st.text_input('CPF')
                   sexo =  st.radio("Genero",('masculino','feminino'))
                   celular = st.text_input("Celular")   
                   senha = st.text_input("senha", type='password')                 
 
                     
             st.write("## 😄 Cadastre seu Rosto \nEnviar foto com Rosto")
             uploaded_file_foto = st.file_uploader("Choose a file" , key=4)

             st.write("## 🚶 Cadastre de Foto de Perfil(De Pé)\nEnviar uma Foto em Pé(se possivel) ")
             uploaded_file_video = st.file_uploader("Choose a file", key=5)

             st.write("## 🗣 Cadastro de Voz\nGrave um audio lendo a frase a baixo ")
             st.write("### Doce de abóbora e laranja com gengibre ")
             uploaded_file_audio = st.file_uploader("Choose a file", key=6)
             submitted = st.form_submit_button("CADASTRAR") 
            
             if submitted:
                  st.write( "data", cpf)
                  data = {
                        "nome": nome,
                        "data_nascimento": data_nascimento,
                        "sexo": sexo,
                        "celular": celular,
                        "cpf": cpf,
                        "numero_inss":inss,
                        "email": email,
                        "senha":senha
                    } 
                  try:  
                      endpoint = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/user/"
                      r = post(endpoint,data).json()
                      #st.write(r)
                      path_face = save_image(uploaded_file_foto ,"facial") 

                      files = {'files': open(path_face,'rb')}
                      data = {"cpf":cpf,"tipo":"facial","operacao":"cadastro"}
                      endpoint_image = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/upload/image"
                      post(url=endpoint_image,data=data,files=files).json()

                      path_pose = save_image(uploaded_file_video,"pose")
                      files = {'files': open(path_pose,'rb')}
                      data = {"cpf":cpf,"tipo":"pose","operacao":"cadastro"}
                      endpoint_image = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/api/v1/upload/image"
                      post(url=endpoint_image,data=data,files=files).json()

                      path_audio = save_audio(uploaded_file_audio,"voz")  
                      user = r['userId']  
                      link_voz = upload_file(user,path_audio,"voz")     # url do s3 
                      dados = r  
                      dados['link_voz'] =  link_voz
                      result = CRUD.update(dados)
                      st.success('Dados Cadastrados Com Sucesso !')
                      st.balloons()
                  except:
                      st.error("FALHA AO CADASTRAR DADOS ! TENTE NOVAMENTE MAIS TARDE !")
                   #st.write(result)
                  #st.write(dados)
                  #r = get(endpoint_search,data).json()
                  #st.write(data)
                
        if option == "Não":
             ## busca por CPF
             st.write("EM construção")   

    
if __name__ == "__main__":
    main()