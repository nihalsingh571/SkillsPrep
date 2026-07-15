# DevOps Fresher Interview Foundation
### Prepared for: Nihal Kumar Singh

> **Resume Context:** Kubernetes project (Jan–Apr 2026) | InternRecom CI/CD project (Oct 2025–Jan 2026)
> **Skills:** Docker, Kubernetes, Terraform, Ansible, Prometheus, Grafana, Jenkins, Nagios, AWS, Git, Java, Python, Linux, Puppet

---

## How to Use This Document

Each question is answered with:
1. **Direct Answer** — concise, interview-ready
2. **Example / Elaboration** — real context from your projects
3. **Follow-up Awareness** — what the interviewer might ask next

**Pro Tip:** After every "what", be ready for a "why" — always have your reasoning ready.

---

## PART 1 — Introduction & General Questions

---

### Q1. Tell me about yourself.

**Answer:**

"I am Nihal Kumar Singh, a computer science graduate with a strong passion for DevOps engineering and cloud-native technologies. During my academic journey, I completed two significant projects that gave me hands-on exposure to the complete DevOps lifecycle.

In my first project — InternRecom — I built and deployed a web application using a full CI/CD pipeline. I used GitHub for source code management, Jenkins for automated builds and deployments, Terraform for infrastructure provisioning on AWS, Ansible for server configuration management, Docker for containerization, and Nagios for monitoring.

In my second project, I focused on Kubernetes orchestration — deploying containerized workloads with automated horizontal scaling using HPA, exposing services via Ingress, and observing the cluster health through Prometheus and Grafana dashboards.

My core skills include Docker, Kubernetes, Terraform, Ansible, Jenkins, AWS, Python, Linux, and Git. I am a fresher eager to contribute to a team that builds reliable, scalable, and automated infrastructure pipelines."

**Why this works:** It covers your projects, tools, and motivation — and it is concise. Keep it under 90 seconds.

---

### Q2. Walk me through your resume.

**Answer:**

Start from education, move to projects, and end with skills and certifications:

"My resume begins with my B.Tech in Computer Science. I then highlight two key projects:

1. **InternRecom (Oct 2025 – Jan 2026):** A full-stack web application where I implemented end-to-end automation — from code commit to deployment on AWS EC2 using Jenkins CI/CD, Docker containers, Terraform-provisioned infrastructure, Ansible-configured servers, and Nagios-based alerting.

2. **Kubernetes Project (Jan – Apr 2026):** A cloud-native deployment project where I containerized a microservices application, orchestrated it with Kubernetes Deployments and ReplicaSets, implemented Horizontal Pod Autoscaling (HPA) driven by CPU metrics, exposed the application externally through an Ingress controller, and set up observability using Prometheus and Grafana.

Finally, my skills section covers the full DevOps toolchain — version control, CI/CD, containers, orchestration, IaC, configuration management, monitoring, and cloud."

---

### Q3. Why did you choose DevOps as a career path?

**Answer:**

"I chose DevOps because it sits at the intersection of development and operations — two disciplines that I find equally exciting. Traditional software delivery was slow and error-prone because development and operations teams worked in silos. DevOps solves this by automating repetitive tasks, enabling faster and more reliable deployments, and fostering a culture of shared ownership.

For example, when I configured the Jenkins pipeline for InternRecom, I realized that what previously would have taken a developer several manual steps — building, testing, packaging, and deploying — could be fully automated and triggered by a single `git push`. That kind of leverage is what drew me deeply into DevOps."

---

### Q4. What does DevOps mean to you, in your own words?

**Answer:**

"To me, DevOps is a culture and a set of practices that enable software teams to deliver changes to production faster, more frequently, and more reliably. It means breaking down the wall between developers who write code and operations engineers who keep systems running. In practice, it involves automation — CI/CD pipelines, infrastructure-as-code, configuration management — combined with monitoring and feedback loops so that issues are caught early.

In simple terms: write code → test automatically → build → deploy automatically → monitor → improve. DevOps is that continuous cycle."

---

### Q5. What is the difference between DevOps and traditional IT operations?

**Answer:**

| Dimension | Traditional IT Ops | DevOps |
|---|---|---|
| **Deployment frequency** | Monthly / Quarterly | Daily / Multiple times a day |
| **Team structure** | Siloed Dev and Ops teams | Cross-functional, collaborative teams |
| **Change management** | Manual approval gates | Automated pipeline with quality gates |
| **Failure response** | Reactive (fix after failure) | Proactive (monitoring + SLOs + runbooks) |
| **Infrastructure** | Hand-crafted servers | Infrastructure as Code (Terraform, Ansible) |
| **Feedback loops** | Slow (months to learn from production) | Fast (minutes through monitoring dashboards) |

**Example:** In traditional ops, deploying InternRecom would require a developer to send a WAR file to an ops team, who would manually SCP it to a server, restart Tomcat, and hope nothing broke. With DevOps, a `git push` to `main` triggers Jenkins, which builds the JAR, packages a Docker image, pushes it to a registry, and deploys it to EC2 automatically.

---

### Q6. What are the core principles of DevOps culture (CALMS)?

**Answer:**

The CALMS framework represents the five pillars of DevOps:

- **C — Culture:** Shared responsibility between Dev and Ops. Everyone owns the reliability of the product, not just the operations team.
- **A — Automation:** Automate repetitive tasks like building, testing, deploying, and provisioning. In your projects: Jenkins pipeline, Terraform, Ansible.
- **L — Lean:** Eliminate waste. Focus on delivering small, incremental changes (feature flags, short-lived branches) rather than big-bang releases.
- **M — Measurement:** Measure everything. Deployment frequency, lead time for changes, MTTR (Mean Time To Recovery), error rates. Prometheus + Grafana enable this.
- **S — Sharing:** Share knowledge, tools, and processes across teams. Post-mortems, runbooks, dashboards accessible to all.

---

### Q7. What is your strongest project, and why?

**Answer:**

"My strongest project is the Kubernetes Orchestration project (Jan–Apr 2026) because it required me to integrate multiple complex tools and concepts simultaneously.

I started by containerizing the application with Docker, then moved to Kubernetes to achieve high availability through ReplicaSets and rolling deployments. I configured Horizontal Pod Autoscaling (HPA) to automatically scale pods when CPU usage exceeded a defined threshold — for example, from 2 pods to 5 pods under load. I exposed the application externally using an Nginx Ingress Controller and set up Prometheus to scrape metrics and Grafana to visualize them in dashboards.

What made it my strongest project is that it touched every layer of a modern cloud-native system: packaging, orchestration, autoscaling, networking, and observability. It gave me a production-like perspective on how real applications are run at scale."

---

### Q8. What was the most challenging problem you solved in your Kubernetes project?

**Answer:**

"The most challenging problem was configuring Horizontal Pod Autoscaling (HPA) correctly. Initially, the HPA was not scaling the pods even under simulated load. After debugging with `kubectl describe hpa`, I found that the Metrics Server was not installed in the cluster, so Kubernetes had no CPU/memory metrics to act on.

I deployed the Kubernetes Metrics Server, verified it with `kubectl top pods`, and then re-applied the HPA configuration. Once the metrics pipeline was working, the HPA correctly scaled from 2 to 5 pods when CPU utilization crossed 50%.

This taught me that in Kubernetes, problems are often not in your own YAML but in a missing cluster-level dependency."

---

### Q9. What was your individual contribution vs. team contribution in InternRecom?

**Answer:**

"In InternRecom, my individual contributions were:
- Writing the Jenkins declarative pipeline (Jenkinsfile) and configuring webhooks with GitHub.
- Writing Terraform scripts to provision the EC2 instance and security groups on AWS.
- Writing Ansible playbooks to install Java, Docker, and dependencies on the EC2 host.
- Writing the Dockerfile to containerize the Spring Boot application.
- Configuring Nagios checks for HTTP service availability and resource thresholds.

The team collaborated on the application code itself and on the overall architecture design — deciding which tools to use and in what sequence they would be integrated."

---

### Q10. Where do you see yourself in 2 years as a DevOps engineer?

**Answer:**

"In two years, I see myself as a proficient DevOps engineer who has contributed to real production systems at scale. Specifically, I want to deepen my expertise in Kubernetes — working with multi-cluster setups, service meshes like Istio, and GitOps workflows using ArgoCD. I also want to become more fluent in writing production-grade Terraform modules and CI/CD pipelines that include security scanning stages (SAST/DAST).

Ultimately, my goal is to move toward a Platform Engineering or SRE role, where I help product teams ship features faster while maintaining system reliability."

---

## PART 2 — Git & Version Control

---

### Q11. Why did you choose Git as your Source Code Management tool?

**Answer:**

"We chose Git because it is the industry-standard distributed version control system. Unlike centralized systems such as SVN, Git gives every developer a complete local copy of the entire repository history, enabling them to commit, branch, and work offline.

Key reasons:
- **Branching is cheap and fast** — creating a feature branch takes milliseconds.
- **Distributed model** — no single point of failure for source code history.
- **Ecosystem integration** — GitHub integrates natively with Jenkins via webhooks, allowing our pipeline to trigger automatically on every push.
- **Community adoption** — Git is used in virtually every DevOps toolchain, so using it builds transferable skills.

**Alternative considered:** SVN (Subversion) is centralized and was common in legacy enterprises, but it lacks Git's branching agility and modern CI/CD integration."

---

### Q12. What is the difference between Git and GitHub?

**Answer:**

| Git | GitHub |
|---|---|
| A **distributed version control system** (a command-line tool) | A **cloud-hosted platform** that hosts Git repositories |
| Installed locally on your machine | Accessed via browser or API |
| Manages history, branches, commits | Adds collaboration features: pull requests, issues, Actions, wikis |
| Open-source software | A service owned by Microsoft |

**Analogy:** Git is the engine; GitHub is the car. You can use Git without GitHub (e.g., GitLab, Bitbucket, or a bare server), but you cannot use GitHub without Git underneath.

---

### Q13. Explain `git merge` vs `git rebase`.

**Answer:**

Both integrate changes from one branch into another, but they do so differently.

**`git merge`:** Creates a new "merge commit" that ties together the histories of both branches. The branch history is preserved with a fork and merge point visible in logs.

```
main:    A --- B --- C ------- M   (M = merge commit)
                      \       /
feature:               D --- E
```

**`git rebase`:** Rewrites the commit history of the feature branch so it appears to have started from the tip of `main`. Produces a cleaner, linear history.

```
main:    A --- B --- C
feature (after rebase): A --- B --- C --- D' --- E'
```

**When to use which:**
- Use `merge` for shared/public branches where history must be preserved.
- Use `rebase` for cleaning up local feature branches before raising a pull request.

> WARNING: Never rebase commits that have already been pushed to a shared remote branch — it rewrites history and will break teammates' repositories.

---

### Q14. What is a merge conflict, and how do you resolve one?

**Answer:**

A **merge conflict** occurs when two branches modify the same line of the same file differently, and Git cannot automatically determine which version to keep.

**Example:**
- `main` branch changes line 5 of `config.yaml` to `port: 8080`
- `feature/auth` branch changes the same line to `port: 9090`
- When you run `git merge feature/auth`, Git cannot auto-resolve this.

**Resolution steps:**
```bash
git merge feature/auth        # Conflict is reported
git status                    # Lists conflicting files
# Open the file — Git marks conflicts like this:
# <<<<<<< HEAD
# port: 8080
# =======
# port: 9090
# >>>>>>> feature/auth
# Manually edit the file to the correct value
git add config.yaml           # Mark as resolved
git commit                    # Complete the merge
```

**Best practice:** Use short-lived feature branches and merge frequently to minimize conflict surface area.

---

### Q15. Why do you push code to the main branch? Is that a good practice?

**Answer:**

"In our project, we pushed directly to `main` because it was a small team with a simple workflow and we were in an academic/learning context. However, in a professional environment, **pushing directly to `main` is not a good practice**.

The recommended approach is:
- Work on feature branches (e.g., `feature/login`, `fix/auth-bug`).
- Raise a **Pull Request (PR)** against `main`.
- The PR is reviewed by peers and must pass automated CI checks (tests, lint, security scans) before it can be merged.
- Protect `main` with **branch protection rules** in GitHub: require PR approval, require status checks to pass, and disable force pushes.

**Why this matters:** Pushing directly to `main` bypasses code review, risks breaking the production branch, and is a violation of compliance in many enterprise environments (SOC 2, ISO 27001)."

---

### Q16. If you push code to another branch, will the Jenkins pipeline trigger?

**Answer:**

"It depends entirely on how the Jenkins pipeline is configured.

In our InternRecom project, the GitHub webhook was configured to notify Jenkins only when a push event occurred on the `main` branch. So pushing to a feature branch like `feature/login` would **not** trigger the pipeline.

However, Jenkins supports multiple triggering strategies:

1. **Branch-specific webhook:** Only the configured branch (e.g., `main`) triggers the pipeline.
2. **Wildcard/regex branch matching:** You can configure Jenkins to trigger on any branch matching `feature/*`.
3. **Multi-branch Pipeline:** Jenkins automatically discovers all branches in the repo and creates a separate pipeline for each. In this case, pushing to any branch triggers its own pipeline.

**Professional practice:** In CI/CD, you want every branch to run unit tests on push (for fast feedback), but only the `main` branch should trigger the deployment stage to production."

---

### Q17. What is a Git branching strategy? Have you used Git Flow?

**Answer:**

A **branching strategy** is a set of conventions that dictates how branches are named, created, and merged in a team project.

**Git Flow** is a popular strategy with the following branches:
- `main` — production-ready code only
- `develop` — integration branch for features
- `feature/*` — individual feature development
- `release/*` — release stabilization and hotfixes
- `hotfix/*` — emergency fixes for production

**Simpler alternatives:**
- **GitHub Flow:** Only `main` + short-lived feature branches. Simple and works well with continuous delivery.
- **Trunk-Based Development:** All developers commit to `main` (trunk) frequently using feature flags. Used by large tech companies for maximum CI/CD speed.

"In our project, we used a simplified GitHub Flow — feature branches were merged to `main` via PRs."

---

### Q18. What is the difference between `git fetch` and `git pull`?

**Answer:**

| Command | What it does |
|---|---|
| `git fetch` | Downloads changes from the remote into your **local remote-tracking branches** (e.g., `origin/main`) but does **NOT** modify your working directory or current branch |
| `git pull` | Is equivalent to `git fetch` + `git merge`. It downloads changes AND immediately merges them into your current local branch |

**When to use `fetch`:** When you want to see what changes exist on the remote before deciding to merge them. Safer for code review purposes.

**When to use `pull`:** When you are ready to bring the remote changes into your working branch immediately.

---

### Q19. What is `git stash` used for?

**Answer:**

`git stash` temporarily shelves (stashes) your uncommitted local changes so you can switch to another branch or pull updates without losing your work.

**Example scenario:**
```bash
# You are mid-way through implementing a feature
# A critical hotfix is needed on main
git stash           # Save your uncommitted work
git checkout main   # Switch to main safely
git pull            # Pull the latest changes
# Fix the hotfix, commit, push
git checkout feature/my-feature
git stash pop       # Restore your shelved work
```

**Useful commands:**
```bash
git stash list        # Show all stashed entries
git stash apply       # Apply stash without removing it
git stash pop         # Apply and remove stash
git stash drop        # Discard the latest stash
```

---

### Q20. How do you revert a commit that has already been pushed?

**Answer:**

Use `git revert` — it creates a **new commit** that undoes the changes of the target commit, preserving the full history.

```bash
git log --oneline              # Find the commit hash
git revert <commit-hash>       # Creates an undo commit
git push origin main           # Push the revert commit
```

**Why NOT `git reset`?** `git reset --hard` rewrites history and is destructive on a shared branch. It will force other developers to re-sync their repositories, causing confusion. Use `revert` on public/shared branches always.

---

## PART 3 — Docker

---

### Q21. What is the difference between a Docker Image and a Docker Container?

**Answer:**

| Aspect | Docker Image | Docker Container |
|---|---|---|
| **Definition** | A **read-only, layered blueprint** — like a class in OOP | A **running instance** of an image — like an object instantiated from a class |
| **State** | Static, immutable | Dynamic, has a writable layer on top |
| **Storage** | Stored in a registry (Docker Hub, ECR, etc.) | Lives in memory/disk on the host until stopped |
| **Creation** | Built from a `Dockerfile` using `docker build` | Created from an image using `docker run` |
| **Analogy** | A recipe for a cake | The actual baked cake |

**Example from your project:**
```bash
# Build an image from your Dockerfile
docker build -t internrecom-app:1.0 .

# Run a container from that image
docker run -d -p 8080:8080 --name internrecom internrecom-app:1.0

# One image can run many containers
docker run -d -p 8081:8080 --name internrecom-2 internrecom-app:1.0
```

---

### Q22. Write a simple Dockerfile and explain each instruction.

**Answer:**

Here is a Dockerfile for your Spring Boot application (InternRecom):

```dockerfile
# Use the official Eclipse Temurin JDK 17 as the base image
FROM eclipse-temurin:17-jdk-alpine

# Set the maintainer label (metadata)
LABEL maintainer="nihal.kumar@example.com"

# Set the working directory inside the container
WORKDIR /app

# Copy only the built JAR file from the host into the container
COPY target/internrecom-0.0.1-SNAPSHOT.jar app.jar

# Expose port 8080 to document that the application listens on this port
EXPOSE 8080

# Define the command that runs when the container starts
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Instruction-by-instruction explanation:**

| Instruction | Purpose |
|---|---|
| `FROM` | Specifies the base image. Every image starts from another image (or `scratch`). |
| `LABEL` | Adds metadata (key-value pairs) to the image. |
| `WORKDIR` | Sets the working directory. Equivalent to `mkdir /app && cd /app`. |
| `COPY` | Copies files from the **build context** (your host machine) into the image. |
| `EXPOSE` | Documentation — declares which port the app uses. |
| `ENTRYPOINT` | Defines the primary process that runs when the container starts. |

---

### Q23. Is your Dockerfile production-ready? What improvements would you make?

**Answer:**

"The basic Dockerfile I wrote is functional but not fully production-ready. Here are the improvements I would make:

**1. Use a multi-stage build** to separate the build environment from the runtime image:
```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline -B   # Cache dependencies
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime (much smaller image)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/internrecom-*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**2. Run as a non-root user** (security hardening):
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

**3. Use a `.dockerignore` file** to prevent copying unnecessary files:
```
.git
target/
*.md
*.log
```

**4. Add health checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -qO- http://localhost:8080/actuator/health || exit 1
```

**5. Pin exact image versions** — instead of `eclipse-temurin:17-jdk-alpine`, use `eclipse-temurin:17.0.9_9-jdk-alpine` to avoid unexpected breaking changes from upstream."

---

### Q24. What is the purpose of `WORKDIR`?

**Answer:**

`WORKDIR` sets the **working directory** inside the image for all subsequent `RUN`, `COPY`, `ADD`, `CMD`, and `ENTRYPOINT` instructions.

**Without `WORKDIR`:**
```dockerfile
RUN mkdir /app
RUN cd /app     # This has NO effect — each RUN spawns a new shell
COPY app.jar /  # File lands in the root /
```

**With `WORKDIR`:**
```dockerfile
WORKDIR /app    # Creates /app if it doesn't exist AND sets it as cwd
COPY app.jar .  # Copies to /app/app.jar — clean and intentional
```

**Benefits:**
- Keeps the image organized and predictable.
- Avoids files being dropped into the root `/` directory.
- Makes `COPY app.jar .` work correctly.
- When you `docker exec -it <container> sh`, you land in the `WORKDIR` path.

---

### Q25. What is the purpose of `ENTRYPOINT`? How is it different from `CMD`?

**Answer:**

Both `ENTRYPOINT` and `CMD` define what executes when a container starts, but they serve different roles:

| | `ENTRYPOINT` | `CMD` |
|---|---|---|
| **Purpose** | Defines the **main executable** — the process the container is built to run | Provides **default arguments** to `ENTRYPOINT`, or a default command that can be overridden |
| **Override behavior** | Cannot be overridden by `docker run` arguments (unless `--entrypoint` flag is used) | Is **overridden** by anything passed after the image name in `docker run` |
| **Use case** | Fixed binary (e.g., `java -jar app.jar`) | Default arguments (e.g., `--server.port=8080`) |

**Example:**
```dockerfile
ENTRYPOINT ["java", "-jar", "app.jar"]
CMD ["--server.port=8080"]
```

```bash
# Uses both — runs: java -jar app.jar --server.port=8080
docker run myapp

# Overrides CMD only — runs: java -jar app.jar --server.port=9090
docker run myapp --server.port=9090
```

**Rule of thumb:** Use `ENTRYPOINT` for the binary, `CMD` for default arguments.

---

### Q26. Why use `COPY app.jar app.jar` instead of `COPY . .`?

**Answer:**

`COPY . .` copies **everything** in the build context into the image — including source code files, test directories, `.git` folders, configuration files, and other artifacts that are never needed at runtime. This leads to:

1. **Bloated image size** — unnecessary files inflate the image.
2. **Security risk** — sensitive files (`.env`, credentials, private keys) may be inadvertently included.
3. **Cache inefficiency** — any change to any file in `.` invalidates the Docker layer cache, forcing a full rebuild.

`COPY target/internrecom-0.0.1-SNAPSHOT.jar app.jar` copies **only the built artifact** — the one file the container actually needs to run.

**Best practice combination:**
```dockerfile
# 1. Use a .dockerignore file to exclude unwanted files
# 2. Copy only the artifact you need
COPY target/internrecom-0.0.1-SNAPSHOT.jar app.jar
```

**Cache optimization pattern — copy pom.xml first:**
```dockerfile
COPY pom.xml .
RUN mvn dependency:go-offline     # This layer is cached as long as pom.xml doesn't change
COPY src ./src
RUN mvn package
```

---

### Q27. What is a multi-stage Docker build, and why is it useful?

**Answer:**

A **multi-stage build** uses multiple `FROM` statements in a single Dockerfile, allowing you to use a heavy build environment in an early stage and copy only the final artifact into a lightweight runtime image.

```dockerfile
# Stage 1: BUILD (heavy — includes JDK, Maven, source code)
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: RUNTIME (lightweight — only JRE, no source, no Maven)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Benefits:**
- **Smaller final image:** The builder stage can be 500 MB; the runtime stage may be only 150 MB.
- **Improved security:** Source code, build tools, and intermediate files never exist in the production image.
- **Single Dockerfile:** No need for separate build scripts.

---

### Q28. How do you reduce Docker image size?

**Answer:**

1. **Use Alpine-based or distroless base images** — `eclipse-temurin:17-jre-alpine` is far smaller than `eclipse-temurin:17-jdk` (full Debian).
2. **Multi-stage builds** — discard build tools from the final image.
3. **Chain RUN commands** to reduce layers:
   ```dockerfile
   # Bad — creates 3 layers
   RUN apt-get update
   RUN apt-get install -y curl
   RUN rm -rf /var/lib/apt/lists/*

   # Good — single layer, and cleanup happens in same layer
   RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
   ```
4. **Use `.dockerignore`** to exclude large unnecessary files from the build context.
5. **Copy only what is needed** — `COPY target/app.jar app.jar` not `COPY . .`.
6. **Avoid installing debug tools in production images** (curl, wget, vim).

---

### Q29. What is the difference between `ADD` and `COPY`?

**Answer:**

| Feature | `COPY` | `ADD` |
|---|---|---|
| **Basic file copy** | Yes | Yes |
| **Copies directories** | Yes | Yes |
| **Auto-extracts tar archives** | No | Yes — `ADD archive.tar.gz /dest` extracts automatically |
| **Fetches remote URLs** | No | Yes — `ADD https://example.com/file.jar /app/` |
| **Recommended for** | Everything except tar extraction and URL fetching | Special cases only |

**Best practice:** Use `COPY` by default. Use `ADD` only when you explicitly need its tar extraction feature. Fetching URLs with `ADD` is discouraged — use `RUN curl` instead because it gives you better control over error handling and cleanup.

---

### Q30. How do containers differ from virtual machines?

**Answer:**

| Aspect | Virtual Machine (VM) | Container |
|---|---|---|
| **Isolation level** | Full OS isolation — each VM has its own kernel | Process-level isolation — shares the host OS kernel |
| **Size** | GBs (includes full guest OS) | MBs (only application + dependencies) |
| **Startup time** | Minutes (boots an OS) | Seconds or milliseconds |
| **Resource overhead** | High (full OS running even when idle) | Low (only app processes consume resources) |
| **Portability** | Less portable (hypervisor dependent) | Highly portable — "build once, run anywhere" |
| **Security boundary** | Strong (separate kernel) | Weaker (kernel is shared) — needs additional hardening |
| **Use case** | Running different OSes, strong isolation, legacy apps | Microservices, CI/CD pipelines, cloud-native apps |

**Analogy:** VMs are like renting separate apartments (each with its own electricity, plumbing, kitchen). Containers are like co-living spaces (shared infrastructure, but each person has their own room).

---

### Q31. What is Docker Compose, and how did you use it in your projects?

**Answer:**

**Docker Compose** is a tool for defining and running multi-container Docker applications. You describe your entire application stack in a single `docker-compose.yml` file — services, networks, volumes — and start everything with one command: `docker-compose up`.

**Example `docker-compose.yml` for InternRecom:**
```yaml
version: '3.8'
services:
  app:
    image: internrecom-app:1.0
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://db:3306/internrecom
      - SPRING_DATASOURCE_PASSWORD=${DB_PASSWORD}
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: internrecom
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
```

**Usage:**
```bash
docker-compose up -d          # Start all services in background
docker-compose logs -f app    # Follow logs for the app service
docker-compose down           # Stop and remove containers
```

---

### Q32. What is `depends_on` in Docker Compose, and what are its limitations?

**Answer:**

`depends_on` controls the **startup order** of services in Docker Compose. It ensures that the listed services are started before the dependent service.

**Example:**
```yaml
services:
  app:
    depends_on:
      - db   # 'db' container starts before 'app'
```

**Critical Limitation:** `depends_on` only waits for the container to **start** (i.e., the `docker run` process succeeds), NOT for the service inside to be **ready** (e.g., MySQL accepting connections). MySQL can take 10–30 seconds to initialize even after its container starts.

**Solution — use healthchecks:**
```yaml
services:
  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    depends_on:
      db:
        condition: service_healthy   # Waits until db passes its healthcheck
```

---

### Q33. How do you deploy multiple microservices using Docker Compose?

**Answer:**

Define each microservice as a separate service in `docker-compose.yml`, connected via a shared network:

```yaml
version: '3.8'
services:
  user-service:
    image: myapp/user-service:1.0
    ports:
      - "8081:8080"
    networks:
      - microservices-net

  order-service:
    image: myapp/order-service:1.0
    ports:
      - "8082:8080"
    depends_on:
      - user-service
    networks:
      - microservices-net

  api-gateway:
    image: myapp/api-gateway:1.0
    ports:
      - "80:8080"
    depends_on:
      - user-service
      - order-service
    networks:
      - microservices-net

networks:
  microservices-net:
```

**Inter-service communication:** Services in the same Compose network can communicate using the **service name as hostname** (Docker's internal DNS). For example, `order-service` can call `http://user-service:8080/users`.

**Scaling:**
```bash
docker-compose up -d --scale user-service=2    # Scale user-service to 2 replicas
```

---

### Q34. How do you manage environment-specific configuration in Docker?

**Answer:**

**Option 1: `.env` file** — Compose automatically reads a `.env` file in the same directory:
```env
# .env
DB_PASSWORD=secret123
APP_ENV=production
```
```yaml
# docker-compose.yml
environment:
  - SPRING_DATASOURCE_PASSWORD=${DB_PASSWORD}
```

**Option 2: Multiple Compose files** for different environments:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Option 3: `ARG` vs `ENV` in Dockerfile:**

| | `ARG` | `ENV` |
|---|---|---|
| **Scope** | Available only during `docker build` | Available at build time AND runtime (inside the container) |
| **Use case** | Build-time configuration (e.g., version numbers) | Runtime configuration (e.g., database URL) |
| **Visible in image** | Not persisted in the final image | Persisted in image layers |

```dockerfile
ARG APP_VERSION=1.0          # Build-time only
ENV SPRING_PROFILES_ACTIVE=prod  # Runtime
```

**Security note:** Never pass secrets via `ARG` — they can be seen in `docker history`. Use Docker secrets or a vault solution for credentials.

---

### Q35. What is a Docker volume, and why would you use one?

**Answer:**

A **Docker volume** is a persistent storage mechanism managed by Docker that exists outside the container's lifecycle. When a container is deleted, its writable layer is lost — but data in a volume persists.

**Why use volumes:**
- Persist database data (MySQL, PostgreSQL) across container restarts.
- Share data between multiple containers.
- Better performance than bind mounts for large data.

**Types of Docker storage:**
1. **Volumes** — managed by Docker (`/var/lib/docker/volumes/`). Best for production.
2. **Bind mounts** — maps a host directory directly into the container. Good for development (live code reload).
3. **tmpfs mounts** — in-memory only. Useful for sensitive data that should not be written to disk.

**Example:**
```bash
# Create a named volume
docker volume create db-data

# Use the volume in a container
docker run -d -v db-data:/var/lib/mysql mysql:8.0

# Inspect volume
docker volume inspect db-data
```

---

### Q36. What is a Docker network, and what types are available?

**Answer:**

A Docker network enables containers to communicate with each other and with the outside world.

| Network Type | Description | Use Case |
|---|---|---|
| **bridge** | Default network. Containers on the same bridge can communicate by IP or name | Single-host multi-container apps |
| **host** | Container shares the host's network namespace — no network isolation | High performance, eliminates NAT overhead |
| **none** | No network access | Completely isolated containers |
| **overlay** | Multi-host networking for Docker Swarm clusters | Distributed, multi-host container communication |
| **macvlan** | Assigns a MAC address to the container, making it appear as a physical device on the network | Legacy app integration |

**Custom bridge network (recommended for Compose):**
```bash
docker network create app-net
docker run --network app-net --name app1 myapp:1.0
docker run --network app-net --name app2 myapp:1.0
# app1 and app2 can now resolve each other by name
```

---

### Q37. How do you check logs of a running container?

**Answer:**

```bash
# View all logs
docker logs <container-name>

# Follow logs in real-time (like tail -f)
docker logs -f <container-name>

# Show only last N lines
docker logs --tail 100 <container-name>

# Show logs with timestamps
docker logs -t <container-name>

# Combine: last 50 lines, real-time, with timestamps
docker logs --tail 50 -ft <container-name>
```

**In Docker Compose:**
```bash
docker-compose logs -f app       # Follow logs for 'app' service
docker-compose logs --tail=50    # Last 50 lines for all services
```

---

### Q38. How would you debug a container that keeps restarting?

**Answer:**

When a container is in a restart loop, follow this systematic approach:

```bash
# 1. Check the container's status and exit code
docker ps -a
# Look for "Restarting" status and the exit code

# 2. Read the logs from the last run (even after container stops)
docker logs <container-name>
# Common errors: "Address already in use", "Connection refused", missing env vars

# 3. Inspect the container configuration
docker inspect <container-name>
# Check: Env vars, port bindings, volume mounts, health check commands

# 4. Override ENTRYPOINT to get a shell and debug interactively
docker run -it --entrypoint sh myapp:1.0
# Now you can manually run the java -jar app.jar command and see the error

# 5. Check host resource constraints
df -h        # Disk space
free -m      # Memory
```

**Common root causes:**
- Missing environment variable (e.g., `SPRING_DATASOURCE_URL` not set — application crashes on startup)
- Port conflict on the host
- Java out of memory error (`-Xmx` too low for the container's memory limit)
- Dependency service not ready (database not accepting connections yet)

---

## PART 4 — Kubernetes

---

### Q39. Explain your Kubernetes project end-to-end.

**Answer:**

"My Kubernetes project involved deploying a containerized web application with enterprise-grade orchestration, autoscaling, and observability.

**Architecture:**

1. **Containerization:** I first built a Docker image of the application and pushed it to Docker Hub.

2. **Kubernetes Deployment:** I created a `Deployment` manifest with 2 initial replicas. The Deployment managed a `ReplicaSet`, which in turn managed the `Pod` instances. This gave us rolling update and rollback capability.

3. **Service (ClusterIP):** I exposed the pods internally using a `ClusterIP` Service so the pods could be discovered within the cluster.

4. **Ingress Controller:** I deployed an Nginx Ingress Controller and created an `Ingress` resource to route external HTTP traffic to the internal service using hostname-based routing.

5. **Horizontal Pod Autoscaling (HPA):** I configured an HPA that monitors CPU utilization. When average CPU across pods exceeded 50%, HPA automatically scaled from 2 to up to 10 replicas. When load dropped, it scaled back down.

6. **Monitoring:** I deployed Prometheus using a Helm chart, which scraped metrics from the cluster. I connected Grafana to Prometheus and built dashboards to visualize pod health, request rates, and resource utilization."

---

### Q40. What is the difference between a Pod, Deployment, and ReplicaSet?

**Answer:**

| Object | Description | Manages |
|---|---|---|
| **Pod** | The smallest deployable unit in Kubernetes. Contains one or more containers that share network and storage. | Individual container(s) |
| **ReplicaSet** | Ensures a specified number of identical Pod replicas are running at all times. Replaces crashed pods automatically. | Pods |
| **Deployment** | A higher-level abstraction that manages ReplicaSets. Adds rolling updates, rollback, and declarative update strategies. | ReplicaSets then Pods |

**Relationship:**
```
Deployment
   └── ReplicaSet (v1)   [old version]
   └── ReplicaSet (v2)   [current version]
          └── Pod-1
          └── Pod-2
          └── Pod-3
```

**You almost always create a Deployment, not a ReplicaSet directly**, because Deployments give you version management on top of the replication guarantee.

---

### Q41. Why did you need ReplicaSets if Deployments already manage Pods?

**Answer:**

"The distinction is important. A `ReplicaSet` provides only **replication** — ensure N copies of a pod are running. But it has no concept of application version or upgrade strategy.

A `Deployment` wraps a `ReplicaSet` and adds:
- **Rolling updates** — creates a new ReplicaSet (v2) and gradually scales it up while scaling down the old ReplicaSet (v1).
- **Rollback** — `kubectl rollout undo deployment/my-app` reverts to the previous ReplicaSet.
- **Revision history** — keeps track of all previous ReplicaSets for rollback purposes.

In practice, when I deploy a new version of the application, Kubernetes creates a second ReplicaSet. The Deployment controller shifts traffic from the old ReplicaSet to the new one, pod by pod. If the new pods fail their readiness probes, the rollout pauses and can be rolled back.

**So: ReplicaSets are the mechanism; Deployments are the policy layer on top of that mechanism.**"

---

### Q42. What is Horizontal Pod Autoscaling (HPA), and how did you configure it?

**Answer:**

**HPA** automatically adjusts the number of pod replicas in a Deployment or ReplicaSet based on observed resource metrics (CPU, memory) or custom metrics.

**Configuration in my project:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: internrecom-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: internrecom-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50   # Scale up when avg CPU > 50%
```

**Prerequisites:** The Kubernetes **Metrics Server** must be installed and running (`kubectl top pods` must work).

**Commands used:**
```bash
kubectl apply -f hpa.yaml
kubectl get hpa                           # View current/desired/max replicas
kubectl describe hpa internrecom-hpa      # Debug scaling decisions
```

---

### Q43. What metrics does HPA use to decide scaling?

**Answer:**

HPA can use three types of metrics:

1. **Resource Metrics** — Built-in CPU and memory metrics from the Metrics Server.
2. **Custom Metrics** — Application-specific metrics exposed via the Prometheus Adapter (e.g., requests per second, queue depth).
3. **External Metrics** — Metrics from external systems (e.g., AWS SQS queue length).

**Scaling formula:**
```
desired_replicas = ceil(current_replicas x (current_metric / target_metric))
```

Example: 3 replicas, current CPU = 90%, target = 50% → `ceil(3 x 90/50) = ceil(5.4) = 6 replicas`

---

### Q44. What is the difference between a Kubernetes Service and an Ingress?

**Answer:**

| | Kubernetes Service | Ingress |
|---|---|---|
| **Purpose** | Stable internal or external network endpoint for pods | HTTP/HTTPS routing layer — routes external traffic to services based on rules |
| **Layer** | Layer 4 (TCP/UDP) | Layer 7 (HTTP/HTTPS) |
| **Routing** | By pod labels only | By hostname and URL path |
| **SSL/TLS** | Not natively (except LoadBalancer via cloud) | Native TLS termination |
| **Cost** | `LoadBalancer` type creates one cloud LB per service | Single Ingress Controller handles all services — cost-efficient |

**Example flow:**
```
Internet → Ingress Controller (Nginx) → Route by host/path → ClusterIP Service → Pods
```

---

### Q45. What types of Services are there in Kubernetes?

**Answer:**

| Type | Description | Use Case |
|---|---|---|
| **ClusterIP** | Default. Exposes the service on an internal cluster IP. Not reachable from outside. | Internal pod-to-pod communication |
| **NodePort** | Exposes the service on each Node's IP at a static port (30000–32767). | Development, testing, or simple external access |
| **LoadBalancer** | Provisions a cloud provider's load balancer. Routes external traffic to the service. | Production external-facing services on AWS/GCP/Azure |
| **ExternalName** | Maps a service to an external DNS name. | Abstracting external services (e.g., an RDS database) |

**In my project:** I used `ClusterIP` for internal pod communication and `Ingress` with an Nginx controller for external traffic routing.

---

### Q46. How does internal service-to-service communication work in Kubernetes?

**Answer:**

Kubernetes has a built-in DNS system (CoreDNS) that assigns every `Service` a DNS name. Pods resolve these names to find each other without needing to know IP addresses.

**DNS format:** `<service-name>.<namespace>.svc.cluster.local`

**Example:**
```
Service: order-service in namespace: default
DNS:     order-service.default.svc.cluster.local
Short:   order-service   (within same namespace)
```

So if `user-service` needs to call `order-service`, it simply uses:
```
http://order-service:8080/orders
```

Kubernetes routes this to the `order-service` ClusterIP, which load-balances across all healthy pods matching the service's selector.

---

### Q47. How did you expose your application to external users?

**Answer:**

"I used an Nginx Ingress Controller and an Ingress resource.

**Steps:**
1. Deploy Nginx Ingress Controller (via Helm):
```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

2. Create an Ingress resource:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: internrecom-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: internrecom.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: internrecom-service
            port:
              number: 8080
```

The user accesses `http://internrecom.local` and the request flows: Internet → Nginx Ingress → ClusterIP Service → Pod."

---

### Q48. What is a namespace in Kubernetes, and why use one?

**Answer:**

A **namespace** is a virtual cluster within a physical Kubernetes cluster. It partitions resources (pods, services, deployments) into separate scopes.

**Default namespaces:**
- `default` — where objects go if no namespace is specified
- `kube-system` — Kubernetes control plane components
- `kube-public` — publicly readable data

**Why use namespaces:**
- **Isolation:** Separate `dev`, `staging`, and `prod` environments on the same cluster.
- **Access control:** Apply RBAC policies per namespace.
- **Resource quotas:** Limit how much CPU/memory a team or environment can use.

```bash
kubectl create namespace dev
kubectl apply -f deployment.yaml -n dev
kubectl get pods -n dev
kubectl get all --all-namespaces
```

---

### Q49. What is a ConfigMap vs a Secret?

**Answer:**

| | ConfigMap | Secret |
|---|---|---|
| **Purpose** | Stores non-sensitive configuration data | Stores sensitive data (passwords, tokens, keys) |
| **Encoding** | Plain text (UTF-8) | Base64 encoded (NOT encrypted by default) |
| **Examples** | `APP_PORT=8080`, `LOG_LEVEL=INFO` | `DB_PASSWORD=secret`, `API_KEY=abc123` |
| **Security** | Not protected | Can be encrypted at rest with KMS (etcd encryption) |

**ConfigMap example:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_PORT: "8080"
  LOG_LEVEL: "INFO"
```

**Secret example:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: c2VjcmV0MTIz   # base64 encoded "secret123"
```

> WARNING: Secrets are only base64-encoded by default, not encrypted. For real security, enable etcd encryption or use external secret managers (AWS Secrets Manager, HashiCorp Vault + External Secrets Operator).

---

### Q50. What happens when a Pod crashes — how does Kubernetes recover it?

**Answer:**

When a pod crashes, the recovery mechanism depends on how it was created:

1. **If managed by a Deployment/ReplicaSet:** The ReplicaSet controller detects that the actual number of running pods is below the desired count. It automatically creates a replacement pod on a healthy node. This is nearly instantaneous.

2. **Restart Policy:** Each pod has a `restartPolicy` field:
   - `Always` (default for Deployments) — container is restarted regardless of exit code.
   - `OnFailure` — restart only if exit code is non-zero.
   - `Never` — container is not restarted.

3. **CrashLoopBackOff:** If a container crashes repeatedly, Kubernetes applies an exponential backoff (10s → 20s → 40s → up to 5 minutes) to prevent a crash-looping container from consuming excessive resources.

**Recovery flow:**
```
Pod crashes → ReplicaSet detects deficit → Scheduler assigns new Pod to a Node
→ Kubelet on that Node pulls image → Container starts → Readiness probe passes
→ Service directs traffic to the new Pod
```

---

### Q51. What is a liveness probe vs a readiness probe?

**Answer:**

Both are health checks Kubernetes performs on containers, but they serve different purposes:

| | Liveness Probe | Readiness Probe |
|---|---|---|
| **Question it answers** | "Is this container alive?" | "Is this container ready to serve traffic?" |
| **On failure** | Kubernetes **kills and restarts** the container | Kubernetes **removes the pod from the Service's endpoint** (stops sending traffic), but does NOT restart |
| **Use case** | Detect deadlocks or hangs | Detect when an app is still starting up or temporarily overloaded |

**Example configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
```

**Startup probe** (a third type): Disables liveness and readiness probes until the container has had enough time to start. Useful for slow-starting applications.

---

### Q52. How do you perform a rolling update/rollback of a Deployment?

**Answer:**

**Rolling Update:**
```bash
# Update the image version
kubectl set image deployment/internrecom-app \
  app=internrecom-app:2.0

# Watch the rollout progress
kubectl rollout status deployment/internrecom-app
```

**Rollback:**
```bash
# View rollout history
kubectl rollout history deployment/internrecom-app

# Rollback to the previous version
kubectl rollout undo deployment/internrecom-app

# Rollback to a specific revision
kubectl rollout undo deployment/internrecom-app --to-revision=2
```

**Rolling Update Strategy (default):**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1         # Max extra pods created during update
    maxUnavailable: 0   # No pods taken down before new one is ready
```

This ensures zero-downtime deployments.

---

### Q53. What is the role of `kubectl` and name a few commands you use often?

**Answer:**

`kubectl` is the command-line interface (CLI) for interacting with a Kubernetes cluster. It communicates with the Kubernetes API server to create, read, update, and delete resources.

**Frequently used commands:**
```bash
kubectl get pods                            # List pods in default namespace
kubectl get pods -n kube-system            # List pods in a specific namespace
kubectl get pods -o wide                   # Shows Node IP, pod IP
kubectl describe pod <pod-name>            # Detailed info and events
kubectl logs <pod-name>                    # Container logs
kubectl logs -f <pod-name>                 # Follow logs
kubectl exec -it <pod-name> -- bash        # Shell into a container
kubectl apply -f deployment.yaml           # Apply a manifest
kubectl delete -f deployment.yaml          # Delete resources from manifest
kubectl scale deployment internrecom-app --replicas=5
kubectl rollout status deployment/internrecom-app
kubectl rollout undo deployment/internrecom-app
kubectl top pods                            # Resource usage (needs Metrics Server)
kubectl get hpa                             # View HPA status
```

---

### Q54. How would you troubleshoot a Pod stuck in `CrashLoopBackOff`?

**Answer:**

`CrashLoopBackOff` means the container is starting, crashing, and Kubernetes is backing off before restarting it again.

**Systematic debugging approach:**
```bash
# Step 1: Get the pod status and exit code
kubectl describe pod <pod-name>
# Look for: Last State, Exit Code, Reason

# Step 2: Read the container logs (including previous crash)
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Step 3: Common causes from logs:
# - "Address already in use" → port conflict
# - "Connection refused: db:3306" → database not ready or wrong env vars
# - "java.lang.OutOfMemoryError" → memory limit too low
# - Missing env var → NullPointerException at startup

# Step 4: Override the ENTRYPOINT to debug interactively
kubectl run debug --image=internrecom-app:1.0 \
  --restart=Never --command -- sleep 3600
kubectl exec -it debug -- sh
# Manually run the startup command to see the error
```

---

### Q55. How would you troubleshoot a Pod stuck in `Pending` state?

**Answer:**

A `Pending` pod has been accepted by Kubernetes but has not been scheduled onto a Node yet.

```bash
kubectl describe pod <pod-name>
# Look at the Events section at the bottom
```

**Common causes in the Events output:**

| Event Message | Root Cause | Solution |
|---|---|---|
| `0/3 nodes available: insufficient cpu` | No node has enough CPU to fit the pod | Scale up the cluster, reduce `resources.requests.cpu` |
| `0/3 nodes available: insufficient memory` | No node has enough memory | Same as above |
| `0/3 nodes: node(s) had taints that the pod didn't tolerate` | Node is tainted (e.g., master-only node) | Add `tolerations` to the pod spec |
| `0/3 nodes: pod has unbound PersistentVolumeClaims` | PVC is not bound to a PV | Check PVC status (`kubectl get pvc`), ensure StorageClass is configured |
| `ImagePullBackOff` | Cannot pull the Docker image | Check image name, tag, and registry credentials |

---

## PART 5 — Jenkins & CI/CD

---

### Q56. What was your role in Jenkins?

**Answer:**

"In the InternRecom project, I was responsible for the end-to-end setup and configuration of the Jenkins CI/CD pipeline:

1. **Installation:** Installed Jenkins on an AWS EC2 instance running Ubuntu, including Java (dependency) and required plugins.
2. **Jenkinsfile authoring:** Wrote the declarative Jenkinsfile with stages: Checkout → Build (Maven) → Test → Docker Build → Docker Push → Deploy.
3. **Credentials management:** Stored Docker Hub credentials and SSH keys securely in Jenkins' credential store (never hardcoded).
4. **Webhook configuration:** Configured a GitHub webhook to trigger the Jenkins pipeline on every push to `main`.
5. **Plugin configuration:** Installed and configured Git, Docker Pipeline, Maven Integration, and SSH Agent plugins.
6. **Build monitoring:** Monitored build logs, diagnosed failures, and iterated on the pipeline configuration."

---

### Q57. Explain the architecture of your CI/CD pipeline.

**Answer:**

```
Developer → git push → GitHub → webhook → Jenkins (EC2)
                                               |
                        +----------------------+-------------------+
                        |                      |                   |
                   Stage: Build           Stage: Test        Stage: Docker
                   (mvn package)         (mvn test)         (docker build & push)
                                                                   |
                                                          Docker Hub Registry
                                                                   |
                                                      Stage: Deploy (SSH to EC2)
                                                      docker pull + docker run
                                                                   |
                                                          Application running
                                                          on port 8080 (AWS EC2)
                                                                   |
                                                           Nagios monitoring
                                                      (HTTP check + resource alerts)
```

**Detailed flow:**
1. Developer pushes code to GitHub `main` branch.
2. GitHub sends a webhook POST to Jenkins.
3. Jenkins Checkout stage clones the repository.
4. Maven Build stage compiles the code and produces a JAR file.
5. Maven Test stage runs unit tests.
6. Docker Build stage builds a new Docker image tagged with the build number.
7. Docker Push stage pushes the image to Docker Hub.
8. Deploy stage SSH's into the AWS EC2 deployment server, pulls the new image, stops the old container, and starts a new one.
9. Nagios performs ongoing HTTP health checks and alerts on failures.

---

### Q58. Explain your CI/CD pipeline project end-to-end.

**Answer:**

"The InternRecom project is a web application that connects interns with companies. The complete E2E flow:

**Infrastructure Provisioning (Terraform):**
```hcl
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  key_name      = var.key_name
  security_groups = [aws_security_group.app_sg.name]
}
```

**Server Configuration (Ansible):**
```yaml
- hosts: app_server
  tasks:
    - name: Install Java 17
      apt: name=openjdk-17-jdk state=present
    - name: Install Docker
      apt: name=docker.io state=present
    - name: Start Docker
      service: name=docker state=started enabled=yes
```

**CI Pipeline (Jenkinsfile):**
```groovy
pipeline {
  agent any
  stages {
    stage('Checkout')  { steps { checkout scm } }
    stage('Build')     { steps { sh 'mvn package -DskipTests' } }
    stage('Test')      { steps { sh 'mvn test' } }
    stage('Docker Build') {
      steps {
        sh 'docker build -t nihal/internrecom:${BUILD_NUMBER} .'
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
            usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          sh 'docker push nihal/internrecom:${BUILD_NUMBER}'
        }
      }
    }
    stage('Deploy') {
      steps {
        sshagent(['ec2-ssh-key']) {
          sh 'ssh ubuntu@${EC2_IP} "docker pull nihal/internrecom:${BUILD_NUMBER} && docker stop internrecom || true && docker rm internrecom || true && docker run -d --name internrecom -p 8080:8080 nihal/internrecom:${BUILD_NUMBER}"'
        }
      }
    }
  }
}
```"

---

### Q59. What is the difference between a Jenkins Freestyle job and a Pipeline job?

**Answer:**

| | Freestyle Job | Pipeline Job |
|---|---|---|
| **Configuration** | GUI-based (click and configure) | Code-based — defined in a `Jenkinsfile` |
| **Complexity** | Simple, linear tasks | Multi-stage, complex workflows with conditions, loops, parallel stages |
| **Version control** | Not stored in SCM — lives in Jenkins only | `Jenkinsfile` is stored in the Git repository alongside the code |
| **Repeatability** | Configuration can drift, harder to reproduce | Fully reproducible — pipeline is code |
| **Advanced features** | Limited | Supports parallelism, shared libraries, input steps, try/catch |
| **Audit trail** | Limited | Full history via Git |

**Best practice:** Always use Pipeline jobs with a `Jenkinsfile` in your repository. This is called **Pipeline-as-Code** and is the industry standard.

---

### Q60. What is a Jenkinsfile, and what is the difference between Declarative and Scripted pipelines?

**Answer:**

A `Jenkinsfile` is a text file written in Groovy that defines the CI/CD pipeline as code. It lives in the root of the source code repository.

**Declarative Pipeline** (recommended):
```groovy
pipeline {
  agent any
  environment {
    APP_NAME = 'internrecom'
  }
  stages {
    stage('Build') {
      steps {
        sh 'mvn package'
      }
    }
    stage('Test') {
      steps {
        sh 'mvn test'
      }
    }
  }
  post {
    failure {
      mail to: 'team@example.com', subject: 'Build Failed'
    }
  }
}
```

**Scripted Pipeline** (more flexible, more complex):
```groovy
node {
  stage('Build') {
    sh 'mvn package'
  }
  stage('Test') {
    sh 'mvn test'
  }
}
```

| | Declarative | Scripted |
|---|---|---|
| **Syntax** | Structured, opinionated | Full Groovy — maximum flexibility |
| **Learning curve** | Easier for beginners | Requires Groovy knowledge |
| **Error handling** | `post` block | `try/catch/finally` |
| **Recommended for** | Most pipelines | Complex, dynamic pipeline logic |

---

### Q61. What triggers did you configure for your Jenkins pipeline?

**Answer:**

"In InternRecom, I configured a **GitHub webhook** as the primary trigger.

**Setup steps:**
1. In GitHub repository → Settings → Webhooks → Add webhook
2. Payload URL: `http://<jenkins-ec2-ip>:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Push events

In Jenkins: Install the 'GitHub Integration' plugin. In the pipeline configuration, enable 'GitHub hook trigger for GITScm polling'.

**Other trigger options Jenkins supports:**
```groovy
triggers {
  // Poll SCM every 5 minutes (backup if webhook fails)
  pollSCM('H/5 * * * *')

  // Schedule a nightly build at 2 AM
  cron('0 2 * * *')

  // Trigger from another upstream job
  upstream(upstreamProjects: 'build-job', threshold: hudson.model.Result.SUCCESS)
}
```

**Webhook vs. polling:** Webhooks are event-driven and instantaneous. Polling checks the SCM at intervals (wastes resources, has latency). Use webhooks in production."

---

### Q62. What are Jenkins agents/nodes, and why are they used?

**Answer:**

A **Jenkins agent (node)** is a machine (physical, VM, container) that Jenkins uses to execute pipeline stages. The **Jenkins controller (master)** manages pipeline coordination but delegates actual build execution to agents.

**Why agents are used:**
- **Scalability:** Run multiple builds in parallel on multiple agents.
- **Isolation:** Separate environments for different jobs (e.g., Java agent, Python agent).
- **Distribution:** Run builds closer to deployment targets.
- **Security:** Don't run untrusted code on the controller.

**Agent types:**
- **Permanent agents:** Dedicated machines configured in Jenkins UI.
- **Cloud agents (Docker/Kubernetes):** Dynamically spun up for each build and destroyed after. This is the modern approach.

```groovy
pipeline {
  agent {
    docker {
      image 'maven:3.9-eclipse-temurin-17'   # Run this stage in a Maven container
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'mvn package'
      }
    }
  }
}
```

---

### Q63. How do you handle secrets/credentials securely in Jenkins?

**Answer:**

"I stored all secrets in Jenkins' built-in **Credential Store** (Manage Jenkins → Credentials). Credentials are stored encrypted and never appear in build logs.

**Types of credentials stored:**
- Docker Hub username/password (for `docker push`)
- EC2 SSH private key (for `ssh` deployment)
- Git personal access token

**Using credentials in Jenkinsfile:**
```groovy
// Username/password binding
withCredentials([usernamePassword(
  credentialsId: 'dockerhub-creds',
  usernameVariable: 'DOCKER_USER',
  passwordVariable: 'DOCKER_PASS'
)]) {
  sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
}

// SSH key binding
sshagent(['ec2-ssh-key']) {
  sh 'ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} "docker ps"'
}
```

**Best practices:**
- Never hardcode credentials in the Jenkinsfile or source code.
- Use `--password-stdin` for Docker login to avoid credentials appearing in process listings.
- Rotate credentials regularly."

---

### Q64. What are Jenkins plugins? Name a few you've used.

**Answer:**

Jenkins plugins are extensions that add functionality to the Jenkins core. Jenkins has over 1,800 plugins available.

**Plugins I used in InternRecom:**

| Plugin | Purpose |
|---|---|
| **Git Plugin** | Enables Jenkins to clone Git repositories |
| **GitHub Integration Plugin** | Processes GitHub webhooks to trigger builds |
| **Maven Integration Plugin** | Adds Maven build step support |
| **Docker Pipeline Plugin** | Provides `docker.build()`, `docker.push()` in Jenkinsfile |
| **SSH Agent Plugin** | Injects SSH private keys for `sshagent { }` block |
| **Credentials Plugin** | Secure storage of credentials |
| **Pipeline Plugin** | Core plugin enabling Jenkinsfile-based pipelines |
| **Blue Ocean Plugin** | Modern visual pipeline UI |

---

### Q65. Your deployment succeeded, but the application isn't opening. How would you troubleshoot it?

**Answer:**

"This is a classic scenario where the infrastructure layer succeeded but the application layer failed. I follow a systematic approach:

**Step 1: Verify the container is running**
```bash
docker ps                      # Is the container listed?
docker ps -a                   # Check if it exited immediately
docker logs internrecom        # Read the application startup logs
```

**Step 2: Check if the application is listening on the correct port**
```bash
docker inspect internrecom | grep -A 5 "Ports"
netstat -tulnp | grep 8080
curl http://localhost:8080/actuator/health   # Test from within the EC2 instance
```

**Step 3: Check AWS Security Group rules**
- EC2 → Security Groups → Inbound rules
- Verify port 8080 is open for your IP or `0.0.0.0/0`

**Step 4: Test from outside**
```bash
curl http://<public-ip>:8080/actuator/health
```

**Step 5: Check application-level errors**
```bash
docker logs internrecom --tail 100   # Look for startup errors
```

**Step 6: Kubernetes-specific checks**
```bash
kubectl get pods             # Pod running?
kubectl describe pod <name>  # Any events/errors?
kubectl get service          # Is the Service correctly mapped?
kubectl get ingress          # Is the Ingress configured with the right host?
```"

---

### Q66. What is a build artifact, and where do you store yours?

**Answer:**

A **build artifact** is the output of a build process — the file(s) that are deployed or distributed. For a Java Spring Boot application, the artifact is the compiled `.jar` or `.war` file produced by `mvn package`.

**In InternRecom:**
- The build artifact was `internrecom-0.0.1-SNAPSHOT.jar` in the `target/` directory.
- It was baked into a Docker image and pushed to **Docker Hub** — tagged with the Jenkins build number.

**Artifact repositories used in practice:**
- **JFrog Artifactory** — stores JAR files, Docker images, npm packages.
- **Nexus Repository** — stores Maven artifacts.
- **AWS ECR (Elastic Container Registry)** — stores Docker images.
- **GitHub Packages** — GitHub-native artifact hosting.

**Best practice:** Store versioned artifacts by build number so you can roll back to any previous version without rebuilding.

---

### Q67. How do you roll back a failed deployment in your pipeline?

**Answer:**

"In our Jenkins pipeline on Docker, rollback involves pulling the previous Docker image version and restarting the container:

```bash
docker pull nihal/internrecom:${PREVIOUS_BUILD_NUMBER}
docker stop internrecom
docker rm internrecom
docker run -d --name internrecom -p 8080:8080 \
  nihal/internrecom:${PREVIOUS_BUILD_NUMBER}
```

**In Kubernetes, rollback is built-in:**
```bash
kubectl rollout undo deployment/internrecom-app
```

**Best practices for rollback:**
1. Always tag Docker images with a specific version (build number, git SHA) — never overwrite `latest` in production.
2. Keep at least the last 3 image versions available in the registry.
3. Add a post-deployment health check in the pipeline that automatically triggers a rollback if the health endpoint returns non-200."

---

## PART 6 — Terraform (Infrastructure as Code)

---

### Q68. What is Infrastructure as Code, and why is it important?

**Answer:**

**Infrastructure as Code (IaC)** is the practice of defining and provisioning infrastructure (servers, networks, databases, load balancers) through machine-readable configuration files rather than manual processes or interactive tools.

**Why it is important:**

| Benefit | Explanation |
|---|---|
| **Reproducibility** | Run the same Terraform script and get the exact same infrastructure every time |
| **Version control** | Infrastructure changes are tracked in Git — full audit trail of who changed what and why |
| **Automation** | Integrate with CI/CD pipelines to provision infra automatically |
| **Speed** | Provisioning 100 EC2 instances takes the same time as 1 |
| **Cost reduction** | Destroy environments when not in use and recreate them on demand |
| **Consistency** | Dev, staging, and prod environments are identical because they use the same code |

**Tools:** Terraform (cloud-agnostic), AWS CloudFormation (AWS-only), Pulumi, Bicep (Azure).

---

### Q69. What is the difference between Terraform and Ansible?

**Answer:**

| Dimension | Terraform | Ansible |
|---|---|---|
| **Primary purpose** | **Infrastructure provisioning** — create/destroy cloud resources (EC2, VPC, RDS) | **Configuration management** — install software, configure servers, manage files |
| **State** | Maintains a **state file** to track what infrastructure exists | Stateless — describes desired state, does not track what it has done |
| **Language** | HCL (HashiCorp Configuration Language) — declarative | YAML playbooks — procedural/declarative |
| **Agent** | Agentless — talks directly to cloud APIs | Agentless — uses SSH |
| **Idempotency** | Inherently idempotent — `terraform apply` makes changes only if needed | Mostly idempotent — depends on the module used |
| **Used for** | Day 0/1: Spinning up the infrastructure | Day 1/2: Configuring what's already running |

**In InternRecom, the workflow was:**
1. **Terraform** → provision the EC2 instance, security groups, VPC.
2. **Ansible** → configure the EC2 instance: install Java, Docker, set up services.

They complement each other — Terraform creates the pizza shop (the building), Ansible decorates and equips it (furniture, equipment).

---

### Q70. What is a Terraform state file, and why is it important?

**Answer:**

The **Terraform state file** (`terraform.tfstate`) is a JSON file that records the current state of your managed infrastructure. It maps your Terraform resource definitions to the real-world resources they represent.

**Why it is critical:**
- **Change detection:** On `terraform plan`, Terraform compares your config against the state file to determine what needs to be created, updated, or deleted.
- **Dependency tracking:** Tracks resource relationships (e.g., a subnet depends on a VPC).
- **Performance:** Avoids querying the cloud API for every resource on every plan.

> WARNING: Never delete or manually edit the state file. This will desync Terraform from reality.

---

### Q71. How do you handle remote state storage/locking in Terraform?

**Answer:**

By default, the state file is stored locally — which doesn't work for teams. **Remote state** solves this:

**AWS S3 + DynamoDB backend (standard pattern):**
```hcl
terraform {
  backend "s3" {
    bucket         = "internrecom-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true          # Encrypt state at rest
    dynamodb_table = "terraform-lock-table"  # State locking
  }
}
```

**How it works:**
- **S3:** Stores the state file with versioning enabled (recover previous states).
- **DynamoDB:** Provides distributed **state locking** — when one engineer runs `terraform apply`, a lock is acquired. If another engineer tries to run simultaneously, they get: *"Error acquiring the state lock"*. This prevents concurrent modifications that would corrupt the state.

---

### Q72. What is the difference between `terraform plan` and `terraform apply`?

**Answer:**

| Command | What it does |
|---|---|
| `terraform plan` | **Dry run** — shows what changes Terraform would make (create, update, destroy) without actually making them. Safe to run at any time. |
| `terraform apply` | **Executes** the changes shown by `plan`. Prompts for confirmation (`yes`) before making changes. |

```bash
terraform init      # Initialize providers and backend
terraform plan      # Preview changes
terraform apply     # Apply changes (prompts confirmation)
terraform apply -auto-approve  # Apply without confirmation (use in CI/CD only)
terraform destroy   # Destroy all managed resources
```

**Best practice in CI/CD:**
```bash
terraform plan -out=tfplan    # Save the plan to a file
terraform apply tfplan        # Apply exactly what was planned (no drift)
```

---

### Q73. What are Terraform providers and modules?

**Answer:**

**Providers:** Plugins that allow Terraform to interact with APIs of specific platforms (AWS, Azure, GCP, Kubernetes, GitHub, etc.).

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}
```

**Modules:** Reusable, self-contained packages of Terraform configuration that group related resources.

```hcl
module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 5.0"
  name          = "internrecom-server"
  instance_type = "t2.micro"
  ami           = data.aws_ami.ubuntu.id
  key_name      = var.key_name
}
```

**Why modules matter:**
- DRY (Don't Repeat Yourself) — define once, use in dev/staging/prod with different variable values.
- Community modules on the Terraform Registry reduce the time to write common patterns.

---

### Q74. What is a Terraform variable file (`.tfvars`) used for?

**Answer:**

A `.tfvars` file provides values for input variables defined in Terraform. It separates configuration from code — keeping environment-specific values out of the main `.tf` files.

**`variables.tf` — declare variables:**
```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
}
variable "db_password" {
  type      = string
  sensitive = true
}
```

**`dev.tfvars`:**
```hcl
instance_type = "t2.micro"
db_password   = "dev-pass-123"
```

**`prod.tfvars`:**
```hcl
instance_type = "t3.large"
db_password   = "prod-super-secure-pass-456"
```

**Usage:**
```bash
terraform apply -var-file="dev.tfvars"
terraform apply -var-file="prod.tfvars"
```

> WARNING: Never commit `.tfvars` files containing secrets to Git. Add `*.tfvars` to `.gitignore`.

---

### Q75. How would you manage different environments (dev/staging/prod) in Terraform?

**Answer:**

**Option 1: Separate directories per environment (simplest):**
```
terraform/
├── modules/
│   └── ec2/           # Reusable module
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
```

**Option 2: Terraform Workspaces:**
```bash
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
terraform apply -var-file="dev.tfvars"
```

Each workspace has its own state file, allowing the same code to manage multiple environments.

**Option 3: Terragrunt** (popular in enterprise) — a wrapper around Terraform that handles DRY configurations across environments.

---

### Q76. What happens if two people run `terraform apply` at the same time?

**Answer:**

"If remote state with DynamoDB locking is configured (which it should be), the second person's `terraform apply` will fail immediately with:

*'Error: Error acquiring the state lock. Lock Info: ID: lock-id, Who: user2@machine'*

The second person must wait for the first to finish (or, in case of a crash, release the lock manually: `terraform force-unlock <lock-id>`).

**Without locking** (local state or S3 without DynamoDB): Both applies would proceed concurrently, potentially reading a stale state, making conflicting API calls, and writing partial results that corrupt the state file — leading to infrastructure drift and potentially destroying resources.

**Lesson:** Always configure remote state with locking. Never use local state in a team."

---

## PART 7 — Ansible & Configuration Management

---

### Q77. What is the difference between Ansible and Puppet?

**Answer:**

| Dimension | Ansible | Puppet |
|---|---|---|
| **Architecture** | Agentless — communicates over SSH | Agent-based — Puppet agent installed on each managed node |
| **Language** | YAML playbooks (human-readable) | Puppet DSL or Ruby-based manifests |
| **Learning curve** | Low — minimal prerequisites | Steeper — requires learning Puppet's declarative DSL |
| **Execution model** | Push-based — controller pushes commands to nodes | Pull-based — agents periodically pull and apply manifests from the Puppet master |
| **Scalability** | Can be slow at scale (N SSH connections) | Scales well with the pull model |
| **Ideal for** | Ad-hoc tasks, simple automation, CI/CD integration | Large-scale, continuous enforcement of configuration |

**Why we chose Ansible for InternRecom:** We needed simple, one-time server configuration (install Java, Docker, configure services). Ansible's agentless model meant zero setup on the target EC2 server — just SSH access. No need to install and maintain a Puppet agent.

---

### Q78. Is Ansible agent-based or agentless? Why does that matter?

**Answer:**

Ansible is **agentless**. It communicates with target nodes using standard SSH (Linux) or WinRM (Windows). No software needs to be installed on the target machines.

**Why agentless matters:**

1. **Reduced maintenance overhead:** No agent software to install, version, update, or troubleshoot on hundreds of servers.
2. **Security:** Fewer services running on nodes means a smaller attack surface.
3. **Simplicity for onboarding:** To add a new server, just add its IP to the Ansible inventory and ensure SSH access — no agent installation required.
4. **Works on ephemeral infrastructure:** Cloud instances that are created and destroyed frequently don't need permanent agents.

**Trade-off:** Ansible's push-based SSH model can be slower at scale (1000+ nodes) compared to Puppet's pull-based agent model.

---

### Q79. What is an Ansible playbook, and what is its structure?

**Answer:**

A **playbook** is a YAML file that defines a set of ordered tasks to be executed on a group of hosts.

**Example playbook for InternRecom server setup:**
```yaml
---
- name: Configure InternRecom Application Server
  hosts: app_servers          # Target group from inventory
  become: yes                 # Run tasks with sudo (root)
  vars:
    java_version: openjdk-17-jdk
    app_port: 8080

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install Java
      apt:
        name: "{{ java_version }}"
        state: present

    - name: Install Docker
      apt:
        name: docker.io
        state: present

    - name: Start and enable Docker service
      service:
        name: docker
        state: started
        enabled: yes

    - name: Add ubuntu user to docker group
      user:
        name: ubuntu
        groups: docker
        append: yes

  handlers:
    - name: Restart Docker
      service:
        name: docker
        state: restarted
```

**Structure:**
- `hosts` — which servers to target
- `become` — privilege escalation (sudo)
- `vars` — variable definitions
- `tasks` — ordered list of actions using modules
- `handlers` — tasks triggered only when notified by other tasks

---

### Q80. What is an inventory file in Ansible?

**Answer:**

An **inventory file** defines the hosts (servers) that Ansible manages, organized into named groups.

**INI format (`inventory.ini`):**
```ini
[app_servers]
18.232.xx.xx   ansible_user=ubuntu   ansible_ssh_private_key_file=~/.ssh/internrecom.pem

[db_servers]
34.201.xx.xx   ansible_user=ubuntu   ansible_ssh_private_key_file=~/.ssh/internrecom.pem

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

**YAML format (`inventory.yaml`):**
```yaml
all:
  children:
    app_servers:
      hosts:
        app1:
          ansible_host: 18.232.xx.xx
          ansible_user: ubuntu
```

**Dynamic inventories:** For cloud environments, use dynamic inventory scripts (e.g., `aws_ec2` plugin) that automatically discover EC2 instances by tags — no manual IP maintenance needed.

```bash
ansible -i inventory.ini app_servers -m ping    # Test connectivity
ansible-playbook -i inventory.ini setup.yaml    # Run playbook
```

---

### Q81. What are Ansible roles, and why use them?

**Answer:**

An **Ansible role** is a structured, reusable way to organize related tasks, variables, templates, and handlers. Think of a role as a modular component — a `docker` role installs Docker, a `java` role installs Java.

**Directory structure of a role:**
```
roles/
└── docker/
    ├── tasks/
    │   └── main.yaml        # Main task list
    ├── handlers/
    │   └── main.yaml        # Handlers
    ├── vars/
    │   └── main.yaml        # Role-level variables
    ├── defaults/
    │   └── main.yaml        # Default variable values
    ├── templates/
    │   └── daemon.json.j2   # Jinja2 templates
    └── files/
        └── docker.conf      # Static files to copy
```

**Using roles in a playbook:**
```yaml
- hosts: app_servers
  roles:
    - java
    - docker
    - internrecom-app
```

**Why roles:**
- **Reusability** — use the same `docker` role across 10 different playbooks.
- **Community** — Ansible Galaxy hosts thousands of ready-made roles (e.g., `geerlingguy.docker`).

---

### Q82. How is idempotency achieved in Ansible?

**Answer:**

**Idempotency** means running the same Ansible playbook multiple times produces the same result — if the desired state is already achieved, Ansible makes no changes.

Ansible achieves this through its modules:

- `apt: name=docker.io state=present` — If Docker is already installed, this task reports `ok` (no change). If not installed, it installs it.
- `service: name=docker state=started enabled=yes` — If Docker is already running, no action is taken.
- `file: path=/var/app state=directory mode=0755` — If the directory exists with the right permissions, no change.

**Contrast with shell commands:**
```yaml
# NOT idempotent — runs every time
- shell: apt-get install docker.io

# Idempotent — checks state first
- apt:
    name: docker.io
    state: present
```

**Best practice:** Always use Ansible modules instead of `shell` or `command` tasks when a module exists.

---

### Q83. How did you use Ansible for server configuration in your projects?

**Answer:**

"In InternRecom, Ansible was used in **Phase 2** of the pipeline — after Terraform provisioned the EC2 instance, Ansible took over to configure it:

**The workflow:**
1. Terraform outputs the EC2 public IP.
2. The IP is added to the Ansible inventory.
3. The Ansible playbook runs:

```yaml
- name: Configure InternRecom App Server
  hosts: app_servers
  become: yes
  tasks:
    - name: Update package cache
      apt: update_cache=yes cache_valid_time=3600

    - name: Install OpenJDK 17
      apt: name=openjdk-17-jdk state=present

    - name: Install Docker
      apt: name=docker.io state=present

    - name: Ensure Docker is started and enabled
      service: name=docker state=started enabled=yes

    - name: Add ubuntu user to docker group
      user: name=ubuntu groups=docker append=yes
```

4. After the playbook completes, the server is ready to receive Docker containers deployed by the Jenkins pipeline.

**Result:** A fresh EC2 instance goes from a bare Ubuntu image to a fully configured, Docker-ready application server in under 5 minutes, fully automated and repeatable."

---

## PART 8 — AWS & Cloud

---

### Q84. How do you connect to an AWS EC2 instance?

**Answer:**

The standard method is **SSH using the key pair** created/assigned at EC2 launch time.

```bash
# Set correct permissions on the key file
chmod 400 ~/internrecom-key.pem

# Connect via SSH
ssh -i ~/internrecom-key.pem ubuntu@<public-ip>
# Or using Public DNS:
ssh -i ~/internrecom-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
```

**Prerequisite in AWS:**
- The EC2 security group must allow **inbound TCP on port 22** from your IP address.

**Username by OS:**
| AMI | Default username |
|---|---|
| Ubuntu | `ubuntu` |
| Amazon Linux 2 | `ec2-user` |
| RHEL | `ec2-user` or `root` |
| Debian | `admin` |

---

### Q85. What if port 22 is closed — how would you troubleshoot SSH access?

**Answer:**

"If port 22 is closed or SSH is not working, here is my troubleshooting flow:

**Step 1: Check Security Group inbound rules**
- AWS Console → EC2 → Instance → Security tab → Security Groups
- Verify that there is an inbound rule: `TCP | Port 22 | Source: My IP`
- If missing, add the rule.

**Step 2: Check the Network ACL (NACL)**
- VPC → Network ACLs → associated NACL for the subnet
- NACLs are stateless — ensure both inbound (port 22) AND outbound (ephemeral ports 1024-65535) are allowed.

**Step 3: Verify the instance has a public IP**
- Private instances in a private subnet cannot be reached from the internet directly — use a **bastion host** or **AWS Session Manager**.

**Step 4: Use AWS Systems Manager Session Manager (alternative to SSH)**
```bash
aws ssm start-session --target i-0abcd1234ef567890
```

**Step 5: EC2 Instance Connect**
- AWS Console → EC2 → Connect → EC2 Instance Connect — opens browser-based SSH without needing port 22 open externally."

---

### Q86. AWS provides an HTTP endpoint. How would you enable HTTPS?

**Answer:**

"To serve HTTPS, you need an SSL/TLS certificate and a load balancer to terminate TLS.

**Approach using AWS ALB + ACM:**

1. **Request a certificate from ACM:**
   - AWS Certificate Manager → Request Certificate → Public Certificate → Enter domain name → DNS validation.

2. **Create an Application Load Balancer (ALB):**
   - Listeners: Port 80 (HTTP → redirect to HTTPS) and Port 443 (HTTPS → forward to target group)
   - Attach the ACM certificate to the port 443 listener.

3. **Create a Target Group** pointing to your EC2 instance on port 8080.

4. **Update Route 53 (DNS):** Create an A record (alias) pointing your domain to the ALB DNS name.

**Traffic flow:**
```
User → internrecom.example.com → Route 53 → ALB (HTTPS/443) → EC2:8080 (HTTP internally)
```

The ALB handles TLS termination — your application only needs to handle plain HTTP internally."

---

### Q87. Does AWS provide SSL certificates? What is AWS Certificate Manager (ACM)?

**Answer:**

"Yes, AWS provides **free SSL/TLS certificates** through **AWS Certificate Manager (ACM)**.

**What ACM does:**
- Issues and manages free public SSL/TLS certificates for domains you own.
- Handles automatic certificate renewal before expiry.
- Certificates are natively integrated with AWS services: ALB, CloudFront, API Gateway.

**ACM Certificate Types:**
1. **Public certificates** — For internet-facing services. Free. Validated via DNS (recommended) or email.
2. **Private certificates** — For internal services (requires AWS Private CA, which has a cost).

**Limitations:**
- ACM certificates **cannot be downloaded** and installed directly on EC2 instances — they can only be attached to AWS managed services (ALB, CloudFront, etc.).
- For direct SSL on an EC2 instance with Nginx terminating SSL, use **Let's Encrypt (Certbot)**.

```bash
# Request a certificate via CLI
aws acm request-certificate \
  --domain-name internrecom.example.com \
  --validation-method DNS \
  --region us-east-1
```"

---

### Q88. What is the difference between a Security Group and a Network ACL?

**Answer:**

| Dimension | Security Group | Network ACL (NACL) |
|---|---|---|
| **Level** | Instance level (attached to ENI) | Subnet level |
| **State** | **Stateful** — if you allow inbound, the return outbound is automatically allowed | **Stateless** — must explicitly allow both inbound AND outbound |
| **Rule evaluation** | All rules are evaluated — most permissive wins | Rules are evaluated in order (by rule number) — first match wins |
| **Default behavior** | Default: deny all inbound, allow all outbound | Default: allow all |
| **Deny rules** | No explicit deny rules — whitelist only | Can explicitly DENY specific IPs (e.g., block a malicious IP) |
| **Association** | One SG can be applied to many instances | One NACL per subnet |

**Analogy:** Security Groups are like personal bodyguards (per instance). NACLs are like the building's security at the entrance (per subnet/floor).

---

### Q89. What is an EC2 instance vs an S3 bucket vs an IAM role?

**Answer:**

| Service | What it is | Use Case |
|---|---|---|
| **EC2 (Elastic Compute Cloud)** | A virtual server in the cloud — compute resources (CPU, RAM, disk) | Running applications, web servers, databases, Jenkins |
| **S3 (Simple Storage Service)** | Object storage — stores files (objects) in buckets, infinitely scalable | Static website hosting, backups, Terraform state files, log storage |
| **IAM Role** | An AWS identity with permissions — can be attached to AWS services (EC2, Lambda) | Granting an EC2 instance permission to access S3, or granting Jenkins access to push to ECR |

**Concrete example from InternRecom:**
- **EC2:** The server where Jenkins and the application container run.
- **S3:** Where Terraform stores its state file (`terraform.tfstate`).
- **IAM Role:** Attached to the EC2 instance, granting it permission to push Docker images to ECR and access S3 — without needing to hardcode AWS access keys.

---

### Q90. What is an Elastic Load Balancer, and why would you use one?

**Answer:**

An **AWS Elastic Load Balancer (ELB)** distributes incoming application traffic across multiple targets (EC2 instances, containers, Lambda functions) in multiple Availability Zones.

**Types of ELB:**
- **Application Load Balancer (ALB)** — Layer 7. Routes based on URL path, hostname, HTTP headers. Best for HTTP/HTTPS applications and microservices.
- **Network Load Balancer (NLB)** — Layer 4. Extremely high performance, handles millions of requests per second.
- **Gateway Load Balancer (GWLB)** — For third-party network appliances (firewalls, IDS).

**Why use an ELB:**
1. **High availability:** Distributes traffic across multiple AZs — if one AZ fails, traffic goes to the healthy ones.
2. **Scalability:** Works with Auto Scaling Groups to handle traffic spikes.
3. **SSL termination:** Attach ACM certificates to ALB — offload TLS from your application servers.
4. **Health checks:** ALB removes unhealthy instances from rotation automatically.
5. **Single entry point:** One DNS name for users, even as the backend scales from 1 to 100 instances.

---

### Q91. How do you securely store secrets/credentials in AWS deployments?

**Answer:**

**Option 1: AWS Secrets Manager (recommended):**
```bash
# Store a secret
aws secretsmanager create-secret \
  --name prod/internrecom/db_password \
  --secret-string "super-secure-pass"
```
- Supports automatic secret rotation.
- Integrated with IAM for fine-grained access control.
- Auditable via CloudTrail.

**Option 2: AWS Parameter Store (cost-effective for simpler needs):**
```bash
aws ssm put-parameter --name "/internrecom/db_password" \
  --value "super-secure-pass" --type SecureString
```

**Option 3: IAM Roles (for service-to-service auth):**
- Attach an IAM role to the EC2 instance — the instance gets temporary credentials automatically through the instance metadata service.
- Never hardcode `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in code or environment variables.

**What NOT to do:**
- Never commit secrets in `.env` files or Terraform `.tfvars` to Git.
- Never pass secrets as Docker environment variables in plain text in docker-compose.yml committed to Git.

---

## PART 9 — Monitoring (Prometheus, Grafana, Nagios)

---

### Q92. What did you monitor using Prometheus and Grafana in your Kubernetes project?

**Answer:**

"In the Kubernetes project, I monitored the following:

**Infrastructure Metrics (via kube-state-metrics and node-exporter):**
- CPU utilization per node and per pod
- Memory utilization per node and per pod
- Network I/O (bytes received/transmitted per pod)
- Disk I/O on nodes

**Kubernetes Object Metrics (via kube-state-metrics):**
- Number of running / pending / failed pods
- Deployment rollout status
- HPA current/desired replica counts
- Node readiness status

**Application Metrics (via Spring Boot Actuator + Micrometer):**
- HTTP request rate (requests per second)
- HTTP error rate (5xx responses)
- JVM heap memory usage
- Active database connections

**Grafana Dashboards:**
- I imported the Kubernetes Cluster Overview dashboard (ID: 6417) from Grafana.com.
- Created a custom dashboard for application-specific metrics.
- Configured alert rules in Grafana to send notifications when CPU > 80% or pod count < minimum for more than 2 minutes."

---

### Q93. How does Prometheus collect metrics (pull vs push model)?

**Answer:**

Prometheus uses a **pull model** — it actively scrapes (HTTP GET) metrics from configured endpoints at regular intervals (default: 15 seconds).

**How it works:**
1. Applications expose a `/metrics` endpoint in OpenMetrics/Prometheus text format.
2. Prometheus is configured with scrape targets in `prometheus.yaml`:
   ```yaml
   scrape_configs:
     - job_name: 'internrecom-app'
       static_configs:
         - targets: ['internrecom-service:8080']
       metrics_path: '/actuator/prometheus'
       scrape_interval: 15s
   ```
3. Every 15 seconds, Prometheus GETs `http://internrecom-service:8080/actuator/prometheus`.
4. Metrics are stored in Prometheus's time-series database.
5. Grafana queries Prometheus using **PromQL** to visualize the data.

**Push model exception — Pushgateway:** For short-lived jobs (batch jobs, cron jobs) that may finish before Prometheus scrapes them, they can push metrics to the Pushgateway.

**Advantages of pull model:**
- Central control over scrape frequency.
- Easy to discover if a target is down (scrape fails = alert).
- No need for the application to know the Prometheus server's address.

---

### Q94. What is a Grafana dashboard, and how did you build yours?

**Answer:**

A **Grafana dashboard** is a visual collection of panels (graphs, gauges, tables, heatmaps) that display time-series data from one or more data sources.

**How I built the dashboard:**

1. **Connected Prometheus as data source:**
   - Grafana UI → Configuration → Data Sources → Add → Prometheus → URL: `http://prometheus-server:9090`

2. **Imported community dashboards:**
   - Grafana.com → Dashboard ID `3119` (Kubernetes Cluster Monitoring) → Import

3. **Created custom panels using PromQL:**
   ```promql
   # Pod CPU Usage
   sum(rate(container_cpu_usage_seconds_total{pod=~"internrecom.*"}[5m])) by (pod)

   # HTTP Request Rate
   rate(http_server_requests_seconds_count{job="internrecom-app"}[1m])

   # JVM Heap Memory
   jvm_memory_used_bytes{area="heap", job="internrecom-app"}
   ```

4. **Set up alerts:**
   - Alert rule: If `avg(cpu_utilization) > 0.8` for 5 minutes → send notification.

---

### Q95. What is the difference between Prometheus and Nagios?

**Answer:**

| Dimension | Prometheus | Nagios |
|---|---|---|
| **Primary purpose** | **Metrics monitoring** — collects, stores, and queries time-series metrics | **Service/host monitoring** — checks if hosts and services are up or returning expected responses |
| **Data model** | Time-series metrics with labels | Binary up/down checks with thresholds |
| **Collection** | Pull-based (scrapes `/metrics` endpoints) | Push/pull via plugins (active and passive checks) |
| **Query language** | PromQL — powerful, flexible | Basic threshold configuration |
| **Visualization** | Grafana (external) | Basic Nagios UI |
| **Best for** | Cloud-native, Kubernetes, microservices monitoring | Legacy infrastructure, network devices, server health checks |

**In your projects:**
- **Nagios** in InternRecom — monitored EC2 host health (CPU, memory, disk) and HTTP service availability. Simple, effective for a single-server setup.
- **Prometheus + Grafana** in Kubernetes project — monitored a dynamic cluster with autoscaling pods. Nagios would not handle Kubernetes' dynamic pod IPs well.

---

### Q96. What kind of alerts would you configure for a production Kubernetes cluster?

**Answer:**

**Infrastructure Alerts:**
```yaml
# Node CPU > 85% for 5 minutes
- alert: HighNodeCPU
  expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
  for: 5m
  labels:
    severity: warning

# Node disk > 90% full
- alert: DiskSpaceCritical
  expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10
  for: 1m
  labels:
    severity: critical
```

**Kubernetes Object Alerts:**
- Pod crash loop: `kube_pod_container_status_restarts_total > 5`
- Deployment unavailable replicas: `kube_deployment_status_replicas_unavailable > 0`
- HPA at max replicas: `kube_horizontalpodautoscaler_status_current_replicas == kube_horizontalpodautoscaler_spec_max_replicas`

**Application Alerts:**
- HTTP 5xx error rate > 1% for 5 minutes
- P99 response time > 2 seconds
- JVM heap > 90% for 3 minutes

**Alert routing:** Route `critical` alerts to PagerDuty (wake someone up). Route `warning` alerts to Slack (monitor during business hours).

---

### Q97. How would you monitor pod lifecycle events and container performance?

**Answer:**

**Pod lifecycle events — Kubernetes Events:**
```bash
kubectl get events --sort-by='.lastTimestamp' -n default
kubectl describe pod <pod-name>   # Shows Events at the bottom
```

Events show: `Scheduled`, `Pulling`, `Pulled`, `Started`, `Killing`, `BackOff`.

**Container performance — Prometheus metrics:**

| Metric | PromQL |
|---|---|
| CPU usage per container | `rate(container_cpu_usage_seconds_total[5m])` |
| Memory usage | `container_memory_usage_bytes` |
| Network I/O | `rate(container_network_receive_bytes_total[5m])` |
| Restart count | `kube_pod_container_status_restarts_total` |

**Real-time monitoring:**
```bash
kubectl top pods                          # Current CPU/memory
kubectl top nodes                         # Node resource usage
watch kubectl get pods                    # Watch pod status in real time
```

---

## PART 10 — Linux, Networking & Java Basics

---

### Q98. What is the difference between Apache Tomcat and Nginx? Why did you use Tomcat?

**Answer:**

| | Apache Tomcat | Nginx |
|---|---|---|
| **Type** | Java Application Server — runs Java Servlet/JSP applications | Web server and reverse proxy — serves static files and proxies to backends |
| **Language** | Java-native | C-based |
| **Primary use** | Hosting Java web apps (WAR files, JSP, Servlets) | Serving static content, load balancing, SSL termination, reverse proxy |
| **Dynamic content** | Native Java support | No Java support — must proxy to a Java server |
| **Common pattern** | Nginx (reverse proxy) → Tomcat (app server) | Nginx handles SSL and static assets; Tomcat handles Java app logic |

**Why I used Tomcat:**
"In the InternRecom project, the Spring Boot application was initially packaged as a WAR file, which requires a Servlet container — Tomcat is the standard and most compatible choice for Spring Boot WAR deployment.

However, Spring Boot can also run as a standalone JAR with an **embedded Tomcat** server — no separate Tomcat installation needed. In this mode, you simply run `java -jar app.jar` and Tomcat starts internally. This is how we deployed in the Docker container — the Dockerfile has a single `ENTRYPOINT ["java", "-jar", "app.jar"]` and Tomcat is embedded inside the JAR."

---

### Q99. What type of Java application did you deploy — WAR or JAR — and what's the difference?

**Answer:**

"In InternRecom, we deployed as an **executable JAR** (Fat JAR / Uber JAR) with embedded Tomcat.

| | WAR (Web Application Archive) | JAR (Java Archive / Fat JAR) |
|---|---|---|
| **Contains** | Compiled Java classes + web resources (JSP, HTML, WEB-INF) | Compiled Java classes + all dependencies + embedded server |
| **Requires** | External application server (Tomcat, JBoss, WildFly) | Only the JRE (`java -jar app.jar`) |
| **Deployment** | Copy WAR to Tomcat's `webapps/` directory | `java -jar app.jar` — self-contained |
| **Container-friendly** | Less ideal — needs Tomcat running | Perfect for Docker — single process |
| **Spring Boot default** | Optional (needs config change) | Default |

**Spring Boot Fat JAR:** Packages all dependencies (Spring Framework, embedded Tomcat, libraries) inside a single JAR file. This is ideal for Docker because the image contains everything needed to run the application.

**Dockerfile for JAR:**
```dockerfile
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Dockerfile for WAR (if needed):**
```dockerfile
FROM tomcat:9-jdk17
COPY target/internrecom.war /usr/local/tomcat/webapps/ROOT.war
```"

---

### Q100. What dependencies are typically defined in a `pom.xml`, and what does Maven do with them?

**Answer:**

**`pom.xml` (Project Object Model)** is Maven's build configuration file. It defines project metadata, dependencies, and build plugins.

**Dependencies used in InternRecom:**
```xml
<dependencies>
  <!-- Spring Boot Web - REST APIs and embedded Tomcat -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>

  <!-- Spring Data JPA - database ORM -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
  </dependency>

  <!-- MySQL JDBC Driver -->
  <dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
  </dependency>

  <!-- Spring Security -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
  </dependency>

  <!-- Actuator - health, metrics endpoints for Prometheus -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
  </dependency>

  <!-- Micrometer Prometheus - exposes /actuator/prometheus endpoint -->
  <dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
  </dependency>

  <!-- Test dependencies -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
  </dependency>
</dependencies>
```

**What Maven does with these dependencies:**
1. **Downloads** the specified JAR files from Maven Central Repository.
2. **Caches** them in `~/.m2/repository` on the local machine.
3. **Adds them to the classpath** during compilation and runtime.
4. **Packages them** into the Fat JAR during `mvn package` (using the Spring Boot Maven Plugin).
5. **Resolves transitive dependencies** — e.g., `spring-boot-starter-web` pulls in Spring MVC, Jackson, embedded Tomcat, and 30+ other libraries automatically.

---

## Bonus Questions

---

### Bonus Q: Have you worked on Spring Boot?

**Answer:**

"Yes, InternRecom is built with Spring Boot. Spring Boot is an opinionated framework built on top of the Spring Framework that simplifies application setup through:

1. **Auto-configuration:** Automatically configures beans based on the classpath.
2. **Embedded server:** Ships with embedded Tomcat — `java -jar app.jar` starts the server directly.
3. **Starter POMs:** Curated dependency bundles that ensure compatible versions of all related libraries.
4. **Spring Actuator:** Provides production-ready endpoints out of the box — `/actuator/health`, `/actuator/metrics`, `/actuator/prometheus` — which we used with Prometheus and Grafana.

**Example REST Controller in InternRecom:**
```java
@RestController
@RequestMapping("/api/internships")
public class InternshipController {

  @Autowired
  private InternshipService service;

  @GetMapping
  public List<Internship> getAllInternships() {
    return service.findAll();
  }

  @PostMapping
  public ResponseEntity<Internship> createInternship(@RequestBody Internship internship) {
    return ResponseEntity.created(URI.create("/api/internships/" + internship.getId()))
                         .body(service.save(internship));
  }
}
```"

---

### Bonus Q: Have you worked with Microservices?

**Answer:**

"In my Kubernetes project, the application followed a microservices-inspired architecture where individual services were independently containerized and deployed.

**What I understand by microservices:**
- An architectural style where an application is decomposed into small, independently deployable services.
- Each service owns its domain (e.g., User Service, Order Service, Notification Service).
- Services communicate via REST APIs or message queues (RabbitMQ, Kafka).
- Each service can be scaled, deployed, and failed independently.

**Key challenges I am aware of:**
- **Service discovery** — how does Order Service find User Service? Solution: Kubernetes DNS (services resolve by name).
- **Distributed tracing** — when a request spans 5 services, how do you trace a failure? Solution: Jaeger, Zipkin.
- **Configuration management** — environment-specific config for each service. Solution: ConfigMaps, Secrets, Spring Cloud Config.
- **API Gateway** — single entry point for clients. Solution: Kong, AWS API Gateway, Spring Cloud Gateway."

---

### Bonus Q: What is the difference between Maven and Gradle?

**Answer:**

| | Maven | Gradle |
|---|---|---|
| **Configuration** | XML (`pom.xml`) | Groovy or Kotlin DSL (`build.gradle`) |
| **Performance** | Slower (no incremental builds by default) | Faster — incremental builds, build caching, parallel execution |
| **Convention** | Strict convention-over-configuration | More flexible and customizable |
| **Learning curve** | Easier for beginners (structured XML) | Steeper (requires understanding Groovy/Kotlin) |
| **Ecosystem** | Mature, vast plugin ecosystem | Growing rapidly (default for Android development) |
| **Spring Boot** | Supported (official support) | Supported (official support) |

**Why we used Maven in InternRecom:**
"Maven was chosen because of its simplicity and the breadth of documentation available for Spring Boot + Maven integration. The `spring-boot-maven-plugin` provided out-of-the-box support for building Fat JARs with `mvn package`."

---

### Bonus Q: Do you have any questions for the interviewer?

**Answer:**

Always prepare 3–5 thoughtful questions. This demonstrates curiosity and genuine interest in the role:

**Recommended questions:**

1. *"What does the onboarding process look like for a DevOps engineer joining the team? Are there structured mentorship opportunities?"*

2. *"What CI/CD toolchain does the team currently use, and are there any areas you are looking to modernize or improve?"*

3. *"How does the team handle on-call rotations and incident response? What monitoring and alerting tools are in use?"*

4. *"What cloud provider(s) does the organization use, and what is the current state of containerization and Kubernetes adoption?"*

5. *"What does a typical first three months look like for someone in this role? What projects might I contribute to early on?"*

6. *"How does the DevOps team collaborate with the development teams — do developers have production access, or is there a clear ops boundary?"*

> Tip: Avoid asking about salary, benefits, or leave policies in the first interview. Save those for HR rounds or after an offer has been extended.

---

## 60-Second Project Pitches

---

### Kubernetes Project (Jan – Apr 2026)

"My Kubernetes project involved deploying a containerized application on a K8s cluster with full production-grade features. I started by Dockerizing the application, then wrote Kubernetes Deployment manifests with 2 replicas managed by a ReplicaSet. I configured an Nginx Ingress Controller for external traffic routing and set up Horizontal Pod Autoscaling (HPA) with CPU-based triggers — the cluster auto-scaled from 2 to 10 pods under load. For observability, I deployed Prometheus via Helm to scrape cluster and application metrics, and built Grafana dashboards to visualize pod health, resource utilization, and request rates. I also configured alert rules to notify when CPU or memory crossed production thresholds."

---

### InternRecom Project (Oct 2025 – Jan 2026)

"InternRecom is a full-stack web application that connects interns with companies. The key achievement was automating the entire delivery pipeline. A developer's git push to main triggers a Jenkins webhook, which runs a declarative pipeline: Maven builds the Spring Boot JAR, runs tests, builds and pushes a Docker image to Docker Hub, and deploys it to AWS EC2. The EC2 infrastructure is provisioned with Terraform and configured with Ansible. Nagios monitors the deployed service with HTTP health checks and resource alerts. The entire process from git push to production takes under 10 minutes — fully automated."

---

## Quick Reference: "Why this over that?"

| Choice | Why chosen | Alternative considered |
|---|---|---|
| **Jenkins** over GitHub Actions | Jenkins gives more control, runs on-premise, has a richer plugin ecosystem, and was better for learning CI/CD fundamentals | GitHub Actions is simpler for GitHub-native workflows |
| **Terraform** over CloudFormation | Cloud-agnostic (works with AWS, GCP, Azure), HCL is cleaner than YAML/JSON CloudFormation, massive community | CloudFormation is AWS-native, no extra tooling needed |
| **Ansible** over Puppet | Agentless, YAML is easy to learn, great for one-time provisioning tasks | Puppet scales better for large fleets with continuous enforcement |
| **Docker** over traditional deployment | Portable, consistent environment, fast startup, easy versioning and rollback | Traditional deployment is simpler but environment-specific |
| **Kubernetes** over plain Docker | Auto-healing, autoscaling, service discovery, rolling updates — production-grade orchestration | Docker Compose is simpler but not production-grade |
| **Prometheus** over Nagios | Kubernetes-native, dynamic service discovery, powerful PromQL, better for microservices | Nagios is simpler for traditional host monitoring |
| **Git** over SVN | Distributed, faster branching, industry standard, integrates with all modern tooling | SVN is centralized and common in legacy enterprises |

---

*Document prepared for Nihal Kumar Singh — DevOps Fresher Interview Preparation*
*Last updated: July 2026*
