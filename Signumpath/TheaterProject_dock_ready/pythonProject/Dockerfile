FROM python:3.8
WORKDIR /home/code
RUN pip3 freeze > requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install flask
RUN pip3 install flask_sqlalchemy
RUN pip3 install python-dotenv
EXPOSE 5000
COPY . .
CMD ["flask", "run","--host=0.0.0.0"]