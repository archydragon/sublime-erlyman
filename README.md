Erlyman
=======

Erlang manual pages navigation plugin for Sublime Text, currently in beta.

Requirements
------------

* Linux or MacOS X as operating system
* installed Erlang distribution with man pages

Installation
------------

Manual:
```
cd /path/to/sublime-text-2/Packages
git clone https://github.com/Mendor/sublime-erlyman.git Erlyman
```

Or use [Package Control](http://wbond.net/sublime_packages/package_control).

Usage
-----

Default key bidgings:

* ``F1`` anywhere — show list of manual pages;
* ``Alt+F1`` on function name — search this function in manual pages.

You may use ``Ctrl+R`` inside manual page view to navigate page sections, type and function definitions.

#### What to do if the list is empty:

  * If you're using Debian, Ubuntu or any other .deb-based Linux distribution, make sure that you've installed ``erlang-manpages`` package.
  * If you're using any other Linux distribution, please open an issue.
  * If you're using [kerl](https://github.com/yrashk/kerl) to manage Erlang installations, make sure that there is the line `KERL_INSTALL_MANPAGES=true` in your `~/.kerlrc`. In case of necessity rebuild your active installation with this tuning.

Screenshot
----------

![screen](https://raw.github.com/Mendor/sublime-erlyman/master/screen.png)

License
-------

[WTFPL](http://sam.zoy.org/wtfpl/)
