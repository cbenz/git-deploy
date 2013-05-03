git-deploy
==========

Deploy git repositories to multiple targets.

The "deploy" command is an overlay built on top of git push and pull commands.
Its main goal is to ease the deployment of a repository on multiple servers, pushing to multiple remotes and pulling
remotely from multiple servers (via SSH).

Also it provides hooks executed before and after pull (for ex. to reload Apache).


Philosophy
----------

TODO


Usage
-----

After configuring your git repositories, you'll be able to use the following sub-commands from a git repository:
targets, pull, push, sync. The workflow is pretty basic: you push then you pull from/to a target.
You can also use the 'sync' command to chain a push then a pull.

targets: get info about the current repository

    $ git deploy targets
    Targets: <all>, prod, preprod (repository "my-repositoy")

push:

    $ git deploy push all

pull:

    $ git deploy pull all

sync:

    $ git deploy sync all


Installation
------------

Register python egg to the user or the system, with or without egg dependencies.
This is convinient if you use a GNU/Linux distribution that ships Python packages.

    $ python setup.py develop [--user] [--no-deps]

For instance with Debian GNU/Linux (waiting for a real .deb):

    $ python setup.py develop --user --no-deps
    $ su -
    # aptitude install python-git python-xdg

Biryani may be installed from sourcesm from the "biryani1" branch.
URL: https://pypi.python.org/pypi/Biryani

Then install the script to your "bin" directory:

    $ ln -s $PWD/scripts/git-deploy ~/.local/bin


Configuration
-------------

You may want to start from sample configuration files:

    $ mkdir ~/.config/git-deploy
    $ cp sample-conf/* ~/.config/git-deploy

Then adapt ~/.config/git-deploy/repositories.json to your projects.

You can create as many files as you want since the configuration is merged from all JSON files.
