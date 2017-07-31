from setuptools import setup

version = '0.3.0'

setup(name='embeddify',
      version=version,
      description="converts URLs to embed codes",
      long_description=open('README.rst').read(),
      classifiers=['License :: OSI Approved :: BSD License', 
                   'Operating System :: OS Independent', 
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Text Processing :: Markup :: HTML',
                   'Topic :: Text Processing :: Filters',
                  ] + [
                   ("Programming Language :: Python :: %s" % x)
                   for x in "2.7 3.4 3.5 3.6".split()
                  ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='oembed embed html youtube vimeo slideshare flickr',
      packages = ['embeddify'],
      author='Christian Scholz, COM.lounge GmbH',
      author_email='mrtopf@gmail.com',
      url='https://github.com/mrtopf/embeddify',
      license='BSD',
      zip_safe=False,
      install_requires=[
        "requests",
      ],
      )

