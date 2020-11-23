FROM python:3.8-buster

ARG USERNAME=xuhy
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG CHROME_VERSION=87.0.4280.20
ARG URL_CHROME=http://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
ARG URL_CHROMEDRIVER=https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai
ENV DEBIAN_FRONTEND=noninteractive

RUN \
    #
    # set local time to Asia Shanghai
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    #
    # use 163 mirror apt source
    && sed -i 's|http://deb.debian.org|http://mirrors.163.com|g' /etc/apt/sources.list \
    && sed -i 's|http://security.debian.org|http://mirrors.163.com|g' /etc/apt/sources.list \
    #
    # install necessary packages
    && apt-get update \
    #
    # create a non-root user
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USERNAME --shell /bin/bash --create-home $USERNAME \
    && adduser $USERNAME audio \
    && adduser $USERNAME video \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME \
    #
    # add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    #
    # install chinese fonts
    && apt-get install -y fonts-noto fonts-noto-cjk \
    #
    # install google chrome
    && wget -O google-chrome.deb $URL_CHROME --no-check-certificate \
    && apt-get -y install ./google-chrome.deb \
    && rm google-chrome.deb \
    #
    # install chromedriver
    && wget -O chromedriver_linux64.zip $URL_CHROMEDRIVER --no-check-certificate \
    && unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip \
    && chmod +x chromedriver \
    && mv -f chromedriver /usr/local/share/chromedriver \
    && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
    #
    # clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN \
    #
    # install python packages for xuexiqiangguo
    pip install --upgrade pip \
    && pip install --no-cache-dir selenium schedule requests 

RUN \
    #
    # install python packages for youtube-dl
    pip install --no-cache-dir youtube-dl 

USER $USERNAME

CMD ["/bin/bash"]
