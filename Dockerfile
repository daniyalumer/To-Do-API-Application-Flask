# using docker base image
FROM python:3.11-slim

# setting working directory
WORKDIR /app

# copying requirements.txt to pwd
COPY requirements.txt /app/

# installing dependencies from requirements.txt
RUN pip install -r requirements.txt

# copy rest of application to pwd
COPY . /app

# port on which flask app runs on
EXPOSE 5000

# setting environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# running the flask application
CMD ["flask", "run", "--host=0.0.0.0"]
