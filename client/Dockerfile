FROM        debian
SHELL       ["/bin/bash", "-c"]

RUN         apt update && apt upgrade -y \
            && apt install -y curl \
            && curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash \
            && apt install -y python3 python3-influxdb speedtest
COPY        ./speedtest.py /etc/speedtest/
CMD         [ "python3", "/etc/speedtest/speedtest.py" ]
