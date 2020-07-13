composer () {
    tty=
    tty -s && tty=--tty
    docker run \
        $tty \
        --interactive \
        --rm \
        --user $(id -u):$(id -g) \
        --volume $(pwd):/app \
        --volume ~/dnmp/composer:/tmp \
        --volume /etc/passwd:/etc/passwd:ro \
        --volume /etc/group:/etc/group:ro \
        composer "$@"
}

# 使用ssh-agent
composer () {
    tty=
    tty -s && tty=--tty

    if [ $(ps ax | grep [s]sh-agent | wc -l) -gt 0 ] ; then
        echo "ssh-agent is already running"
    else
        eval `ssh-agent -s`
    fi

    docker run \
        $tty \
        --interactive \
        --rm \
        --user $(id -u):$(id -g) \
        --volume $(pwd):/app \
        --volume ~/dnmp/composer:/tmp \
        --volume /etc/passwd:/etc/passwd:ro \
        --volume /etc/group:/etc/group:ro \
        --volume $SSH_AUTH_SOCK:/ssh-auth.sock \
        --volume ~/.ssh:/root/.ssh:ro \
        --env SSH_AUTH_SOCK=/ssh-auth.sock \
        composer "$@"
}
alias dnginx='docker exec -it openresty /bin/sh'
alias dphp71='docker exec -it php71 /bin/sh'
alias dphp72='docker exec -it php72 /bin/sh'
alias dphp73='docker exec -it php73 /bin/sh'
alias dphp74='docker exec -it php74 /bin/sh'
alias dphp56='docker exec -it php56 /bin/sh'
alias dmysql='docker exec -it mysql /bin/bash'
alias dredis='docker exec -it redis /bin/sh'
alias dngrok='docker exec -it ngrok /bin/sh'
alias dscm='docker exec -it scm-manager /bin/sh'
alias dgogs='docker exec -it gogs /bin/sh'
alias djenkins='docker exec -it jenkins /bin/sh'


export PATH=$PATH:/root/dnmp/composer/vendor/bin