var Webterm = function(api_endpoint, init_element, options) {
    var sock;
    var term;
    var connected = false;
    default_options = {
        session_id: null,
        scale: true,
        height: null,
        width: null,
        rows: null,
        columns: null,
    };
    if (options == null) {
        options = {};
    }
    options = jQuery.extend(default_options, options);

    function connect_to_ws() {
        sock = new SockJS(api_endpoint);
        sock.onopen = function() {
            if (options.session_id) {
                sock.send("c" + options.session_id);
            } else {
                sock.send('c');
            }
            sock.ready = true;
            term.fixResize();
        };
        sock.onmessage = function(e) {
            if (e.data) {
                var header = e.data[0];
                e.data = e.data.substr(1);
                switch (header) {
                    case '0':
                        term.write(e.data);
                        break;
                    case '1':
                        var msg = atob(e.data);
                        term.write(msg);
                        break;
                }
                term.urlify();
            }
        };
        sock.onclose = function() {
            sock.ready = false;
            term.reset();
            term.writeln("Session Disconnected.");
        };

    }

    function get_text_size(element) {
        if (element == null) {
            element = $("body");
        }
        var x = $("<span>#</span>").addClass("terminal").css("padding", "0px").css("margin", "0px");
        element.append(x);
        size_obj = {
            width: x[0].getBoundingClientRect().width,
            height: x[0].getBoundingClientRect().height,
        }
        x.remove();
        return size_obj;
    }

    function get_element_sizes(element) {
        if (!options.scale) {
            return {
                cols: options.columns,
                rows: options.rows,
                height: options.height,
                width: options.width,
            }
        }
        var w_margins = element.outerWidth(true) - element.innerWidth();
        var h_margins = element.outerHeight(true) - element.innerHeight();
        var width = element.width() - w_margins;
        var height = element.height() - h_margins;
        var font_size = get_text_size(element);
        var col_size = Math.floor(width / font_size.width);
        var row_size = Math.floor(height / font_size.height);
        return {
            cols: col_size,
            rows: row_size,
            height: height,
            width: width,
        }
    }

    function raw_send(msg) {
        sock.send(msg);
    }

    function send_char_to_terminal(x) {
        sock.send("0" + x);
    }

    function init(term_id) {
        var jquery_element = $(term_id)
        var html_element = jquery_element[0];
        var sizes = get_element_sizes(jquery_element);
        term = new Terminal({
            cols: sizes.cols,
            rows: sizes.rows,
            screenKeys: true,
        });
        term.open(html_element);
        term.on('data', function(data) {
            send_char_to_terminal(data);
        });
        term._resize = term.resize;
        term.resize = function(x, y) {
            term._resize(x, y);
            sock.send("1" + x + "," + y);
        }
        term.fixResize = function() {
            var font_size = get_text_size(jquery_element);
            var sizes = get_element_sizes(jquery_element);
            term.resize(sizes.cols, sizes.rows);
        }
        term.urlify = function() {
            $("span").each(function(index, element) {
                if (element.innerText.indexOf("|") == -1) {
                    element.innerHTML = element.innerText.autoLink({target: "_blank"});
                }
            });
        }

        if (!connected) {
            connect_to_ws();
            connected = true;
        }

        var rtime = new Date(1, 1, 2000, 12,00,00);
        var timeout = false;
        var delta = 200;
        $(window).resize(function() {
            rtime = new Date();
            if (timeout === false) {
                timeout = true;
                setTimeout(resizeend, delta);
            }
        });
        function resizeend() {
            if (new Date() - rtime < delta) {
                setTimeout(resizeend, delta);
            } else {
                timeout = false;
                term.fixResize();
            }
        }

    }

    console.log("====================================");
    console.log("Ahh, so you are interested in how things work? Press G in Vim to go to the last few paragraphs to");
    console.log("find out how this was pulled off. Also don't forget to checkout the repository for more information");
    console.log("https://github.com/demophoon/webvim");
    console.log("Also don't forget to check out my website! http://www.brittg.com/ Thanks :) -- Britt Gresham");
    console.log("====================================");
    $(document).ready(function(){init(init_element)});
    console.log(term);
    return {
        send: send_char_to_terminal,
        options: options,
        raw_send: raw_send,
    };
};
