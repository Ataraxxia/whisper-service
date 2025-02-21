This repository is a supplement to the youtube video explaning this solution:
https://www.youtube.com/watch?v=xpLMTh8xoj8

Requires python version from 3.8 to 3.11 but that may possibly change.

A quickstart code:
```
sudo apt install ffmpeg

git pull https://github.com/Ataraxxia/whisper-service.git
python3 -m venv whisper-service-venv
source whisper-service-venv/bin/activate
pip install -r whisper-service/requirements.txt

python3 whisper-service/app.py
```
