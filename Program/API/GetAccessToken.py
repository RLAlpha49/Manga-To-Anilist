"""
This module contains functions for getting the access token and
authentication code for the AniList API.

Functions:
- Get_Access_Token: Gets the access token from the environment variables
    or opens the authorization URL in the web browser.
- Get_Authentication_Code: Opens the authorization URL in the web browser
    with the parameters and checks if the access token is set in the
    environment variables.
"""

# pylint: disable=C0103
# Import necessary modules
import os
import platform
import time
import webbrowser

# Define the authorization URL for AniList OAuth
authorization_url = "https://anilist.co/api/v2/oauth/authorize"


# Function to get the access token
def Get_Access_Token(thread, app):
    """
    Gets the access token.

    This function gets the client ID from the environment variables and checks if it's found.
    If the client ID is not found, it prints an error message. If the client ID is found,
    it opens the authorization URL in the web browser and gets the authentication code.

    Parameters:
    thread (Thread): The thread object.
    app (App): The application object.

    Returns:
    str: The authentication code if the client ID is found, otherwise None.
    """
    # Get the client ID from the environment variables
    client_id = os.environ.get("ANILIST_CLIENT_ID")
    auth_code = None

    # If the client ID is not found, print an error message
    if client_id is None:
        message = (
            "No client ID found. Please enter your AniList client ID with the "
            "'Set API Values' button."
        )
        app.update_terminal(message)
    else:
        if platform.system() == "Linux":
            app.update_terminal(
                "Please open the following URL in your web browser and follow the instructions:"
            )
            print(
                "Please open the following URL in your web browser and follow the instructions:"
            )
            auth_url = f"{authorization_url}?client_id={client_id}&response_type=token"
            app.update_terminal(auth_url)
            print(auth_url)
            auth_code = Get_Authentication_Code(client_id, thread)
        elif platform.system() == "Windows":
            auth_code = Get_Authentication_Code(client_id, thread)

    return auth_code


def Get_Authentication_Code(client_id, thread):
    """
    Gets the authentication code.

    This function opens the authorization URL in the web browser with the parameters
    and checks if the access token is set in the environment variables.

    Parameters:
    client_id (str): The client ID for the AniList API.
    thread (Thread): The thread object.

    Returns:
    str: The access token if it's set in the environment variables, otherwise None.
    """
    while True:
        auth_params = {
            "client_id": client_id,
            "response_type": "token",
        }

        # Construct the URL and parameters
        url_params = "&".join([f"{key}={value}" for key, value in auth_params.items()])
        webbrowser.open(f"{authorization_url}?{url_params}")

        while True:
            if thread.stop:
                return None
            if os.environ.get("ACCESS_TOKEN") is not None:
                return os.environ.get("ACCESS_TOKEN")
            time.sleep(0.5)