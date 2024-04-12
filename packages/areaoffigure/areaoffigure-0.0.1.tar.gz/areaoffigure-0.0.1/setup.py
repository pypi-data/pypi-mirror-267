from setuptools import setup, find_packages


def readme():
  with open('C:/Users/kiril/.vscode/ProjectTemplates/AreaOfFiagure/README.md', encoding='utf-8') as f:
    return f.read()


setup(
  name='areaoffigure',
  version='0.0.1',
  author='Skkiba',
  author_email='kirilld1122@gmail.com',
  description='This is the module for finding area of figures',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Varakin-Kirill/AreaOfFigure',
  packages=find_packages(),
  install_requires=[''],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='area figures ',
  project_urls={
    'GitHub': 'https://github.com/Varakin-Kirill'
  },
  python_requires='>=3.6'
)