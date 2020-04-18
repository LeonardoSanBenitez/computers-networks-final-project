FROM python:3.6.9
ADD . /app
WORKDIR /app
RUN apt -y update && apt install -y sshpass openssh-client
RUN pip install -r requirements.txt
CMD python3 app.py