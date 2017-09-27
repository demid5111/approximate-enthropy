### To run unit tests

From the root run the following command:

`python -m unittest discover -s tests/ -p '*_test.py'`

To collect coverage:
1. Run: `coverage run -m unittest discover -s tests/ -p '*_test.py'`
2. Generate html report: `coverage html --include='*.py'`
3. Open `index.html` in `htmlcov` directory