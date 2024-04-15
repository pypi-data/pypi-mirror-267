from setuptools import setup

requirements = ['requests']
readme = ''
with open('README.md', encoding="utf8") as f:
    readme = f.read()

setup(
    name='MayuriScanner',
    author='Alpha',
    author_email='alphacoders@yahoo.com',
    version='0.1',
    long_description=readme,
    url='https://github.com/XZeipher/MayuriScanner',
    license='GNU General Public License v3.0',
    classifiers=[
        "Framework :: AsyncIO",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Build Tools",

    ],
    description='A API bassed telegram scanner.',
    include_package_data=True,
    keywords=['telegram', 'mayuri', 'bot', 'api', 'gban',
              'scan'],
    install_requires=requirements
)
