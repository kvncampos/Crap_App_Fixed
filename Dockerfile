# Use the base image with Python3 and pip pre-installed
FROM python:3

# Update package lists and install additional packages
RUN apt-get update \
    && apt-get install -y python3 python3-pip

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

EXPOSE 3000

ENTRYPOINT ["python"]
CMD ["app.py"]
