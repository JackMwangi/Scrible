from setuptools import setup

setup(name='scrible',
      version='1.0',
      description='Note taking application',
      url='https://github.com/jaxtreme01/Scrible',
      author='Jack Mwangi',
      author_email='jackmwa94@gmail.com',
      license='MIT',
      entry_points = {
        'console_scripts': ['scrible = scrible.notes.scrible:main'],
      },
      packages=['scrible'],
       install_requires=['docopt','clint'
      ],
      include_package_data=True,
      zip_safe=False)