# Monitoring Documentation – Linux Environment

## Services Duty

The following services are involved in the monitoring system:

1. **Grafana**: Visualization and dashboard tool.
2. **Prometheus**: Time-series database for collecting metrics.
3. **Node Exporter**: Collects system-level metrics (CPU, RAM, Disk, Network).
4. **Blackbox Exporter**: Checking the availability of services.
5. **Alertmanager**: Handles alerts sent by Prometheus.
6. **cAdvisor-health**: Collects container metrics (CPU, RAM, Disk, Network) and container status and health.

## Description of Services

### 1. **Grafana**

- A web-based dashboard and visualization tool.
- Connects to Prometheus and queries the stored data.
- Users can create custom dashboards with charts, tables, and graphs.

### 2. **Prometheus**

- Periodically scrapes metrics from exporters like Node Exporter, cAdvisor, and Blackbox.
- Stores the data as time-series in its own database.
- Can also send alerts to Alertmanager based on defined rules.

### 3. **Node Exporter**

- Installed on each Linux server.
- Collects system-level metrics like CPU usage, memory, disk, network, etc.
- Exposes data on port `9100`. Prometheus scrapes these metrics regularly.

### 4. **Blackbox Exporter**

- Used to monitor the availability of external endpoints.
- Checks if a service is reachable and how it responds.
- Prometheus sends test probes via Blackbox and stores the response data.

### 5. **cAdvisor-health**

- Used for monitoring Docker containers and installed on each container server.
- Collects per-container resource usage (CPU, memory, I/O) and container status (starting, exited, etc.) and health (healthy, unhealthy).
- Runs on port `8080` by default. Prometheus pulls metrics from it as well.

---

### Setup

The project files are located here:  
[https://github.com/hossein1335/grafana-prometheus](https://github.com/hossein1335/grafana-prometheus)

### 1. **Prometheus Configuration** (`grafana-prometheus/prometheus/prometheus.yml`)

- Modify scrape targets and alert manager configurations.
- Replace `<your-ip>` with the actual IP address of the machines running Prometheus, Grafana, Node Exporter, and cAdvisor.
- If additional job configurations are needed, you can add more `static_configs` under `scrape_configs`.

### 2. **Docker Compose Configuration for Prometheus and Grafana** (`grafana-prometheus/docker-compose.yml`)

This file configures Prometheus and Grafana.  
Ensure the following directories are correct:  
`./prometheus:/etc/prometheus`  
`./grafana/provisioning:/etc/grafana/provisioning`

- Modify the environment variables for Grafana (`GF_SECURITY_ADMIN_USER` and `GF_SECURITY_ADMIN_PASSWORD`) to match your desired login credentials.

To start the Prometheus and Grafana service, run:

```bash
docker compose up -d
## 3. Docker Compose Configuration for Node Exporter and cAdvisor (`exporter/docker-compose.yml`)

This file contains the configurations for **Node Exporter** and **cAdvisor**. Ensure that paths like `/:/host:ro,rslave` are accessible for volumes reading from the host machine.

- Modify CPU and memory limits according to your system capacity.

To start the **Node Exporter** and **cAdvisor-health** services, run the following command:

```bash
docker compose up -d

### 4. **Alertmanager Configuration** (`alert/alertmanager/alertmanager.yml`)

- Modify the **webhook URLs** for your actual endpoints.
- This file is used for defining **alert routes** and **receivers** in **Alertmanager**.
- Modify the fields under `webhook_configs` with the correct IP and URL addresses (e.g., `http://ip:5000/send-sms`, `http://ip:5000/send-bale`).
- You can also add or remove receivers based on your requirements.

---

### 5. **Flask App** (`alert/flask/app.py`)

This file includes two endpoints:

- **`/send-sms`**: For sending SMS via the SMS API.
- **`/send-bale`**: For sending messages to "Bale" chats.

Example endpoints:

- `http://ip:5000/send-sms`
- `http://ip:5000/send-bale`

You need to configure the input information based on your SMS service and personalize the recipient phone numbers in this file. These values should be entered in the sections of the code responsible for sending SMS and Bale messages.
Actually, sends the alerts to the script, and then Alertmanager app.py the script forwards the alerts to the main SMS service.app.py

### 6. **Docker Compose Configuration for Flask** (`alert/flask/app.py`)

This Docker Compose file is very simple for this script and Flask.

To start the **Flask** service, run the following command:

```bash
docker compose up -d
### 7. **Docker Compose Configuration for Alertmanager** (`alert/docker-compose.yml`)

The configuration file for **Alertmanager** specifies the image, docker-compose.yml configuration file path, volumes, and network mode.

- Ensure the volume path `./alertmanager:/config` points to the correct location of `alertmanager.yml` on your local machine.

To start the **Alertmanager** service, run the following command:

```bash
docker compose up -d

## How Do Alerts Work?

### 1. **Prometheus TCP Connection Alert** (`grafana-prometheus/prometheus/connection_alert.yml`)

This file contains a **Prometheus** alerting rule for monitoring TCP connection states on a specific node (for example, an nginx server).

- If the sum of active TCP connections, in-use sockets, and orphan sockets exceeds **30,000**, it triggers a **critical** alert.
  
The alert is useful for detecting overloaded or misconfigured nodes that may be experiencing network issues.

### 2. **Container Status Alert** (`grafana-prometheus/prometheus/container_alerts.yml`)

This file monitors the status of containers, specifically alerting if a container has exited unexpectedly.

- It checks if the `container_status` is `-1` (indicating the container has exited).
  
The alert is evaluated every **59 seconds**. If the condition holds for **120 seconds**, a **critical** alert is raised, detailing which container on which server has exited.

For example, you will receive an alert when a Docker container unexpectedly stops running.

- Alert manager link: [Alertmanager Config](http://alertmanager/config)

### 3. **Container Health Alert** (`grafana-prometheus/prometheus/container_alert_health.yml`)

This file monitors the health status of containers.

- If a container is unhealthy (i.e., `health status == 0`), it triggers a **critical** alert.
  
The alert is triggered if the container remains unhealthy for more than **150 seconds**.

This alert is critical in production environments where the health of containers (such as those running services) must be monitored for issues like misconfigurations or application failures.

### 4. **CPU Usage Alert** (`grafana-prometheus/prometheus/server_cpu_alerts.yml`)

This file monitors CPU usage on servers.

- If the CPU usage exceeds **80%** for more than **150 seconds**, it triggers a **critical** alert.
  
The alert includes the **server instance** and the exact percentage of **CPU usage**.

This alert ensures that servers are not overburdened and can help in identifying servers that might require scaling or optimization.

### 5. **Disk Usage Alert** (`grafana-prometheus/prometheus/server_hard_alerts.yml`)

This file monitors disk usage on servers.

- If disk usage exceeds **80%** for more than **1200 seconds** (20 minutes), it triggers a **critical** alert.
  
The alert provides details on the **server instance** and the percentage of **disk usage**.

This alert is particularly useful for detecting servers that may be running out of disk space, which could lead to data loss or system instability.
