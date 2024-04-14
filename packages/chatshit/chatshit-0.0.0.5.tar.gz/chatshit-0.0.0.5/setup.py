# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatshit', 'chatshit.network', 'chatshit.screens', 'chatshit.widgets']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.54.0,<0.55.0']

entry_points = \
{'console_scripts': ['chatshit = chatshit.__main__:main']}

setup_kwargs = {
    'name': 'chatshit',
    'version': '0.0.0.5',
    'description': 'Worst chatroom ever',
    'long_description': '# WORST CHATROOM EVER\n',
    'author': 'mark bragin',
    'author_email': 'm4rk.brag1n@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
