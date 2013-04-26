#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""git-deploy: deploy git repository changes to targets."""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Christophe Benz',
    author_email=u'cbenz@easter-eggs.com',
    description=doc_lines[0],
    include_package_data=True,
    install_requires=[
        'Biryani1 >= 0.9dev',
        'dulwich >= 0.8.5',
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
