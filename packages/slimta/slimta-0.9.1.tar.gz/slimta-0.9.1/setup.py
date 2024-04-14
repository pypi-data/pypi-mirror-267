# Copyright (c) 2021 Ian C. Good
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from setuptools import setup, find_namespace_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(name='slimta',
      version='0.9.1',
      author='Ian Good',
      author_email='ian@icgood.net',
      description='Configurable MTA based on the python-slimta library.',
      long_description=readme + license,
      long_description_content_type='text/markdown',
      license='MIT',
      url='http://slimta.org/',
      python_requires='~=3.11',
      include_package_data=True,
      packages=find_namespace_packages(include=['slimta.*']),
      install_requires=[
          'python-slimta[spf] ~= 5.0',
          'pysasl < 1.1',
          'passlib',
          'PyYAML'],
      extras_require={
          'optional': ['python-slimta[redis,aws,disk] ~= 5.0']},
      entry_points={'console_scripts': [
              'slimta = slimta.app.main:main',
              'slimta-setup = slimta.app.setup:setup']},
      classifiers=['Development Status :: 3 - Alpha',
                   'Topic :: Communications :: Email :: Mail Transport Agents',
                   'Intended Audience :: Information Technology',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python'])


# vim:et:fdm=marker:sts=4:sw=4:ts=4
