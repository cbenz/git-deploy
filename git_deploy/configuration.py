# -*- coding: utf-8 -*-


import json
import logging
import os

from . import conv


log = logging.getLogger(os.path.basename(__file__))


def get_conf(config_file_path):
    if not os.path.isfile(config_file_path):
        return None
    with open(config_file_path) as config_file:
        config_str = config_file.read()
    json_conf = json.loads(config_str)
    conf, errors = conv.json_values_to_conf(json_conf)
    if errors is not None:
        log.error(u'Repository configuration errors: {}'.format(errors))
        return None
    return conf


def get_repo_conf(conf, repo_url):
    if conf['repositories']:
        for repo_alias, repo_conf in conf['repositories'].iteritems():
            if repo_conf['url'] == repo_url:
                return repo_alias, repo_conf
    return None, None
