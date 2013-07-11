import sublime, sublime_plugin
import os
import os.path
import string
import re

# On mofule load:
MODULES = os.popen(os.getcwd() + "/get_modules").read().split()

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
        self.render_page(manpage)

    def render_page(self, page_name):
        man = self.window.new_file()
        content_raw = os.popen("erl -man " + page_name).read()
        r = re.compile('\[[0-9]*m')
        content = r.sub('', filter(lambda x: x in string.printable, content_raw))
        man.set_name("[MAN] " + page_name + " - Erlang")
        e = man.begin_edit()
        man.insert(e, 0, content)
        man.end_edit(e)
        man.set_read_only(True)
        man.set_scratch(True)
        home = man.text_point(0, 0)
        man.sel().clear()
        man.sel().add(sublime.Region(home))
        man.show(home)
        man.settings().set("tab_size", 32)
        man.set_syntax_file("Packages/Erlyman/Erlang Manual.tmLanguage")
