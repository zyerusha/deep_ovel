# syntax=docker/dockerfile:1
# Line above instructs the Docker builder what syntax to use when parsing the Dockerfile

FROM python:3.9.7

# Create a working directory
WORKDIR /app
RUN apt-get update
EXPOSE 5000

#We’ll copy the requirements.txt file into our working directory
COPY requirements.txt requirements.txt
# RUN command to execute the command pip3 install.
RUN python -m pip install --upgrade pip
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

# Add our source code into the image. 
COPY . .

# set command we want to run when our image is executed inside a container.
# Setting application externally visible (i.e. from outside the container) by specifying --host=0.0.0.0.
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python", "main_app.py"]