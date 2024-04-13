# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brave_torch']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'einops_exts', 'torch>=2.1.1,<3.0', 'zetascale']

setup_kwargs = {
    'name': 'brave-torch',
    'version': '4.7.9',
    'description': 'Swarms - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# BRAVE or Swarms of Vision Transformers\nImplementation of the paper: "BRAVE : Broadening the visual encoding of vision-language models". BRAVE achieves state-of-the-art performance on a broad range of captioning and VQA benchmarks and significantly reduces the aforementioned issues of VLMs, while requiring a smaller number of trainable parameters than existing methods and having a more compressed representation.\n\n## install\n`pip3 install brave-torch`\n\n\n## usage\n\n### \n```python\nimport torch\nfrom brave_torch.main import SwarmOfViTs\n\n# IMG Tensor\nx = torch.randn(1, 3, 224, 224) \n\n# Model\nmodel = SwarmOfViTs(\n    image_size=224,\n    patch_size=32,\n    encoder_dim=512,\n    encoder_depth=6,\n    encoder_heads=8,\n    num_of_vits=4\n)\n\n# Forward\nout = model(x)\nprint(out)\n```\n\n# Citations\n\n## Todo\n- [ ] Citation link\n- [ ] Citation Bibtex\n- [ ] Diagram photo\n- [ ] Implement Andromeda Base LLM architecture\n- [ ] Provide multi-modal tokenizer\n- [ ] Train and release the model ',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/BRAVE-ViT-Swarm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
