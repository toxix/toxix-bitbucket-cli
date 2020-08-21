#!/usr/bin/python3

# This is to automate some bitbucket tasks like create a pull request to the story branch

from .Client import Client
import os
import re
from git import Repo
#import pyperclip

class ToxixBB:
    def __init__(self, user, password):
        """Initial session with user/password, and setup repository owner
        Args:
            user: Bitbucket user name (not email) from "personal settings" -> "account settings"
            password: Bitbucket App password from "personal settings" -> "app passwords"
            workspace: If you are member in more than one workspace you can choose here a different one. (first part of the url after bitbucket.org)
        Returns:
        """
        self.client = Client(user, password)
        self.repo = Repo(os.getcwd(), search_parent_directories=True)
        self.jiraRegex = re.compile('^[A-Z]+-\d+$')
        
        # check if things worked
        assert not self.repo.bare

    def create_pullrequest(self, destination, reviewers=None, source=None, close=True,  story_name=None):
        # make sure things are pushed
        self.repo.remotes.origin.push()
        
        # check source branch
        if source is None:
            source = self._get_current_branch()

        # construct the title
        titleFragments = []
        for s in source.split('_'):
            if self.jiraRegex.match(s):
                titleFragments.append(s)
            else:
                # setting story name from current branch
                #if story_name == None:
                #    story_name = s
                titleFragments.append(s.replace('-',' ').title())
        title = ' '.join(titleFragments)

        # use magic keyword story to make pr to story branch
        if destination == 'story':
            storyId = source.split('_')[0] 
            destination = self._get_or_create_story_branch(storyId, story_name=story_name)
        
        # check if there is a diff to the destination branch
        self.repo.remotes.origin.fetch(destination)
        if not self.repo.index.diff('origin/%s' %(destination)):
            print("There is no difference between your current code and the branch you want to open the pullrequest to. Make sure you commited your changes and are opening the pullrequest to the correct branch.")
            exit(1)

        data = {
                'close_source_branch': close,
                #'description': 'zenos example',
                'destination': {'branch': {'name': destination}},
                'source': {'branch': {'name': source}},
                #'reviewers': [{'username': 'reviewerUsername'}],
                'title': title
                }
                
        # print something nice to the user
        pr = self.client.creat_pullrequest(self._get_bitbucket_repro_path(), data)
        print("\n##### Done ####")
        link = pr['links']['html']['href']
        msg = 'Pull Request: %s\n%s\npick:' % (title,  link)
        # todo copy text baustein to clipboard
        #pyperclip.copy(msg)
        # todo print link klickable
        print(msg)
                  ##### Done ####
        print('#################')
        # https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
        # might considder raw output
        # https://stackoverflow.com/questions/31917595/how-to-write-a-raw-hex-byte-to-stdout-in-python-3
        #colorama.init()
        #print("\n\n")
        #sys.stdout.buffer.write('\e]8;;'+link+'\e\\'+'LinkText'+'\e]8;;\e')
        #sys.stdout.flush()
        # \e]8;;http://example.com\e\\This is a link\e]8;;\e
        
    # todo implement pipeline running
        
    def _get_current_branch(self):
        return self.repo.active_branch.name
        
    def _get_bitbucket_repro_path(self):
        '''Guessing the remote url from the origin url of the git repository of the current folder'''
        # todo this only works with ssh urls, check for https urls
        url = self.repo.remotes.origin.url
        return url.replace('git@bitbucket.org:', '').replace('.git','')
        
    def _get_or_create_story_branch(self,  storyId, story_name=None):
        #check if story branch exist and return name
        candidats = self.client.get_repository_branches(self._get_bitbucket_repro_path(), params={'q': 'name ~ "%s"' % storyId})
        for candidat in candidats['values']:
            name = candidat['name']
            i = 0
            for s in name.split('_'):
                if self.jiraRegex.match(s):
                    i+=1
            if i == 1:
                print("Use existing story branch: "+name)
                return name
        #create story branch and return name
        if story_name == None:
            story_name = input("Story Branch Name (only alphanumeric and hyphen allowed) [story-branch]:\n %s_"%storyId)
        if not story_name:
            story_name = "story-branch"
        # strip not allowed characters
        story_name = re.sub('[^a-zA-Z0-9\-]', '',  story_name)
        data = {
            'name': storyId + '_' + story_name , 
            'target': {'hash': 'dev'}, 
            }
        print("Create new story branch: "+data['name'])
        return self.client.create_repository_branche(self._get_bitbucket_repro_path(), data)['name']
