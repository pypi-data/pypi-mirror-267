# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import setuptools  # type: ignore


setuptools.setup(
    name='util_searchads360_hm',
    version='0.0.1',
    packages=setuptools.PEP420PackageFinder.find(),
    # namespace_packages=('google', 'google.ads'),
    platforms='Posix; MacOS X; Windows',
    author='Joe Fedorowicz',
    author_email='jfedorowicz@harmelin.com',
    include_package_data=True,
    install_requires=[
        "google-api-core[grpc] >= 1.28.0, < 3.0.0dev",
        "grpcio >= 1.10.0",
    ],
    python_requires='>=3.7',
    setup_requires=[
        'grpcio >= 1.38.0',  # You might want to specify a version based on your requirements
    ],
    scripts=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False,
)
