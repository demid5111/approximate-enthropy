[![unit testing and osx packaging](https://travis-ci.org/demid5111/approximate-enthropy.svg?branch=master)](https://travis-ci.org/demid5111/approximate-enthropy)

### To run unit tests

From the root run the following command:

`python -m unittest discover -s tests/ -p '*_test.py'`

To collect coverage:
1. Run: `coverage run -m unittest discover -s tests/ -p '*_test.py'`
2. Generate html report: `coverage html --include='*.py'`
3. Open `index.html` in `htmlcov` directory

### To run e2e tests

From the root run the following command:

`python -m pytest tests/gui/

### Adding new version

1. Create tag:
`git tag latest-master`
2. Push tag:
`git push origin latest-master`