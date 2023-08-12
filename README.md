# speedtest

A Helm chart with:

* A Headless Service to expose the database to the client in the cluster.
* A Headless Service to expose the dashboard to the whole network.
* A Deployment for the InfluxDB pod.
  * An InfluxDB server with the official Docker image to store the time series data. 
* A Deployment for the Grafana pod.
  * A Grafana server with the official Docker image for visualization of the stored data.
* A CronJob to repeat the speed test on a schedule.
  * Pod with a Python stateless app that talks to the Ookla speedtest API and the time series db.

## Prerequisites
1. [Set up](https://santisbon.github.io/reference/rpi/) your Raspberry Pi with a static IP.
2. [Install and configure MicroK8s](https://santisbon.github.io/reference/k8s/#microk8s) (or another lightweight Kubernetes distribution with DNS and Helm addons) on your Pi.

Note: MicroK8s by default uses `Dqlite` as its storage backend instead of `etcd`. [Encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for either one to further secure `Secret` objects is outside the scope of this project.

## Install

1. Prepare your Raspberry Pi's local storage for both the database and dashboard
    ```shell
    # On your Pi
    sudo mkdir -p /var/lib/influxdb2
    sudo mkdir -p /etc/influxdb2
    sudo mkdir -p /var/lib/grafana
    ```

<details>
<summary>Example use of the Okkla Speedtest CLI</summary>

```zsh
$ speedtest --accept-license --accept-gdpr

   Speedtest by Ookla

      Server: GSL Networks - New York, NY (id: 46120)
         ISP: Packethub s.a.
Idle Latency:    21.19 ms   (jitter: 0.33ms, low: 20.38ms, high: 21.30ms)
    Download:   394.73 Mbps (data used: 481.0 MB)
                470.89 ms   (jitter: 88.55ms, low: 23.93ms, high: 2454.44ms)
      Upload:   222.61 Mbps (data used: 394.0 MB)
                 30.81 ms   (jitter: 6.65ms, low: 21.07ms, high: 262.71ms)
 Packet Loss:    32.5%
  Result URL: https://www.speedtest.net/result/c/e5a52491-a9ef-4057-90a0-41afb727752d
```

</details>
