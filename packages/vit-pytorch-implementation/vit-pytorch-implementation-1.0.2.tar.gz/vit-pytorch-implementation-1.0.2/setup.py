from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'vit-pytorch-implementation',
  version = '1.0.2',
  license='MIT',
  description = 'Vision Transformer (ViT) - Pytorch',
  long_description=long_description,
  long_description_content_type = 'text/markdown',
  author = 'SM',
  url = 'https://github.com/soumya1729/vit-pytorch-implementation/',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'image recognition'
  ],
  install_requires=[
    'einops>=0.7.0',
    'torch>=1.10',
    'torchvision'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
