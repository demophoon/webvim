Webvim
======

Run Vim in a web browser using Docker

Version 1.0.0

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
    $ # Or install dependencies with requirements.txt
    $ pip install -r requirements.txt
    ```

2. Preload demophoon/webvim docker container or build from Dockerfile

    ```bash
    $ # Load from Docker Registry
    $ docker run demophoon/webvim +q
    $
    $ # Build from Dockerfile
    $ docker build -t custom/build .
    ```

3. Modify the `commands` section of `production.ini` if needed.
4. Run Webvim and visit [http://localhost:9090/](http://localhost:9090/) in a browser!

    ```bash
    $ # Run Webvim
    $ webterm_server production.ini
    ```

Future
------
* [ ] Handle all unicode characters in the browser.
* [ ] Tests.

Contributing
------------

Fork, Create topic branch, Submit Pull request.
