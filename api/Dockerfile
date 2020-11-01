FROM python:3.7.3-stretch

WORKDIR /mydir

COPY requirements.txt /mydir/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /mydir/


CMD [ "python", "/mydir/app/routes.py"]