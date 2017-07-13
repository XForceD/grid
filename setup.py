import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
CHANGES = open(os.path.join(here, "CHANGES.txt")).read()

requires = [
    "pyramid",
    "pyramid_beaker",
    "pyramid_debugtoolbar",
    "waitress",
	'velruse',
    'paste',
    'redis',
    'requests'
    ]

entry_points = """\
[paste.app_factory]
main = appgrid:main
"""

setup(name="appgrid",
      version="0.1",
      description="Grid backend app for GRID project.",
      long_description=README + "\n\n" +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Programming Language :: Python",
        "License :: OSI Approved : MIT License",
        ],
      author="Force",
      author_email="xforsaged@gmail.com",
      url="https://github.com/XForceD/grid",
      license="MIT",
      keywords="grid",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="appgrid",
      entry_points="""\
      [paste.app_factory]
      main = appgrid:main
      """,
      )

