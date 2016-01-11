# twitter_scraper_selenium

Scrape twitter user info, friendshio and tweets by using selenium. Twitter api is not used.

This project is ment as a exercise to learn a little about selenium scraping.

Not finished, but you can get it to work

RUN:
	- Need cromdriver.exe and place it wherever it should for your OS. in windows.  "C:\Python27\Scripts" Folder.
	- Create db tables. sbot.twitter.screaper.db.sql_create.txt should work. Not fully tested
	- Set get_twitter_scraper_database_string in config.py
	- Use functions in sbot.twitter.screaper.controller.scrape.py to scrape information	

WARNING:
	- robot.txt is not followed, this project was only ment as a small scale test
	- Exessive use of this project might get you ip banned from twitter for a period bacause it dos not follow robot.txt
		- This might be avoided by adding a few lines to make selenium use diferetn proxies, but exessive scraping of twitter is not the meaning of this project.