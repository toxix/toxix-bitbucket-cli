#!/usr/bin/python3

# This is to automate some bitbucket tasks like create a pull request to the story branch

from .BitbucketRestClientExceptions import NotAuthenticatedError
import sys, argparse, textwrap
from configobj import ConfigObjError
import stdiomask
from pathlib import Path
from .Client import Client
from .ToxixConfigObj import ToxixConfigObj
from .ToxixBB import ToxixBB

# todo make use of arparse complete to enable tab completion of params
#https://kylebebak.github.io/post/enabling-tab-completion

class ToxixBitbucketCli:
    # source for multilevel argphrase https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
    def __init__(self):
        self._load_config()
        
        parser = argparse.ArgumentParser(description='This helps you interacting with Bitbucket from the command-line and be more efficient.')
        parser.add_argument('action', metavar='action',  choices=self._get_allowed_actions(),  help='What should we do?')
        parser.add_argument('--version',action='version', version='%(prog)s 0.1')
        
        args = parser.parse_args(sys.argv[1:2])
        
        try:
            self.toxixBB = ToxixBB(self.conf['bb_username'], self.conf.get_password('bb_password'))
        except(NotAuthenticatedError):
            if(args.action != 'config'):
                  print('No valid Bitbucket credentials. Please config application with "%s config"'%sys.argv[0])
                  exit(1)
        
        if not hasattr(self, args.action):
            print('Unrecognized action')
            parser.print_help()
            exit(1)
        getattr(self, args.action)()
        
    def pr(self):
        self.pull_request()
    
    def pull_request(self):
        parser = argparse.ArgumentParser(
            description=textwrap.dedent('''\
            Create a pullrequest on Bitbucket from the current branch.\n
            If "story" is used as target-branch it will create or find story branch based on jira ticket number that is phrased from the branch name.
            '''), 
            formatter_class=argparse.RawTextHelpFormatter
            )
        parser.add_argument('target_branch', metavar='target-branch',  help='Branch name used for action.',  default='story')
        args = parser.parse_args(sys.argv[2:])
        self.toxixBB.create_pullrequest(args.target_branch)
        
    def config(self):
        print('This tests and saves your credentials in your keyring, for later use with this application.\n')
        username = input('Enter your Bitbucket user name (This is not your email! You can get it from "personal settings" -> "account settings"): ')
        password =(stdiomask.getpass (prompt='Bitbucket App password (You can get/generate it in "personal settings" -> "app passwords"): '))
        # check config
        try:
            Client(username, password).get_user()
        except(NotAuthenticatedError):
            print('Your provided configuration is not valid, it will not be stored.')
            exit(1)
        # store the config
        self.conf['bb_username'] = username
        self.conf.set_password('bb_password',  password)
        self.conf.write()
        
    def _load_config(self):
        configpath = Path().home() /  '.config/toxix-bitbucket'
        configfile = configpath / 'config'
        try:
            # create directory if not exist
            configpath.mkdir(parents=True, exist_ok=True)
            # load the config
            self.conf = ToxixConfigObj(str(configfile), create_empty=True,  file_error=True)
        except (ConfigObjError, IOError) as e:
            print('Could not read "%s": %s' % (configfile, e))
            exit(1)
        
    def _get_allowed_actions(self):
        # return all public methods of this class
        return [ m for m in dir(ToxixBitbucketCli) if not m.startswith('_') ]
        
def main():
    ToxixBitbucketCli()
