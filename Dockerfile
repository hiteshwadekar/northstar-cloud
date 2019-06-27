FROM python:3.6
RUN python -m pip install --upgrade pip
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .
# CMD ["northstar-cloud"]