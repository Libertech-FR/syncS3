FROM debian:12

ENV TIMEZONE=Europe/Paris \
    LANGUAGE=fr_FR.UTF-8 \
    LANG=fr_FR.UTF-8 \
    TERM=xterm \
    DEBFULLNAME="Libertech suncS3" \
    DEBEMAIL="product@libertech.Fr"

RUN apt-get clean -yq
RUN apt-get  update -yq 
RUN apt-get upgrade -yq 
RUN apt-get install --no-install-recommends -yq ca-certificates python3 python3-pyinotify python3-boto3 gettext python3-paramiko

COPY ./rootfs /

ENTRYPOINT /docker-entrypoint.sh
