FROM python:3.7.0

# Last updated
ENV REFRESHED_AT 2018-7-22

# init
RUN apt-get update -y && apt-get upgrade -y

# packages
RUN pip install -U pip
RUN pip install beautifulsoup4
RUN pip install -U selenium
RUN pip install numpy
RUN pip install file-downloader
RUN pip install requests
RUN pip install tqdm
RUN pip install certifi
RUN pip install pip-review
RUN pip-review --auto

# env
ENV LANG ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8

# user
RUN export uid=1000 gid=1000 && \
    echo "denden047:x:${uid}:${gid}:denden047,,,::/bin/bash" >> /etc/passwd && \
    echo "denden047:x:${uid}:" >> /etc/group
USER denden047
CMD ["/bin/bash"]
