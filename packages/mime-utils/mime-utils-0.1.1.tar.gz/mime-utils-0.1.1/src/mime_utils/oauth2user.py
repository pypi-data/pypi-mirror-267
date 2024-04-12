"""
Helper class to use user interaction in browser to get token

"""
from __future__ import annotations
from typing import Any
from logg import Logg

from oauthlib.oauth2 import BackendApplicationClient, WebApplicationClient
from requests import Response
from requests_oauthlib import OAuth2Session
from selenium import webdriver
import time


class Credentials:
    """
    Class to store credential attributes

    Attributes:
    -----------
    *client_id* : str
        Oauth2 Client ID
    *client_secret* : str
        Oauth2 Client Secret
    *authorization_base_url* : str
        Base URL for authenticating user
    *token_url* : str
        Location to get Oauth2 token from
    *redirect_uri* : str
        Where client should be redirected to store tokens. 
        Note: This uri must be configured in OIDC Server setup
    *scope* : str
        Login scope
        
    """
    client_id: str
    client_secret: str
    authorization_base_url: str
    token_url: str
    redirect_uri: str
    scope: str

    def __init__(self, client_id:str, client_secret:str, authorization_base_url:str, token_url:str, redirect_uri:str, scope:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope

    def __str__(self):
        return f"Credentials: client_id={self.client_id}, client_secret=<redacted {len(self.client_secret)} characters>, authorization_base_url={self.authorization_base_url}, token_url={self.token_url}, redirect_uri={self.redirect_uri}, scope={self.scope}"

class Oauth2User:
    """
    Class for getting login session from web-url with user interaction

    Attributes:
    -----------
    *TIMEOUT* : int
        Default timeout. Number of seconds to wait for user interaction
    
    """
    TIMEOUT: int = 30

    __credentials: Credentials = None
    l: Logg = None

    def __init__(self, *, credentials:Credentials, logg:Logg):
        """
        Parameters
        ----------
        *credentials* : Credentials
            Object containing information for Oauth2 authentication

        *logg* : Logg
            Logg object for output logging.
        """
        self.__credentials = credentials
        self.l = logg
        self.l.debug(f"Oauth2User created with {self.__credentials}")
        
    def authenticate(self, timeout:int=None) -> dict[str, Any]:
        if timeout is None:
            timeout = self.TIMEOUT

        client = WebApplicationClient(client_id=self.__credentials.client_id)
        oauth = OAuth2Session(client=client)

        authorization_url, state = oauth.authorization_url(url=self.__credentials.authorization_base_url)
        self.l.debug(f"Got state {state}, statauthorization_url {authorization_url}")

        browser = webdriver.Chrome()
        browser.get(authorization_url)

        while timeout:
            time.sleep(1)
            timeout -= 1
            uri_part:str = browser.current_url.split("?", 1)[0]
            if uri_part == self.__credentials.redirect_uri:
                timeout = 0

        redirected_url = browser.current_url
        self.l.debug(f"Redirected URL {redirected_url}")

        browser.quit()

        tokens: dict[str, Any] = oauth.fetch_token(token_url=self.__credentials.token_url, authorization_response=redirected_url, client_secret=self.__credentials.client_secret)
        self.l.debug(f"Got tokens: {tokens}")

        return tokens

