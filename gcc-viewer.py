# A pygtk program for viewing GCC .dot dumps
# To output .dot files from gcc, use:
#   -fdump-tree-all-graph -fdump-rtl-all-graph
# This program provides an interface for easily going
# forwards and backwards through the dumps, so that you
# can see where a particular change happened.

import glob
import os

import gtk
import xdot

class Window(gtk.Window):
    def __init__(self, output_dir, base_filename):
        gtk.Window.__init__(self)

        self.output_dir = output_dir
        self.base_filename = base_filename

        g = os.path.join(self.output_dir, self.base_filename) + ".*.dot"
        self.dot_filenames = sorted(glob.glob(g))
        if 0:
            print(self.dot_filenames)

        self.widget = xdot.DotWidget()
        self.add(self.widget)

        self.connect('key-press-event', self.on_key_press_event)

        self.idx = 0
        self.update_idx()

        self.show_all()

    def on_key_press_event(self, widget, event):
        # TODO: pick some other keys?
        if event.keyval == gtk.keysyms.a and self.idx > 0:
            # go back
            self.idx -= 1
            self.update_idx()
        elif event.keyval == gtk.keysyms.s and self.idx < len(self.dot_filenames) - 1:
            # go forwards
            self.idx += 1
            self.update_idx()

    def update_idx(self):
        filename = self.dot_filenames[self.idx]
        with open(filename) as f:
            self.widget.set_dotcode(f.read(), filename)
        self.set_title(filename)

if __name__ == "__main__":

    # FIXME: fix these hardcoded values:
    output_dir = "/home/david/coding-3/gcc-git-clean/build-with-jit/gcc"
    base_filename = "test.c"

    win = Window(output_dir, base_filename)
    win.connect('destroy', gtk.main_quit)

    gtk.main()


