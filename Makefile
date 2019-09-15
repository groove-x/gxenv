.PHONY: deb
deb:
	python3 setup.py --command-package=stdeb.command debianize --with-python3=True
	fakeroot debian/rules clean
	fakeroot cebian/rules binary

