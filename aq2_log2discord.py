#!/usr/bin/python3.5

import sys, os, time, re, logging
from discord_webhook import DiscordWebhook

# IMPORTANT
#
# q2proded
#
# seta logfile_prefix '@ [%Y-%m-%d %H:%M] '
# seta logfile 1
# seta logfile_flush 2
#

WEBHOOK = os.getenv('WEBHOOK_URL','YOUR_WEBHOOK_URL')
DISCORD_USERNAME = os.getenv('BOTNAME', 'Console')
CLOG = os.getenv('CLOGFILE','console.log')
CURRENT = False

# Logging setup
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(stream=sys.stdout, format=Log_Format, level=LOGLEVEL)
logger = logging.getLogger()
logger.info("Log level set to %s", LOGLEVEL)

def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue

        yield line
        
event_msgs = {
        "join":"A .+\] (.+) entered the game",
        "diss":"A .+\] (.+)\[.+ disconnected",
        "cname":"A .+\] (.+)\[.+ changed name to (.+)",
        "chat":"T .+\] (\w.+)\: (.+)",
        "map":"A .+\] Next map is (.+)",
        "map2":"A .+\] SpawnServer: (.+)",
        "score":"A .+\] Current score is.+\:.(.+) to .+\: (.+)",
        "gameend":"A .+\] Game ending at: (.+)",
}

if __name__ == '__main__':
    try:
        logfile = open("./logs/"+CLOG,"r")
        loglines = follow(logfile)
    except OSError:
        logger.info("Cannot open "+CLOG)    
    else:
        logger.info("Logfile ("+CLOG+") Opened!")
    
    for line in loglines:
        for k, v in event_msgs.items():
            m = re.search(v,line)
            if m and 'MVDSPEC' not in m.group(1):
                logger.info(k+" >> "+line)
                if k == "score":
                    last_score = m
                    if CURRENT:
                        fmsg ='***``` Current score: {} to {}\n```***'.format(m.group(1),m.group(2))
                if k == "gameend":
                    fmsg ='***``` Game ends with score {} to {}\n```***'.format(last_score.group(1),last_score.group(2))
                if k == "cname":
                    fmsg ='```diff\n- {} is known as {}\n```'.format(m.group(1),m.group(2))
                if k == "diss":
                    fmsg ='```diff\n- {} disconnected\n```'.format(m.group(1))
                if k == "join":
                    fmsg ='```diff\n- {} entered the game\n```'.format(m.group(1))
                if k == "chat":
                    if '[DEAD]' in line:
                        fmsg ='```diff\n+ [DEAD] {}: {}\n```'.format(m.group(1),m.group(2))
                    else:
                        fmsg ='```diff\n+ {}: {}\n```'.format(m.group(1),m.group(2))
                if k == "map" or k == "map2":
                    fmsg ='**```fix\n SpawnMap: {}\n```**'.format(m.group(1))
                if fmsg:
                    webhook = DiscordWebhook(url=WEBHOOK, username=DISCORD_USERNAME, rate_limit_retry=True, content=fmsg )
                    response = webhook.execute()
                    del fmsg
