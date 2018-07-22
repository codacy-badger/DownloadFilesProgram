FROM python:3.7.0

# Last updated
ENV REFRESHED_AT 2018-7-22

# init
RUN apt-get update -y && apt-get upgrade -y

# packages
RUN pip install beautifulsoup4

# user
RUN export uid=1000 gid=1000 && \
    echo "denden047:x:${uid}:${gid}:denden047,,,::/bin/bash" >> /etc/passwd && \
    echo "denden047:x:${uid}:" >> /etc/group
USER denden047
CMD ["/bin/bash"]
