"""Module to start a webservice to interact with the user"""
from flask import Flask, request
from blocker import WebUntisAccountBlocker
from logging_formatter import ConfigLogger

class WebBlockAPI:
    """Lets the client interact with the backend, with diffrent methods"""
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route('/api/schools', methods=['GET'])(self.get_schools)
        self.app.route('/api/school', methods=['POST'])(self.set_school)
        self.app.route('/api/user', methods=['POST'])(self.set_user)
        self.app.route('/api/block', methods=['POST'])(self.send_block)
        self.blocker = WebUntisAccountBlocker()
        self.logger = ConfigLogger().setup()
        self.logger.info("Server started")

    def get_schools(self):
        """returns all saved schools"""
        schools = self.blocker.get_saved_schools()
        return {'schools': schools}

    def set_school(self):
        """lets the user set the school"""
        school_name = request.json['school_name']
        status = self.blocker.set_school(school_name)
        return {'status': status}

    def set_user(self):
        """let the user set the user"""
        username = request.json['username']
        status = self.blocker.set_username(username)
        return {'status': status}

    def send_block(self):
        """sends block request to the backend"""
        status = self.blocker.block()
        return {'result': status}

    def run(self):
        """runs the app"""
        self.app.run(debug=True)
