import streamlit as st
from random import choice
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
import altair as alt
import datetime
import streamlit.components.v1 as stc
from requests import post,get,put 

def status():
    return choice(range(100))


def save_image(img_file_buffer,name):
    image = Image.open(img_file_buffer)
    img_array = np.array(image)
    filename = "{}.jpeg".format(name)
    cv2.imwrite(filename, img_array)
    return filename

def save_audio(file_buffer, name):
    pass

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
    HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;"> 
         TO vivo - provando que existe vida.     </h1>
    <p style="color:white;text-align:center;">Built with DataFlavor</p>
    </div>"""
    
    stc.html(HTML_BANNER)
    
    st.write("""
    ----
    """)
    col1,col2,col3=st.beta_columns(3)
    
    menu = st.sidebar.selectbox(
    "Funcionalidade",
    ("Processo", "Acompanhar processo","Minhas informações","Prova de Vida")) 
    
    #st.write(menu)
    if menu == "Processo":
        with st.form("process"):
            col5,col6=st.beta_columns(2)
            with col5:
                st.write("## Digite Seu CPF por favor")
            with col6:
                cpf = st.text_input('CPF')
                
            submitted = st.form_submit_button("Buscar") 
            if submitted:
              st.write( "data", cpf)
              endpoint_search = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5004/api/v1/user/"
              data = {
                 "cpf":"110.363.085-70"
              }
              r = get(endpoint_search,data).json()
              st.write(r)
              
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
              st.write( "data", date)
              st.write(date,uploaded_file_foto,uploaded_file_video, uploaded_file_audio)
              st.balloons()
              ## enviar para api de autenticação 
              ## enciar para s3 e rodar sagemaker para validação 
              ## usar ec2 para hosting
              st.write(" ")

    if menu == 'Acompanhar processo':
        col3,col4=st.beta_columns(2)
        
        with col3:
           st.info("""
        ## Status da sua prova de vida 💡
         """ ) 
        
        with col4:
           st.write("""
        ## Status do processo [ em ANDAMENTO ]
         """ )  
           my_bar = st.progress(90)
            
        st.warning("""
        Caso tenha passado mais de 2 horas entre contato com
        
        📣 +55 41 992149181 
         """ ) 
        
    if menu == "Minhas informações" :
        option = st.selectbox(
       'Primeiro Acesso ?',
        ('Sim', 'Não'))
        if option == "Sim":
          with st.form("info"):
             col5,col6=st.beta_columns(2)
                
             with col5:
                   nome = st.text_input('NOME COMPLETO')
                   data_nascimento = st.date_input( "Data de Nascimento",
                                                  datetime.date(1958, 7, 6))
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
                  endpoint_search = "http://ec2-3-238-49-213.compute-1.amazonaws.com:5004/api/v1/user/"
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
                  save_image(uploaded_file_foto ,"facial")                
                  save_image(uploaded_file_video,"pose")
                  #save_audio(uploaded_file_audio,"voz")
                    
                    
                  #r = get(endpoint_search,data).json()
                  st.write(data)
                
        if option == "Não":
             ## busca por CPF
             st.write("EM construção")   

    
if __name__ == "__main__":
    main()