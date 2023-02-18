from setuptools import find_packages, setup
import re

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('datadir/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = {
    'test': [
        'pytest',
    ],
}

packages = find_packages(exclude=('tests',))

setup(
    name='datadir',
    author='Hugo Boueix',
    url='https://github.com/hboueix/datadir',
    project_urls={
        'Issue tracker': 'https://github.com/hboueix/datadir/issues',
    },
    version=version,
    packages=packages,
    license='MIT',
    description='A data directory helper Python package',
    long_description=readme,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.10.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)