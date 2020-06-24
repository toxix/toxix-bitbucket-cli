# toxix-bitbucket-cli
Toxix Bitbucket Cli

This Softweare is currently in alpha status expect errors and unitendend behavior or braking changes.

## Installation

Clone this repository and run an

```
pip3 install -e .
```

This should let you run an

```
toxix-bitbucket-cli -h
```

On your console. You can use the in programm help to continue. Recomended to start with an 
`toxix-bitbucket-cli config`
that will help you to set some basic settings like bitbucket usernames and passwords.

## Tasks you can do

This is ment to be running from a cloned copy of the remote repository. The url/project will be guessed from
the remote/origin of git in the current directory.

## Pullrequests

#### Create pr to specific branch

```
toxix-bitbucket-cli pr dev
```

#### Create pr to story branch

```
toxix-bitbucket-cli pr story
```

If you are on `MW-893_MW-1086_fix-preview-for-quick-order` branch:
This will automaticaly check if there is an story branch (having the format 
`MW-893_some-branch-name`) existing on bitbucket. If it exists it will open the
Pullrequest to this branch. Otherwise a story branch will be created and a name chunk
will be asked.

