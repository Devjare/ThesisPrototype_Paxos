FROM python:3.10.4

COPY . /middleware/
WORKDIR /middleware

RUN apt-get -y update
RUN apt-get install -y iputils-ping
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# When using compose, since env variables will be defined there.
# on dockerfile only the instruccion below is needed
# ARG PORT
# If not using compose, define by using ENV
ENV PORT=60001
EXPOSE 60001

CMD ["python3", "main.py"]
