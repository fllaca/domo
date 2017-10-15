run:
	find . -name "*.pyc" -exec rm -f {} \;
	python domo.py
