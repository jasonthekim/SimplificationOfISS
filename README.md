# Title

## Description of Project:
We have found an abundance of positional data for the International Space Station (ISS). Our goal and objective is to build a containerized flask application for querying and returning desired information from the ISS data set, full of interesting information including ISS position and velocity data at given times, as well as when the ISS can be seen over select cities. This project aims to sift through the large and complex dataset with ease through simple commands. 

## Description of Important Files:
*app.py*:
- flask application for tracking ISS position and sightings.
- loads in the two datasets, positional.xml and sighting.xml.
- contains routes that return important, desired information.

*test_app.py*:
- makes sure each function in app.py has no errors.
- tests check that return types are correct.

*Dockerfile*:
- containerizes the flask application and both datasets.

*Makefile*:
- written with targets to build a container and to start the containerized Flask application.

## Instructions to Download Datasets:
1. Log into ISP and connect to TACC server.
2. Click on [this link](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq) to access data files.
3. Under "Public Distribution File", right click `XML` and click `Open link in new tab`
4. Copy the URL and type in the command line:
```
wget <xml link>>
```
5. After downloading the positional data, now download specific sighting data by going to the same link. 
6. Under "XMLsightingData_citiesUSA09", right click `XML` and click `Open link in new tab`.
7. Repeat same process of using `wget` command.

## Instructions for Building and Container from Dockerfile:
1. Type in command line: `touch Dockerfile`
2. Specify requirements needed for the Flask application by typing in command line: `vim requirements.txt`
3. In the file created in step 2 type: `Flask==2.0.3` and save.
4. Open the created Dockerfile and enter in:
```
FROM python:3.9

RUN mkdir /app

RUN pip3 install --user xmltodict

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"] 
```
5. Build the container by typing in command line: `docker build -t <username>/<file-name>:<name> .` 
    - NOTE: do NOT forget the `.` at the end
6. Push the container by typing in command line: `docker push <username>/<file-name>:<name>

## Instructions to Pull Pre-Containerized Copy of App from Docker Hub:
1. Type in command line: `docker pull <username>/<file-name>:<name>`

## Instructions to Interact With the Application:
1. Type and run in command line:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5014
```
2. Open a separate window terminal and type in command line: `curl localhost:5014/`
   The screen should display a list of routes that obtains specific information in which the user may interact with to get desired info:
```
ISS Sighting Location
/                                                      (GET) print this information
/reset                                                 (POST) reset data, load from file
Routes for querying positional and velocity data:

/epochs                                                (GET) lists all epochs in positional and velocity data
/epochs/<epoch>                                        (GET) lists all data associated with a specific epoch
Routes for Querying Sighting Data

/countries                                             (GET) lists all countries in sighting data
/countries/<country>                                   (GET) lists all data for a specific country
/countries/<country>/regions                           (GET) lists all regions in a specific country
/countries/<country>/regions/<region>                  (GET) lists all data for a specific region
/countries/<country>/regions/<region>/cities           (GET) lists all cities in a specific region
/countries/<country>/regions/<region>/cities/<city>    (GET) lists all data for a specific city
```
3. 


