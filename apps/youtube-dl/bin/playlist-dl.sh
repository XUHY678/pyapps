docker run --rm \
           --interactive \
           --tty \
           --env DISPLAY=host.docker.internal:0.0 \
           --env LIBGL_ALWAYS_INDIRECT=0 \
           --volume /mnt/d/Temporary:/home/xuhy/app \
           --net host \
           --user xuhy \
           --workdir /home/xuhy/app \
           --privileged \
           xuhy/pyapps \
	   youtube-dl --write-auto-sub -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' $1
