# Dockerfile for creating vim_base container
# Experimental

FROM ubuntu:14.04
MAINTAINER Britt Gresham <brittcgresham@gmail.com>

RUN apt-get update
RUN apt-get install git python vim tmux -y
RUN apt-get install timelimit -y

RUN git clone https://github.com/demophoon/dotfiles.git
RUN git clone https://github.com/demophoon/vundle-headless-installer.git

RUN ./dotfiles/setup.sh -f                               # Sets up symlinks for dotfiles
RUN python ./vundle-headless-installer/install.py        # Installs Vundle plugins without running Vim

ADD ./brittg.md /README.md

ENTRYPOINT ["vim"]
CMD ["-u", "/dotfiles/.evimrc", "README.md"]
