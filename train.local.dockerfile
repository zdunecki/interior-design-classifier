FROM python:3.7

ARG SSH_PRIVATE_KEY
ARG SSH_PUB_KEY

RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan gitlab.com > /root/.ssh/known_hosts

RUN echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    echo "$SSH_PUB_KEY" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

WORKDIR /app/

ADD ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN rm -rf /root/.ssh/

ADD . .

ENTRYPOINT python ./train.py $ARGUMENTS