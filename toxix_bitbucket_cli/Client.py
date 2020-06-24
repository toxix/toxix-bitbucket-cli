#!/usr/bin/python3

# This class is to abstract the calls to the rest api of bitbucket

# reference of bitbucket
# https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests#post

import requests

from .BitbucketRestClientExceptions import UnknownError, InvalidIDError, NotFoundIDError, NotAuthenticatedError, PermissionError

class Client():
    BASE_URL = 'https://api.bitbucket.org/2.0/'
    
    def __init__(self, user, password):        
        """Initial bitbucket session with user/password
        Args:
            user: Bitbucket user name (Not the email! Get it from "personal settings" -> "account settings")
            password: Bitbucket App password (get/generate it in "personal settings" -> "app passwords")
        Returns:
        """

        self.user = user
        self.password = password

        user_data = self.get_user()
        self.username = user_data.get('username')
        
    def get_user(self, params=None):
        """Returns the currently logged in user.
        Args:
            params:
        Returns:
        """
        return self._get('user', params=params)
    
    def creat_pullrequest(self,repository_path, data, params=None):
        """Creates a new pullrequest.
        This call requires authentication. Private repositories or private issue trackers require
        the caller to authenticate with an account that has appropriate authorisation.
        The authenticated user is used for the issue's reporter field.
        
        Example for data:
        {
          "title": "Merge some branches",
          "description": "stackoverflow example",
          "source": {
              "branch": {
                 "name": "mybranchToMerge"
               },
               "repository": {
                 "full_name": "account/reponame"
               }
          },
          "destination": {
              "branch": {
                  "name": "master"
               }
           },
           "reviewers": [ { "username": "reviewerUsername" } ],
           "close_source_branch": false
        }


        Args:
            repository: {workspace}/{repo_slug}
            data: 
            params:
        Returns:
        """
        return self._post('repositories/{}/pullrequests'.format(repository_path), data=data,  params=params)

    def get_repository_branches(self, repository_path, params=None):
        return self._get('repositories/{}/refs/branches'.format(repository_path), params=params)

    def create_repository_branche(self, repository_path, data,  params=None):
        print(repository_path)
        print('repositories/{}/refs/branches'.format(repository_path))
        return self._post('repositories/{}/refs/branches'.format(repository_path), data=data, params=params)


    def _get(self, endpoint, params=None):
        response = requests.get(self.BASE_URL + endpoint, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _post(self, endpoint, params=None, data=None):
        response = requests.post(self.BASE_URL + endpoint, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _put(self, endpoint, params=None, data=None):
        response = requests.put(self.BASE_URL + endpoint, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _delete(self, endpoint, params=None):
        response = requests.delete(self.BASE_URL + endpoint, params=params, auth=(self.user, self.password))
        return self._parse(response)
        
    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if 'errorMessages' in r:
                message = r['errorMessages']
        except Exception:
            message = 'No error message.'
        # todo refector as mapping
        if status_code == 400:
            raise InvalidIDError(message)
        if status_code == 401:
            raise NotAuthenticatedError(message)
        if status_code == 403:
            raise PermissionError(message)
        if status_code == 404:
            raise NotFoundIDError(message)
        raise UnknownError(message)
