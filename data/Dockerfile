FROM postgres:11
LABEL maintainer "Joseph Farrell <joe@joefarrell.dev>"

WORKDIR /data

COPY create.sql /data
COPY deployDb.sh /data

RUN chmod a+x create.sql
RUN chmod a+x deployDb.sh

RUN /data/deployDb.sh
