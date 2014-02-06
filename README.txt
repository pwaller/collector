collector README
==================

Getting Started
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/initialize_collector_db development.ini

- $venv/bin/pserve development.ini

TODO
----

Known defects:

	- Very slow pages

		- [ ] http://0.0.0.0:6543/covers/1870#{"music_id":10675}
			- This is because autocomplete is set on every single field at the page
			  load. Instead I should set an $().on("focus?") event to put
			  autocomplete in place just-in-time.


		- [ ] Not being able to search for cover names?

		- [ ] Not being able to edit soloists

		- [ ] Conductor first/last name ordering

		- [ ] Editing newly added rows doesn't work

- Front page

	- [x] Clicking the "+" should work
		- Field type is now "submit" and it works.

- Adding covers

	- [x] Making a new cover record
	- [ ] Being able to add music to an empty cover

- Editing covers
	
	- Editing the cover itself
		- [x] title
		- [ ] date
		- [ ] format
		- [x] notes

	- Editing Music
		- Ensuring that editing all fields works
			- [ ] Make editing soloists work
			- [x] All other fields

		- Deleting records
			- [ ] Make this work?

	- Adding new pieces of music to a cover
		- [x] Appears to work

- Listing music
	
	- [x] Links to individual music

	- [x] Searching by title search

	- [ ] Sub-selecting by instrument or music type
