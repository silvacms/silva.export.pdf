# -*- coding: utf-8 -*-
# Copyright (c) 2002-2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from setuptools import setup, find_packages
import os

version = '1.0dev'

tests_require = [
    'Products.Silva [test]',
    ]

setup(name='silva.export.pdf',
      version=version,
      description="Export Silva content to PDF",
      long_description=open("README.txt").read() + "\n" + open(
          os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Zope2",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='silva export pdf',
      author='Infrae',
      author_email='info@infrae.com',
      url='https://github.com/silvacms/silva.export.pdf',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['silva', 'silva.export'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Zope2',
          'five.grok',
          'silva.core.interfaces',
          'silva.export.html',
          'xhtml2pdf'
      ],
      tests_require=tests_require,
      extras_require={'test': tests_require},
      )
