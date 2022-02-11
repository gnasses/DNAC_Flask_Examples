FROM python:3.8-alpine


MAINTAINER Gus Nasses "gunasses@cisco.com"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "dnac_flask_working.py" ]
