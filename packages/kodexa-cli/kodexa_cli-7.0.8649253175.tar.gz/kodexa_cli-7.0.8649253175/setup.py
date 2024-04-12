# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kodexa_cli']

package_data = \
{'': ['*'],
 'kodexa_cli': ['charts/extension-pack/*',
                'charts/extension-pack/resources/*',
                'charts/extension-pack/templates/*',
                'charts/resource-container/*',
                'charts/resource-pack/*',
                'charts/resource-pack/templates/*',
                'templates/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.7,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'kodexa>=7.0.0,<8.0.0',
 'rich>=13.7.0,<14.0.0',
 'wrapt>=1.15.0,<2.0.0']

entry_points = \
{'console_scripts': ['kodexa = kodexa_cli.cli:safe_entry_point']}

setup_kwargs = {
    'name': 'kodexa-cli',
    'version': '7.0.8649253175',
    'description': 'Command Line Tools for Kodexa',
    'long_description': '# Kodexa Command Line Tools\n\n[![Kodexa CLI Python Package](https://github.com/kodexa-ai/kodexa-cli/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/kodexa-ai/kodexa-cli/actions/workflows/build-and-release.yml)\n\n![img.png](https://docs.kodexa.com/img.png)\n\nKodexa is a platform for building intelligent document processing pipelines. It is a set of tools and services that\nallow you to build a pipeline that can take a document, extract the content, and then process it to extract the\ninformation you need.\n\nIt is built on a set of core principles:\n\n* **Document Centric** - Kodexa is built around the idea of a document. A document is a collection of content\n  nodes that are connected together. This is a powerful model that allows you to build pipelines that can\n  extract content from a wide range of sources.\n\n* **Pipeline Oriented** - Kodexa is built around the idea of a pipeline. A pipeline is a series of steps that\n  can be executed on a document. This allows you to build a pipeline that can extract content from a wide range\n  of sources.\n\n* **Extensible** - Kodexa is built around the idea of a pipeline. A pipeline is a series of steps that can be executed\n  on a document. This allows you to build a pipeline that can extract content from a wide range of sources.\n\n* **Label Driven** - Kodexa focuses on the idea of labels. Labels are a way to identify content within a document\n  and then use that content to drive the processing of the document.\n\n# Command Line Tools\n\nThis repository contains the command line tools for Kodexa. The tools are the primary way to interact with Kodexa. It\nallows you to configure components and manage aspects of your Kodexa Platform installation.\n\n## Documentation & Examples\n\nDocumentation is available at the [Kodexa Documentation Portal](https://docs.kodexa.com)\n\n## Set-up\n\nWe use poetry to manage our dependencies, so you can install them with:\n\n    poetry install\n\nYou can then run the tests with:\n\n    poetry run pytest\n\n# Contributing\n\nWe welcome contributions to the Kodexa platform. Please see our [contributing guide](CONTRIBUTING.md) for more details.\n\n# License\n\nApache 2.0\n',
    'author': 'Austin Redenbaugh',
    'author_email': 'austin@kodexa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
