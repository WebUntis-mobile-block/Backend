"""Module to start the WebBlockApi"""
from handlers.api_handler import WebBlockAPI


if __name__ == '__main__':
    api = WebBlockAPI()
    api.run()
