import setuptools

version = '0.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='py-queue-factory',
    version=version,
    author='Anujith Singh',
    author_email='anujith.singh@gmail.com',
    description='Queue factory to work with multiple types of queue',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/practo/py-queue-factory',
    packages=setuptools.find_packages(),
    install_requires=[
       'boto3>=1.9.*',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    keywords='queue factory',
    project_urls={
        'Documentation': 'https://github.com/practo/py-queue-factory/wiki',
        'Source': 'https://github.com/practo/py-queue-factory',
        'Tracker': 'https://github.com/practo/py-queue-factory/issues',
    },
)
