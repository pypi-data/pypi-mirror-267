from setuptools import setup, find_packages

setup(
    name='util_searchads360_hm',
    version='0.0.5',  # Update with your package version
    description='A package of the Search Ads 360 Utility Tool',
    url='https://developers.google.com/search-ads/reporting/client-libraries/client-libraries',  # Update with your package URL
    author='Joe Fedorowicz',
    author_email='jfedorowicz@harmelin.com',
    license='MIT',  # Update with your package license
    packages=find_packages(),
    py_modules=['client', 'config'],
    options={'install': {'install_lib': 'util_searchads360'}},
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
