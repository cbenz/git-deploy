# -*- coding: utf-8 -*-


import glob
import json
import logging
import os

from . import conv


log = logging.getLogger(os.path.basename(__file__))


def get_conf(config_dir_path):
    if not os.path.isdir(config_dir_path):
        return None
    conf = {}
    for config_file_path in glob.iglob(os.path.join(config_dir_path, '*.json')):
        log.debug(u'get_conf: config_file_path = {}'.format(config_file_path))
        with open(config_file_path) as config_file:
            config_file_str = config_file.read()
        try:
            config_file_json = json.loads(config_file_str)
        except ValueError, exc:
            log.error(u'Failed to decode repository JSON configuration for file "{}": {}'.format(
                config_file_path, unicode(exc)))
            return None
        config_file_conf, errors = conv.json_values_to_conf(config_file_json)
        if errors is None:
            conf.update(config_file_conf)
            log.debug(u'get_conf: updated conf = {}'.format(conf))
        else:
            log.error(u'Repository configuration errors for file "{}": {}'.format(config_file_path, errors))
            return None
    log.debug(u'get_conf: final conf = {}'.format(conf))
    return conf


def get_repo_conf(conf, repo_url):
    if conf['repositories']:
        for repo_alias, repo_conf in conf['repositories'].iteritems():
            if repo_conf['url'] == repo_url:
                log.debug(u'get_repo_conf: repo_alias = {}, repo_conf = {}'.format(repo_alias, repo_conf))
                return repo_alias, repo_conf
    return None, None
