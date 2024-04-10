import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()

with open('requirements.txt', encoding='utf-8') as f:
	required = f.read().splitlines()


setuptools.setup(
	name='telepoller',
	version="0.0.1",
	author="STaper_Admin",
	description="Poller for Telegram Bot on Pytelegrambotapi",
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires=required,
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.10'
)
