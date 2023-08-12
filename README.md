# Internet Speed Monitor

A Helm chart with:
* InfluxDB time series database
  * Headless Service to expose the database to the client in the cluster.
  * Pod and Deployment with InfluxDB server using the Docker official image.
* Grafana dashboard
  * Headless Service to expose the dashboard to the whole network.
  * Pod and Deployment with Grafana server using the Docker image from Grafana.
* Client app
  * A Pod and CronJob to repeat the speed test on a schedule using the `speedtest` image from my Docker Hub repo.

## Prerequisites
1. [Set up](https://santisbon.github.io/reference/rpi/) your Raspberry Pi with a static IP.
2. [Install and configure MicroK8s](https://santisbon.github.io/reference/k8s/#microk8s) (or another lightweight Kubernetes distribution with DNS and Helm addons) on your Pi.

Note: MicroK8s by default uses `Dqlite` as its storage backend instead of `etcd`. Further securing of `Secret` objects with [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for either storage backend is outside the scope of this project.

## Install

1. Prepare your Raspberry Pi's local storage for both the database and dashboard
    ```shell
    # On your Pi
    sudo mkdir -p /var/lib/influxdb2
    sudo mkdir -p /etc/influxdb2
    sudo mkdir -p /var/lib/grafana
    ```
