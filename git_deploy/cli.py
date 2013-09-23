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


import argparse
import logging
import os

import xdg.BaseDirectory

from . import commands


def main():
    default_config_dir_path = os.path.join(xdg.BaseDirectory.xdg_config_home, 'git-deploy')
    parser = argparse.ArgumentParser(description=u'Deploy git repositories to multiple targets.')
    parser.add_argument('--config-dir', default=default_config_dir_path, help=u'Path of the config file')
    parser.add_argument('--origin-remote-name', default='origin', help=u'Name of the main remote repository')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help=u'Display info messages')
    parser.add_argument('sub_args', nargs='+')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, help=u'Do not execute actions')
    args = parser.parse_args()
    args.config_dir = os.path.abspath(os.path.expanduser(args.config_dir))
    logging.basicConfig(
        format=u'%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s:%(funcName)s line %(lineno)d] %(message)s'
        if args.verbose else '%(message)s',
        level=logging.DEBUG if args.verbose else logging.INFO,
        )
    return commands.run_command(args)
