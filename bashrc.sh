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

    if ps -p $SSH_AGENT_PID > /dev/null
    then
       echo "ssh-agent is already running"
       # Do something knowing the pid exists, i.e. the process with $PID is running
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
alias dphp='docker exec -it php /bin/sh'
alias dphp74='docker exec -it php74 /bin/sh'
alias dphp56='docker exec -it php56 /bin/sh'
alias dmysql='docker exec -it mysql /bin/bash'
alias dredis='docker exec -it redis /bin/sh'
alias dngrok='docker exec -it ngrok /bin/sh'
alias dscm='docker exec -it scm-manager /bin/sh'


export PATH=$PATH:/root/dnmp/composer/vendor/bin