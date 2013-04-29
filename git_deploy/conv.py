# -*- coding: utf-8 -*-


import logging
import os

from biryani1.baseconv import empty_to_none, not_none, pipe, test_in, struct, uniform_mapping, uniform_sequence


log = logging.getLogger(os.path.basename(__file__))


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
