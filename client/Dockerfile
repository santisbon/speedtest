FROM  debian
SHELL ["/bin/bash", "-c"]

RUN   apt update && apt upgrade -y \
      && apt install -y curl \
      && curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash \
      && apt install -y python3 pip speedtest \
      && pip3 install 'influxdb-client' --break-system-packages
COPY  ./speedtest.py /etc/speedtest/
CMD   [ "python3", "/etc/speedtest/speedtest.py" ]
