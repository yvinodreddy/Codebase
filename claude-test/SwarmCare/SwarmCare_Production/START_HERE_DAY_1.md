# 🚀 DAY 1: Your First Steps (30 Minutes)

**Welcome!** This is where you start your journey from zero to infrastructure expert.

**Today's Goal:** Run your first Docker container and understand what happened.

---

## ✅ Step 1: Check if Docker is Installed (2 min)

```bash
# Check Docker version
docker --version

# If you see: Docker version 20.x.x or higher → You're good! ✅
# If you see: command not found → Install Docker (see below)
```

### Install Docker (if needed):

**Ubuntu/WSL:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and log back in
```

**Verify installation:**
```bash
docker run hello-world
# Should print: "Hello from Docker!"
```

---

## ✅ Step 2: Run Your FIRST Container (5 min)

```bash
# Run the simplest possible container
docker run hello-world
```

**What just happened?** (Read this!)

1. Docker looked for "hello-world" image on your computer
2. Didn't find it, so downloaded it from Docker Hub
3. Created a container from that image
4. Ran the container (printed a message)
5. Container stopped (it finished its job)

**That's it! You just ran your first container!** 🎉

---

## ✅ Step 3: Run a Web Server (5 min)

```bash
# Run nginx (a web server) in a container
docker run -d -p 8080:80 --name my-first-webserver nginx

# What each part means:
# docker run     → Run a container
# -d             → Run in background (detached)
# -p 8080:80     → Map port 8080 (your computer) to port 80 (container)
# --name ...     → Give it a friendly name
# nginx          → The image to use

# Check it's running
docker ps
```

**Now open your browser:** http://localhost:8080

You should see: "Welcome to nginx!"

**CONGRATULATIONS!** You're running a web server in a container! 🎉

---

## ✅ Step 4: Explore Your Container (5 min)

```bash
# See running containers
docker ps

# See ALL containers (even stopped ones)
docker ps -a

# View container logs
docker logs my-first-webserver

# Get inside the container (like SSH)
docker exec -it my-first-webserver /bin/bash
# You're now INSIDE the container!
# Type: ls
# Type: exit (to get out)
```

---

## ✅ Step 5: Stop and Remove Container (3 min)

```bash
# Stop the container
docker stop my-first-webserver

# Check it's stopped
docker ps
# (Should be empty now)

# Check all containers
docker ps -a
# (Should show stopped container)

# Remove the container
docker rm my-first-webserver

# Verify it's gone
docker ps -a
# (Should be empty now)
```

---

## ✅ Step 6: Run SwarmCare Test (5 min)

Now let's run something related to SwarmCare!

```bash
# Run Python in a container
docker run -it python:3.11 python

# You're now in Python REPL inside a container!
# Try this:
print("Hello from SwarmCare!")
print("I'm running inside Docker!")

# Exit Python
exit()
```

---

## ✅ Step 7: Understanding What You Learned (5 min)

**Today you learned:**

✅ **What a container is:** A running instance of an image
✅ **What an image is:** A template for creating containers
✅ **How to run containers:** `docker run`
✅ **How to see containers:** `docker ps`
✅ **How to stop containers:** `docker stop`
✅ **How to remove containers:** `docker rm`

**Key Commands to Remember:**
```bash
docker run <image>      # Run a container
docker ps               # See running containers
docker ps -a            # See all containers
docker stop <name>      # Stop a container
docker rm <name>        # Remove a container
docker logs <name>      # View container logs
```

---

## 🎯 Day 1 Challenge (Optional, 10 min)

Can you run these 3 containers?

```bash
# 1. Redis (database)
docker run -d --name my-redis -p 6379:6379 redis

# 2. Postgres (database)
docker run -d --name my-postgres -e POSTGRES_PASSWORD=password123 -p 5432:5432 postgres

# 3. Another nginx (on different port)
docker run -d --name my-nginx2 -p 8081:80 nginx

# Check all 3 are running
docker ps
# Should show 3 containers!

# Stop and remove all
docker stop my-redis my-postgres my-nginx2
docker rm my-redis my-postgres my-nginx2
```

---

## ✅ Verification Checklist

Mark what you completed today:

- [ ] Installed Docker
- [ ] Ran hello-world container
- [ ] Ran nginx web server
- [ ] Accessed http://localhost:8080 in browser
- [ ] Explored container with `docker exec`
- [ ] Stopped and removed container
- [ ] Ran Python container
- [ ] Understood basic Docker commands

**If you checked all boxes: Day 1 COMPLETE!** ✅

---

## 🚀 What's Next?

**Tomorrow (Day 2):** Building Docker images

**Preview:**
```bash
# Tomorrow you'll create your own Dockerfile
# And build custom images
# But for today, you're done! 🎉
```

---

## 🆘 Troubleshooting

**"docker: command not found"**
→ Docker not installed. Follow install steps above.

**"permission denied"**
→ Run: `sudo usermod -aG docker $USER` then log out/in

**"port already in use"**
→ Change the port: use `-p 8081:80` instead of `-p 8080:80`

**"cannot connect to docker daemon"**
→ Start Docker: `sudo systemctl start docker`

---

## 📊 Progress Tracker

```
Day 1: ✅ Docker Basics
Day 2: ⏳ Building Images
Day 3: ⏳ Docker Compose
Day 4: ⏳ Networking
Day 5: ⏳ Practice

Week 1: □ Docker (0/5 days complete)
Week 2: □ Kubernetes
Week 3: □ Neo4j
Week 4: □ Terraform
```

---

**Great job today! Tomorrow we build our first Docker image!** 🚀

---

*Time spent today: ~30 minutes*
*Containers run: 3+ containers*
*Skills gained: Docker basics*
*Your status: 🎯 Day 1 COMPLETE!*
