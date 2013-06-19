from setuptools import setup, find_packages
import sys, os

version = '2.0b1'

setup(name='embeddify',
      version=version,
      description="converts URLs to embed codes",
      long_description="""This library converts links to youtube, slideshare etc. into their respective embed codes like wordpress does that. \
      So in case you are writing a blog platform you might use this to convert links on the fly without the user to bother with finding and copying the embed code.\
      Moreover it's far more secure if you don't allow the user to embed iframes themselves.\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='oembed embed youtube vimeo slideshare flickr',
      author='COM.lounge',
      author_email='info@comlounge.net',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "requests",
      ],
      )

