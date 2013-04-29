# -*- coding: utf-8 -*-


import logging
import os

from biryani1.baseconv import empty_to_none, not_none, pipe, test_in, struct, uniform_mapping, uniform_sequence


log = logging.getLogger(os.path.basename(__file__))


# Level 1 converters.

json_values_to_repository_conf = struct(
    {
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


def make_inputs_to_targets_conf(repo_conf):
    def inputs_to_targets_conf(values, state=None):
        u'''
        Ensure that target name given by user belongs to targets declared in repository configuration.
        Then resolves special target "all" to real target names.
        '''
        if values is None:
            return None, None
        if 'all' in values:
            return repo_conf['targets'], None
        else:
            errors = {}
            for target_name in values:
                if target_name not in repo_conf['targets']:
                    errors[target_name] = u'Invalid target name (repository targets: {})'.format(
                        u', '.join(repo_conf['targets'].keys()))
            if errors:
                return values, errors
            targets_conf = {target_name: repo_conf['targets'][target_name] for target_name in values}
            log.debug(u'str_to_targets_conf: targets_conf = {}'.format(targets_conf))
            return targets_conf
    return inputs_to_targets_conf


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
