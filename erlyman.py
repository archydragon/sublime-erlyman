import sublime, sublime_plugin
import os
import os.path
import string
import re

def get_modules():
    trygrep = os.popen("man -k . | grep 3erl | awk '{print $1}'").read()
    if trygrep:
        return trygrep.split("\n")
    kerlpath = os.popen("kerl active | sed -e 's/^[^/].*$//' -e '/^$/d'").read()
    manpaths = [
        "/usr/lib64/erlang/man",
        "/usr/local/lib/erlang/man",
        kerlpath + "/man"
    ]
    for p in manpaths:
        if os.path.isdir(p):
            mans = []
            for root, dirs, files in os.walk(p):
                mans += files
            return [f.split('.')[0] for f in mans]
    return ['']

def erl():
    if not os.popen("which erl").read():
        return "/usr/local/bin/erl"
    else:
        return "erl"

# On module load:
MODULES = get_modules()
ERL = erl()

class InsertviewCommand(sublime_plugin.TextCommand):
    def run(self, edit, pos, text):
        self.view.insert(edit, pos, text)

class Erlyman_findCommand(sublime_plugin.WindowCommand):
    """
    Shows manual search input field
    """

    def run(self):
        self.window.show_quick_panel(MODULES, self.show)

    def show(self, item):
        if item is -1:
            return
        manpage = MODULES[item]
        render_page(manpage, False)

class Erlyman_contextCommand(sublime_plugin.TextCommand):
    """
    Look for selected command in manual pages
    """

    def run(self, edit):
        for region in self.view.sel():
            word = self.view.word(region)
            word_c = self.view.substr(word)
            if word_c in MODULES:
                end = word.end()
                ch = self.view.substr(sublime.Region(end, end+1))
                if ch == ':':
                    fun = self.view.word(sublime.Region(end+1, end+1))
                    fun_c = self.view.substr(fun)
                    render_page(word_c, fun_c)
            else:
                begin = word.begin()
                ch = self.view.substr(sublime.Region(begin-1, begin))
                if ch == ':':
                    mod = self.view.word(sublime.Region(begin-1, begin-1))
                    mod_c = self.view.substr(mod)
                    if mod_c in MODULES:
                        render_page(mod_c, word_c)
                    else:
                        sublime.status_message("There is no manual page for '" + mod_c +"' module.")
                else:
                    if man_read("erlang").find("       " + word_c + "(") != -1:
                        render_page("erlang", word_c)
                    else:
                        sublime.status_message("There is no BIF named '" + word_c +"'.")
        return

def render_page(page_name, fun):
    man = sublime.active_window().new_file()
    content = re.sub(r'\t', r'    ', man_read(page_name))
    man.set_name("[MAN] " + page_name + " - Erlang")
    man.run_command('insertview', {'pos': 0, 'text': content})
    man.set_read_only(True)
    man.set_scratch(True)
    home = man.text_point(0, 0)
    man.sel().clear()
    man.sel().add(sublime.Region(home))
    man.show(home)
    man.settings().set("tab_size", 32)
    man.set_syntax_file("Packages/Erlyman/Erlang Manual.tmLanguage")
    if fun != False:
        # print fun
        f = man.find("^\s{7}" + fun + "\(.*\)", 0)
        man.show_at_center(f)
        man.sel().add(f)

def man_read(man_name):
    content_raw = os.popen(ERL + " -man " + man_name + " | col -b").read()
    # content_raw = os.popen("uptime").read()
    # print(content_raw)
    r = re.compile('\[[0-9]*m')
    return r.sub('', ''.join(filter(lambda x: x in string.printable, content_raw)))
