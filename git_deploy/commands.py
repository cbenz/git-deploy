# -*- coding: utf-8 -*-


import logging
import os
import subprocess

from . import configuration, conv, repository


log = logging.getLogger(os.path.basename(__file__))


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
    repo_alias, repo_conf = configuration.get_repo_conf(conf, repo_url)
    if not repo_conf:
        log.error(u'No configuration found for this repository.')
        return 1
    command_kwargs = {
        'args': args,
        'conf': conf,
        'repo_alias': repo_alias,
        'repo_conf': repo_conf,
        'repo_url': repo_url,
        }
    if args.command == 'pull':
        return run_pull_command(**command_kwargs)
    elif args.command == 'push':
        return run_push_command(**command_kwargs)
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


def run_pull_command(args, conf, repo_alias, repo_conf, repo_url):
    if args.dry_run:
        log.info(u'Dry-run mode!')
    targets_conf, errors = conv.make_inputs_to_targets_conf(repo_conf=repo_conf)(args.targets)
    if errors is not None:
        log.error(u', '.join(u'{}: {}' for target_name, error in errors.iteritems))
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
            log.error(u'Host "{}" not globally-configured (repository "{}").'.format(host_name, repo_alias))
            return 1
        # before hooks
        if host_conf['hooks']['before']:
            return_code = run_hooks(dry_run=args.dry_run, hooks=host_conf['hooks']['before'], hooks_conf=conf['hooks'],
                host_name=host_name)
            if return_code != 0:
                log.error(u'Error running command, exit.')
                return return_code
        # pull command
        return_code = repository.pull(dry_run=args.dry_run, host_conf=host_conf, host_name=host_name)
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


def run_push_command(args, conf, repo_alias, repo_conf, repo_url):
    if args.dry_run:
        log.info(u'Dry-run mode!')
    targets_conf, errors = conv.make_inputs_to_targets_conf(repo_conf=repo_conf)(args.targets)
    if errors is not None:
        log.error(u', '.join(u'{}: {}' for target_name, error in errors.iteritems))
        return 1
    remotes = []
    for target_name, target_conf in targets_conf.iteritems():
        if not target_conf:
            log.error(u'Target "{}" is not configured (repository "{}").'.format(target_name, repo_alias))
            return 1
        remotes.extend(target_conf.values())
    remotes = sorted(set(remotes))
    return repository.push(dry_run=args.dry_run, remotes=remotes)


def run_targets_command(args, conf, repo_alias, repo_conf, repo_url):
    targets = repo_conf.get('targets')
    if not targets:
        log.error(u'Targets are not configured (repository "{}").'.format(repo_alias))
        return 1
    log.info(u'Targets: <all>, {} (repository "{}")'.format(u', '.join(targets.keys()), repo_alias))
    return 0
