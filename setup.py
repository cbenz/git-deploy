#!/usr/bin/env python
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


"""Deploy git repositories to multiple targets."""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Christophe Benz',
    author_email=u'cbenz@easter-eggs.com',
    description=doc_lines[0],
    entry_points={
        'console_scripts': 'git-deploy = git_deploy.cli:main',
        },
    include_package_data=True,
    install_requires=[
        'Biryani1 >= 0.9dev',
        'GitPython >= 0.3.2',
        'pyxdg >= 0.19',
        ],
    keywords='git deploy targets remotes ssh',
    license=u'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description='\n'.join(doc_lines[2:]),
    name=u'GitDeploy',
    packages=find_packages(),
#    url=u'http://',
    version='0.1',
    zip_safe=False,
    )
