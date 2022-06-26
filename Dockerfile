FROM ubuntu:20.04

ENV BOTNAME=Console
ENV WEBHOOK_URL=webhook_url
ENV CLOGFILE=./console.log

WORKDIR /opt/aq2_log2disc

RUN     apt-get update; \
        apt-get install -y --no-install-recommends \
                python3-minimal \
                wget \
                nano \
                python3-pip; \
                pip install discord-webhook; \
                wget -q https://raw.githubusercontent.com/m4son/log2discord_aq2/main/aq2_log2discord.py

CMD [ "cp", "./aq2_log2discord.py","/opt/aq2_log2disc"]
CMD [ "python3", "./aq2_log2discord.py"]
