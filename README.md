# Title

## Description of Project:
We have found an abundance of positional data for the International Space Station (ISS). Our goal and objective is to build a containerized flask application for querying and returning desired information from the ISS data set, full of interesting information including ISS position and velocity data at given times, as well as when the ISS can be seen over select cities. This project aims to sift through the large and complex dataset with ease through simple commands. 

## Description of Important Files:
app.py:
- flask application for tracking ISS position and sightings.
- loads in the two datasets, positional.xml and sighting.xml.
- contains routes that return important, desired information.

test_app.py:
- makes sure each function in app.py has no errors.
- tests check that return types are correct.

Dockerfile:
- containerizes the flask application and both datasets.

Makefile:
- written with targets to build a container and to start the containerized Flask application.

## Instructions to Download Datasets:
1. Log into ISP and connect to TACC server.
2. Click on [this link](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq) to access data files.
3. Under "Public Distribution File", right click `XML`, click 






