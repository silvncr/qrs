version = '0.1.0'

from setuptools import setup

setup(
	name='qrs',
	version=version,
	description='Tool for Quarrel (and other word games)',
	long_description=open('README.md', 'r').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/silvncr/qrs',
	author='silvncr',
	include_package_data=True,
	license='MIT',
	packages=['qrs'],
	package_data={
		'qrs': [
			'*.json',
			'*.py',
			'*.txt',
		]
	},
	setup_requires=['pytest_runner'],
	python_requires='>=3.9',
	scripts=[],
	tests_require=['pytest'],
	entry_points={},
	zip_safe=True,
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.9',
		'Topic :: Games/Entertainment :: Board Games',
		'Topic :: Games/Entertainment :: Puzzle Games',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)
