# Chapter 3: Observability and Resilience Engineering

Welcome to the deep end of the pool. In this chapter, we are going to learn how to build systems that not only tell you when they are broken but also try very hard not to break in the first place. 

Imagine you are driving a car at 150 mph. Monitoring is the dashboard telling you your speed and engine temperature. Observability is being able to ask the car *why* the engine is running hot and getting a detailed answer about a specific valve sticking. Resilience is the car automatically shifting down and reducing speed to prevent an explosion while keeping you safe.

We are going to learn how companies like Netflix, Google, Amazon, and Uber keep their massive, distributed, terrifyingly complex systems running. 

---

## PART A: OBSERVABILITY

### SECTION 1: The Three Pillars of Observability

#### 1. Definition + Why it exists
**Monitoring** is the act of collecting data to tell you *when* things go wrong. "The CPU is at 99%."
**Observability** is a property of a system. A system is observable if you can understand its internal state just by looking at its external outputs (metrics, logs, traces). It tells you *why* things went wrong. "The CPU is at 99% because User 123 sent a malformed JSON payload that caused a regex backtrack loop in the auth service."

Why do we need this? Because microservices are a murder mystery where everyone is a suspect, and observability is your magnifying glass.

#### 2. Real-world analogy
Imagine a restaurant.
- **Metrics**: The manager counts how many meals are served per hour. (Numbers).
- **Logs**: The waiter writes down exactly what each customer ordered. (Detailed text records).
- **Traces**: A GPS tracker attached to a specific steak, showing exactly how long it spent in the fridge, on the grill, and on the waiter's tray. (Journey of a single request).

#### 3. ASCII diagram
```text
[ User Request ] ---> ( API Gateway ) ---> ( Service A ) ---> ( Service B ) ---> [ Database ]
                         |                     |                  |
                         |                     |                  |
    Metrics   <----------+---------------------+------------------+
    (Counters/Rates)     |                     |                  |
                         v                     v                  v
    Logs      <-------[ "Auth failed" ]   [ "Processing X" ] [ "DB Query Y" ]
    (Events)             |                     |                  |
                         v                     v                  v
    Traces    <-------[ Span 1: 10ms ]----[ Span 2: 45ms ]---[ Span 3: 15ms ]
    (Journey)
```

#### 4. Internal working
- **Metrics** are aggregated numbers. They are cheap to store. They tell you *what* is happening at a macro level.
- **Logs** are discrete events. They are expensive to store. They tell you *what happened* in detail.
- **Traces** are connected spans representing a single request's lifecycle across multiple services. They tell you *where* the time went.

#### 5. Complete workflow
1. An alert fires based on **Metrics** (e.g., Error rate > 5%).
2. You look at a Dashboard and see the spike.
3. You pivot to **Traces** to see which specific service in the chain is taking too long or failing.
4. You pivot from the Trace to the specific **Logs** for that exact request to see the stack trace or error message.

#### 6. Production use case
Uber uses all three to debug why a user couldn't request a ride. Metrics show a spike in 500 errors in the `Dispatch` service. Traces show the request stalling between `Dispatch` and `Driver-Location` services. Logs reveal a timeout connecting to Redis.

#### 7. Commands + Complete YAML
(See following sections for specific tool YAMLs. The Three Pillars are a concept, not a tool.)

#### 8. Interview explanation
"Observability is about answering unknown unknowns. Monitoring answers known unknowns (we know CPU can spike, so we monitor it). Observability lets us ask arbitrary questions about our system's behavior without deploying new code to gather more data, by relying on high-fidelity metrics, logs, and distributed traces."

#### 9. Common mistakes + Best practices
- **Mistake**: Logging everything. (Too expensive).
- **Best Practice**: Use metrics for aggregations, sample traces, and log only actionable or context-rich events.

#### 10. Troubleshooting
If you have metrics but no context, check if your apps are emitting logs. If logs are disjointed, check trace context propagation.

#### 11. Interview Q&A
**Q:** What is the difference between monitoring and observability?
**A:** Monitoring tells you *that* a system is broken. Observability tells you *why* it's broken. Monitoring relies on predefined dashboards. Observability relies on raw, high-cardinality telemetry to debug novel problems.

---

### SECTION 2: Metrics and Prometheus

#### 1. Definition + Why it exists
Prometheus is a time-series database (TSDB) and monitoring system. It exists because scraping massive amounts of metric data (numbers over time) requires a specialized system. Traditional SQL DBs choke on time-series data.

#### 2. Real-world analogy
Prometheus is like a census taker who visits every house (pod) in your city (cluster) every 15 seconds, asks for a quick summary of who lives there (metrics), and writes it down in a massive ledger organized by time.

#### 3. ASCII diagram
```text
  [ App Pod 1 ] --( /metrics )--\
                                 \  [pull]
  [ App Pod 2 ] --( /metrics )-----> ( Prometheus Server ) ---> [ TSDB (Disk) ]
                                 /          |
  [ Node Expr ] --( /metrics )--/           | (Alerts)
                                            v
                                     ( Alertmanager ) ---> [ PagerDuty / Slack ]
```

#### 4. Internal working
Prometheus uses a **Pull model** (scrape). It doesn't wait for apps to send data; it reaches out to their `/metrics` endpoint. 
It uses **PromQL** to query this TSDB.
Metric Types:
- **Counter**: Only goes up (e.g., total HTTP requests).
- **Gauge**: Goes up and down (e.g., current CPU usage).
- **Histogram**: Buckets observations (e.g., request duration in <10ms, <50ms buckets).
- **Summary**: Similar to histogram but calculates quantiles client-side.

#### 5. Complete workflow
1. Dev instruments app to expose `/metrics` (e.g., Prometheus client library).
2. Prometheus Operator creates a `ServiceMonitor`.
3. Prometheus discovers the pods and scrapes them every 15s.
4. Grafana queries Prometheus via PromQL.
5. Prometheus evaluates `PrometheusRule` and sends alerts to Alertmanager.

#### 6. Production use case
Google (Borgmon, the predecessor to Prometheus) uses this to monitor millions of containers. If an app crashes, Prometheus stops getting scrapes, and an `Up` alert fires.

#### 7. Commands + Complete YAML (line-by-line)

**ServiceMonitor YAML**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app-monitor
  labels:
    release: prometheus # Must match Prometheus selector
spec:
  selector:
    matchLabels:
      app: my-app # Selects the Service of your app
  endpoints:
  - port: web # Port name on the Service
    path: /metrics # Path to scrape
    interval: 15s # How often to scrape
```

**PrometheusRule (Alerting) YAML**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: high-error-rate
spec:
  groups:
  - name: application-rules
    rules:
    - alert: HighHttpErrorRate # The name of the alert
      # PromQL: rate of 5xx errors > 5% over 5 minutes
      expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
      for: 5m # Must be failing for 5m before firing
      labels:
        severity: critical
      annotations:
        summary: "High error rate on {{ $labels.app }}"
        description: "Error rate is above 5% for the last 5 minutes."
```

**10 Essential PromQL Queries:**
1. **CPU utilization**: `rate(container_cpu_usage_seconds_total[5m])`
2. **Memory usage**: `container_memory_working_set_bytes`
3. **HTTP error rate**: `sum(rate(http_requests_total{status=~"5.*"}[5m])) by (service)`
4. **P99 latency**: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
5. **Pod restart rate**: `rate(kube_pod_container_status_restarts_total[5m])`
6. **HPA current vs desired**: `kube_hpa_status_current_replicas` vs `kube_hpa_spec_max_replicas`
7. **Node disk pressure**: `kube_node_status_condition{condition="DiskPressure",status="true"}`
8. **Request throughput**: `sum(rate(http_requests_total[1m])) by (service)`
9. **Container throttling**: `rate(container_cpu_cfs_throttled_seconds_total[5m])`
10. **OOMKill rate**: `rate(kube_pod_container_status_terminated_reason{reason="OOMKilled"}[5m])`

#### 8. Interview explanation
"Prometheus is a pull-based TSDB. It's highly reliable because it pulls data, meaning if the target is down, it knows immediately. PromQL allows dimensional querying using labels, which is vastly superior to hierarchical metric models (like StatsD). Counters measure cumulative events, while Histograms help calculate percentiles like P99."

#### 9. Common mistakes + Best practices
- **Mistake**: High Cardinality. Adding dynamic data (like user IDs) as labels. E.g., `http_requests{user_id="123"}`. This creates a new time series for EVERY user and will OOM kill Prometheus.
- **Best Practice**: Use alert inhibition (e.g., if Node is down, don't alert on Pods being down on that node).

#### 10. Troubleshooting
If metrics are missing, use PromQL `up{job="my-app"}`. If it's `0`, Prometheus can reach target. Check network policies and ServiceMonitor labels.

#### 11. Interview Q&A
**Q:** Why does Prometheus use a pull model instead of push?
**A:** Pull makes it easier to spot dead targets, prevents the monitoring system from being overwhelmed by a flood of pushed metrics, and makes local testing trivial (just curl the `/metrics` endpoint).

---

### SECTION 3: Grafana Dashboards

#### 1. Definition + Why it exists
Grafana is a visualization layer. Prometheus stores the numbers; Grafana makes them look pretty. It exists because raw JSON metric arrays are unreadable by humans during an outage.

#### 2. Real-world analogy
Prometheus is the engine's ECU gathering sensor data. Grafana is the speedometer and temperature gauge on your dashboard.

#### 3. ASCII diagram
```text
[ Prometheus TSDB ] ----( PromQL )----> [ Grafana Server ] ----( Web UI )----> [ SRE Engineer ]
[ Loki Logs ]       ----( LogQL )-----/
[ Tempo Traces ]    ----( TraceQL )--/
```

#### 4. Internal working
Grafana connects to Data Sources (Prometheus, Loki, Elasticsearch, PostgreSQL). You build Panels (graphs). Panels use queries (like PromQL) to fetch data and render it.

#### 5. Complete workflow
1. Add Prometheus as a Data Source in Grafana.
2. Create a Dashboard.
3. Add a Panel.
4. Write PromQL: `rate(http_requests_total[5m])`.
5. Save as code (JSON).

#### 6. Production use case
Amazon creates Golden Signal dashboards for every tier-1 service, providing a unified view of Latency, Traffic, Errors, and Saturation.

#### 7. Commands + Complete YAML (line-by-line)
Dashboards should be provisioned as code (GitOps).

**ConfigMap for Dashboard Provisioning**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-my-app
  labels:
    grafana_dashboard: "1" # Grafana sidecar looks for this label
data:
  my-app.json: |-
    {
      "title": "My App Dashboard",
      "panels": [
        {
          "type": "timeseries",
          "title": "Request Rate",
          "targets": [
            {
              "expr": "sum(rate(http_requests_total[1m]))",
              "legendFormat": "Requests / sec"
            }
          ]
        }
      ]
    }
```

#### 8. Interview explanation
"Grafana is our single pane of glass. We use Dashboard-as-code to version control our visualizations. We strictly follow the RED method (Rate, Errors, Duration) for services and the USE method (Utilization, Saturation, Errors) for infrastructure."

#### 9. Common mistakes + Best practices
- **Mistake**: "Spaghetti dashboards" with 50 unrelated panels that no one understands.
- **Best Practice**: Use Variables (templating) so one dashboard can serve all environments (dev/stage/prod) by simply changing a dropdown.

#### 10. Troubleshooting
If a panel says "No Data", check the time range, ensure the data source is connected, and verify the PromQL syntax directly in Prometheus.

#### 11. Interview Q&A
**Q:** What are the Golden Signals?
**A:** Latency (time to serve a request), Traffic (demand/throughput), Errors (rate of failed requests), and Saturation (how "full" the system is, e.g., CPU or DB connection pool).

---

### SECTION 4: Logging Stack

#### 1. Definition + Why it exists
Logs are text records of events. When you have 500 microservices across 50 nodes, SSHing into nodes to run `grep` is impossible. We need Log Aggregation.

#### 2. Real-world analogy
Imagine 500 diaries written by 500 different people. Log aggregation is a librarian who collects all the diaries every night, indexes them, and lets you search "who mentioned a dog" across all diaries instantly.

#### 3. ASCII diagram
```text
[ Pod 1 (stdout) ] --> ( Promtail DaemonSet ) \
[ Pod 2 (stdout) ] --> ( Promtail DaemonSet ) --> [ Loki (Indexer) ] --> [ Grafana (Search) ]
[ Pod 3 (stdout) ] --> ( Promtail DaemonSet ) /
```

#### 4. Internal working
- **Promtail**: Agent on every node. Reads `/var/log/containers/*.log`. Attaches Kubernetes labels (pod name, namespace).
- **Loki**: Datastore. Unlike Elasticsearch which indexes the *text* of the log (expensive), Loki only indexes the *metadata/labels* (cheap). The logs are stored compressed in S3/GCS.
- **LogQL**: Query language similar to PromQL.

#### 5. Complete workflow
1. App writes `{"level":"error", "msg":"DB timeout"}` to stdout.
2. Container runtime writes this to disk.
3. Promtail reads the file, attaches labels `{app="payment"}`, and sends to Loki.
4. Engineer queries `{app="payment"} |= "timeout"` in Grafana.

#### 6. Production use case
At Shopify, Black Friday generates petabytes of logs. Using Elasticsearch (EFK) would cost millions. They use Loki because indexing only labels allows massive, cheap ingestion.

#### 7. Commands + Complete YAML (line-by-line)

**Promtail ConfigMap snippet (How it maps labels)**
```yaml
scrape_configs:
- job_name: kubernetes-pods
  kubernetes_sd_configs:
  - role: pod # Discover pods
  relabel_configs:
  - source_labels: [__meta_kubernetes_pod_label_app]
    target_label: app # Attach the 'app' label to the log stream
```

**LogQL Examples:**
- Find errors: `{app="frontend"} |= "error"`
- Parse JSON and filter: `{app="backend"} | json | status > 500`
- Count errors over time (Metric query from logs): `sum(rate({app="backend"} |= "error" [5m]))`

#### 8. Interview explanation
"We chose Loki over EFK (Elasticsearch/Fluentd/Kibana) because Loki doesn't full-text index the logs. It indexes labels, just like Prometheus. This makes Loki highly cost-effective and perfectly integrated with Grafana and our existing Prometheus label taxonomy."

#### 9. Common mistakes + Best practices
- **Mistake**: Unstructured logging. `printf("User %s failed", name)` makes parsing hard.
- **Best Practice**: Structured logging. `logger.error("Auth failed", {"user": name, "status": 401})` outputted as JSON.
- **Best Practice**: Don't log PII (Passwords, Credit Cards).

#### 10. Troubleshooting
If logs are missing in Loki, check the Promtail pod logs. It might not have volume mounts configured correctly to read `/var/log/containers/` on the host node.

#### 11. Interview Q&A
**Q:** When would you use Elasticsearch over Loki?
**A:** If you need heavy, full-text search capabilities, complex log analytics, or are building a SIEM (Security Information and Event Management) system, Elasticsearch is better. For standard application debugging, Loki is cheaper and faster.

---

### SECTION 5: Distributed Tracing

#### 1. Definition + Why it exists
Logs tell you an error happened. Metrics tell you it happened 50 times. Traces tell you *where* it happened across a chain of microservices.

#### 2. Real-world analogy
Like a package tracking number (Trace ID). You can see every facility (Span) the package went through, how long it stayed there, and if it got delayed.

#### 3. ASCII diagram
```text
Trace ID: 12345
[ Frontend Span: 100ms ]
    |
    +-- [ Auth Service Span: 20ms ]
    |
    +-- [ Payment Service Span: 80ms ]
             |
             +-- [ Stripe API Span: 50ms ]
             |
             +-- [ DB Update Span: 20ms ]
```

#### 4. Internal working
- **Trace ID**: Unique ID for the entire request journey.
- **Span ID**: Unique ID for a specific operation.
- **Context Propagation**: The Trace ID is passed in HTTP headers (W3C `traceparent: 00-TraceID-SpanID-01`) from Service A to Service B.
- **OpenTelemetry (OTel)**: The industry standard SDK to generate these spans.

#### 5. Complete workflow
1. Request hits Gateway. Gateway generates Trace ID = X.
2. Gateway sends HTTP header `traceparent: X` to Auth.
3. Auth reads header X, does work, generates a Span, sends Span to OTel Collector asynchronously.
4. Auth calls DB, generates DB span, sends to Collector.
5. Collector batches spans and sends them to Tempo (Trace DB).

#### 6. Production use case
Netflix uses tracing to map their extremely complex microservice graphs. If playing a video is slow, a trace instantly shows that the `Subtitle-Service` is taking 500ms, immediately isolating the root cause.

#### 7. Commands + Complete YAML (line-by-line)

**OpenTelemetry Collector ConfigMap**
```yaml
receivers:
  otlp:
    protocols:
      grpc: # Receives traces from app SDKs
      http:

processors:
  batch: # Batches traces before exporting to save network overhead

exporters:
  otlp/tempo: # Sends traces to Tempo backend
    endpoint: tempo-server:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/tempo]
```

#### 8. Interview explanation
"We utilize OpenTelemetry for instrumentation to remain vendor-agnostic. Our services propagate W3C trace context headers. The OTel Collector receives spans via OTLP, batches them, and exports them to Grafana Tempo. We also inject the Trace ID into our JSON logs, allowing us to pivot seamlessly from a Log in Loki to a Trace in Tempo."

#### 9. Common mistakes + Best practices
- **Mistake**: Tracing 100% of requests. This costs a fortune.
- **Best Practice**: Sampling. **Head-based sampling** (randomly trace 1% of requests). **Tail-based sampling** (trace 100%, but keep them in Collector memory, and only export to Tempo if the trace contains an error or latency > 500ms).

#### 10. Troubleshooting
"Broken traces" (a trace that stops halfway). This means a service in the middle failed to propagate the `traceparent` header to its downstream calls.

#### 11. Interview Q&A
**Q:** What is the difference between Jaeger and Tempo?
**A:** Jaeger typically uses Elasticsearch or Cassandra for storage and indexes all traces. Tempo uses object storage (S3) and only indexes the Trace ID. Tempo is massively cheaper but requires you to find the Trace ID via Logs or Exemplars first.

---

### SECTION 6: SLO / SLI / SLA / Error Budget

#### 1. Definition + Why it exists
You can't have 100% uptime. It's too expensive. SLOs define exactly what level of failure is acceptable, bridging the gap between engineering and business.

#### 2. Real-world analogy
- **SLI (Indicator)**: The speedometer (I am driving at 60mph).
- **SLO (Objective)**: The speed limit (I should drive between 50-70mph 99% of the time).
- **SLA (Agreement)**: The speeding ticket (If I break the limit, I pay a fine).
- **Error Budget**: How many minutes I am allowed to speed this month without getting a ticket.

#### 3. ASCII diagram
```text
[ 100% ]
   |
   |   <--- Unnecessary perfection (Costs $$$$)
   |
[ 99.9% ] <--- SLO Target
   |
   |   <--- Error Budget (0.1% = 43.8 mins of allowed downtime/month)
   |
[ 0.0% ]
```

#### 4. Internal working
An SLI is a ratio: `Good Events / Total Events`.
Example: `HTTP 200s / Total HTTP Requests`.
If SLO is 99.9% over 30 days. You are allowed 0.1% failures.
If you burn through your budget in 2 days, you freeze feature development and focus on reliability.

#### 5. Complete workflow
1. Define SLI (Latency < 200ms).
2. Set SLO (99% over 28 days).
3. Calculate Error Budget.
4. Configure Prometheus to monitor the "Burn Rate" (how fast you are consuming the budget).
5. Alert if burn rate is so high that you will exhaust the 28-day budget in 2 hours.

#### 6. Production use case
Google SREs use Multi-Window Multi-Burn-Rate alerting. Instead of alerting when the SLO drops below 99% (too late), they alert if the budget is draining at 14x the normal speed for 1 hour.

#### 7. Commands + Complete YAML (line-by-line)

**SLO Alerting PrometheusRule (Burn Rate)**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-alerts
spec:
  groups:
  - name: SLO
    rules:
    - alert: ErrorBudgetBurnHigh
      # Burn rate > 14 (exhausts budget in ~2 days) over a 1 hour window
      expr: job:slo_errors_per_request:ratio_rate1h{job="my-app"} > (14 * 0.001) # 0.001 is 1 - 99.9%
      for: 5m
      labels:
        severity: page
      annotations:
        summary: "High Error Budget Burn Rate for {{ $labels.job }}"
```

#### 8. Interview explanation
"SLIs are the metrics we measure. SLOs are our internal goals. SLAs are legal contracts with customers. The Error Budget is 1 minus the SLO. We use error budgets to balance feature velocity with reliability; if the budget is exhausted, we stop shipping features and focus on tech debt."

#### 9. Common mistakes + Best practices
- **Mistake**: Setting an SLO of 100%. This is impossible and paralyzes development.
- **Best Practice**: Alert on Burn Rate, not absolute SLO breaches. 

#### 10. Troubleshooting
If your SLO alerts are flapping, your time windows might be too short. Use the multi-window approach (check 1h and 5m windows simultaneously).

#### 11. Interview Q&A
**Q:** What do you do when your error budget is depleted?
**A:** We enact an "error budget policy." Typically, this means halting all non-critical feature deployments and dedicating all engineering cycles to reliability improvements until the budget recovers (rolling window).

---

### SECTION 7: Root Cause Analysis (RCA)

#### 1. Definition + Why it exists
RCA is the structured process of finding the underlying cause of an incident so it never happens again.

#### 2. Real-world analogy
A doctor diagnosing a patient. 
Symptom: Fever (Alert). 
Metrics: Heart rate (Prometheus). 
Logs: Patient history (Loki). 
Traces: MRI scan (Tempo). 
Fix: Antibiotics (Rollback/Patch).

#### 3. Complete worked example: 500 error rate spike
1. **Symptom**: PagerDuty alerts: `HighHttpErrorRate` on `checkout-service`.
2. **Metrics**: Open Grafana. See `checkout-service` 5xx rate spiked at 14:00. CPU/Memory look fine.
3. **Traces**: Look at a Trace from 14:02. `checkout-service` span is fast, but it calls `payment-service` which takes 10,000ms and fails.
4. **Logs**: Query Loki for `payment-service` logs at 14:02. Log says: `FATAL: Connection pool exhausted to Database`.
5. **Fix**: Scale up `payment-service` replicas or increase DB connection pool limit.
6. **Post-Mortem**: Write a blameless document. Action item: Implement connection pooling proxy (PgBouncer).

#### 4. Grafana Unified Investigation
Because we embedded Trace IDs in our logs, we click a log line in Loki, and Grafana instantly opens the Tempo trace. Because Prometheus labels match Loki labels, we pivot from graphs to logs with one click.

---

## PART B: RESILIENCE ENGINEERING

### SECTION 8: Probes Deep Dive

#### 1. Definition + Why it exists
Kubernetes needs to know the health of your application to route traffic and restart dead processes. Probes are Kubernetes' way of checking your app's pulse.

#### 2. Real-world analogy
- **Liveness**: "Are you breathing?" If not, I will shock you with a defibrillator (restart pod).
- **Readiness**: "Are you ready to take an order?" If not, I will take you off the floor, but I won't kill you (remove from Service endpoints).
- **Startup**: "Are you done putting on your uniform?" (Delays other probes for slow-starting apps).

#### 3. ASCII diagram
```text
Kubelet ---> [ Startup Probe ] --(Pass)--> [ Readiness Probe ] ---> (Traffic flows from Service)
                                    \
                                     +---> [ Liveness Probe ] --(Fail x3)--> (Restart Container)
```

#### 4. Internal working
The Kubelet on the node executes the probe. It can be an HTTP GET request, a TCP socket check, or a shell command (`exec`).

#### 5. Complete workflow
1. Pod starts.
2. Startup probe runs every 10s. Succeeds after 30s.
3. Readiness probe runs every 5s. Succeeds. Pod added to Service endpoints. Traffic arrives.
4. App deadlocks. Liveness probe fails 3 times. Kubelet kills container.
5. Container restarts.

#### 6. Production use case
A Java Spring Boot app takes 60 seconds to boot. Without a `startupProbe`, a strict `livenessProbe` might kill it after 30 seconds, putting it in a crash loop forever.

#### 7. Commands + Complete YAML (line-by-line)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resilient-app
spec:
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:v1
        # Startup: Wait up to 30 * 10s = 5 minutes for legacy apps to start
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8080
          failureThreshold: 30
          periodSeconds: 10
        # Readiness: Fails? Stop sending traffic.
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        # Liveness: Fails? Restart container.
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 15
          failureThreshold: 3 # Fail 3 times before restarting
```

#### 8. Interview explanation
"We strictly separate Liveness and Readiness. Liveness should only fail if the app is unrecoverably deadlocked. Readiness should fail if the app is temporarily overwhelmed, cannot connect to its database, or is warming up caches. Using the same endpoint for both is an anti-pattern that leads to cascading failures during DB outages."

#### 9. Common mistakes + Best practices
- **Mistake**: Making Liveness probe check database connectivity. If the DB goes down, K8s will restart ALL your pods. Restarting doesn't fix a broken DB.
- **Best Practice**: Liveness should be a dumb "thread is not blocked" check. Readiness should check downstream dependencies.

#### 10. Troubleshooting
If pods keep restarting (`CrashLoopBackOff` or high restart count), `kubectl describe pod <name>` and look at Events at the bottom for `Liveness probe failed: HTTP status 500`.

#### 11. Interview Q&A
**Q:** When would readiness fail but liveness pass?
**A:** When the application is running fine but its downstream database connection is temporarily lost. It shouldn't be restarted (liveness pass), but it shouldn't receive user traffic (readiness fail).

---

### SECTION 9: Graceful Shutdown

#### 1. Definition + Why it exists
When you deploy a new version, scale down, or drain a node, Kubernetes kills pods. If it kills them violently (SIGKILL), any in-flight HTTP requests or database transactions are abruptly dropped, causing 500 errors for users.

#### 2. Real-world analogy
A store closing.
**Violent**: Manager screams "GET OUT!" and turns off the lights while you are at the register.
**Graceful**: Manager locks the front door (no new customers), lets people in line finish checking out, then turns off the lights.

#### 3. ASCII diagram
```text
K8s API -> "Delete Pod"
  |
  +-> 1. Endpoint Controller removes pod from Service (stops new traffic)
  |
  +-> 2. Kubelet sends SIGTERM to Pod
           |
           +-> App catches SIGTERM, finishes active requests.
           |
  +-> 3. (After grace period) Kubelet sends SIGKILL (die immediately)
```

#### 4. Internal working
Because of network propagation delays, Step 1 and Step 2 happen in parallel. This means the app might receive SIGTERM *before* kube-proxy updates iptables to stop routing traffic to it. The app must wait a few seconds before shutting down.

#### 5. Complete workflow
1. Add a `preStop` hook to sleep for 5-10 seconds. (Allows iptables to update globally).
2. App receives SIGTERM.
3. App stops accepting new connections but finishes existing ones (Connection Draining).
4. App exits gracefully with code 0.

#### 6. Production use case
Without graceful shutdown, every deployment at Netflix would drop thousands of user video streams. 

#### 7. Commands + Complete YAML (line-by-line)
```yaml
spec:
  containers:
  - name: node-app
    image: node-app:v1
    lifecycle:
      preStop:
        exec:
          # Sleep for 10s to ensure kube-proxy has time to remove this pod 
          # from network rules BEFORE the app stops accepting traffic.
          command: ["/bin/sh", "-c", "sleep 10"]
    # Give the app up to 60 seconds to finish in-flight requests
    terminationGracePeriodSeconds: 60
```
*(In your app code, you must trap SIGTERM!)*
```javascript
// Node.js example
process.on('SIGTERM', () => {
  server.close(() => {
    console.log('Finished all requests');
    process.exit(0);
  });
});
```

#### 8. Interview explanation
"Kubernetes termination is asynchronous. We use a `preStop` sleep hook to mitigate the race condition between the Kubelet sending SIGTERM and the Endpoint controller updating kube-proxy across the cluster. We also configure our frameworks (like Tomcat or Uvicorn) to drain connections on SIGTERM, and extend `terminationGracePeriodSeconds` beyond the default 30s for long-running websocket servers."

#### 9. Common mistakes + Best practices
- **Mistake**: Using PID 1 as a shell script that doesn't forward signals. If `entrypoint.sh` doesn't `exec` the app, the shell absorbs the SIGTERM, the app ignores it, and 30 seconds later it gets SIGKILL'd violently.
- **Best Practice**: Use `exec` in your Dockerfile `ENTRYPOINT`.

#### 10. Troubleshooting
If users see 502/503 errors exactly during a deployment rollout, your graceful shutdown is broken.

#### 11. Interview Q&A
**Q:** What happens exactly when Kubernetes deletes a pod?
**A:** Two parallel tracks start. The Control Plane removes the pod from the Endpoints object, which propagates to kube-proxy on all nodes. Simultaneously, the node's Kubelet runs the preStop hook, then sends a SIGTERM. After `terminationGracePeriodSeconds`, it sends a SIGKILL.

---

### SECTION 10: Autoscaling (HPA, VPA, Cluster Autoscaler)

#### 1. Definition + Why it exists
Traffic is not static. If you provision for peak traffic, you waste money. If you provision for average traffic, you crash during peaks. Autoscalers adjust capacity dynamically.

#### 2. Real-world analogy
- **HPA (Horizontal Pod Autoscaler)**: Hiring more cashiers when the line gets long (more pods).
- **VPA (Vertical Pod Autoscaler)**: Giving an existing cashier a faster scanner and an energy drink (more CPU/RAM for the pod).
- **Cluster Autoscaler**: Building a new physical store building because you hired too many cashiers and ran out of floor space (adding EC2/GCE nodes).

#### 3. Complete workflow (The Autoscaling Trinity)
1. CPU spikes to 80%.
2. **HPA** sees CPU > 50% target. HPA scales deployment from 2 to 5 pods.
3. Node is full. 3 new pods are `Pending`.
4. **Cluster Autoscaler** sees `Pending` pods due to insufficient CPU on nodes.
5. Cluster Autoscaler talks to AWS Auto Scaling Group to spin up a new EC2 instance.
6. Node joins, pods are scheduled.

#### 4. Commands + Complete YAML (line-by-line)

**HPA YAML**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60 # Scale out if avg CPU across pods > 60%
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300 # Wait 5 mins before scaling down (prevents thrashing)
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

#### 5. Common mistakes + Best practices
- **Mistake**: Running HPA and VPA on the same metric (CPU/Memory). They will fight each other. VPA will increase the pod's requested CPU, which drops the utilization percentage, causing HPA to scale down.
- **Best Practice**: Use KEDA (Kubernetes Event-driven Autoscaling) to scale based on external metrics, like "Messages in a Kafka topic" or "SQS queue depth."

---

### SECTION 11: Pod Disruption Budget (PDB)

#### 1. Definition + Why it exists
Autoscalers and humans (draining nodes for upgrades) cause "voluntary disruptions." A PDB tells Kubernetes: "You can move my pods around, but NEVER let available pods drop below this number."

#### 2. Real-world analogy
A hospital must have at least 2 doctors on duty. The doctors can swap shifts, take breaks, or switch rooms (disruptions), but the scheduler (Kubernetes) is legally forbidden from letting the number of active doctors drop below 2.

#### 3. Commands + Complete YAML (line-by-line)
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: zookeeper-pdb
spec:
  # Require at least 2 pods running at all times
  minAvailable: 2 
  selector:
    matchLabels:
      app: zookeeper
```

#### 4. Interview Q&A
**Q:** If your PDB has `minAvailable: 1` and only 1 pod is currently running, what happens when you try to drain the node it runs on?
**A:** The `kubectl drain` command will block indefinitely. Kubernetes will refuse to evict the pod because doing so would drop the available count to 0, violating the PDB.

---

### SECTION 12: Resilience Patterns (Code Level)

#### 1. Circuit Breaker
If a downstream service is failing, stop calling it immediately. Give it time to recover instead of hammering it.
- **Closed**: Requests flow normally.
- **Open**: Failures exceeded threshold. Requests fail fast instantly without hitting network.
- **Half-Open**: Let 1 request through to test if service recovered.

#### 2. Retry with Exponential Backoff and Jitter
If network fails, retry. But don't retry immediately. Wait 1s, 2s, 4s, 8s (Exponential). Add random Jitter (e.g., 2.3s, 4.1s) so thousands of clients don't all retry at the exact same millisecond and cause a thundering herd.

#### 3. Bulkhead
Isolate failures. If the Image Upload service uses up all connection threads, it shouldn't crash the Text Chat service in the same app. Separate their thread pools. (Like bulkheads in a submarine—if one compartment floods, the ship survives).

#### 4. Load Shedding
When the server is absolutely overwhelmed, it should explicitly drop cheap/unimportant requests to save capacity for critical requests. Better to return 503 to 20% of users than crash and return 500 to 100% of users.

---

### SECTION 13: Service Mesh (Istio)

#### 1. Definition + Why it exists
Implementing retries, circuit breakers, mTLS, and distributed tracing in application code for 10 different languages is a nightmare. A Service Mesh injects a sidecar proxy (Envoy) next to every pod to handle this transparently at the network layer.

#### 2. Real-world analogy
Instead of teaching every citizen (service) to encrypt messages and handle routing, you assign a bodyguard (Envoy sidecar) to every citizen. Citizens just talk; the bodyguards intercept, encrypt, and route the traffic.

#### 3. Complete YAML (VirtualService for Canary and Circuit Breaking)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 90 # Route 90% traffic to v1
    - destination:
        host: reviews
        subset: v2
      weight: 10 # Route 10% traffic to v2 (Canary)
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: 5xx
```

---

### SECTION 14: Chaos Engineering

#### 1. Definition + Why it exists
You don't know if your resilience patterns (PDBs, HPA, Circuit Breakers) work until they are tested in production. Chaos engineering is the discipline of intentionally injecting failure to prove the system survives.

#### 2. Production use case
Netflix Chaos Monkey kills random EC2 instances in production during business hours. Because engineers know this happens, they build stateless, highly available systems by default.

#### 3. Complete YAML (Chaos Mesh Network Delay)
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: delay-database
spec:
  action: delay # Inject network latency
  mode: all
  selector:
    namespaces:
      - production
    labelSelectors:
      app: mysql
  delay:
    latency: "200ms"
    correlation: "100"
  duration: "10m" # Run experiment for 10 minutes
```
**Hypothesis**: The frontend circuit breaker will trip, and the fallback cache will be served.
**Result**: Measure MTTR (Mean Time To Recovery). Did alerts fire?

---

### SECTION 15: Multi-Region and Disaster Recovery

#### 1. Active-Active vs Active-Passive
- **Active-Active**: Traffic served from us-east-1 and us-west-2 simultaneously. Complex DB replication (CRDTs or Spanner). Zero downtime.
- **Active-Passive**: us-east-1 takes all traffic. us-west-2 database is a read-replica. If east fails, manual failover promotes west DB to master and flips DNS. Cheaper, but has downtime.

#### 2. RTO and RPO
- **RTO (Recovery Time Objective)**: How long can you afford to be down? (e.g., "Must be back up in 4 hours").
- **RPO (Recovery Point Objective)**: How much data can you afford to lose? (e.g., "Max 15 minutes of data loss").

---

## END OF CHAPTER

### Complete Cheat Sheet
- **Prometheus**: Pulls metrics. PromQL. Use for alerting.
- **Grafana**: Dashboards. RED/USE methods.
- **Loki**: Log aggregation. Indexes labels, not text.
- **Tempo/Jaeger**: Traces. Find latency bottlenecks.
- **SLO/Error Budgets**: Mathematical approach to reliability.
- **Probes**: Liveness (restart), Readiness (route traffic), Startup (wait).
- **Graceful Shutdown**: SIGTERM -> preStop -> drain -> SIGKILL.
- **HPA/VPA**: Scale pods out/up.
- **PDB**: Prevent voluntary eviction of all pods.
- **Service Mesh**: Decouple resilience/security from app code.

### Mini Project
**Goal:** Deploy a complete stack.
1. Run `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
2. Install `kube-prometheus-stack` (installs Prometheus, Grafana, Alertmanager).
3. Install `loki-stack` (installs Promtail and Loki).
4. Deploy a sample Node.js app with `/metrics` endpoint.
5. Create a `ServiceMonitor` to scrape it.
6. Write a `PrometheusRule` that alerts if error rate > 5%.
7. Use Chaos Mesh to inject a `PodChaos` (kill the pod).
8. Observe the alert firing in Alertmanager and the pod restarting via ReplicaSet.
