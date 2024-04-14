
python3 setup.py sdist
python3 setup.py bdist_wheel
python3 setup.py bdist_wheel
twine upload dist/*

update
rm -rf dist/*
python3 setup.py sdist bdist_wheel
twine upload dist/*
