from pathlib import Path

from qrs import __author__, __doc__, __license__, __module__, __version__
from setuptools import setup

setup(
	name=__module__,
	version=__version__,
	description=__doc__ or '',
	long_description=Path('README.md').read_text(),
	long_description_content_type='text/markdown',
	url=f'https://github.com/{__author__}/{__module__}',
	author=__author__,
	include_package_data=True,
	license=__license__,
	packages=[__module__],
	package_data={f'{__module__}': ['*.py', '*.txt']},
	install_requires=['jarguments==0.1.0'],
	setup_requires=['pytest_runner'],
	python_requires='>=3.8',
	scripts=[],
	tests_require=['pytest'],
	entry_points={'console_scripts': [f'{__module__}={__module__}:main']},
	zip_safe=True,
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Topic :: Games/Entertainment :: Board Games',
		'Topic :: Games/Entertainment :: Puzzle Games',
	],
)
