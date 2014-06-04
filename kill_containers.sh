#!/bin/sh

containers=$(sudo docker ps -a | grep '\([3-9][0-9] minutes\|hour\|day\|Exit\)')

if [ -n "$containers" ]; then
    sudo docker ps -a | grep '\([3-9][0-9] minutes\|hour\|day\|Exit\)' | awk '{print $1}' | xargs sudo docker kill
    sudo docker ps -a | grep '\([3-9][0-9] minutes\|hour\|day\|Exit\)' | awk '{print $1}' | xargs sudo docker rm
fi
