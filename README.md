![GitHub Actions status | sdras/awesome-actions](https://github.com/plysytsya/conjugator/workflows/CI/badge.svg)


## deepl-scraper


Uses selenium to Scrape the deepL translator


## Description

Installation:
	python setup.py install

Usage:
	>>> from deepl_scraper.translator import DeepLEngine
	>>> translator = DeepLEngine(source_language="en", target_language="de")
	Initializing DeepL translator
	Choosing language code EN
	Choosing language code DE
	>>> translator.translate("hello, world!")
	'Hallo, Welt!'

Waring:
Every initialized engine leaves an open selenium webdriver instance.
you can close it with:
	>>> translator.browser.driver.quit()
You can also close them the hard way:
	>>> from deepl_scraper import browser
	>>> browser.kill_process_by_keyword("chromedriver")
The second option will close all processes called chromedriver.
Use geckodriver respectively if you use Firefox.