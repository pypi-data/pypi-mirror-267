# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.runtime']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=7.0.4,<8.0.0',
 'mojo-collections>=1.3.0,<1.4.0',
 'mojo-config>=1.3.10,<1.4.0',
 'mojo-errors>=1.3.0,<1.4.0',
 'mojo-extension>=1.3.12,<1.4.0',
 'mojo-xmodules>=1.3.0,<1.4.0']

setup_kwargs = {
    'name': 'mojo-runtime',
    'version': '1.3.14',
    'description': 'Automation Mojo Runtime Module (mojo-runtime)',
    'long_description': '# Contextualize\nA package used to create a global context that allows for the distribution of options and configuration.\n',
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
