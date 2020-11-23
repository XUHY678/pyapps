docker run --rm \
           --interactive \
           --tty \
           --env DISPLAY=host.docker.internal:0.0 \
           --env LIBGL_ALWAYS_INDIRECT=0 \
           --volume $HOME/Workspace/pyapps/apps/xuexiqiangguo:/home/xuhy/app \
           --net host \
           --user xuhy \
           --workdir /home/xuhy/app \
           --privileged \
           xuhy/pyapps \
	   python src/main.py
