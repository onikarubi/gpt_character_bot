FROM python:3.10-slim-buster

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim
RUN apt-get install -y git

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

WORKDIR /products

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]
