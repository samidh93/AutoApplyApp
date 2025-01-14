
docker run --name aws -it -v "$(pwd):/docker_mount" amazonlinux:latest bash -c 'mkdir -p ~/$(basename /docker_mount) && cp -r /docker_mount ~/$(basename /docker_mount) && cd ~/$(basename /docker_mount) && bash'
