FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
  firefox-esr \
  wget \
  unzip \
  && apt-get clean

RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
  && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
  && rm /tmp/geckodriver.tar.gz

ENV DISPLAY=:99

EXPOSE 80

CMD ["python", "main.py"]
