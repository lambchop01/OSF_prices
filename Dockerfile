FROM python:3.9-slim

### install java
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

### Get required python packages
ADD requirements.txt /
RUN pip install -r requirements.txt


### add program from worknig directory
COPY ./ /

CMD [ "python", "./weeklypricesosf.py" ]