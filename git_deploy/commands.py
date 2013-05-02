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
import subprocess

from . import configuration, repository


log = logging.getLogger(__name__)


def run_command(args):
    log.debug(u'run_command: args = {}'.format(args))
    repo = repository.get_repo()
    if repo is None:
        log.error(u'Not a git repository (sub-)directory.')
        return 1
    repo_url = repository.get_repo_url(repo=repo, origin_remote_name=args.origin_remote_name)
    if not repo_url:
        log.error(u'Remote "{}" not found in .git/config for this repository.'.format(args.origin_remote_name))
        return 1
    conf = configuration.get_conf(config_dir_path=args.config_dir)
    if not conf:
        log.error(u'Could not load configuration from directory "{}".'.format(args.config_dir))
        return 1
    repo_alias, repo_conf = configuration.get_repo_alias_and_conf(conf, repo_url)
    if not repo_conf:
        log.error(u'This repository is not managed by git-deploy. '
            'Hint: add its configuration to a JSON file in {}'.format(args.config_dir))
        return 1
    command_kwargs = {
        'args': args,
        'conf': conf,
        'repo': repo,
        'repo_alias': repo_alias,
        'repo_conf': repo_conf,
        'repo_url': repo_url,
        }
    if args.command == 'pull':
        return run_pull_command(**command_kwargs)
    elif args.command == 'push':
        return run_push_command(**command_kwargs)
    elif args.command == 'sync':
        return_code = run_push_command(**command_kwargs)
        if return_code != 0:
            return return_code
        return run_pull_command(**command_kwargs)
    elif args.command == 'targets':
        return run_targets_command(**command_kwargs)
    assert False, u'Should never reach this line.'


def run_hooks(dry_run, hooks, hooks_conf, host_name):
    for hook_name in hooks:
        hook_conf = hooks_conf[hook_name]
        command_args = ['ssh', host_name]
        if hook_conf['user']:
            command_args.extend(['-l', hook_conf['user']])
        command_args.append(hook_conf['command'])
        log.info(u'= command ("after" hook): {}'.format(u' '.join(command_args)))
        if not dry_run:
            return_code = subprocess.call(command_args)
            if return_code != 0:
                return return_code
    return 0


def run_pull_command(args, conf, repo, repo_alias, repo_conf, repo_url):
    if args.dry_run:
        log.info(u'Dry-run mode!')
    if any(target_name not in repo_conf['targets'] for target_name in args.targets if target_name != 'all'):
        log.error(u'Invalid target name (repository targets: {})'.format(u', '.join(repo_conf['targets'].keys())))
        return 1
    targets_conf = repo_conf['targets'] if 'all' in args.targets else \
        {target_name: repo_conf['targets'][target_name] for target_name in args.targets}
    if not targets_conf:
        log.error(u'No targets configured (repository "{}")'.format(repo_alias))
        return 1
    targets_host_names = []
    for target_name, target_conf in targets_conf.iteritems():
        if not target_conf:
            log.error(u'Target "{}" is not configured (repository "{}").'.format(target_name, repo_alias))
            return 1
        targets_host_names.extend(target_conf.keys())
    targets_host_names = sorted(set(targets_host_names))
    for host_name in targets_host_names:
        log.info(u'== pull from host "{}"'.format(host_name))
        host_conf = repo_conf['hosts'].get(host_name)
        if not host_conf:
            log.error(u'Host "{}" not configured (repository "{}").'.format(host_name, repo_alias))
            return 1
        # before hooks
        if host_conf['hooks']['before']:
            return_code = run_hooks(dry_run=args.dry_run, hooks=host_conf['hooks']['before'], hooks_conf=conf['hooks'],
                host_name=host_name)
            if return_code != 0:
                log.error(u'Error running command, exit.')
                return return_code
        # pull command
        return_code = repository.pull(dry_run=args.dry_run, host_name=host_name, repo_conf=repo_conf)
        if return_code != 0:
            log.error(u'Error running command, exit.')
            return return_code
        # after hooks
        if host_conf['hooks']['after']:
            return_code = run_hooks(dry_run=args.dry_run, hooks=host_conf['hooks']['after'], hooks_conf=conf['hooks'],
                host_name=host_name)
            if return_code != 0:
                log.error(u'Error running command, exit.')
                return return_code
    return 0


def run_push_command(args, conf, repo, repo_alias, repo_conf, repo_url):
    if args.dry_run:
        log.info(u'Dry-run mode!')
    if any(target_name not in repo_conf['targets'] for target_name in args.targets if target_name != 'all'):
        log.error(u'Invalid target name (repository targets: {})'.format(u', '.join(repo_conf['targets'].keys())))
        return 1
    if 'all' in args.targets:
        remotes = [remote.name for remote in repo.remotes]
    else:
        # Build remotes from repo targets.
        targets_conf = {target_name: repo_conf['targets'][target_name] for target_name in args.targets}
        if not targets_conf:
            log.error(u'No targets configured (repository "{}")'.format(repo_alias))
            return 1
        remotes = []
        for target_name, target_conf in targets_conf.iteritems():
            if not target_conf:
                log.error(u'Target "{}" is not configured (repository "{}").'.format(target_name, repo_alias))
                return 1
            remotes.extend(target_conf.values())
        remotes = sorted(set(remotes))
    return repository.push(dry_run=args.dry_run, remotes=remotes)


def run_targets_command(args, conf, repo, repo_alias, repo_conf, repo_url):
    targets = repo_conf.get('targets')
    if not targets:
        log.error(u'Targets are not configured (repository "{}").'.format(repo_alias))
        return 1
    log.info(u'Targets: <all>, {} (repository "{}")'.format(u', '.join(targets.keys()), repo_alias))
    return 0
