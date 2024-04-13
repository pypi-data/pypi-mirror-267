from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='cropwiseworker',
  version='0.0.2',
  author='Molev Arkhip',
  author_email='jobarkhip@gmail.com',
  description='Модуль реализует функции для работы с API цифровой платформы управления агропредприятием Cropwise Operations.',
  long_description=readme(),

  url='https://github.com/molevaa/cropwiseworker',
  download_url='https://github.com/molevaa/cropwiseworker/archive/refs/heads/main.zip',

  
  long_description_content_type='text/markdown',
  packages=['cropwiseworker'],
  install_requires=['requests','pandas'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
  keywords='cropwise',
  python_requires='>=3.7'
)
