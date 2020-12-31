cd ..
git submodule update --recursive --remote
cd db
del data.db
cd ..
cd src
python dbloader.py
python dbbrowser.py