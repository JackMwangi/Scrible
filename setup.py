from setuptools import setup

setup(name='scrible',
      version='1.0',
      description='Note taking application',
      url='https://github.com/jaxtreme01/Scrible',
      author='Jack Mwangi',
      author_email='jackmwa94@gmail.com',
      license='MIT',
      entry_points={
          'console_scripts': ['scrible = scrible.notes.scrible:main'],
      },
      packages=['scrible','scrible/notes','scrible/sync','scrible/tests'],
      install_requires=['docopt', 'clint', 'requests', 'python-firebase',
                        'colorama', 'termcolor', 'pyfiglet'],
      include_package_data=True,
      zip_safe=False)
