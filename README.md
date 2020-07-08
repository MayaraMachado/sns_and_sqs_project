# Projeto SQS e SNS

Este projeto implementa de forma abstrata algumas ações que podem ser corriqueiras em qualquer ecommerce. Este é um projeto de estudo, que ainda está em progresso, onde eu exploro algumas funcionalidades da AWS SNS e AWS SQS para uma comunicação no padrão Publish/Subscribe. Este projeto foi desenvolvido utilizando Django Rest Framework, PostgreSQL, Celery e Boto3.

**Atenção! Para total funcionamento da aplicação, é necessário possuir uma conta na AWS e inserir as credenciais de acesso no arquivo .env de cada aplicação. Além disso, é preciso pré-configurar o console AWS para disponibilização do Tópico SNS e das filas SQS. Para maiores explicações de como configurar utilizando Boto3, eu fiz uma [série de postagens lá no meu blog](https://mchdax.now.sh/tag/sqs_sns_series).**

Na primeira aplicação, **ecommerce**, é possível criar um usuário para realizar login, criar vendedores e produtos vinculados a eles, realizar pedidos de compras e visualizar o seu histórico de compras. A aplicação utiliza autenticação JWT para requisições de compra e histórico de compras, desse modo, é preciso enviar o token de autenticação nesse cenário. A aplicação ecommerce, então dispara uma mensagem para o tópico SNS cujo a aplicação tem acesso, e este tópico irá disparar a notificação para as filas necessárias.

A segunda aplicação, **payment_gateway**, realiza tasks periódicas para consumo constante da fila de mensagem a qual ele tem acesso. Ao receber novas mensagens, a aplicação contabiliza o quanto cada vendedor vendeu a cada compra, assim como guarda um registro desse valor a ser recebido pelo vendedor. A aplicação também disponibiliza uma rota para consumo do lucro para cada vendedor.

## Getting Started

Essas são as instruções para realizar a preparação do ambiente. O projeto está rodando utilizando Docker, e é necessário uma pré configuração dos banco de dados.

### Pré-Requisitos

- docker

### Installing

Apenas clone este repositório e crie seu arquivo .env a partir do arquivo example_env.txt de cada projeto. 

*Detalhe: A base de dados utilizada, PostgreSQL, já encontra-se configurado no arquivo docker-compose.yml, por isso o arquivo de exemplo da .env já tem a configuração padrão para acesso do postgre da aplicação, não sendo necessário realizar a alteração de qualquer dado sobre o banco.*

Com o arquivo .env configurado, agora vamos buildar e executar o projeto, para isso apenas execute:

```
make run
```

Como as aplicações não encontrarão as bases de dados criadas, as duas aplicações irão dar exit. Não se preocupe, o próximo passo é para resolver essa situação.

##### Configurar Base de Dados

Agora nós precisamos criar o banco, como deixamos a instância do banco rodando em background é possível acessar o psql, para isso execute:

```shell
$ make psql
```

Uma vez já conectado agora basta criar os bancos de dados necessários, para isso execute:

```shell
postgres=# CREATE DATABASE ecommerce;
CREATE DATABASE
postgres=# CREATE DATABASE payments;
CREATE DATABASE
postgres=# \q

```

Pronto, agora nós podemos restartar os containers da aplicação:

```
$ sudo docker-compose restart ecommerce_container
$ sudo docker-compose restart payments_gateway_container
```


##### Conexão com AWS

Caso você possua configuração AWS e deseja que a aplicação realize essa comunicação, precisaremos antes configurar nas duas aplicações. 

Na aplicação ecommerce edite o campo USAR_AWS na linha 178 do arquivo **ecommerce/ecommerce/settings.py** para o seguinte status:


```
USAR_AWS = True
```

E na aplicação payment_gateway, vamos alterar a fixture do tasks de verificação. Na linha 80 do arquivo **payment_gateway/api/fixtures/tasks.json**:

```
80. "enabled": true,
```

Desse modo a aplicação irá reconhecer que pode realizar a comunicação.

##### Rodando as Fixtures

Para facilitar o uso da aplicação eu deixei algumas fixtures para serem criadas no banco de dados. Para isso basta executar:

```
$ make shell_ecommerce

# python3 manage.py loaddata api/fixtures/users.json 
# python3 manage.py loaddata api/fixtures/sellers.json
# python3 manage.py loaddata api/fixtures/products.json 
```

##### Para finalizar a execução do projeto:

```
make stop
```

## Running the tests

Para executar os teste:

```
$ make shell_ecommerce
$ pytest --cov=api api/tests/ -vv
```

## Requisições

1- Login de Usuário (Form URL-Encoded):

Url: localhost:8000/login/

username | password
---------| --------
mayara |123

2- GET Produto

URL: localhost:8000/products/

3- POST Compra

Authorization: JWT {TOKEN}

URL: localhost:8000/purchase/

Body:

```json
{
	"products" : [
		{
			"product_id" : "dfde0a97-ba8a-4b37-bb0e-61ae75ae4380"
		}
	],
   "credit_card":{
      "card_number":"1234123412341234",
      "cvv":789,
      "card_holder_name":"Luke Skywalker",
      "exp_date":"12/24"
   }
}
```

4- GET Histórico de compras

Authorization: JWT {TOKEN}
URL: localhost:8000/purchase/

5- GET Vendedores

URL: localhost:8000/seller

6- GET Lucro de vendedor

URL: localhost:8001/revenue/591878dd-783a-4d73-abf2-7314048f563b

## Built With

* [Django](https://www.djangoproject.com/) 
* [Django Rest Framework](https://maven.apache.org/) - The web framework used
* Celery
* Redis
* Boto3
* [pytest-django](https://pytest-django.readthedocs.io/en/latest/tutorial.html) - Django Test Suite
* [pytest-cov](https://pypi.org/project/pytest-cov/) - Python Pytest Coverage

## Authors

* **Mayara Machado** - *Initial work* - [mchdax.now.sh](https://mchdax.now.sh/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
