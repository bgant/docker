# Source: https://wiki.lineageos.org/devices/bullhead/build

FROM ubuntu:focal

WORKDIR /root

# Install packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y vim-tiny wget \
    bc bison build-essential ccache curl flex g++-multilib \
    gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev \
    lib32readline-dev lib32z1-dev liblz4-tool libncurses5 \
    libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils \
    lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev \
    openjdk-14-jdk-headless

# Install Google platform-tools adb and fastboot
RUN wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
RUN unzip platform-tools-latest-linux.zip -d .

# Add platform-tools to your PATH
RUN echo '' >> /root/.profile
RUN echo '# add Android SDK platform tools to path' >> /root/.profile
RUN echo 'if [ -d "$HOME/platform-tools" ] ; then' >> /root/.profile
RUN echo '    PATH="$HOME/platform-tools:$PATH"' >> /root/.profile
RUN echo 'fi' >> ~/.profile

# Repo Command
RUN curl https://storage.googleapis.com/git-repo-downloads/repo > /usr/local/bin/repo
RUN chmod a+x /usr/local/bin/repo

# 100GB mount for build
RUN mkdir -p /root/android/lineage

RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"

RUN ln -s /usr/bin/python3 /usr/bin/python

COPY lineageos-build-bullhead.sh .

WORKDIR /root/android/lineage

# /usr/local/bin/repo --color=always init -u https://github.com/LineageOS/android.git -b lineage-17.1
# repo sync
