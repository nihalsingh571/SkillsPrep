# Chapter 1: Master Helm - The Kubernetes Package Manager

Welcome! If you're reading this, you probably know how to write a basic Kubernetes `Deployment` or `Service`. You can run `kubectl apply -f deployment.yaml` and watch your pods spin up. But what happens when you have 50 microservices? What happens when you need to deploy the *exact same* application to Dev, Staging, and Production, but with slightly different configurations (like different CPU limits, different database URLs, or different replicas)?

Do you copy and paste your YAML files 50 times? Do you maintain `deployment-dev.yaml`, `deployment-staging.yaml`, `deployment-prod.yaml`?

That way lies madness. And that is exactly why Helm exists.

In this chapter, we're going to break down Helm from zero to production. We will use the Feynman technique: explaining complex concepts in simple, everyday language before diving into the hardcore technical details. By the end of this chapter, you won't just know how to use Helm; you'll understand *how it thinks*, how to design production architectures with it, and how to ace any FAANG interview question about it.

---

## SECTION 1: What is Helm?

### 1. Definition
Helm is the package manager for Kubernetes. Just like `apt` is for Ubuntu, `yum` is for CentOS, `npm` is for Node.js, or `pip` is for Python, Helm is for Kubernetes. It allows you to package, configure, and deploy complex Kubernetes applications easily.

### 2. Why this concept exists / Problem it solves
Imagine you want to install WordPress on Kubernetes. WordPress isn't just one pod. It's a Deployment for the web server, a StatefulSet for the MySQL database, a Service to expose it, an Ingress for routing, a Secret for passwords, a ConfigMap for settings, and maybe a PersistentVolumeClaim for storage.
Without Helm, you'd have to find or write 7+ complex YAML files, modify them manually for your cluster, and run `kubectl apply` on all of them in the correct order.

With Helm, you simply run:
`helm install my-blog bitnami/wordpress`

Helm solves three massive problems:
1.  **Complexity:** Packages all Kubernetes resources into one logical unit.
2.  **Reusability:** Instead of copying YAMLs, you use one template and pass variables (values) to it.
3.  **Lifecycle Management:** Helm tracks what it installed. You can upgrade, rollback, or completely uninstall an entire application with a single command.

### 3. Real-world analogy
Think of buying a car.
**Without Helm:** You go to a factory and manually buy 4 wheels, a steering wheel, an engine, seats, and doors. Then you read a manual and bolt them all together yourself in your garage. If you want a different color, you have to buy entirely new doors and swap them manually.
**With Helm:** You go to a dealership (Helm Repository), pick a model (Helm Chart), choose your options like color and engine size (Values), and they hand you the keys to a fully assembled, working car (Release).

### 4. ASCII architecture diagram

```text
+-------------------+        +--------------------+
|                   |        |                    |
|   Helm Client     |        |   Helm Repository  |
|  (Your Laptop/CI) | <----> |   (e.g., Artifact  |
|                   |        |    Hub, AWS ECR)   |
+--------+----------+        +--------------------+
         |
         | (gRPC / Kubernetes API)
         v
+-------------------------------------------------+
|               Kubernetes Cluster                |
|                                                 |
|  +----------------+      +-------------------+  |
|  |                |      |                   |  |
|  |   Secret       |      |  Deployed K8s     |  |
|  | (Helm Release  | <--- |  Resources        |  |
|  |  State - v1)   |      | (Pods, Svc, etc.) |  |
|  +----------------+      +-------------------+  |
|                                                 |
+-------------------------------------------------+
```

### 5. Internal working
When you run `helm install`, Helm does the following:
1.  Downloads the **Chart** (the templates).
2.  Merges your custom **Values** (configurations) into those templates.
3.  **Renders** the final, plain Kubernetes YAML.
4.  Sends the YAML to the Kubernetes API server.
5.  Stores a record of this installation (a **Release**) as a Kubernetes Secret in the namespace where the app was deployed.

### 6. Complete workflow
1. Add a repo: `helm repo add bitnami https://charts.bitnami.com/bitnami`
2. Search for a chart: `helm search repo nginx`
3. Customize it: Create a `my-values.yaml` file.
4. Install it: `helm install my-web bitnami/nginx -f my-values.yaml`
5. Upgrade it: `helm upgrade my-web bitnami/nginx -f my-values-v2.yaml`
6. Rollback if broke: `helm rollback my-web 1`

### 7. Production use case
At **Netflix**, they have thousands of microservices. Each microservice doesn't write its own raw Kubernetes YAML. The platform team maintains a standard "Netflix Microservice" Helm chart. Every team just provides a small `values.yaml` specifying their image name, port, and required CPU/RAM. Helm templates handle the rest, ensuring every app complies with Netflix's security and routing standards.

### 8. Step-by-step example (Helm 2 vs Helm 3)
*Note on History:* If you read old tutorials, you'll see mention of **Tiller**.
*   **Helm 2:** Had a client (helm) and an in-cluster server component called Tiller. Tiller ran as a pod with root-level cluster permissions to install things. This was a massive security nightmare.
*   **Helm 3 (Current):** Tiller is dead. Helm is now just a client-side binary. It uses your `kubeconfig` to talk directly to the Kubernetes API, inheriting your exact RBAC permissions. If you can't create a namespace, Helm can't either. It stores state in standard K8s Secrets.

### 9. Commands
*   `helm version` - Check what version you are running (should be v3+).

### 10. Complete YAML/config (line-by-line explained)
N/A for this high-level section.

### 11. Interview explanation
**"Explain Helm to me like I'm 5."**
"Helm is the package manager for Kubernetes. Instead of manually writing and applying dozens of YAML files to deploy an application, Helm groups them into a reusable package called a Chart. It uses a templating engine, so you can deploy the exact same Chart to dev, staging, and prod just by injecting different variables. Helm also tracks deployments, allowing for 1-click upgrades and rollbacks."

### 12. Common mistakes
*   Assuming Helm is an operator. Helm does not run in the cluster watching for changes. It runs once when you type the command, applies the YAML, and exits. If someone manually deletes a pod via kubectl, Helm won't automatically recreate it (Kubernetes controllers do that).

### 13. Best practices
*   Always use Helm 3.
*   Treat Helm charts as code: version control them in Git.

### 14. Production recommendations
*   Don't use `helm install` from developer laptops for production. Have a CI/CD pipeline (like GitHub Actions or Jenkins) run the helm commands, or better yet, use GitOps tools like ArgoCD.

### 15. Troubleshooting guide
*   *Error: Kubernetes cluster unreachable* -> Check your `~/.kube/config` or `KUBECONFIG` env var. Helm uses the exact same config as kubectl.

### 16. Advanced concepts
*   **Helm State Storage:** By default, Helm 3 stores the release history in K8s Secrets (`sh.helm.release.v1.my-release.v1`). You can change this to ConfigMaps or even an external SQL database, though Secrets is the production standard.

### 17. Frequently asked interview questions with answers
**Q: Why was Tiller removed in Helm 3?**
A: Tiller required cluster-admin permissions to deploy anything anywhere. In a multi-tenant cluster, a user with access to Tiller could escalate privileges and deploy resources in namespaces they shouldn't have access to. Removing it aligned Helm with standard Kubernetes RBAC.

### 18. Scenario-based interview questions with answers
**Q: A developer manually edits a Deployment via `kubectl edit` that was originally deployed by Helm. What happens on the next `helm upgrade`?**
A: Helm performs a three-way merge patch. It compares the old chart state, the new chart state, and the *current live state* in the cluster. Depending on what exactly was changed, Helm will try to reconcile it to the new chart state, effectively overwriting the manual `kubectl edit`. This is why you should never manually edit Helm-managed resources.

---

## SECTION 2: Chart Structure

### 1. Definition
A **Chart** is a collection of files that describe a related set of Kubernetes resources. A chart is organized as a directory.

### 2. Why this concept exists / Problem it solves
Kubernetes needs structure. If you just had a folder of 100 YAML files, how do you know what version the app is? What variables it needs? A Chart provides a standard filesystem layout that the Helm engine knows how to read.

### 3. Real-world analogy
A Chart is like a recipe book for a specific dish. `Chart.yaml` is the title and author. `values.yaml` is the default list of ingredients. The `templates/` folder contains the actual cooking instructions (with blanks for the ingredients).

### 4. ASCII architecture diagram

```text
mychart/
|-- Chart.yaml       (Metadata: Name, version, description)
|-- values.yaml      (Default configuration values)
|-- charts/          (Dependencies/Subcharts live here)
|-- templates/       (The magic happens here: K8s YAML + Go Templates)
|   |-- deployment.yaml
|   |-- service.yaml
|   |-- _helpers.tpl (Reusable template blocks)
|   |-- NOTES.txt    (Instructions printed after install)
|-- .helmignore      (Files to exclude when packaging)
```

### 5. Internal working
When Helm loads a chart, it reads `Chart.yaml` to validate it. It then loads `values.yaml`. Finally, it iterates through every file in `templates/` that ends in `.yaml`, `.yml`, or `.tpl`, passes the values into them, and generates the final manifests.

### 6. Complete workflow
Run `helm create my-app`. This instantly scaffolds a perfectly formatted chart directory following best practices.

### 7. Production use case
At **Uber**, developers don't build charts from scratch. The platform team runs a generator that outputs this exact structure, pre-filled with Uber's specific security policies and sidecar configurations in the `templates/` directory.

### 8. Step-by-step example
Let's look at the core files.

### 9. Commands
*   `helm create mychart`

### 10. Complete YAML/config (line-by-line explained)

**Chart.yaml**
```yaml
apiVersion: v2             # REQUIRED: API version. Helm 3 requires 'v2'.
name: my-web-app           # REQUIRED: The name of the chart.
description: A Helm chart for our Node.js API # OPTIONAL: 1-sentence description.
type: application          # OPTIONAL: 'application' (deployable) or 'library' (reusable helpers).
version: 1.0.0             # REQUIRED: SemVer version of the CHART itself (changes when you modify templates).
appVersion: "1.16.0"       # OPTIONAL: Version of the actual APP inside the chart (e.g., Node app version).
dependencies:              # OPTIONAL: Other charts this chart relies on (e.g., a database).
  - name: postgresql
    version: 12.1.0
    repository: https://charts.bitnami.com/bitnami
```

**values.yaml (Design Pattern)**
```yaml
# This is a flat, simple structure.
replicaCount: 2

image:
  repository: nginx # Group related configs under logical blocks
  pullPolicy: IfNotPresent
  tag: "1.21"

service:
  type: ClusterIP
  port: 80
```

**templates/NOTES.txt**
```text
Thank you for installing {{ .Chart.Name }}.
Your release is named {{ .Release.Name }}.
To access your app:
  kubectl port-forward svc/{{ .Release.Name }}-{{ .Chart.Name }} 8080:80
```
*(This gets printed to the terminal after a successful install, providing customized instructions based on what the user named their release).*

### 11. Interview explanation
"A Helm Chart is simply a directory with a specific structure. `Chart.yaml` contains metadata like the version. `values.yaml` holds the default configurations. The `templates/` directory contains Kubernetes YAML files infused with Go text templates. When installed, Helm combines the values with the templates to output standard Kubernetes manifests."

### 12. Common mistakes
*   Confusing `version` and `appVersion` in `Chart.yaml`. `version` must follow Semantic Versioning (1.0.1) and gets incremented when you change the Helm YAMLs. `appVersion` is just a string (like a git commit hash) representing the code version of the app running in the container.

### 13. Best practices
*   Use `.helmignore` to exclude `.git`, `.DS_Store`, and large local files. This keeps the packaged chart tiny.
*   Keep `values.yaml` clean and heavily commented. It is the public API of your chart for your users.

### 14. Production recommendations
*   Never hardcode values in `templates/`. If it can change per environment, it belongs in `values.yaml`.

### 15. Troubleshooting guide
*   If your chart isn't rendering a specific file, ensure it's inside `templates/` and ends in `.yaml`, not `.txt` (unless it's NOTES.txt).

### 16. Advanced concepts
*   **_helpers.tpl:** Files starting with an underscore (`_`) are not rendered into Kubernetes manifests. They are used solely to define reusable template logic (like standard naming conventions) that other templates can import.

### 17. Frequently asked interview questions with answers
**Q: What is the purpose of the `.helmignore` file?**
A: Similar to `.gitignore`, it tells Helm which files in the chart directory to skip when packaging the chart into a `.tgz` archive. This saves space and prevents sensitive local files from being uploaded to a chart repository.

### 18. Scenario-based interview questions with answers
**Q: Your team wants to standardize the labels applied to every single resource (Deployments, Services, ConfigMaps) across 50 different microservice charts. How do you do this without copy-pasting the label logic into every file?**
A: We define a named template block in `_helpers.tpl` that outputs the standard labels. Then, in every YAML file in the `templates/` directory, we use the `include` function to inject that block.

---

## SECTION 3: Template Rendering Engine

### 1. Definition
Helm uses the **Go text/template** engine under the hood. It allows you to inject variables, use conditionals (if/else), loops (range), and functions inside what looks like standard YAML.

### 2. Why this concept exists / Problem it solves
YAML is static. If you write `replicas: 3`, it's forever 3. The templating engine makes YAML dynamic. It turns YAML into a basic programming language.

### 3. Real-world analogy
Think of a Mad Libs game.
"The ___(adjective)___ dog jumped over the ___(noun)___."
The sentence is the Template. The blank spaces are the Go template syntax `{{ }}`. The words you fill in are the Values.

### 4. ASCII architecture diagram

```text
+----------------+      +----------------+
| templates/     |      | values.yaml    |
| deploy.yaml    |      | (or --set)     |
| replicas:      |      | replicaCount: 5|
| {{ .Values.r }}|      +-------+--------+
+-------+--------+              |
        |                       |
        v                       v
+----------------------------------------+
|           HELM RENDER ENGINE           |
|         (Go text/template)             |
+-------------------+--------------------+
                    |
                    v
+----------------------------------------+
|          FINAL K8S YAML                |
|          replicas: 5                   |
+----------------------------------------+
```

### 5. Internal working
Everything inside double curly braces `{{ }}` is evaluated by Helm. Everything outside is treated as plain text. The engine starts with a "root context" represented by a dot (`.`).

### 6. Complete workflow
1. You write `{{ .Values.image.repository }}`.
2. Helm looks at the root `.`.
3. It accesses the `Values` object.
4. It traverses down to `image` then `repository`.
5. It replaces the `{{ }}` block with the actual string.

### 7. Production use case
Setting resource limits dynamically based on the environment. Dev gets 100m CPU, Prod gets 2000m CPU. The template stays identical.

### 8. Step-by-step example
Understanding the Built-in Objects.
Helm provides several objects automatically at the root (`.`):
*   `.Release`: Details about the installation (e.g., `.Release.Name`, `.Release.Namespace`, `.Release.IsUpgrade`).
*   `.Chart`: Details from `Chart.yaml` (e.g., `.Chart.Name`, `.Chart.Version`).
*   `.Values`: Values passed from `values.yaml` or user overrides.
*   `.Capabilities`: Info about what the Kubernetes cluster supports (e.g., `.Capabilities.KubeVersion`).

### 9. Commands
*   `helm template my-release ./mychart` - This is your best friend. It runs the engine and prints the YAML to the screen *without* sending it to Kubernetes. Great for testing.

### 10. Complete YAML/config (line-by-line explained)

**templates/deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  # .Release.Name is the name you type in 'helm install <NAME>'
  # .Chart.Name is the name from Chart.yaml
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  namespace: {{ .Release.Namespace }}
spec:
  # Navigates the Values object. If replicaCount is missing, it will error unless defaulted.
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: app
          # Pipelines! Take the value, and pass it to the 'quote' function
          # If tag is 1.0, it becomes "1.0". Critical for YAML parsing (strings vs floats).
          image: {{ .Values.image.repository }}:{{ .Values.image.tag | quote }}
```

**Variables in templates:**
You can assign variables using `$`:
```yaml
{{- $relName := .Release.Name -}}
name: {{ $relName }}-app
```
*(The `-` inside the curly braces strips whitespace/newlines. `{{-` strips leading whitespace, `-}}` strips trailing whitespace. This is crucial for valid YAML formatting).*

### 11. Interview explanation
"Helm uses Go text templates to generate Kubernetes YAML. It evaluates expressions enclosed in double curly braces `{{ }}`. You access data through built-in objects starting with a dot, representing the root context. For example, `.Values` accesses user-defined configurations, and `.Release` accesses deployment metadata."

### 12. Common mistakes
*   Forgetting that the dot `.` changes context inside a `range` loop or `with` block. This is the #1 cause of Helm errors! (More on this in Flow Control).

### 13. Best practices
*   Always use `| quote` for image tags and versions. If a tag is `1.20` and you don't quote it, YAML parsers might read it as a floating-point number, stripping the trailing zero to `1.2`, which breaks your image pull.

### 14. Production recommendations
*   Use `helm template` in your CI/CD pipelines as a validation step before attempting `helm install`.

### 15. Troubleshooting guide
*   Error: `nil pointer evaluating interface {}` -> You are trying to access a nested value in `.Values` that doesn't exist. e.g., `.Values.app.name`, but `app` isn't defined in `values.yaml`.

### 16. Advanced concepts
*   **Pipelines:** Just like bash piping (`ls | grep`), Helm templates use `|` to chain functions.
    `{{ .Values.name | upper | quote }}` -> "MY-APP"

### 17. Frequently asked interview questions with answers
**Q: What is the difference between `.Release.Name` and `.Chart.Name`?**
A: `.Chart.Name` is hardcoded in the `Chart.yaml` file (e.g., "nginx"). `.Release.Name` is the arbitrary name the user gives this specific installation at deploy time (e.g., `helm install my-cool-blog nginx`, where "my-cool-blog" is the Release Name).

### 18. Scenario-based interview questions with answers
**Q: You see the syntax `{{- .Values.foo -}}`. What do the dashes do, and why are they necessary in Helm?**
A: The dashes are whitespace control modifiers. `{{-` removes all whitespace to the left, and `-}}` removes all whitespace to the right, including newlines. Because YAML is extremely strict about indentation, if a Go template renders an empty newline, it can break the entire YAML structure. Dash modifiers keep the YAML neat and valid.

---

## SECTION 4: All Template Functions

### 1. Definition
Helm includes over 60 built-in functions (mostly imported from the Sprig template library) to manipulate data inside your templates.

### 2. Why this concept exists / Problem it solves
Sometimes `values.yaml` has raw data, but Kubernetes requires it in a specific format (e.g., Kubernetes Secrets require Base64 encoding). Functions bridge this gap during rendering.

### 3. Real-world analogy
Functions are like kitchen appliances. You have raw ingredients (Values). You need chopped ingredients. You put them through the food processor (Function).

### 4. ASCII architecture diagram
N/A - Function processing is internal.

### 5. Internal working
Functions are invoked either prefix style: `functionName arg1 arg2` or pipeline style: `arg1 | functionName arg2`.

### 6. Complete workflow
Let's review the critical functions you MUST know for production and interviews.

### 7. Production use case
Generating dynamic Kubernetes Secrets securely during deployment by converting raw passwords to Base64 on the fly.

### 8. Step-by-step example (The Master List)

*   **String Manipulation:**
    *   `quote`: Adds double quotes. `{{ .Values.version | quote }}` -> `"1.0"`
    *   `upper` / `lower`: Changes case.
    *   `trim`, `trimPrefix`, `trimSuffix`: Removes characters. `{{ trimPrefix "v" "v1.0" }}` -> `1.0`

*   **Defaults and Safety:**
    *   `default`: Provides a fallback if the value is empty/null.
        `replicas: {{ .Values.replicas | default 3 }}`
    *   `required`: Fails the chart rendering immediately if a value is missing, with a custom error message. (CRITICAL for production).
        `password: {{ required "You MUST provide a db.password!" .Values.db.password }}`

*   **Indentation (Crucial for YAML):**
    *   `indent`: Indents a block of text by X spaces.
    *   `nindent`: Adds a newline, THEN indents by X spaces. (Always use this over `indent`).
        ```yaml
        annotations:
          {{- toYaml .Values.annotations | nindent 4 }}
        ```

*   **Type Conversion:**
    *   `toYaml` / `fromYaml`: Converts maps/lists to YAML strings. Very common for rendering arbitrary blocks of user config.
    *   `toJson` / `fromJson`: Same, but for JSON.

*   **Security (Encoding):**
    *   `b64enc`: Base64 encodes a string. Perfect for K8s Secrets.
        `password: {{ .Values.db.pass | b64enc }}`
    *   `b64dec`: Decodes.

*   **Data Structures:**
    *   `list`, `dict`: Create lists or dictionaries inline.
    *   `keys`, `values`: Extract keys or values from a dictionary.
    *   `hasKey`: Checks if a dictionary has a specific key.

*   **Cluster Interaction (Advanced):**
    *   `lookup`: Allows Helm to query the *live* Kubernetes API during rendering to see if a resource exists. (e.g., "Don't create a Secret if it already exists in the cluster").
        `{{ $mySecret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}`

*   **Template Rendering (The big ones):**
    *   `include`: Evaluates a named template and returns the output as a string. Can be pipelined. (Use this 99% of the time).
        `{{ include "mychart.labels" . }}`
    *   `template`: Same as include, but CANNOT be pipelined. (Legacy, avoid).
    *   `tpl`: Evaluates a string as if it were a Go template. Useful if your user puts Go template syntax *inside* their `values.yaml`!
    *   `printf`: Formats strings similar to C's printf. `{{ printf "app-%s" .Values.name }}`

### 9. Commands
N/A - Used inside templates.

### 10. Complete YAML/config (line-by-line explained)

**templates/secret.yaml**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # 1. required: Ensure user provided password.
  # 2. b64enc: Convert it to base64 for K8s.
  # 3. quote: Ensure it's treated as a string.
  db-password: {{ required "DB Password required!" .Values.db.password | b64enc | quote }}
```

### 11. Interview explanation
"Helm functions allow dynamic manipulation of data during rendering. The most important ones are `default` to provide fallbacks, `required` to enforce mandatory variables, `nindent` to handle strict YAML indentation, and `toYaml` to render nested configuration blocks directly from `values.yaml`."

### 12. Common mistakes
*   Using `indent` instead of `nindent`. `indent` just adds spaces to the current line. If you are injecting a multi-line block, the first line will start exactly where the cursor is, messing up alignment. `nindent` drops down one line and then indents, ensuring perfect alignment.

### 13. Best practices
*   Use `required` for credentials, API keys, and anything that will cause the app to crash loop if omitted. Fail fast during `helm install` rather than letting K8s create broken pods.

### 14. Production recommendations
*   Be very careful with the `lookup` function. If you run `helm template` (which doesn't talk to the cluster), `lookup` returns empty. This can cause tests to fail if your template logic depends on `lookup` results.

### 15. Troubleshooting guide
*   If a multi-line configuration from `values.yaml` is causing a YAML parsing error, you probably forgot `| nindent`.

### 16. Advanced concepts
*   Using `tpl`. Imagine in `values.yaml` a user writes: `welcomeMessage: "Hello {{ .Release.Name }}"`. If you just use `{{ .Values.welcomeMessage }}`, it prints the literal string with the curly braces. If you use `{{ tpl .Values.welcomeMessage . }}`, Helm will render the *value itself* as a template!

### 17. Frequently asked interview questions with answers
**Q: How do you inject a complex dictionary from values.yaml (like tolerations or nodeSelectors) directly into a deployment.yaml without hardcoding every key?**
A: We use the `toYaml` function combined with `nindent`. For example: `{{- toYaml .Values.nodeSelector | nindent 8 }}`. This converts the dictionary in values.yaml into properly indented YAML lines.

### 18. Scenario-based interview questions with answers
**Q: You want to add a label to a pod only if the user explicitly defined it in values.yaml. How do you check if it exists?**
A: You can use an `if` statement combined with the `hasKey` function if it's a dictionary, or just check the value directly: `{{ if .Values.customLabel }}{{ .Values.customLabel }}{{ end }}`.

---

## SECTION 5: Flow Control

### 1. Definition
Flow control refers to conditional logic (`if`, `else`, `else if`), looping (`range`), and scope modification (`with`) inside your templates.

### 2. Why this concept exists / Problem it solves
Not every environment needs the same resources. Dev might not need an Ingress or an HorizontalPodAutoscaler (HPA). Production does. You need `if` statements to optionally render entire blocks of YAML or entire files.

### 3. Real-world analogy
Flow control is the decision-making brain of the chart.
IF (raining) { take umbrella } ELSE { take sunglasses }
RANGE (over groceries) { print grocery item }

### 4. ASCII architecture diagram
N/A

### 5. Internal working
In Go templates, "false" means boolean false, 0, an empty string `""`, `nil`, or an empty collection. Everything else is true.

### 6. Complete workflow

**IF / ELSE**
```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ...
{{- else if .Values.ingress.legacy }}
# ... old ingress ...
{{- else }}
# ... do nothing ...
{{- end }}
```

**RANGE (Loops)**
Used to iterate over a list or a map in `values.yaml`.
**Crucial Concept:** Inside a `range` block, the dot `.` changes! It no longer means the root context (`.Values`, `.Release`). The dot `.` now represents the *current item in the loop*.

```yaml
# values.yaml
envVars:
  - name: DB_HOST
    value: "localhost"
  - name: DB_PORT
    value: "5432"

# deployment.yaml
env:
{{- range .Values.envVars }}
  # The '.' is now the current list item!
  - name: {{ .name }}
    value: {{ .value | quote }}
{{- end }}
```

**How to access Root inside a Range?**
If you need `.Release.Name` inside a loop, `.` won't work. You must use `$` (which always points to the root context) or assign the root to a variable before the loop.
`name: {{ $.Release.Name }}-{{ .name }}`

**WITH (Scoping)**
`with` is a shortcut to avoid typing deep paths. It temporarily changes the dot `.` to point to a specific scope.

```yaml
# Instead of this:
# replicas: {{ .Values.app.server.config.replicas }}
# port: {{ .Values.app.server.config.port }}

# Do this:
{{- with .Values.app.server.config }}
  # '.' is now .Values.app.server.config
  replicas: {{ .replicas }}
  port: {{ .port }}
{{- end }}
```

### 7. Production use case
Dynamically creating multiple Kubernetes Services or Ingress paths based on a list defined by the developer in `values.yaml`.

### 8. Step-by-step example
See YAML above.

### 9. Commands
N/A

### 10. Complete YAML/config (line-by-line explained)
Included in Workflow.

### 11. Interview explanation
"Helm provides control structures like `if` for conditional rendering, which is essential for turning features like HPAs or Ingresses on/off per environment. It uses `range` to iterate over lists and maps, which is powerful for dynamically generating environment variables. `with` is used to narrow the variable scope for cleaner code."

### 12. Common mistakes
*   **The Scope Trap:** Forgetting that `range` and `with` change the context of `.`. This results in `nil pointer` errors when you try to access `.Values` inside a loop. Always use `$.Values` inside loops if you need root access.

### 13. Best practices
*   Always use whitespace strippers `{{-` and `-}}` heavily around flow control statements. Otherwise, an `{{ if }}` statement that evaluates to false will leave a blank, empty line in your YAML.

### 14. Production recommendations
*   Wrap entire optional resources (like `hpa.yaml` or `ingress.yaml`) in a single big `{{ if .Values.ingress.enabled }}` at the very top of the file. If false, Helm renders nothing, and Kubernetes creates nothing.

### 15. Troubleshooting guide
*   Error: `can't evaluate field Values in type interface {}` inside a loop. -> You used `.Values` instead of `$.Values`.

### 16. Advanced concepts
*   **Iterating over Maps (Dictionaries):** You can get both the key and value in a range loop:
    ```yaml
    {{- range $key, $value := .Values.myDictionary }}
      {{ $key }}: {{ $value }}
    {{- end }}
    ```

### 17. Frequently asked interview questions with answers
**Q: How do you conditionally render an entire Kubernetes Secret file so it only deploys in production?**
A: At the very top of `secret.yaml`, place `{{- if eq .Values.environment "prod" -}}` and at the very bottom `{{- end -}}`.

### 18. Scenario-based interview questions with answers
**Q: Inside a `range` block iterating over a list of databases in `values.yaml`, you need to construct a name combining the current database name and the overall Helm Release Name. How do you write this template?**
A: `{{ $.Release.Name }}-{{ .dbName }}`. I must use the `$` to access the root context for the Release Name, because the `.` context is currently scoped to the list item inside the range block.

---

## SECTION 6: Named Templates and _helpers.tpl

### 1. Definition
Named templates are reusable snippets of template code defined once and included anywhere. They are typically stored in a file called `_helpers.tpl`.

### 2. Why this concept exists / Problem it solves
DRY: Don't Repeat Yourself. Every K8s resource (Deployment, Pod, Service, Ingress) needs matching `app.kubernetes.io/name` and `app.kubernetes.io/instance` labels. Typing these out 10 times is error-prone. If you change the logic, you have to change it in 10 files.

### 3. Real-world analogy
It's a function or a macro in programming. You write the logic in one place (`_helpers.tpl`) and call it (`include`) from everywhere else.

### 4. ASCII architecture diagram
```text
_helpers.tpl
[define "myapp.labels"]
app: {{ .Chart.Name }}
[end]
      |
      | (include)
      v
deployment.yaml       service.yaml
metadata:             metadata:
  labels:               labels:
    {{ include }}         {{ include }}
```

### 5. Internal working
Any file starting with an underscore (like `_helpers.tpl`) is not treated as a Kubernetes manifest by Helm. It's solely loaded into the engine's memory. You use the `define` keyword to name the template block.

### 6. Complete workflow
1. Create `templates/_helpers.tpl`.
2. Write a `define` block.
3. Go to `deployment.yaml`.
4. Use `include` to inject it.

### 7. Production use case
Standardizing labels across the entire enterprise to ensure Datadog/Prometheus can properly scrape and group metrics.

### 8. Step-by-step example

**templates/_helpers.tpl**
```yaml
{{/*
Expand the name of the chart.
(Comments in Helm start with /* and end with */)
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels to be applied to EVERYTHING
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.name" . }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

**templates/deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.name" . }}
  labels:
    # include evaluates the template.
    # . passes the root context to the helper!
    # nindent 4 ensures it aligns properly under 'labels:'
    {{- include "mychart.labels" . | nindent 4 }}
```

### 9. Commands
N/A

### 10. Complete YAML/config (line-by-line explained)
See above. Notice how we pass the dot `.` at the end of the `include` statement: `include "mychart.labels" .`. This passes the root context into the helper template. If you don't pass `.`, the helper won't have access to `.Values` or `.Release`!

### 11. Interview explanation
"Named templates, usually defined in `_helpers.tpl`, allow us to write DRY (Don't Repeat Yourself) code in Helm. We `define` blocks of reusable logic—like standard metadata labels or service account names—and then use the `include` function in our resource YAMLs to inject them. This ensures consistency across all Kubernetes resources in the chart."

### 12. Common mistakes
*   Using `template` instead of `include`.
    *   `template` is an action. It cannot be piped. `{{ template "name" . | nindent 4 }}` will FAIL.
    *   `include` is a function. It returns a string that can be piped. `{{ include "name" . | nindent 4 }}` works perfectly. ALWAYS use `include`.

### 13. Best practices
*   Namespace your template definitions. `{{ define "labels" }}` is bad. If another subchart also defines "labels", they will collide and one will overwrite the other. Use `{{ define "mychart.labels" }}`.

### 14. Production recommendations
*   Put all complex logic (like generating image registry URLs, constructing connection strings) in `_helpers.tpl`. Keep your `deployment.yaml` as clean and readable as possible.

### 15. Troubleshooting guide
*   Helper returning blank? You probably forgot to pass the context: `{{ include "mychart.labels" }}` instead of `{{ include "mychart.labels" . }}`.

### 16. Advanced concepts
*   You can include helpers inside other helpers! Notice in the example above, `"mychart.labels"` includes `"mychart.name"`.

### 17. Frequently asked interview questions with answers
**Q: Why do files like `_helpers.tpl` start with an underscore?**
A: The Helm rendering engine ignores files starting with an underscore when it gathers files to send to the Kubernetes API. It treats them solely as utility files for the templating engine.

### 18. Scenario-based interview questions with answers
**Q: You define a named template but when you include it in a Deployment, you get a YAML parsing error about indentation. How do you fix it?**
A: Use the `include` function (not `template`) and pipe it to `nindent X`, where X is the number of spaces needed to align the block correctly in the Deployment YAML.

---

## SECTION 7: values.yaml Design

### 1. Definition
`values.yaml` is the default configuration file for a Helm chart. It exposes the "knobs and dials" that users can tweak.

### 2. Why this concept exists / Problem it solves
A chart shouldn't be hardcoded to a specific environment. `values.yaml` separates the *configuration* from the *code* (templates), adhering to 12-factor app principles.

### 3. Real-world analogy
If the Helm chart is a blueprint for a house, `values.yaml` is the customer's order form:
Bedrooms: 3
Paint_Color: Blue
Has_Pool: true

### 4. ASCII architecture diagram
N/A

### 5. Internal working
Helm merges values from multiple sources in a specific order of precedence.

### 6. Complete workflow (Values Precedence Order)
From lowest priority to highest priority (highest wins):
1.  **Built-in values:** `.Release.Name`, etc.
2.  **Chart values:** The `values.yaml` inside the chart directory.
3.  **Parent Chart values:** If this is a subchart, values passed from the parent.
4.  **User Value Files:** Files passed via `-f custom-values.yaml`.
5.  **Set flags:** Values passed via `--set key=value` on the command line.

### 7. Production use case
Maintaining multiple environment files.
*   `values-dev.yaml` (replicas: 1, debug: true)
*   `values-prod.yaml` (replicas: 10, debug: false)
Run: `helm upgrade my-app ./chart -f values-prod.yaml`

### 8. Step-by-step example (Flat vs Nested)

**Bad Design (Flat - too cluttered)**
```yaml
dbHost: localhost
dbPort: 5432
dbUser: admin
appReplicas: 3
appImage: nginx
```

**Good Design (Nested - grouped logically)**
```yaml
database:
  host: localhost
  port: 5432
  user: admin

app:
  replicas: 3
  image: nginx
```

### 9. Commands
*   `helm install app ./chart -f values-prod.yaml --set app.replicas=5`
    (Here, replicas will be 5, overriding whatever is in `values-prod.yaml`).

### 10. Complete YAML/config (line-by-line explained)

**Global Values:**
Sometimes a chart has dependencies (subcharts). Usually, values in `values.yaml` only apply to the main chart. If you want a value to be accessible to the main chart AND all subcharts, put it under the `global` key.

```yaml
global:
  imagePullSecrets:
    - name: my-docker-secret
  environment: production
```
Access it via: `{{ .Values.global.environment }}`.

### 11. Interview explanation
"The `values.yaml` file defines the default parameters for a chart. In a production workflow, we override these defaults using environment-specific files (like `values-prod.yaml`) passed via the `-f` flag, or via `--set` for ad-hoc overrides. Helm handles merging these values, with `--set` having the highest precedence."

### 12. Common mistakes
*   **Storing Secrets in values.yaml in Git.** NEVER put real passwords in `values.yaml` and commit it to GitHub. It is plain text.

### 13. Best practices
*   Structure your `values.yaml` to mirror the Kubernetes resources they configure (e.g., group Ingress configs under an `ingress:` key).
*   Document every single key in `values.yaml` with comments.

### 14. Production recommendations
*   For secrets, use a tool like **External Secrets Operator** or **Sealed Secrets**. The Helm chart simply configures the ExternalSecret CRD, which then securely fetches the real password from AWS Secrets Manager or HashiCorp Vault at runtime.

### 15. Troubleshooting guide
*   If your override isn't working, check your nesting. `--set db.port=5432` maps to the nested dictionary, not a flat key named "db.port". To set a key that actually has a dot in the name, escape it: `--set db\.port=5432`.

### 16. Advanced concepts
*   **Type Coercion via set:** `--set` interprets "true" as boolean and "1" as an integer. If you want to force it to be a string, use `--set-string version="1.0"`.

### 17. Frequently asked interview questions with answers
**Q: How do you pass an array/list using the `--set` flag?**
A: You use curly braces. `--set ingress.hosts={foo.com,bar.com}`.

### 18. Scenario-based interview questions with answers
**Q: You have a chart with a subchart. You define `username: admin` in the parent's `values.yaml`. When the subchart renders, it says `username` is nil. Why?**
A: Variables defined at the root of a parent's `values.yaml` do not automatically cascade down to subcharts. You must either place the variable under a key named after the subchart (e.g., `mysubchart.username`), or place it under the `global` block (`global.username`).

---

## SECTION 8: Core Helm Commands

### 1. Definition
Helm CLI commands manage the entire lifecycle of a chart: searching, fetching, installing, testing, upgrading, and removing.

### 2. Why this concept exists / Problem it solves
You need a unified interface to interact with chart repositories, the rendering engine, and the Kubernetes cluster.

### 3. Real-world analogy
It's like `apt-get` on Linux. `apt search`, `apt install`, `apt upgrade`, `apt remove`.

### 4. ASCII architecture diagram
N/A

### 5. Internal working
The Helm CLI reads your `KUBECONFIG`, compiles the Go templates locally, and sends the resulting JSON payload to the Kubernetes API via REST/gRPC.

### 6. Complete workflow & Commands

**1. Repo Management:**
*   `helm repo add bitnami https://charts.bitnami.com/bitnami` (Add a store)
*   `helm repo update` (Fetch latest versions from all added stores - like `apt update`)
*   `helm search repo nginx` (Find a chart)
*   `helm repo list` (List added repositories)
*   `helm repo remove bitnami` (Remove a repository)

**2. Chart Creation & Validation:**
*   `helm create mychart` (Scaffold a new chart)
*   `helm lint ./mychart` (Checks for bad YAML or missing fields. Always run this in CI/CD).
*   `helm template my-release ./mychart -f dev.yaml` (Renders YAML to terminal. Great for debugging).
*   `helm package ./mychart` (Packages chart into a .tgz archive).
*   `helm pull bitnami/nginx` (Downloads a chart from a repository and unpacks it locally for inspection).

**3. Deployment (The Big Three):**
*   `helm install my-release ./mychart` (Creates a brand new release).
*   `helm upgrade my-release ./mychart` (Updates an existing release).
    *   **Pro Flag:** `helm upgrade --install my-release ./mychart` (The God Command. If it doesn't exist, install it. If it does, upgrade it. This is what you put in CI/CD pipelines!).
    *   **Pro Flag:** `--atomic` (If the upgrade fails, automatically roll back to the previous version immediately).
    *   **Pro Flag:** `--cleanup-on-fail` (Allow deletion of new resources created in this upgrade when upgrade fails).
*   `helm rollback my-release 1` (Revert to revision 1).

**4. Observation:**
*   `helm list` or `helm ls` (List all installed releases in the current namespace).
*   `helm list -A` (Across all namespaces).
*   `helm history my-release` (See all previous versions/upgrades of this release).
*   `helm status my-release` (See if it's deployed, and reprint the NOTES.txt).
*   `helm get values my-release` (See what custom values were passed to this specific release).
*   `helm get manifest my-release` (See the actual Kubernetes YAML that is currently running).
*   `helm get notes my-release` (Print the release notes).
*   `helm get hooks my-release` (Show all hooks declared for the release).

**5. Removal:**
*   `helm uninstall my-release` (Deletes all K8s resources created by this release).

### 7. Production use case
A Jenkins pipeline that runs:
1. `helm lint`
2. `helm upgrade --install my-app ./chart -f prod.yaml --atomic --wait --timeout 10m`
(`--wait` ensures the pipeline doesn't report "Success" until all pods are actually running and healthy).

### 8. Step-by-step example
N/A

### 9. Commands
(See above)

### 10. Complete YAML/config (line-by-line explained)
N/A

### 11. Interview explanation
"For deploying apps, `helm upgrade --install` is the industry standard because of its idempotency. For production safety, appending the `--atomic` flag ensures that if a deployment fails health checks, Helm automatically rolls the cluster back to the previous stable state, preventing downtime."

### 12. Common mistakes
*   Running `helm upgrade` and getting "release not found". Use `--install` to fix this.
*   Assuming `helm uninstall` deletes everything. It does NOT delete PersistentVolumeClaims (PVCs) by default, to prevent accidental data loss. You must delete those manually via kubectl.

### 13. Best practices
*   Use `--dry-run --debug` with `helm install/upgrade`. It pretends to do the install, renders everything, talks to the K8s API to validate it, but doesn't actually save anything. Perfect for pre-flight checks.

### 14. Production recommendations
*   Limit direct `helm` command access in production clusters. Let ArgoCD or Flux (GitOps) run the Helm commands internally based on Git commits.

### 15. Troubleshooting guide
*   Command hangs? You might have used `--wait` and your pods are crash looping. Open a new terminal and run `kubectl get pods` to investigate.

### 16. Advanced concepts
*   **Plugins:** Helm can be extended. e.g., `helm plugin install <url>`. Examples: `helm diff` (shows a git-like diff of what will change before you upgrade) or `helm secrets` (integrates with Mozilla SOPS to encrypt values files in Git).

### 17. Frequently asked interview questions with answers
**Q: You want to see the Kubernetes YAML that Helm actually generated for a deployment that is currently running in the cluster. How do you do it?**
A: `helm get manifest <release-name>`. This retrieves the exact rendered templates that were applied.

### 18. Scenario-based interview questions with answers
**Q: Your CI/CD pipeline runs `helm upgrade`. It succeeds. However, users report the app is down. You find the pods are in CrashLoopBackOff due to a bad image. How do you prevent Helm from reporting success if the pods fail to start?**
A: Add the `--wait` flag to the `helm upgrade` command. Helm will wait until all Pods, PVCs, and Services are in a Ready state before exiting with a 0 (success) code. If they never become ready, Helm will exit with a non-zero code, failing the CI/CD pipeline. Combining this with `--atomic` will also trigger an automatic rollback.

---

## SECTION 9: Helm Hooks

### 1. Definition
Hooks are a mechanism that allows you to intervene at specific points in a release's lifecycle (e.g., right before an install, right after an upgrade, right before deletion).

### 2. Why this concept exists / Problem it solves
Imagine your new app version requires a database schema change. If Helm just deploys the new app pods, they might crash because the schema hasn't updated yet. You need to run a DB Migration script *before* the new pods start. Hooks solve this.

### 3. Real-world analogy
Hooks are like airport security checkpoints.
Pre-flight (Pre-install hook): Check bags.
Flight (Install): The actual journey.
Post-flight (Post-install hook): Pick up luggage.

### 4. ASCII architecture diagram
```text
helm upgrade --> [Pre-Upgrade Hook] (e.g., DB Backup/Migration)
                       |
                 (Wait for hook to succeed)
                       |
                       v
                 [Upgrade resources in K8s]
                       |
                       v
                 [Post-Upgrade Hook] (e.g., Slack notification, Cleanup)
```

### 5. Internal working
You create a standard Kubernetes resource (usually a Job or a Pod) in your `templates/` directory. You add a specific annotation: `helm.sh/hook: pre-upgrade`. Helm intercepts this. Instead of applying it with the rest of the YAML, Helm creates it first, waits for it to finish successfully, and *then* proceeds with the rest of the deployment.

### 6. Complete workflow (Hook Types)
*   `pre-install` / `post-install`
*   `pre-upgrade` / `post-upgrade`
*   `pre-rollback` / `post-rollback`
*   `pre-delete` / `post-delete`
*   `test` (Run via `helm test` command)

### 7. Production use case
1.  **Database Migrations:** Running a Job to update DB schemas (`pre-upgrade`).
2.  **Secret Generation:** Generating a random password or TLS certificate before deploying the app that needs it (`pre-install`).
3.  **Data Seeding:** Populating an empty DB on first launch (`post-install`).

### 8. Step-by-step example (DB Migration Hook)
N/A - See YAML below.

### 9. Commands
N/A

### 10. Complete YAML/config (line-by-line explained)

**templates/db-migration-job.yaml**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-db-migrate
  annotations:
    # 1. Define this as a pre-upgrade AND pre-install hook
    "helm.sh/hook": pre-install,pre-upgrade
    
    # 2. Hook Weights (Order of execution if multiple hooks exist). Lowest runs first.
    "helm.sh/hook-weight": "-5"
    
    # 3. Cleanup Policy. Delete this Job object automatically when it succeeds!
    # Without this, dead Jobs will pile up in your cluster after every upgrade.
    # Other policies: before-hook-creation, hook-failed
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: db-migrate
          image: my-app:{{ .Values.image.tag }}
          command: ["npm", "run", "db:migrate"]
```

### 11. Interview explanation
"Helm Hooks allow us to execute Kubernetes Jobs at specific lifecycle events. The most common use case is database migrations, where we use a `pre-upgrade` hook to ensure a schema migration Job runs and succeeds before Helm attempts to update the application Deployments."

### 12. Common mistakes
*   **Hanging Hooks:** If your hook is a Deployment or a Pod that doesn't terminate (like a web server), Helm will wait forever for it to "complete". Hooks should almost always be Kubernetes `Job` objects that run a task and exit.
*   **Orphaned Hooks:** Forgetting `hook-delete-policy`. Helm does not manage hook resources the same way it manages normal release resources. If you don't set a delete policy, the completed Jobs sit in the cluster forever.

### 13. Best practices
*   Always use `hook-delete-policy: hook-succeeded`.
*   Keep hooks fast. A `pre-upgrade` hook blocks the entire deployment.

### 14. Production recommendations
*   If a `pre-upgrade` hook fails (e.g., DB migration crashes), Helm aborts the entire upgrade. The new app versions are never deployed. This is exactly what you want in production to prevent data corruption.

### 15. Troubleshooting guide
*   "Helm upgrade is stuck and timing out." -> Check your cluster. A pre-upgrade hook job is probably in an Error or CrashLoopBackOff state, and Helm is waiting for it to succeed.

### 16. Advanced concepts
*   **Hook Weights:** If you have a hook that backs up the DB, and a hook that migrates the DB, you need them to run in order. Set weight `-10` for backup and `-5` for migration. Helm executes them in ascending order.

### 17. Frequently asked interview questions with answers
**Q: Does a `helm rollback` trigger the `pre-upgrade` hooks?**
A: No. A rollback triggers the `pre-rollback` and `post-rollback` hooks. If your database migration was destructive, rolling back the application code via Helm will NOT automatically roll back the database schema unless you explicitly write a `pre-rollback` hook to do so (which is incredibly hard to do safely).

### 18. Scenario-based interview questions with answers
**Q: You write a `pre-install` hook Job to generate a random password and save it as a Kubernetes Secret. However, when you run `helm delete`, the Secret isn't deleted. Why?**
A: Resources created by hooks are not considered part of the Helm Release state. Therefore, when you delete the release, Helm leaves the hook-generated resources behind. You must use a `pre-delete` hook or a specific `helm.sh/resource-policy: keep` annotation to manage this, or just manually clean it up.

---

## SECTION 10: Helm Dependencies (Subcharts)

### 1. Definition
A chart can depend on other charts. These are called subcharts.

### 2. Why this concept exists / Problem it solves
Your web app needs a Redis cache and a PostgreSQL database. You don't want to write the K8s YAML for Redis and Postgres yourself. You want to pull the official Bitnami charts and bundle them with your app so a user can install the whole stack with one command.

### 3. Real-world analogy
Your car chart has a dependency on a "Tire" chart and an "Engine" chart provided by a third-party manufacturer.

### 4. ASCII architecture diagram
```text
my-app/
|-- Chart.yaml (Lists deps)
|-- charts/
|   |-- postgresql-12.tgz  <-- Helm downloads it here
|   |-- redis-7.tgz        <-- Helm downloads it here
|-- templates/
|   |-- deployment.yaml (Your app code)
```

### 5. Internal working
Dependencies are defined in `Chart.yaml`. When you run `helm dependency update`, Helm reaches out to the remote repositories, downloads the `.tgz` packages of the subcharts, and places them in your `charts/` folder.

### 6. Complete workflow
1. Add to `Chart.yaml`.
2. Run `helm dependency update`.
3. Override subchart values in your root `values.yaml`.

### 7. Production use case
Bundling a logging sidecar (Fluentd) or a database with the main application.

### 8. Step-by-step example

**1. Define in Chart.yaml**
```yaml
apiVersion: v2
name: my-app
version: 1.0.0
dependencies:
  - name: postgresql
    version: 12.1.0
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled # This is magic!
```

**2. Run command**
`helm dependency update`

**3. Override in root values.yaml**
To configure the subchart, you create a key in your main `values.yaml` with the exact name of the subchart.

```yaml
# root values.yaml

# My app settings
replicas: 3

# Subchart override! Helm will pass everything under here into the postgresql chart.
postgresql:
  enabled: true # Ties to the 'condition' in Chart.yaml. If false, DB isn't installed.
  auth:
    postgresPassword: "supersecret"
    database: "myapp_db"
```

### 9. Commands
*   `helm dependency update` (Downloads missing deps, updates `Chart.lock`)
*   `helm dependency build` (Builds deps exactly as specified in `Chart.lock`)

### 10. Complete YAML/config (line-by-line explained)
See above.

### 11. Interview explanation
"Helm allows composing complex applications via Dependencies, or subcharts. You declare external charts in your `Chart.yaml`. Helm downloads them into the `charts/` directory. You can then override the subchart's default values by nesting configurations under a key matching the subchart's name in your root `values.yaml`."

### 12. Common mistakes
*   Forgetting to run `helm dependency update`. If the `charts/` folder is empty, Helm will complain that it can't find the subchart.
*   Committing the `charts/` directory to Git. You should only commit `Chart.yaml` and `Chart.lock`, just like `package.json` and `package-lock.json` in Node.js. Add `charts/` to your `.gitignore`.

### 13. Best practices
*   Use the `condition` field in `Chart.yaml`. This allows users to easily turn off the dependency (e.g., `--set postgresql.enabled=false`) if they want to use an external, cloud-managed database (like AWS RDS) in production, but use the in-cluster subchart for local development.

### 14. Production recommendations
*   Lock your dependency versions strictly. Don't use `^1.0.0`, use exactly `1.0.5`. An unexpected database upgrade in a subchart can break production.

### 15. Troubleshooting guide
*   "Chart not found" -> Add the repository to your local helm client first (`helm repo add`), then run `helm dep up`.

### 16. Advanced concepts
*   **Aliases:** If you need TWO databases (e.g., a read DB and a write DB), you can depend on the same chart twice by using aliases.
    ```yaml
    dependencies:
      - name: postgresql
        version: 12.0.0
        alias: pg-read
      - name: postgresql
        version: 12.0.0
        alias: pg-write
    ```

### 17. Frequently asked interview questions with answers
**Q: Can a subchart access values defined in the parent chart's `values.yaml`?**
A: By default, no. Subcharts are isolated. The parent can pass values *down* to the subchart by namespacing them (e.g., putting them under the `postgresql:` block). However, if the parent puts values in the `global:` block, both the parent and all subcharts can access them.

### 18. Scenario-based interview questions with answers
**Q: You want to use a Bitnami Redis subchart. In the Bitnami documentation, the value to set the password is `auth.password`. How do you set this password from your umbrella chart's `values.yaml`?**
A: You nest it under the subchart name.
```yaml
redis:
  auth:
    password: "my-password"
```

---

## SECTION 11: Library Charts

### 1. Definition
A Library Chart is a special type of Helm chart that contains NO deployable Kubernetes templates. It only contains reusable named templates (`_helpers.tpl`).

### 2. Why this concept exists / Problem it solves
If you have 50 microservices, and you want all of them to use the exact same template logic for generating Deployment YAMLs or standard company labels, you shouldn't copy-paste `_helpers.tpl` 50 times. You create one Library Chart and make the 50 microservices depend on it.

### 3. Real-world analogy
It's a shared code library (like a `.dll` or `.jar` file) that other applications import.

### 4. ASCII architecture diagram
N/A

### 5. Internal working
In `Chart.yaml`, you set `type: library`. If a user accidentally tries to run `helm install` on a library chart, Helm blocks it and throws an error.

### 6. Complete workflow
1. Create chart: `type: library`.
2. Write templates in `_helpers.tpl`.
3. Other charts add it as a dependency.
4. Other charts use `include` to call the library's templates.

### 7. Production use case
A Platform Engineering team creates a `company-standard-lib` chart. It contains a template called `company.deployment`. Developers writing an app chart just write a 3-line `deployment.yaml` that calls `{{ include "company.deployment" . }}`.

### 8. Step-by-step example
N/A - Concept is straightforward.

### 9. Commands
N/A

### 10. Complete YAML/config (line-by-line explained)
**Chart.yaml (Library)**
```yaml
apiVersion: v2
name: my-lib
version: 1.0.0
type: library # This makes it a library chart
```

### 11. Interview explanation
"A Library Chart is a Helm chart defined with `type: library`. It doesn't create Kubernetes resources on its own. Instead, it serves as a central repository for shared named templates and helpers that other charts can import as a dependency, enforcing DRY principles across an organization."

### 12. Common mistakes
*   Trying to put a `deployment.yaml` in a library chart. It won't render.

### 13. Best practices
*   Heavily version your library charts. A breaking change in a library chart will break every microservice that depends on it.

### 14. Production recommendations
*   Use them to enforce security standards (e.g., a helper that always injects `runAsNonRoot: true` securityContexts).

### 15. Troubleshooting guide
N/A

### 16. Advanced concepts
N/A

### 17. Frequently asked interview questions with answers
**Q: What happens if you run `helm install` on a library chart?**
A: Helm will immediately exit with an error stating that library charts cannot be installed directly.

### 18. Scenario-based interview questions with answers
N/A

---

## SECTION 12: Helm CRDs

### 1. Definition
Custom Resource Definitions (CRDs) extend the Kubernetes API. Helm has special handling for installing them.

### 2. Why this concept exists / Problem it solves
If an application requires a CRD (like Prometheus `ServiceMonitor` or Cert-Manager `Certificate`), the CRD *must* be installed in the cluster before Helm tries to create instances of that custom resource. Helm needs to know which files are CRDs so it can install them first.

### 3. Real-world analogy
You can't buy a ticket for a train line that hasn't been built yet. The CRD is building the train line. The custom resource is the ticket.

### 4. ASCII architecture diagram
N/A

### 5. Internal working
Helm looks for a special directory named `crds/` at the root of the chart (next to `templates/`). Any YAML files placed in `crds/` are installed *before* anything in `templates/`.

### 6. Complete workflow
Put CRD YAML files in the `crds/` directory.

### 7. Production use case
Deploying the Nginx Ingress Controller or Cert-Manager, which heavily rely on CRDs.

### 8. Step-by-step example
N/A

### 9. Commands
N/A

### 10. Complete YAML/config (line-by-line explained)
N/A

### 11. Interview explanation
"Helm handles CRDs specially by looking for a `crds/` directory. It installs everything in that directory before rendering and installing the `templates/` directory. However, a major limitation is that Helm deliberately will *not* upgrade or delete CRDs on subsequent `helm upgrade` or `helm uninstall` commands to prevent accidental cluster-wide data loss."

### 12. Common mistakes
*   **Templating CRDs:** Files in the `crds/` folder CANNOT use Go templates (`{{ }}`). They must be pure, static Kubernetes YAML. If you try to template them, Helm will ignore the templating and likely fail.

### 13. Best practices
*   If you need to template a CRD, you must place it in the `templates/` directory, but you must ensure it installs first using Helm hooks (`helm.sh/hook: pre-install`).

### 14. Production recommendations
*   Because Helm doesn't upgrade CRDs (it only installs them initially), Platform teams often manage CRDs entirely outside of Helm, using tools like Kustomize or Terraform, to ensure they can be safely updated over time.

### 15. Troubleshooting guide
*   "Resource type not known" error during install -> Your CRD wasn't installed first. Ensure it's in the `crds/` folder.

### 16. Advanced concepts
*   You can pass `--skip-crds` during `helm install` if the cluster admin has already installed the CRDs for you and you lack the RBAC permissions to do so.

### 17. Frequently asked interview questions with answers
**Q: You update a CRD definition in your chart's `crds/` folder and run `helm upgrade`. What happens?**
A: Nothing. Helm by design ignores the `crds/` folder during an upgrade. It only processes it during the initial `helm install`. Upgrading CRDs must be done manually or via alternative methods.

### 18. Scenario-based interview questions with answers
**Q: You uninstall a Helm release that included CRDs in the `crds/` folder. You notice the CRDs are still in the cluster. Why?**
A: Helm does not delete CRDs during `helm uninstall`. Because CRDs define cluster-wide resources, deleting a CRD automatically deletes *every instance* of that custom resource across the entire cluster, even in other namespaces. Helm leaves them behind to prevent catastrophic data loss.

---

## SECTION 13: Helm Testing

### 1. Definition
Helm has a built-in testing framework to verify that a deployed chart is functioning correctly.

### 2. Why this concept exists / Problem it solves
A CI/CD pipeline deploys the app successfully. But is the database actually accepting connections? Does the API return a 200 OK? Helm tests validate runtime behavior, not just YAML syntax.

### 3. Real-world analogy
Helm Install is building the car. Helm Test is turning the key to see if the engine actually starts.

### 4. ASCII architecture diagram
N/A

### 5. Internal working
Tests are just standard Kubernetes Pods or Jobs placed in the `templates/` directory, annotated with `helm.sh/hook: test`.

### 6. Complete workflow
1. Add test Pod to `templates/tests/` (convention).
2. Deploy app: `helm install my-app ./chart`.
3. Run tests: `helm test my-app`.
Helm creates the test Pod, watches its exit code, reports success/failure, and deletes the test Pod.

### 7. Production use case
Running a `curl` command against the web app's internal Service IP to ensure it returns an HTTP 200, verifying network policies and service routing.

### 8. Step-by-step example

**templates/tests/test-connection.yaml**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    # This is what makes it a test!
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      # Try to connect to our service
      command: ['wget']
      args: ['{{ .Release.Name }}-{{ .Chart.Name }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

### 9. Commands
*   `helm test <release-name>`

### 10. Complete YAML/config (line-by-line explained)
See above.

### 11. Interview explanation
"Helm testing utilizes Kubernetes Pods annotated with `helm.sh/hook: test`. After a chart is deployed, running `helm test` triggers these pods. They execute scripts (like curl or ping) against the deployed application. If the container exits with code 0, the test passes."

### 12. Common mistakes
*   Making the test Pod run forever. The test container MUST exit on its own.

### 13. Best practices
*   Keep tests lightweight. Test basic connectivity and configuration, don't run heavy integration test suites through Helm (use CI for that).

### 14. Production recommendations
*   Include `helm test` as a mandatory step in your CD pipeline after `helm upgrade`.

### 15. Troubleshooting guide
*   Use `helm test --logs` to print the output of the test pod to the console so you can see why the `curl` failed.

### 16. Advanced concepts
N/A

### 17. Frequently asked interview questions with answers
**Q: How does Helm determine if a test passed or failed?**
A: By the exit code of the test Pod's container. A 0 exit code is a pass. Any non-zero exit code is a failure.

### 18. Scenario-based interview questions with answers
N/A

---

## SECTION 14: Production Helm Design

### 1. Real production folder structure (Mono-repo style)
In a modern DevOps environment, you don't keep values files loose. You structure them for GitOps.

```text
helm-infrastructure/
|-- base-charts/
|   |-- microservice-lib/    (Library chart)
|-- apps/
|   |-- frontend-app/
|       |-- Chart.yaml
|       |-- values.yaml      (Defaults)
|       |-- values-dev.yaml  (Dev overrides)
|       |-- values-prod.yaml (Prod overrides)
|-- argo-cd/                 (GitOps configurations pointing to apps)
```

### 2. Umbrella Chart Pattern
An "Umbrella Chart" is a chart that contains NO templates of its own. It consists purely of a `Chart.yaml` listing a dozen dependencies (frontend, backend, database, redis), and a massive `values.yaml` configuring all of them. This allows deploying an entire architecture (e.g., the complete e-commerce stack) with a single `helm install my-stack ./umbrella-chart`.

### 3. Secret Management
Never store plaintext passwords in `values.yaml`. In production, you use tools like **External Secrets Operator (ESO)**.
1. Store password in AWS Secrets Manager.
2. In Helm `values.yaml`: `dbSecretName: aws-rds-password`
3. Helm deploys an `ExternalSecret` custom resource.
4. The ESO controller reads it, talks to AWS, fetches the password, and creates a native K8s Secret dynamically.

### 4. Image Tag Pinning
Never use `image: myapp:latest`.
`latest` is mutable. If a pod crashes and reschedules, it will pull the *new* latest, resulting in mixed versions in production. Always pin to a specific tag (e.g., a Git commit hash like `image: myapp:a1b2c3d`) passed via `--set image.tag=$GIT_COMMIT` in CI/CD.

### 5. Helm + CI/CD
Modern CD completely avoids running `helm upgrade` manually.
Tools like **ArgoCD** or **FluxCD** sit *inside* the Kubernetes cluster. They watch your Git repository. When you commit a change to `values-prod.yaml`, ArgoCD detects it, runs the equivalent of `helm template` internally, and directly applies the diff to the cluster. This is GitOps.

---

## SECTION 15: Helm Debugging

### 1. Common error messages and fixes:

*   **Error:** `UPGRADE FAILED: "my-app" has no deployed releases`
    *   **Fix:** You tried to `helm upgrade` something that was never installed. Use `helm upgrade --install` to fix this forever.
*   **Error:** `cannot re-use a name that is still in use`
    *   **Fix:** A release with this name exists, but it might be stuck in a "pending" or "failed" state. Run `helm list -a` to see it. If it failed, delete it, or upgrade it.
*   **Error:** `rendered manifests contain a resource that already exists. Unable to continue with install`
    *   **Fix:** Helm is trying to create a K8s resource (like a Service named 'web'), but a Service named 'web' ALREADY exists in the cluster (maybe created manually via `kubectl`). Helm refuses to overwrite it to prevent adopting rogue resources. Delete the manual resource first, then run Helm.
*   **YAML indentation errors**
    *   **Fix:** Run `helm template --debug ./chart`. It will show you exactly which line in the rendered YAML has the bad indentation. Usually, you forgot an `| nindent`.

---

## END OF CHAPTER

### Complete Cheat Sheet
| Command | What it does | Production use |
|---|---|---|
| `helm create <name>` | Scaffolds new chart | Starting new projects |
| `helm lint <dir>` | Validates syntax | CI pipeline step 1 |
| `helm template <dir>` | Renders YAML locally | Debugging complex loops |
| `helm install <name> <dir>` | Deploys chart | Initial deployment |
| `helm upgrade --install <name> <dir>`| Upgrades or installs | Standard CI/CD command |
| `--set key=value` | Overrides a value | Passing runtime variables |
| `-f values.yaml` | Overrides with file | Environment config |
| `--dry-run --debug` | Simulates install | Safe validation |
| `--atomic` | Auto-rollback on fail | Production safety |
| `helm rollback <name> <rev>`| Reverts to version | Incident response |
| `helm list -A` | Shows releases | Auditing |
| `helm get manifest <name>` | Shows deployed YAML | Troubleshooting |

### One-page Summary
Helm is the package manager for Kubernetes, solving the complexity of managing and deploying multi-file K8s applications. It uses a directory structure called a **Chart**. `Chart.yaml` holds metadata. `values.yaml` holds configurable defaults. The `templates/` folder contains K8s YAML files injected with Go template syntax (`{{ .Values.app }}`). Helm merges the values with the templates to render plain YAML, which it applies to the cluster, tracking the state as a **Release**. Helm supports flow control (if/range), reusable snippets (helpers), lifecycle hooks for DB migrations, and subcharts for dependencies. In production, Helm is driven by CI/CD or GitOps (ArgoCD), with values overridden per environment, and secrets managed externally.

### Mini Project: 3-Tier App

*(This project combines everything learned above into a production-ready structure).*

**File Structure:**
```text
mini-project/
  Chart.yaml
  values.yaml
  templates/
    _helpers.tpl
    deployment.yaml
    service.yaml
    ingress.yaml
    NOTES.txt
    pre-upgrade-hook.yaml
```

**1. Chart.yaml**
```yaml
apiVersion: v2
name: three-tier-app
version: 1.0.0
description: A production grade helm chart
```

**2. values.yaml**
```yaml
replicaCount: 2
image:
  repository: nginx
  tag: "stable"
environment: dev

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  host: myapp.local

database:
  runMigration: false
```

**3. templates/_helpers.tpl**
```yaml
{{- define "app.labels" -}}
app: {{ .Chart.Name }}
env: {{ .Values.environment }}
release: {{ .Release.Name }}
{{- end }}
```

**4. templates/deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deploy
  labels:
    {{- include "app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        {{- include "app.labels" . | nindent 8 }}
    spec:
      containers:
        - name: web
          image: {{ .Values.image.repository }}:{{ required "Image tag is mandatory!" .Values.image.tag | quote }}
          ports:
            - containerPort: 80
```

**5. templates/service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-svc
  labels:
    {{- include "app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: 80
  selector:
    app: {{ .Chart.Name }}
```

**6. templates/ingress.yaml**
```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ing
spec:
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ .Release.Name }}-svc
                port:
                  number: {{ .Values.service.port }}
{{- end }}
```

**7. templates/pre-upgrade-hook.yaml**
```yaml
{{- if .Values.database.runMigration }}
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-db-migrate
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: busybox
          command: ['sh', '-c', 'echo "Migrating DB..."; sleep 5; echo "Done!"']
{{- end }}
```

**8. templates/NOTES.txt**
```text
Successfully deployed {{ .Chart.Name }} into {{ .Values.environment }}!
{{- if .Values.ingress.enabled }}
Access your app at http://{{ .Values.ingress.host }}
{{- else }}
Run 'kubectl port-forward svc/{{ .Release.Name }}-svc 8080:{{ .Values.service.port }}'
{{- end }}
```

**Deploying to Dev (Terminal 1):**
`helm upgrade --install myapp ./mini-project --set environment=dev`
*(Ingress is skipped, DB migration is skipped, replicas is 2)*

**Deploying to Prod (Terminal 2):**
`helm upgrade --install myapp-prod ./mini-project --set environment=prod --set replicaCount=10 --set ingress.enabled=true --set ingress.host=prod.example.com --set database.runMigration=true`
*(Ingress created, Migration job runs BEFORE the deployment updates, replicas set to 10)*
