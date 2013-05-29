# -*- coding: utf-8 -*-


# GitDeploy -- Deploy git repositories to multiple targets.
# By: Christophe Benz <cbenz@easter-eggs.com>
#
# Copyright (C) 2013 Christophe Benz, Easter-eggs
# https://github.com/cbenz/git-deploy
#
# This file is part of GitDeploy.
#
# GitDeploy is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# GitDeploy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import subprocess

import git


log = logging.getLogger(__name__)


def get_repo():
    try:
        return git.Repo(os.getcwd())
    except git.InvalidGitRepositoryError:
        return None


def get_repo_url(repo, origin_remote_name):
    return repo.remotes[origin_remote_name].config_reader.config.get('remote "{}"'.format(origin_remote_name), 'url')


def pull(host_name, repo_conf, dry_run=False):
    host_conf = repo_conf['hosts'][host_name]
    command_args = ['ssh']
    if host_conf['user']:
        command_args.extend(['-l', host_conf['user']])
    pull_command = repo_conf['commands']['pull'] if repo_conf['commands'] and repo_conf['commands'].get('pull') \
        else u'git pull'
    command_args.extend([host_name, 'cd {}; {}'.format(host_conf['path'], pull_command)])
    log.info(u'= command: {}'.format(u' '.join(command_args)))
    if not dry_run:
        subprocess.call(command_args)
    return 0


def push(remotes=None, dry_run=False):
    if remotes is None:
        remotes = ['origin']
    for remote in remotes:
        log.info(u'== push to remote "{}"'.format(remote))
        command_args = ['git', 'push', remote]
        log.info(u'= command: {}'.format(u' '.join(command_args)))
        if not dry_run:
            subprocess.call(command_args)
    return 0
