from setuptools import setup

setup(
    name='secutil',
    version='0.1.0',
    description='Utils that provides some useful methods.',
    url='https://github.com/jarzab3/keychain_utils.git',
    author='Adam Jarzębak',
    author_email='adam@jarzebak.eu',
    license='MIT',
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "secutil=secutil:main",
        ]
    },

    classifiers=[
        'Development Status :: 1 - Testing',
        'Intended Audience :: Work',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux :: MacOS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
