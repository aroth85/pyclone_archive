from distutils.core import setup

description = '''Easy Python Plotting Library. A library to wrap matplotlib and make generation of standard plots
easier.'''

setup(
      name='eppl',
      version='0.2.0',
      description=description,
      author='Andrew Roth',
      author_email='andrewjlroth@gmail.com',
      url='https://bitbucket.org/aroth85/eppl',
      package_dir = {'eppl': 'lib/eppl'},    
      packages=[ 
                'eppl'
                ],
      package_data={'eppl': ['data/genome/*.tsv']},
     )
