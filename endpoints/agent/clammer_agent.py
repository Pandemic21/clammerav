import configparser
import datetime
import sys
import logging
import requests
from pygtail import Pygtail

class Clammer():
    def __init__(self):
        # TODO: change the clammer agent log location to /opt/clammer/var/log

        # read config file to get the clammer agent log file and log level
        try:
            config = configparser.ConfigParser()
            config.read("clammer.conf")
            self.logfile = config['Clammer']['logfile']
            self.loglevel = config['Clammer']['loglevel']

            # clammer server info
            self.login_url = config['Server']['loginURL']
            self.logout_url = config['Server']['logoutURL']
            self.rawlog_url = config['Server']['rawlogURL']

            # agent info
            self.asset = config['Agent']['asset']
            self.username = config['Agent']['username']
            self.password = config['Agent']['password']
            self.home_dir = config['Agent']['home']
        except Exception as e:
            logging.basicConfig(filename='./out.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
            logger=logging.getLogger(__name__)
            logger.error("Critical error: couldn't find clammer.conf file, or the Clammer section in it")
            logger.error(e)
            exit()

        # create logger
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)

    ### Get new ClamAV log files ###
    # parameters:
    #   location of log file to check (e.g. "/var/log/clam.log")
    # returns:
    #   an empty array if no new lines are found
    #   array of new log lines if new log lines exist
    def read_log_file(self, log):
        self.logger.debug("Checking log file: " + log)
        new_lines = []

        try:
            for line in Pygtail(log):
                new_lines.append(line)
        except Exception as e:
            self.logger.error("Couldn't read log file")
            self.logger.error(e)

        # if the list is empty
        if not new_lines:
            self.logger.debug("No new lines in log file, returned empty array")
            return new_lines
        # if the list has items
        else:
            self.logger.debug("Found " + str(len(new_lines)) + " new lines in log file")
            return new_lines

    ### Send raw logs to Clammer server ###
    # parameters:
    #   an array of new logs to send
    # returns:
    #   0 if successful
    #   different number if unsuccessful
    def send_raw_log(self, log_lines):
        # verify there are actually new logs to send
        if not log_lines:
            self.logger.error("Called send_raw_log but no new log lines to send to server")
            return 1

        # login to Clammer server
        try:
            s = requests.Session()
            resp = s.get(self.login_url)

            self.logger.debug("Get CSRF token: GET '" + self.login_url + "' status: " + str(resp.status_code))

            csrf_token = s.cookies['csrftoken']
            resp = s.post(self.login_url, data= \
                { \
                'csrfmiddlewaretoken': csrf_token, \
                'username': self.username, \
                'password': self.password \
                })

            self.logger.debug("Logged into Clammer server: " + self.login_url)
        except Exception as e:
            self.logger.error("Couldn't login to server: " + self.login_url)
            self.logger.error(e)

        # POST log lines to Clammer server
        self.logger.debug("Sending these new lines to Clammer:")
        try:
            for line in log_lines:
                csrf_token = s.cookies['csrftoken']
                resp = s.post(self.rawlog_url, data= \
                    { \
                    'csrfmiddlewaretoken': csrf_token, \
                    'log_data': line \
                    })

                self.logger.debug(line)
        except Exception as e:
            self.logger.error("Couldn't POST new log line to server: " + line)
            self.logger.error("POST url: " + self.rawlog_url)
            self.logger.error(e)

        # logout of Clammer server
        try:
            s.get(self.logout_url)
            self.logger.debug("Logged out: " + self.logout_url)
        except Exception as e:
            self.logger.error("Couldn't logout of server")
            self.logger.error(e)

        # return 0, all good
        return 0


if __name__ == "__main__":
    clammer = Clammer()

    config = configparser.ConfigParser()
    config.read("clammer.conf")
    freshclam_log = config['LogFiles']['FreshClam']

    new_logs = clammer.read_log_file(freshclam_log)
    result = clammer.send_raw_log(new_logs)

    if result == 0:
        print("Sent logs all good")
    else:
        print("Couldn't send logs, result: " + str(result))
