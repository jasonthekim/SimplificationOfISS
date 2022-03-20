FROM python:3.9

RUN pip3 install --user xmltodict

COPY positional.xml /code/positional.xml

COPY sighting.xml /code/sighting.xml

COPY app.py /code/app.py

COPY test_app.py /code/test_app.py


