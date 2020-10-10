FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /nlpapi

RUN apt install bash

COPY requirements.txt ./

COPY . /var/www/nlpapi

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]