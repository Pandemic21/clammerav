import logging
import json
import requests

### Does the initial setup.
### Only run once, when the agent is first installed.

logging.basicConfig(filename="./clammer_init.log", level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

try:
    file = open("ingest_join_url", "r")
    ingest_join_url = file.read().splitlines()[0]
    logger.debug("Using ingest join URL: " + ingest_join_url)
except Exception as e:
    logger.error("Couldn't get ingest join URL (does file exist?)")
    logger.error(e)

# GET ingest join URL for CSRF token
try:
    s = requests.Session()
    resp = s.get(ingest_join_url)

    logger.debug("Successful GET on " + ingest_join_url)
except Exception as e:
    logger.error("Couldn't GET ingest join URL: " + ingest_join_url)
    logger.error(e)

# GET ingest join URL with headers
try:
    headers = {'create-user': '1'}
    resp = s.get(ingest_join_url, headers=headers)

    logger.debug("Successful GET with headers, response: " + resp.text)
except Exception as e:
    logger.error("Couldn't GET ingest join URL with headers: " + ingest_join_url)
    logger.error("GET url: " + ingest_join_url)
    logger.error(e)

# Create conf file
try:
    config_info = json.loads(resp.text)

    # Save credentials
    file = open("clammer.conf", "a")
    file.write("[Clammer]\n")
    file.write("logfile = " + config_info['home'] + "/clammer.log\n")
    file.write("loglevel = " + config_info['log_level']\n)

    file.write("\n[Agent]\n")
    file.write("asset = " + config_info['username'] + "\n")
    file.write("username = " + config_info['username'] + "\n")
    file.write("password = " + config_info['password'] + "\n")
    file.write("home = " + config_info['home'] + "\n")

    # Save server info
    # TODO: make these URLs dynamic, the host/port may change
    file.write("\n[Server]\n")
    file.write("LoginURL = " + config_info['login_url'] + "\n")
    file.write("logoutURL = " + config_info['logout_url'] + "\n")
    file.write("rawlogURL = " + config_info['rawlog_url'] + config_info['username'] + "/sendrawlog/\n")

    # if there's an existing ClamAV install, configure to monitor the logs and manage configs
    if config_info['existing_clamav']:
        logger.debug("Existing ClamAV install flag set, writing log and config files...")

        # write the log files to clammer.conf
        file.write("\n[LogFiles]\n")
        log_files = config_info['log_files'].split(',')

        for log_file in log_files:
            # this gets the file name for the log file
            file.write(log_file.split('.')[0].split('/')[len(s.split('.')[0].split('/'))-1] + " = " + log_file)

        # do the same for the config files
        file.write("\n[ConfigFiles]\n")
        config_files = config_info['config_files'].split(',')

        for config_file in config_files:
            # this gets the file name for the config file
            file.write(config_file.split('.')[0].split('/')[len(s.split('.')[0].split('/'))-1] + " = " + config_file)

    else:
        logger.debug("Existing ClamAV install flag NOT set, installing ClamAV")

        # TODO: write code to install clamav and create clammer.log entries for clamav logs, config files
        file.write("\n[LogFiles]\n")
        file.write("\n[ConfigFiles]\n")

    file.close()

    logger.debug("Saved credentials to clammer.conf")
except Exception as e:
    logger.error("Couldn't save credentials: " + resp.text)
    logger.error(e)



# TODO: write POST method after a user account has been created with the GET with headers to send info (hostname, IPs...)
