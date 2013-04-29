git-deploy
==========

Deploy git repositories to multiple targets.

The "deploy" command is an overlay built on top of git push and pull commands.
Its main goal is to ease the deployment of a repository on multiple servers, pushing to multiple remotes and pulling
remotely from multiple servers (via SSH).

Also it provides hooks executed before and after pull (for ex. to reload Apache).


Installation
------------

For example:

    $ python setup.py develop --no-deps --user
    $ ln -s $PWD/scripts/git-deploy ~/.local/bin
