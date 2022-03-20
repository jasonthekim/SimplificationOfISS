all: build run push

images:
        docker images | grep jasonthekim

ps:
        docker ps -a | grep jasonthekim

build:
        docker build -t jasonthekim/flask-iss-work:midterm .

run:
        docker run -d -p 5014:5000 jasonthekim/flask-iss-work:midterm

push:
        docker push jasonthekim/flask-iss-work:midterm
