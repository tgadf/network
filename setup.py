from distutils.core import setup
import setuptools

setup(
  name = 'network',
  py_modules = ['network', 'networkTimeUtils', 'networkTrips', 'networkTripUtils', 'networkCategories'],
  version = '0.0.1',
  description = 'A Python Wrapper For Network Tool',
  long_description = open('README.md').read(),
  author = 'Thomas Gadfort',
  author_email = 'tgadfort@gmail.com',
  license = "MIT",
  url = 'https://github.com/tgadf/network',
  keywords = ['geohash', 'location', 'network'],
  classifiers = [
    'Development Status :: 3',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ],
  install_requires=['utils==0.0.1', 'geocluster==0.0.1', 'networkX', 'haversine', 'pandas', 'numpy'],
  dependency_links=['git+ssh://git@github.com/tgadf/utils.git#egg=utils-0.0.1', 'git+ssh://git@github.com/tgadf/geocluster.git#egg=geocluster-0.0.1']
)
 
