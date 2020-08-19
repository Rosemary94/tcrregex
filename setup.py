from setuptools import setup, find_packages
PACKAGES = find_packages()

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

opts = dict(name='tcrregex',
            maintainer='Koshlan Mayer-Blackwell',
            maintainer_email='kmayerbl@fredhutch.org',
            description='Regex style motif search for epitope specific TCRs ',
            long_description=long_description,
            long_description_content_type='text/markdown',
            url='https://github.com/kmayerb/tcrregex',
            license='MIT',
            author='Koshlan Mayer-Blackwell',
            author_email='kmayerbl@fredhutch.org',
            version='0.0.1',
            packages=PACKAGES,
            package_data={"": ["*.csv","*.tsv","*.txt","*.fasta"]})

install_reqs = [
      'pandas>=0.24.2',
      'numpy>=1.16.4',
      'parasail>=1.1.17',
      'scipy>=1.4.1',
      'pwseqdist>=0.2.1',
      'numba',
      'zipdist>=0.1.5',
      'fishersapi',
      'hierdiff>=0.4',
      'palmotif>=0.2',
      'tcrsampler>=0.1.7',
      'parmap>=1.5.2',
      'olga>=1.2.1']

if __name__ == "__main__":
      setup(**opts, install_requires=install_reqs)