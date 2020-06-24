#!/usr/bin/python3

# This is to automate some bitbucket tasks like create a pull request to the story branch

import keyring
from configobj import ConfigObj

class ToxixConfigObj(ConfigObj):
    def set_password(self, key,  password):
        keyring.set_password('ToxixBitbucket', key, password)

    def get_password(self,  key):
        return keyring.get_password('ToxixBitbucket', key)
