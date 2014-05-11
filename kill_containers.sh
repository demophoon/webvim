#!/bin/sh

`docker ps | grep 'hour ago' | awk '{print $1}' | xargs docker kill` > /dev/null
`docker ps | grep 'hours ago' | awk '{print $1}' | xargs docker kill` > /dev/null
`docker ps | grep 'day ago' | awk '{print $1}' | xargs docker kill` > /dev/null
`docker ps | grep 'days ago' | awk '{print $1}' | xargs docker kill` > /dev/null
`docker ps | grep 'week ago' | awk '{print $1}' | xargs docker kill` > /dev/null
`docker ps | grep 'weeks ago' | awk '{print $1}' | xargs docker kill` > /dev/null
