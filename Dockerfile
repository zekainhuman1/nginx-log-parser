FROM python:3.9-slim

WORKDIR /app

COPY . /app

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

RUN echo "/app/*\n!/app/output/" > .gitignore

RUN apt-get update && apt-get install -y git

RUN git config --global user.name "YOUR_NAME" && \
    git config --global user.email "YOUR_EMAIL" && \
    git config --global init.defaultBranch "main"

# RUN pip install -r requirements.txt

CMD ["python", "parse_nginx_log.py", "--auto"]
