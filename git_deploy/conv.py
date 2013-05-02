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

from biryani1.baseconv import empty_to_none, not_none, pipe, test_in, struct, uniform_mapping, uniform_sequence


log = logging.getLogger(__name__)


# Level 1 converters.

json_values_to_repository_conf = struct(
    {
        'commands': struct(
            {
                'pull': empty_to_none,
                },
            drop_none_values=False,
            ),
        'hosts': uniform_mapping(
            pipe(empty_to_none, not_none),
            struct(
                {
                    'hooks': pipe(
                        struct(
                            {
                                'after': empty_to_none,
                                'before': empty_to_none,
                                },
                            drop_none_values=False,
                        ),
                        uniform_mapping(
                            pipe(test_in(['after', 'before']), not_none),
                            uniform_sequence(
                                # TODO Check value is in declared hooks.
                                pipe(empty_to_none, not_none),
                                ),
                            ),
                        ),
                    'path': empty_to_none,
                    'user': empty_to_none,
                    },
                drop_none_values=False,
                ),
            ),
        'targets': uniform_mapping(
            pipe(empty_to_none, not_none),
            uniform_mapping(
                # TODO Check value is in declared hosts.
                pipe(empty_to_none, not_none),
                # TODO Check value is in repository remotes.
                pipe(empty_to_none, not_none),
                ),
            ),
        'url': pipe(empty_to_none, not_none),
        },
    drop_none_values=False,
    )


# Level 2 converters.

json_values_to_conf = struct(
    {
        'hooks': uniform_mapping(
            pipe(empty_to_none, not_none),
            struct(
                {
                    'command': pipe(empty_to_none, not_none),
                    'user': empty_to_none,
                    },
                drop_none_values=False,
                )
            ),
        'repositories': uniform_mapping(
            pipe(empty_to_none, not_none),
            json_values_to_repository_conf,
            ),
        },
    drop_none_values=True,
    )
