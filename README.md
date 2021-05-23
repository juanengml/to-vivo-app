# API APP TO VIVO


# como Rodar ? 

# Configure as credenciais da AWS 

![](https://raw.githubusercontent.com/juanengml/to-vivo-app/master/Screenshot_13.png)

# Configure Seu Bucket S3 

![](https://raw.githubusercontent.com/juanengml/to-vivo-app/master/Screenshot_14.png)

# Configure Seu Banco de Dados na LightSail

![](https://raw.githubusercontent.com/juanengml/to-vivo-app/master/Screenshot_15.png)

---
## Agora Por fim Com suas Credenciais em Mãos use o Comando a baixo 

make deploy-prod 
make deploy-prod 
```bash
foo $ make deploy-prod 

ENDPOINT http://ec2-3-238-49-213.compute-1.amazonaws.com:5003/

```

```bash
foo $ streamlit run interface.py  --server.port 5004
 

ENDPOINT http://ec2-3-238-49-213.compute-1.amazonaws.com:5004/

```

## PARA DOCUMENTAÇÃO SOBRE A API e seu USO

## Cadastro de usuario


```python
!pip3 install Faker 
```

    Defaulting to user installation because normal site-packages is not writeable
    Collecting Faker
      Downloading Faker-8.2.1-py3-none-any.whl (1.2 MB)
    [K     |████████████████████████████████| 1.2 MB 23.8 MB/s eta 0:00:01
    [?25hRequirement already satisfied: python-dateutil>=2.4 in /usr/local/lib/python3.6/dist-packages (from Faker) (2.8.1)
    Collecting text-unidecode==1.3
      Using cached text_unidecode-1.3-py2.py3-none-any.whl (78 kB)
    Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.6/dist-packages (from python-dateutil>=2.4->Faker) (1.15.0)
    Installing collected packages: text-unidecode, Faker
    Successfully installed Faker-8.2.1 text-unidecode-1.3



```python
endpoint = "http://172.31.70.217:5003/api/v1/user/"
```


```python
def generate_cpf(): 
    import random
    cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                
    for _ in range(2):                                                          
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
        cpf.append(11 - val if val > 1 else 0)                                  
                                                                                
    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)
```


```python
generate_cpf()
```




    '860.550.480-35'




```python
from requests import get,post,put
from faker import Faker
fake = Faker()

from random import choice,shuffle 

age = choice(["05-10-1956","01-12-1951","05-10-1966"])


data = {
    "nome": fake.name(),
    "data_nascimento": age,
    "sexo":"male",
    "celular":fake.phone_number(),
    "cpf":generate_cpf(),
    "numero_inss":fake.msisdn(),
    "email": fake.ascii_free_email(),
    "senha":fake.color_name()
    
}

post(endpoint,data).json()

```




    {'id': 1,
     'nome': 'Melissa Shepard',
     'data_nascimento': '01-12-1951',
     'sexo': 'male',
     'celular': '(399)861-9579x596',
     'cpf': '110.363.085-70',
     'numero_inss': '7048487344663',
     'email': 'michelleshelton@hotmail.com',
     'senha': 'LightBlue',
     'userId': 'usr_56b03806735049b2a87d6e49062f5a25'}



## Checando usuario 


```python
data = {
    "cpf":"110.363.085-70"
}
get(endpoint,data).json()
```




    {'id': 1,
     'nome': 'Melissa Shepard',
     'data_nascimento': '01-12-1951',
     'sexo': 'famale',
     'celular': '(399)861-9579x596',
     'cpf': '110.363.085-70',
     'numero_inss': '7048487344663',
     'email': 'michelleshelton@hotmail.com',
     'senha': 'LightBlue',
     'userId': 'usr_56b03806735049b2a87d6e49062f5a25'}



## Atualizando dados do Usuario


```python
data = {'nome': 'Melissa Shepard',
 'data_nascimento': '01-12-1951',
 'sexo': 'male',
 'celular': '(399)861-9579x596',
 'cpf': '110.363.085-70',
 'numero_inss': '7048487344663',
 'email': 'michelleshelton@hotmail.com',
 'senha': 'LightBlue',
 'userId': 'usr_56b03806735049b2a87d6e49062f5a25'}

put(endpoint,data).json()
```




    {'status': 'atualizado com sucesso !'}



## Upload Image S3


```python
!ls test/einstein.jpg

```

    compare.py
    einstein.jpg
    graph_opt.pb
    output_12b26471-378b-40b4-a4d8-0129eae4a8b9einstein.jpg
    output_6acbaee9-99fd-4270-bc1b-a7a85592c994einstein.jpg
    output_a41f204c-04e3-446d-9c02-5f9af823a177einstein.jpg
    output_d0169b49-a6e7-413b-a847-0c5dc5004bfeeinstein.jpg
    output_einstein.jpg
    output_einstein_compare.jpg
    output_einstein_diferente.jpg
    renato_corpo_inteiro.jpg
    test_api.py
    test_audio.py
    test_pose.py



```python

```


```python
open('test/einstein.jpg','rb')
```




    <_io.BufferedReader name='test/einstein.jpg'>




```python
files = {'files': open('test/einstein.jpg','rb')}
data = {"cpf":"110.363.085-70","tipo":"facial","operacao":"check"}

#headers = {'Content-Type' : 'image/jpeg'}
endpoint_image = 'http://172.31.70.217:5003/api/v1/upload/image'
print(endpoint_image)
post(url=endpoint_image,data=data,files=files).json()
```

    http://172.31.70.217:5003/api/v1/upload/image





    {'url': 'https://to-vivo-app.s3.amazonaws.com/users/usr_56b03806735049b2a87d6e49062f5a25/facial.jpg',
     'tipo': 'facial'}




```python
'http://172.31.70.217:5003/api/v1/upload/image'
```




    'http://172.31.70.217:5003/api/v1/user/'




```python
!ls test
```

    compare.py
    einstein.jpg
    graph_opt.pb
    output_12b26471-378b-40b4-a4d8-0129eae4a8b9einstein.jpg
    output_6acbaee9-99fd-4270-bc1b-a7a85592c994einstein.jpg
    output_a41f204c-04e3-446d-9c02-5f9af823a177einstein.jpg
    output_d0169b49-a6e7-413b-a847-0c5dc5004bfeeinstein.jpg
    output_einstein.jpg
    output_einstein_compare.jpg
    output_einstein_diferente.jpg
    renato_corpo_inteiro.jpg
    test_api.py
    test_audio.py
    test_pose.py


### - TESTAR NOVAMENTE AUTENTICACAO 


```python
data_verificacao = {'url': 'https://to-vivo-app.s3.amazonaws.com/users/usr_56b03806735049b2a87d6e49062f5a25/facial.jpg',
 'tipo': 'facial'}

endpoint_verificacao = "http://172.31.70.217:5003/api/v1/verificacao/"
post(endpoint_verificacao,data_verificacao).json()

```




    {'dados': {'url': 'https://to-vivo-app.s3.amazonaws.com/users/usr_56b03806735049b2a87d6e49062f5a25/facial.jpg',
      'tipo': 'facial'},
     'check': {'facial': 'aprovado'}}




```python
import pandas as pd 

db = get("http://172.31.70.217:5003/api/v1/admin/db").json()

df = pd.DataFrame(db)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>nome</th>
      <th>data_nascimento</th>
      <th>sexo</th>
      <th>celular</th>
      <th>cpf</th>
      <th>numero_inss</th>
      <th>email</th>
      <th>senha</th>
      <th>userId</th>
      <th>link_facial</th>
      <th>link_pose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Melissa Shepard</td>
      <td>01-12-1951</td>
      <td>male</td>
      <td>(399)861-9579x596</td>
      <td>110.363.085-70</td>
      <td>7048487344663</td>
      <td>michelleshelton@hotmail.com</td>
      <td>LightBlue</td>
      <td>usr_56b03806735049b2a87d6e49062f5a25</td>
      <td>https://to-vivo-app.s3.amazonaws.com/users/usr...</td>
      <td>https://to-vivo-app.s3.amazonaws.com/users/usr...</td>
    </tr>
  </tbody>
</table>
</div>



