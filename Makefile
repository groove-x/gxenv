.PHONY: deb
deb:
	/usr/bin/python3 setup.py --command-package=stdeb.command debianize --with-python3=True
	fakeroot debian/rules clean
	fakeroot debian/rules binary

