ENV=. .env/bin/activate;

.env:
	python3 -m venv .env
	$(ENV) python3 -m pip install -U setuptools
	$(ENV) python3 -m pip install yt_dlp

run: .env
	$(ENV) python3 main.py

.DEFAULT_GOAL := run
