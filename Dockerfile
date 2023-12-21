FROM python:3.11-alpine
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]