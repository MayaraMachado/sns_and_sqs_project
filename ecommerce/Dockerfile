# Imagem oficial que servirá de base
FROM ubuntu:18.04

#VOLUME app
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Instala ferramentas necessárias
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install git

# Copia o arquivo requirements do diretório atual para o diretório /home/app do container
COPY ./requirements.txt ./

# Instala libs necessárias
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

# Remove arquivo requirements do diretório /home/app do container
RUN rm requirements.txt

# Cria um diretório para o projeto
RUN mkdir /app

# Define o diretório /home/app como um working directory
WORKDIR /app

# Realiza as migrações
#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate

# Remove pacotes não utilizados
RUN apt-get autoclean && apt-get autoremove

#CMD python3 manage.py runserver -p 0.0.0.0:8000
#CMD tail -f /dev/null
