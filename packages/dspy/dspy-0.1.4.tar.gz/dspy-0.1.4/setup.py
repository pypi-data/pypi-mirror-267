# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dspy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ka = kiera.main:main', 'kiera = kiera.main:main']}

setup_kwargs = {
    'name': 'dspy',
    'version': '0.1.4',
    'description': 'Placeholder package for DSPy',
    'long_description': '',
    'author': 'Tom Dörr',
    'author_email': 'tomdoerr96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
