# Internet Speed Monitor

A Helm chart with:
* InfluxDB time series database
  * Headless Service to expose the database to the client app in the cluster.
  * Pod and Deployment with InfluxDB server using the Docker official image.
* Grafana dashboard
  * NodePort Service to expose the dashboard outside the cluster.
  * Pod and Deployment with Grafana server using the Docker image from Grafana.
* Client app
  * A Pod and CronJob to repeat the speed test on a schedule using the `speedtest` image from my Docker Hub repo.

## Prerequisites
1. [Set up](https://santisbon.github.io/reference/rpi/) your Raspberry Pi.
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
2. If installing from the repository:
    ```shell
    # On your Pi
    helm repo add santisbon https://santisbon.github.io/charts/
    CHART="santisbon/speedtest"
    ```

    Or if installing from source, grab the code
    ```shell
    # On your Pi
    CHART="./speedtestchart"

    git clone https://github.com/santisbon/speedtest.git && cd speedtest
    nano $CHART/values.yaml
    # edit the values
    ```
3. Install the Helm chart which will [enforce the installation order](https://helm.sh/docs/intro/using_helm). Set parameters if you didn't do it through the `values.yaml` file. If using MicroK8s add it to the typed commands e.g. `microk8s helm`, `microk8s kubectl`.
    ```shell
    # On your Pi
    RELEASE=speedtest
    NAMESPACE=speedtest-n

    helm install $RELEASE $CHART \
        -n $NAMESPACE \
        --create-namespace \
        --set nodeHostname=raspberrypi4 \
        --set influxdbpassword=supersecret
    ```
4. Grab the `NodePort` assigned to the Grafana service (by default in the 30000-32767 range)
    ```shell
    kubectl -n $NAMESPACE get svc $RELEASE-grafana-svc
    ```
5. From your desktop, access the Grafana dashboard using your Raspberry Pi's IP address or DNS name and the `NodePort` from the previous step e.g. 
http://raspberrypi4.local:30001.

## Upgrade
```shell
helm upgrade $RELEASE $CHART -n $NAMESPACE
```

## Uninstall
```shell
helm uninstall $RELEASE -n $NAMESPACE --wait
kubectl delete namespaces $NAMESPACE
```
