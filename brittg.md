================================================================================

                         Britt Gresham's Awesome Vimrc
                             http://vim.brittg.com

================================================================================

Welcome to http://vim.brittg.com!
This is where I am able to show off my completely awesome Vim configuration!

Now I realize that some of you are not well-versed in Vim so I have turned on
some helpful options like navigating the page with your arrow keys instead of
using "hjkl" for moving the cursor. That being said this website is dedicated to
showing off how awesome I believe my Vim configurations are and is in no way
suppose to show off the best practices of Vim. My dotfiles are a living and
breathing set of configuration files and may change over time.

{{{ New to Vim? Move the cursor here and press space -
======================================================

What Is Vim?
============

  Vim is a highly configurable text editor built to enable efficient text
  editing. It is an improved version of the vi editor distributed with most UNIX
  systems.

  Vim is often called a "programmer's editor," and so useful for programming
  that many consider it an entire IDE. It's not just for programmers, though.
  Vim is perfect for all kinds of text editing, from composing email to editing
  configuration files.

  Despite what the above comic suggests, Vim can be configured to work in a very
  simple (Notepad-like) way, called evim or Easy Vim.

What Vim Is Not?
================

  Vim isn't an editor designed to hold its users' hands. It is a tool, the use
  of which must be learned.

  Vim isn't a word processor. Although it can display text with various forms of
  highlighting and formatting, it isn't there to provide WYSIWYG editing of
  typeset documents. (It is great for editing TeX, though.)

Vim's License
=============

  Vim is charityware. Its license is GPL-compatible, so it's distributed freely,
  but we ask that if you find it useful you make a donation to help children in
  Uganda through the ICCF. The full license text can be found in the
  documentation. Much more information about charityware on Charityware.info.

}}}

Now on to the fun stuff!

Modifying Configurations on the Fly
===================================

If you would like to see my current `.vimrc` press ",v" and navigate around.
This command will open a new vertical split with my `.vimrc` settings. Use the
space bar to open and close sections. When you are finished the command ":q!"
will close the split the cursor is in. Make sure you run that command when your
cursor is in the `.vimrc` window! ;)

Opening Files using NERDTree
============================

To open up the file browser (NERDTree) press ",n". This command will also close
NERDTree if you repeat the command inside of NERDTree.



How am I Doing This?
====================

If you've been using Vim for a while you have probably noticed that everything
you have been able to do in Vim you can do here. So what gives? Is this really
the most advanced javascript implementation of Vim? Well... Yes and no.

You are actually connected to a real server with a real running instance of Vim.
There are just some javascript bits that let me deliver Vim to you like how it
was meant to be delivered to you.

Docker lets me play around with lightweight Linux containers. One of which I
have configured and installed my own Dotfiles. There is a Python web server
sitting on the same server that spins up and down docker instances on the fly
for visitors like you to play around with. The same Python web server that is
spinning up and down these Linux containers is also a websocket server that lets
you stream the terminals to you in real time!

Still interested?
=================

Checkout the repository holding the source code here:

  - https://github.com/demophoon/webvim

Also don't forget to check my websites out for more information regarding me!

  - http://www.brittg.com/
  - https://github.com/demophoon
  - http://brittg.com/linkedin
  - http://twitter.com/demophoon
  - http://brittg.com/googleplus
  - http://brittg.com/resume

  Or shoot me an email at brittcgresham@gmail.com


---------------------------------------------------------
--- Important wibbly wobbly Vim stuff below this line ---
---------------------------------------------------------

vim: ft=markdown foldmethod=marker nospell
