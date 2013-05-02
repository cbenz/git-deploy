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


import unittest

from git_deploy import configuration


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.project_1_repo_url = 'git@git.my.domain:project_1.git'
        self.project_1_conf = {
            'hosts': {
                'amy': {
                    'hooks': {'after': ['reload_apache']},
                    'path': 'deps/project_1',
                    'user': 'user_1'
                    },
                'howard': {
                    'hooks': {'after': ['reload_apache']},
                    'path': 'application',
                    'user': 'user_2'
                    },
                'leslie': {
                    'hooks': {'after': ['reload_apache']},
                    'path': 'deps/project_1',
                    'user': 'user_1'
                    }
                },
            'targets': {
                'preprod': {'leslie': 'origin'},
                'prod': {'amy': 'amy', 'howard': 'origin'}
                },
            'url': self.project_1_repo_url
            }
        self.conf_dicts = [
            {
                'hooks': {
                    'reload_apache': {
                        'command': 'service apache2 force-reload',
                        'user': 'root'
                        }
                    }
                },
            {
                'hooks': {
                    'reload_apache_aspremont': {
                        'command': 'sudo service apache2 force-reload',
                        'user': 'cbenz'
                        }
                    }
                },
            {
                'repositories': {
                    'project_1': self.project_1_conf,
                    },
                },
            {
                'repositories': {
                    'project_2': {
                        'hosts': {
                            'howard': {
                                'hooks': {'after': ['reload_apache']},
                                'path': 'vhost',
                                'user': 'user_1'
                                }
                            },
                        'targets': {
                            'prod': {'amy': 'amy', 'howard': 'origin'}
                            },
                        'url': 'git@git.my.domain:vhosts/project_1.my.domain.git'
                        },
                    },
                },
            ]
        self.conf = configuration.merge_conf_dicts(self.conf_dicts)

    def test_get_repo_alias_and_conf(self):
        repo_alias, repo_conf = configuration.get_repo_alias_and_conf(self.conf, self.project_1_repo_url)
        self.assertEqual(repo_alias, 'project_1')
        self.assertEqual(repo_conf, self.project_1_conf)

    def test_merge_conf_dicts(self):
        self.assertIn('hooks', self.conf)
        self.assertIn('reload_apache', self.conf['hooks'])
        self.assertIn('reload_apache_aspremont', self.conf['hooks'])
        self.assertIn('repositories', self.conf)
        self.assertIn('project_1', self.conf['repositories'])
        self.assertIn('project_2', self.conf['repositories'])


if __name__ == '__main__':
    unittest.main()
