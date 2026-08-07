# Appendix B: Docker Commands Cheatsheet

Welcome to the complete Docker command reference, Appendix B of the DevOps Mastery Notes series. This comprehensive guide covers the essential and advanced Docker commands required for production workloads.

## SECTION 1: Image Commands

### `docker build`
- **Purpose**: Build a Docker image from a Dockerfile.
- **Syntax**: `docker build [OPTIONS] PATH | URL | -`
- **Important Flags**:
  - `-t, --tag`: Name and optionally a tag in the 'name:tag' format
  - `-f, --file`: Name of the Dockerfile (Default is 'PATH/Dockerfile')
  - `--no-cache`: Do not use cache when building the image
  - `--build-arg`: Set build-time variables
  - `--target`: Set the target build stage to build
  - `--platform`: Set platform if server is multi-platform capable
  - `--pull`: Always attempt to pull a newer version of the image
  - `--progress`: Set type of progress output (auto, plain, tty)
- **Example**: `docker build -t myapp:1.0 --build-arg VERSION=1.0 --no-cache -f ./docker/Dockerfile.prod .`
- **Production Pattern**: Always use specific tags and build args for reproducible builds.
- **Common Mistakes**: Forgetting the `.` at the end of the command to specify the build context.
- **Troubleshooting**: If builds are slow, check the `.dockerignore` file to ensure you aren't sending too much context.
- **Interview Angle**: Understand how caching works in `docker build` and how order of commands in Dockerfile affects caching.

### `docker image ls` / `docker images`
- **Purpose**: List available images on the local host.
- **Syntax**: `docker image ls [OPTIONS] [REPOSITORY[:TAG]]`
- **Important Flags**:
  - `-a, --all`: Show all images (default hides intermediate images)
  - `--digests`: Show digests
  - `--format`: Format the output using a Go template
- **Example**: `docker image ls --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"`
- **Production Pattern**: Use formatting in CI/CD scripts to extract specific info.
- **Common Mistakes**: Not realizing `<none>:<none>` images (dangling) consume disk space.
- **Troubleshooting**: If disk is full, dangling images are a common culprit.

### `docker image inspect`
- **Purpose**: Display detailed information on one or more images in JSON format.
- **Syntax**: `docker image inspect [OPTIONS] IMAGE [IMAGE...]`
- **Example**: `docker image inspect myapp:1.0`
- **Production Pattern**: Use `jq` or `--format` to parse the JSON for specific properties, like exposed ports or entrypoints, in automation scripts.
- **JSON Breakdown**:
  - `Id`: The SHA256 digest of the image.
  - `RepoTags`: Tags associated with this image.
  - `Config.Env`: Environment variables baked into the image.
  - `Config.Cmd`: Default command to run if none is specified.
- **Interview Angle**: Knowing how to extract specific information without relying on `grep`.

### `docker image history`
- **Purpose**: Show the history of an image, useful for auditing layers.
- **Syntax**: `docker image history [OPTIONS] IMAGE`
- **Example**: `docker image history ubuntu:latest`
- **Production Pattern**: Analyzing image bloat by identifying which layer adds the most size.
- **Common Mistakes**: Assuming `CREATED BY` shows the exact Dockerfile line (it's often truncated). Use `--no-trunc` to see the full command.

### `docker image rm` / `docker rmi`
- **Purpose**: Remove one or more images.
- **Syntax**: `docker rmi [OPTIONS] IMAGE [IMAGE...]`
- **Important Flags**:
  - `-f, --force`: Force removal of the image, even if it has running containers.
- **Example**: `docker rmi -f myapp:old`
- **Production Pattern**: Use carefully in cleanup scripts; prefer `docker image prune`.
- **Troubleshooting**: "image is being used by running container" -> use `-f` or stop container first.

### `docker image prune`
- **Purpose**: Remove unused images.
- **Syntax**: `docker image prune [OPTIONS]`
- **Important Flags**:
  - `-a, --all`: Remove all unused images, not just dangling ones.
  - `--filter`: Provide filter values (e.g., 'until=24h').
- **Example**: `docker image prune -a --filter "until=168h"` (Removes images older than 1 week)
- **Production Pattern**: Set up as a cron job on worker nodes to prevent disk exhaustion.

### `docker tag`
- **Purpose**: Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE.
- **Syntax**: `docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]`
- **Example**: `docker tag myapp:latest registry.example.com/myapp:1.0.0`
- **Production Pattern**: Essential for preparing images for registry push (Image Promotion).

### `docker push`
- **Purpose**: Push an image or a repository to a registry.
- **Syntax**: `docker push [OPTIONS] NAME[:TAG]`
- **Important Flags**:
  - `--all-tags`: Push all tags of an image repository.
- **Example**: `docker push registry.example.com/myapp --all-tags`
- **Troubleshooting**: "denied: requested access to the resource is denied" -> Requires `docker login`.

### `docker pull`
- **Purpose**: Pull an image or a repository from a registry.
- **Syntax**: `docker pull [OPTIONS] NAME[:TAG|@DIGEST]`
- **Important Flags**:
  - `--platform`: Set platform if server is multi-platform capable (e.g., `linux/amd64`).
- **Example**: `docker pull --platform linux/arm64 nginx:latest`
- **Production Pattern**: Pulling specific SHAs (`@DIGEST`) rather than tags for immutability.

### `docker save`
- **Purpose**: Save one or more images to a tar archive (streamed to STDOUT by default).
- **Syntax**: `docker save [OPTIONS] IMAGE [IMAGE...]`
- **Example**: `docker save -o myapp.tar myapp:1.0`
- **Production Pattern**: Air-gapped environments where registries are inaccessible.

### `docker load`
- **Purpose**: Load an image from a tar archive or STDIN.
- **Syntax**: `docker load [OPTIONS]`
- **Example**: `docker load -i myapp.tar`
- **Common Mistakes**: Confusing `load` with `import`.

### `docker image import` vs `docker load`
- **docker load**: Restores an image along with its history and metadata (created by `docker save`).
- **docker image import**: Creates a single-layer image from a flattened filesystem archive (created by `docker export`). You lose history and metadata.
- **Interview Angle**: Be prepared to explain this exact difference.

## SECTION 2: Container Lifecycle Commands

### `docker run`
- **Purpose**: Run a command in a new container. The most complex and frequently used Docker command.
- **Syntax**: `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`
- **Important Flags**:
  - `-d, --detach`: Run container in background and print container ID.
  - `-it`: Keep STDIN open even if not attached (`-i`), and allocate a pseudo-TTY (`-t`). Used for interactive shells.
  - `--name`: Assign a name to the container.
  - `--rm`: Automatically remove the container when it exits.
  - `-p, --publish`: Publish a container's port(s) to the host (format: `hostPort:containerPort`).
  - `-P, --publish-all`: Publish all exposed ports to random ports on the host.
  - `-v, --volume`: Bind mount a volume.
  - `--mount`: Attach a filesystem mount to the container (preferred over `-v` for clarity).
  - `-e, --env`: Set environment variables.
  - `--env-file`: Read in a file of environment variables.
  - `--network`: Connect a container to a network.
  - `--ip`: IPv4 address (e.g., 172.30.100.104).
  - `--memory, -m`: Memory limit (e.g., `512m`).
  - `--cpus`: Number of CPUs.
  - `--cpu-shares`: CPU shares (relative weight).
  - `--restart`: Restart policy to apply when a container exits (no/always/on-failure/unless-stopped).
  - `--user, -u`: Username or UID (format: `<name|uid>[:<group|gid>]`).
  - `--workdir, -w`: Working directory inside the container.
  - `--cap-add, --cap-drop`: Add or drop Linux capabilities.
  - `--security-opt`: Security Options (e.g., AppArmor, SELinux profiles).
  - `--read-only`: Mount the container's root filesystem as read only.
  - `--tmpfs`: Mount a tmpfs directory.
  - `--label`: Set meta data on a container.
  - `--hostname, -h`: Container host name.
  - `--entrypoint`: Overwrite the default ENTRYPOINT of the image.
  - `--health-cmd`: Command to run to check health.
  - `--health-interval`: Time between running the check.
  - `--gpus`: GPU devices to add to the container ('all' to pass all GPUs).
  - `--init`: Run an init inside the container that forwards signals and reaps processes.
  - `--pid, --ipc, --network`: Namespace sharing options (e.g., `--pid=host`).
- **Example**:
  ```bash
  docker run -d --name web_server \
    --restart unless-stopped \
    -p 8080:80 \
    --memory 512m --cpus 1.0 \
    --read-only --tmpfs /tmp \
    --user 1000:1000 \
    --security-opt no-new-privileges:true \
    --cap-drop ALL \
    --network my_network \
    nginx:alpine
  ```
- **Production Pattern**: Running least privileged (non-root, read-only rootfs, dropped capabilities) with strict resource limits.
- **Troubleshooting**: If a container starts and immediately exits, the main process is terminating. Use `docker logs` or run with `-it` instead of `-d` to see why.
- **Interview Angle**: Explain the difference between `-v` and `--mount`.

### `docker start / stop / restart / pause / unpause / kill`
- **Purpose**: Manage the state of existing containers.
- **Example**: `docker restart web_server`
- **Production Pattern**: Use `stop` for graceful shutdown (sends SIGTERM, then SIGKILL after grace period). Use `kill` for immediate termination (sends SIGKILL).

### `docker rm`
- **Purpose**: Remove one or more containers.
- **Syntax**: `docker rm [OPTIONS] CONTAINER [CONTAINER...]`
- **Important Flags**:
  - `-f, --force`: Force the removal of a running container (uses SIGKILL).
  - `-v, --volumes`: Remove the anonymous volumes associated with the container.
- **Example**: `docker rm -fv web_server`

### `docker rename`
- **Purpose**: Rename a container.
- **Example**: `docker rename old_name new_name`

### `docker update`
- **Purpose**: Update configuration of one or more containers (usually resource limits).
- **Example**: `docker update --cpus 2 web_server`
- **Production Pattern**: Adjusting resources on the fly without restarting the container (if the engine/kernel supports it).

### `docker wait`
- **Purpose**: Block until one or more containers stop, then print their exit codes.
- **Example**: `docker wait my_job_container`
- **Production Pattern**: Useful in scripts that spin up a container to perform a task and need to know if it succeeded before continuing.

## SECTION 3: Container Information Commands

### `docker ps`
- **Purpose**: List containers.
- **Important Flags**:
  - `-a, --all`: Show all containers (default shows just running).
  - `-q, --quiet`: Only display container IDs.
  - `--format`: Pretty-print containers using a Go template.
  - `--filter`: Filter output based on conditions provided.
- **Example**: `docker ps --filter "status=exited" -q` (Useful for piping to `docker rm`)

### `docker inspect`
- **Purpose**: Return low-level information on Docker objects.
- **Important Formats**:
  - Get IP: `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container`
  - Get env: `docker inspect -f '{{.Config.Env}}' container`
  - Get mounts: `docker inspect -f '{{json .Mounts}}' container | jq`
- **Production Pattern**: Essential for debugging network connectivity or mount issues.

### `docker stats`
- **Purpose**: Display a live stream of container(s) resource usage statistics.
- **Important Flags**:
  - `--no-stream`: Disable streaming stats and only pull the first result.
  - `--format`: Pretty-print images using a Go template.
- **Example**: `docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"`

### `docker top`
- **Purpose**: Display the running processes of a container.
- **Example**: `docker top web_server`
- **Troubleshooting**: Verifying that the expected processes (and only the expected processes) are running.

### `docker diff`
- **Purpose**: Inspect changes to files or directories on a container's filesystem.
- **Output Codes**: `A` (Added), `C` (Changed), `D` (Deleted).
- **Example**: `docker diff web_server`
- **Security Angle**: Finding unexpected file modifications indicative of a compromise.

### `docker events`
- **Purpose**: Get real time events from the server.
- **Important Flags**: `--filter, --since, --until`
- **Example**: `docker events --filter 'type=container' --filter 'event=die'`

### `docker port`
- **Purpose**: List port mappings or a specific mapping for the container.
- **Example**: `docker port web_server`

## SECTION 4: Interaction Commands

### `docker exec`
- **Purpose**: Run a command in a running container.
- **Important Flags**:
  - `-i, --interactive`: Keep STDIN open even if not attached.
  - `-t, --tty`: Allocate a pseudo-TTY.
  - `-u, --user`: Username or UID (format: `<name|uid>[:<group|gid>]`).
  - `-w, --workdir`: Working directory inside the container.
  - `-e, --env`: Set environment variables.
  - `-d, --detach`: Detached mode: run command in the background.
- **Examples**:
  - `docker exec -it web_server bash` (or `sh` for Alpine)
  - `docker exec -u root web_server sh` (Debugging permission issues)
  - `docker exec web_server env` (Check live environment variables)
- **Production Pattern**: Used for live debugging, but shouldn't be used to change state in production (state changes should happen via image rebuilds).

### `docker attach`
- **Purpose**: Attach local standard input, output, and error streams to a running container.
- **Dangers**: Pressing `CTRL+C` will pass SIGINT to the container and kill it! Use `CTRL+P, CTRL+Q` to detach without stopping.
- **Pattern**: `docker exec` is generally preferred over `docker attach`.

### `docker cp`
- **Purpose**: Copy files/folders between a container and the local filesystem.
- **Examples**:
  - `docker cp file.txt web_server:/app/`
  - `docker cp web_server:/app/logs.txt ./`
- **Production Pattern**: Extracting core dumps, debug logs, or injecting diagnostic tools temporarily.

### `docker logs`
- **Purpose**: Fetch the logs of a container.
- **Important Flags**:
  - `-f, --follow`: Follow log output.
  - `--tail`: Number of lines to show from the end of the logs.
  - `--since, --until`: Show logs since/until timestamp.
  - `-t, --timestamps`: Show timestamps.
- **Example**: `docker logs -f --tail 100 -t web_server`

## SECTION 5: Volume Commands

### `docker volume create`
- **Purpose**: Create a volume.
- **Example**: `docker volume create pgdata`

### `docker volume ls`
- **Purpose**: List volumes.

### `docker volume inspect`
- **Purpose**: Display detailed information on one or more volumes.
- **Example**: `docker volume inspect pgdata` (useful to find the mountpoint on the host filesystem).

### `docker volume rm` / `docker volume prune`
- **Purpose**: Remove one or more volumes / Remove all unused local volumes.
- **Caution**: Data loss!

### Volume Types Syntax in `docker run`
- **Named Volume**: `--mount type=volume,src=my-volume,target=/app`
- **Bind Mount**: `--mount type=bind,src=/path/on/host,target=/app`
- **tmpfs**: `--mount type=tmpfs,target=/app`
- **Interview Angle**: Know when to use each. Bind mounts depend on host filesystem structure; Named volumes are managed by Docker; tmpfs is in-memory only.

### Volume Backup Pattern
- **Command**: `docker run --rm --volumes-from db_container -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata`
- **Pattern**: Spins up an ephemeral container, attaches to the target container's volumes, mounts a local directory, and creates a tarball of the volume data.

## SECTION 6: Network Commands

### `docker network create`
- **Purpose**: Create a network.
- **Important Flags**:
  - `--driver`: Driver to manage the Network (bridge, overlay, macvlan, ipvlan).
  - `--subnet`: Subnet in CIDR format.
  - `--gateway`: IPv4 or IPv6 Gateway for the master subnet.
  - `--ip-range`: Allocate container ip from a sub-range.
- **Example**: `docker network create --driver bridge --subnet 172.20.0.0/16 custom_net`

### `docker network ls / inspect / connect / disconnect / rm / prune`
- Manage network lifecycles and container connectivity.
- `docker network connect custom_net web_server`

### User-defined Network DNS
- **Concept**: Containers on the default `bridge` network can only communicate via IP. Containers on a user-defined network can resolve each other by container name or `--network-alias`.
- **Interview Angle**: A classic question is "Why can't my containers talk by name?" -> Because they are on the default bridge network.

## SECTION 7: Docker Compose Commands

### `docker compose up`
- **Purpose**: Create and start containers.
- **Important Flags**:
  - `-d, --detach`: Detached mode.
  - `--build`: Build images before starting containers.
  - `--scale`: Scale SERVICE to NUM instances.
  - `--force-recreate`: Recreate containers even if their configuration and image haven't changed.
  - `--no-deps`: Don't start linked services.
- **Example**: `docker compose up -d --build`

### `docker compose down`
- **Purpose**: Stop and remove containers, networks, images, and volumes.
- **Important Flags**:
  - `-v, --volumes`: Remove named volumes declared in the `volumes` section and anonymous volumes.
  - `--rmi type`: Remove images (type: 'all' or 'local').

### `docker compose ps / logs / exec / run`
- Equivalents of standard docker commands, but context-aware of the compose project.
- **run vs exec**: `run` starts a *new* container based on the service definition to run a one-off command. `exec` runs a command in an *already running* container.

### `docker compose build / pull / push`
- Manage images defined in the compose file.

### `docker compose config`
- **Purpose**: Validate and view the Compose file. Extremely useful to see the final parsed configuration after all overrides and `.env` files are applied.

### Compose Flags
- `-f, --file`: Specify one or more compose files (merges them in order).
- `-p, --project-name`: Specify an alternate project name (defaults to directory name).

## SECTION 8: System Commands

### `docker system df`
- **Purpose**: Show docker disk usage (images, containers, volumes, build cache).
- **Example**: `docker system df -v` (Detailed breakdown).

### `docker system prune`
- **Purpose**: Remove unused data.
- **Flags**:
  - `-a, --all`: Remove all unused images, not just dangling ones.
  - `--volumes`: Prune volumes as well.
- **Caution**: The nuclear option for clearing disk space.

### `docker system info` / `docker info`
- **Purpose**: Display system-wide information (Storage Driver, Logging Driver, Cgroup Driver, Plugins, Node info).

### `docker system events` / `docker events`
- Stream events.

### `docker version`
- Distinguishes between the Client API version and Server API version.

## SECTION 9: Registry Commands

### `docker login`
- **Purpose**: Log in to a Docker registry.
- **Security Note**: Never use `-p` on the CLI as it enters bash history. Use `--password-stdin`.
- **Example**: `echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin`
- **ECR Login**: `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com`

### `docker logout`
- Clear credentials.

### `docker search`
- Search Docker Hub.

### `docker manifest inspect`
- **Purpose**: Display the manifest of an image. Crucial for understanding if an image supports multiple architectures (amd64, arm64).

## SECTION 10: BuildKit and Buildx Commands

### `docker buildx create / ls / use / inspect`
- **Purpose**: Manage build instances. Allows setting up builders capable of cross-platform builds via QEMU.

### `docker buildx build`
- **Purpose**: Extended build capabilities using BuildKit.
- **Important Flags**:
  - `--platform`: E.g., `linux/amd64,linux/arm64`.
  - `--push`: Push the image to the registry after building.
  - `--load`: Load the single-platform image into the local docker engine.
  - `--cache-from, --cache-to`: External cache sources (e.g., registry, local directory, GitHub Actions).

### Multi-platform Build Sequence
```bash
docker buildx create --use --name mybuilder
docker buildx build --platform linux/amd64,linux/arm64 -t myrepo/myapp:latest --push .
```

### BuildKit Cache and Secret Mounts
- **Cache Mount**: Speeds up package managers.
  - `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y gcc`
- **Secret Mount**: Safely use secrets at build time without leaving them in layers.
  - `RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret > /app/config`
  - Run with: `docker buildx build --secret id=mysecret,src=./secret.txt .`

## SECTION 11: Docker Scout Commands (Security)

### `docker scout cves`
- **Purpose**: Show vulnerabilities for an image.
- **Example**: `docker scout cves ubuntu:latest`

### `docker scout quickview / compare / recommendations / sbom`
- Fast security assessment tools integrated directly into Docker CLI to provide actionable advice on base image updates.

## SECTION 12: Advanced and Debugging Commands

### `docker commit`
- **Purpose**: Create a new image from a container's changes.
- **WHY it's bad practice**: Creates un-reproducible, untraceable "black box" images. You lose the declarative nature of a Dockerfile. Only use for temporary debugging or data recovery.

### `docker export / docker import`
- Export/import container filesystem contents. Flattens layers.

### `docker context`
- **Purpose**: Manage multiple Docker endpoints (local desktop, remote server, swarm).
- **Example**: `docker context create remote-server --docker "host=ssh://user@remote-ip"`
- `docker --context remote-server ps`

### `docker debug`
- A Docker Desktop Pro/Team feature that attaches a Swiss-army-knife debugging container to a target container that might lack shells or tools (like distroless images).

## SECTION 13: Production Command Patterns

### Production run command template (all security flags)
```bash
docker run -d \
  --name app_prod \
  --restart always \
  --read-only \
  --tmpfs /tmp \
  --user 1000:1000 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --network custom_net \
  -m 512m --cpus 1.0 \
  -p 8080:8080 \
  myrepo/app:v1.2.3
```

### Container cleanup cron job commands
```bash
0 3 * * * docker system prune -af --filter "until=168h"
```

### Container resource inspection one-liner
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

### Find containers by label
```bash
docker ps --filter "label=env=production"
```

### Kill all containers of a specific image
```bash
docker rm -f $(docker ps -q --filter "ancestor=nginx:latest")
```

### Complete production Dockerfile build and push script (bash)
```bash
#!/bin/bash
set -e
IMAGE_NAME="myrepo/app"
COMMIT_SHA=$(git rev-parse --short HEAD)
TAG="${IMAGE_NAME}:${COMMIT_SHA}"

echo "Building ${TAG}..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=${IMAGE_NAME}:buildcache \
  --cache-to type=registry,ref=${IMAGE_NAME}:buildcache,mode=max \
  -t ${TAG} \
  -t ${IMAGE_NAME}:latest \
  --push .
echo "Build and push successful."
```

---
## END OF APPENDIX

### Quick Reference Table
| Command | Purpose | Example |
|---|---|---|
| `docker build` | Build image | `docker build -t app:1.0 .` |
| `docker run` | Start container | `docker run -d -p 80:80 app:1.0` |
| `docker ps` | List running | `docker ps -a` |
| `docker stop` | Graceful stop | `docker stop web` |
| `docker rm` | Remove container | `docker rm -f web` |
| `docker rmi` | Remove image | `docker rmi app:1.0` |
| `docker exec` | Run in container | `docker exec -it web sh` |
| `docker logs` | View logs | `docker logs -f web` |
| `docker inspect` | Deep dive details | `docker inspect web` |

### Troubleshooting Command Sequences
- **Symptom: Container exits immediately**
  1. `docker ps -a` (find ID)
  2. `docker logs <ID>`
  3. `docker inspect -f '{{.State.ExitCode}}' <ID>`
  4. Run interactively to test entrypoint: `docker run -it --entrypoint sh <image>`
- **Symptom: Cannot connect to container port**
  1. `docker port <container_name>` (verify mapping)
  2. `docker inspect -f '{{.NetworkSettings.IPAddress}}' <container>` (verify IP)
  3. `docker exec <container> netstat -tuln` (is process listening on 0.0.0.0 inside?)
- **Symptom: Disk is full**
  1. `docker system df`
  2. `docker image prune`
  3. `docker container prune`
  4. `docker volume prune` (Warning: checks for data loss)

### Production Alias File (`~/.bash_aliases`)
```bash
# Docker Shortcuts
alias d='docker'
alias dc='docker compose'
alias dps='docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
alias dclean='docker system prune -f'
alias dkillall='docker rm -f $(docker ps -aq)'
alias dexec='docker exec -it'
alias dlogs='docker logs -f'
alias dip='docker inspect -f "{{.NetworkSettings.IPAddress}}"'
```
