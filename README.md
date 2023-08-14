# Internet Speed Monitor

Keep track of your internet connection speeds over time with a Raspberry Pi.

![Dashboard](https://i.imgur.com/xjp8tSg.png)

This Helm chart deploys:
* InfluxDB 2.x database for time series data.
* Grafana dashboard.
* Python app to run the speed test on a schedule.

<p align="center">
    <img src="https://i.imgur.com/1SqCDuZ.png"  width="80%">
</p>

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
2. If installing from the repository
    ```shell
    # On your Pi
    
    helm repo add santisbon https://santisbon.github.io/charts/
    # or 
    helm repo update
    
    CHART="santisbon/speedtest"
    ```

    Or if installing from source
    ```shell
    # On your Pi
    git clone https://github.com/santisbon/speedtest.git && cd speedtest
    CHART="./speedtestchart"

    nano $CHART/values.yaml
    # edit the values
    ```
3. Install the Helm chart which will [enforce the installation order](https://helm.sh/docs/intro/using_helm). Set parameters like the [schedule](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#schedule-syntax) to run the test if you didn't do it through the `values.yaml` file.  
If using MicroK8s add it to the typed commands e.g. `microk8s helm`, `microk8s kubectl`.
    ```shell
    # On your Pi
    RELEASE=speedtest
    NAMESPACE=speedtest-n

    helm install $RELEASE $CHART \
        -n $NAMESPACE \
        --create-namespace \
        --set nodeHostname=raspberrypi4 \
        --set influxdbpassword=supersecret \
        --set influxdbtoken=my-super-secret-auth-token \
        --set schedule="*/10 * * * *"
    ```
4. Grab the `NodePort` assigned to the Grafana service (by default in the 30000-32767 range). 
    ```shell
    # On your Pi
    kubectl -n $NAMESPACE get svc $RELEASE-grafana-svc

    NAME                    TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    speedtest-grafana-svc   NodePort   10.152.182.171   <none>        3000:32425/TCP   52s
    ```
    In this example it's **32425**.
5. From your desktop, access the Grafana dashboard using your Raspberry Pi's IP address or DNS name and the `NodePort` from the previous step e.g. 
http://raspberrypi4.local:32425. The default credentials are *admin/admin*.
6. Add a new connection with data source InfluxDB.
    1. Set query language to Flux.
    2. Set the URL using your Helm release name and InfluxDB port e.g. 
    http://speedtest-influxdb-svc:8086. 
    3. Use the organization, token, and bucket you set in `values.yaml` or the command line. If you didn't set a token, one was created for you. You can retrieve it from a shell in the `influxdb-c` container with the command `influx auth list`.
    4. Click on *Save & Test*.
    5. Build a dashboard and add a visualization (panel) with the data source you created.
    6. Write the Flux queries you want for your visualizations filtering by `_measurement` or `_field`. Some examples:
        ```
        speeds = from(bucket: "internetspeed")
            |> range(start: -1d)
            |> filter(fn: (r) => r._field == "download" or r._field == "upload")
            |> yield(name: "_results")

        latency = from(bucket: "internetspeed")
            |> range(start: -1d)
            |> filter(fn: (r) => r._field == "ping" or r._field == "jitter")
            |> yield(name: "_results")
        ```
    7. Save your dashboard. You can add multiple panels and set units like megabits per second (Mbps) and ms. The units are in the *Standard options* section of the panel.

## Upgrade
```shell
helm upgrade $RELEASE $CHART -n $NAMESPACE
```

## Uninstall
```shell
helm uninstall $RELEASE -n $NAMESPACE --wait
kubectl delete namespaces $NAMESPACE
```
