# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neo_sapiens']

package_data = \
{'': ['*']}

install_requires = \
['pydantic', 'swarms']

setup_kwargs = {
    'name': 'neo-sapiens',
    'version': '0.0.5',
    'description': 'Neo Sapiens - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Neo Sapiens\n\n\n## install\n`$ pip install -U swarms neo-sapiens`\n\n\n## usage\n```python\nfrom neo_sapiens import run_swarm\n\n# Run the swarm\nout = run_swarm("Create a self-driving car system using a team of AI agents")\nprint(out)\n```\n\n# Todo\n- [ ] Add tool processing\n\n- [ ] Add tool router\n\n- [ ] Add rules processing to map to each agent\n\n- [ ] Prompt for swarm orchestrator to make the children workers in JSON\n\n- [ ] Prompt to create functions with a tool decorator above the function with specific types and documentation. Create a tool for this: {input}, and create the functions in python with a tool decorator on top of the function with specific types and documentation with docstrings\n\n- [ ] Logic to add each agent to a swarm network\n\n- [ ] Add memory to boss agent using Chromadb\n\n- [ ] Add agents as tools after the boss creates them\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/NeoSapiens',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
