#!/bin/sh

containers=$(docker ps | grep '\([3-9][0-9] minutes\|hour\|day\)')

if [ -n "$containers" ]; then
    docker ps | grep '\([3-9][0-9] minutes\|hour\|day\)' | awk '{print $1}' | xargs docker kill
fi
