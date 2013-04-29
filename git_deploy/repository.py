# -*- coding: utf-8 -*-


import logging
import os
import subprocess

import git


log = logging.getLogger(os.path.basename(__file__))


def get_repo():
    try:
        return git.Repo(os.getcwd())
    except git.InvalidGitRepositoryError:
        return None


def get_repo_url(repo, origin_remote_name):
    return repo.remotes[origin_remote_name].config_reader.config.get('remote "{}"'.format(origin_remote_name), 'url')


def pull(host_conf, host_name, dry_run=False):
    command_args = ['ssh']
    if host_conf['user']:
        command_args.extend(['-l', host_conf['user']])
    command_args.extend([host_name, 'cd {}; git pull'.format(host_conf['path'])])
    log.info(u'= command: {}'.format(u' '.join(command_args)))
    if not dry_run:
        return_code = subprocess.call(command_args)
        if return_code != 0:
            log.error(u'Error running command, exit.')
            return return_code
    return 0


def push(remotes=None, dry_run=False):
    if remotes is None:
        remotes = ['origin']
    for remote in remotes:
        log.info(u'== push to remote "{}"'.format(remote))
        command_args = ['git', 'push', remote]
        log.info(u'= command: {}'.format(u' '.join(command_args)))
        if not dry_run:
            return_code = subprocess.call(command_args)
            if return_code != 0:
                log.error(u'Error running command, exit.')
                return return_code
    return 0
