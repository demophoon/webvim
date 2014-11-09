Webvim
======

Run Vim in a web browser using Docker

Version 0.1.0

* * *

Installation
------------

1. Clone this repo and install dependencies in a python virtual environment.

    ```bash
    $ # Clone the repo
    $ git clone https://github.com/demophoon/webvim
    $
    $ # Setup Virtual Environment with virtualenvwrapper
    $ mkvirtualenv webvim
    $
    $ # or Setup Virtual Environment with virtualenv
    $ virtualenv webvim
    $ cd webvim
    $ source bin/activate
    $
    $ # Install dependencies with setup.py
    $ python setup.py develop
    ```

2. Preload demophoon/webvim docker container or build from Dockerfile

    ```bash
    $ # Load from Docker Registry
    $ docker run demophoon/webvim +q
    $
    $ # Build from Dockerfile
    $ docker build -t custom/build .
    ```

3. Modify 'User Settings' section of `production.ini` if needed.
4. Run Webvim and visit [http://localhost:6543/](http://localhost:6543/) in a browser!

    ```bash
    $ # Run Webvim
    $ pserve production.ini
    ```

On the 1.0 Roadmap
------------------

* [ ] Create a javascript library for embedding webvim into other websites.
* [ ] More settings in configuration files like init_command, memory_limit, ect.

Contributing
------------

Fork, Create topic branch, Submit Pull request.
