# Backend

The backend is responsible for receiving requests from the frontend, processing the data, and performing the blocking of a user. It is built using the Flask RESTful API and includes the following modules:

    json: Used to parse JSON objects in the requests and responses.
    os: Used to interact with the operating system and access files.
    re: Used for regular expressions in the parsing of the HTML page.
    validators: Used to validate URLs.
    bs4: Used to parse the HTML page.
    requests_html: Used to perform HTTP requests.

## WebUntisBlocker Class

This class contains the main logic for blocking a user. It has the following attributes:

    logger: A logger instance used for logging.
    url: The URL to which login requests are sent.
    logurl: The URL of the logging page.
    payload: A dictionary that contains the login data.

## The class has the following methods:


### block()

This method performs the actual blocking of the user. It sends login requests to the WebUntis website and checks whether the user is blocked or not. If the user is blocked, it returns a success message, and if not, it returns an error message.
### get_saved_schools()

This method reads the list of saved school IDs from a file and returns them as a list.
### set_username(username)

This method sets the username in the payload dictionary.
### set_school(schoolname)

This method sets the school in the payload dictionary. It also checks whether the input is a valid URL or a saved school ID.


## To run the project using your own server:

    Clone the repository to your local machine.

    Navigate to the backend directory and run the following command to install the required dependencies:

    pip install -r requirements.txt

    Run the following command to start the backend server: python main.py
