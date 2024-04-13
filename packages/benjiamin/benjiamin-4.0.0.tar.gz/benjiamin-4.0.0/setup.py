from setuptools import setup, find_packages
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
  name='benjiamin',
  version='4.0.0',
  author='Your Name',
  author_email='your.email@example.com',
  description='A short description of your package',
  packages=find_packages(),
  install_requires=install_requires,
  classifiers=[
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent',
],
python_requires='>=3.6',
)

