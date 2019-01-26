# pipeup
Pipe images to shareable link

alias pipeup='curl -X POST --data-binary @- https://u.dh.ax -sSu someguy:supersecretpassword'

cat foo.webm | pipeup
