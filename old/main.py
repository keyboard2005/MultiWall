import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class MonitorSettings:
    def __init__(self):
        pass

    def get_monitors(self):
        monitors = []
        display = Gdk.Display.get_default()
        connected_monitor_count = Gdk.Display.get_n_monitors(display)
        for item in range(0, connected_monitor_count):
            monitor = Gdk.Display.get_monitor(display, item)
            geometry = monitor.get_geometry()
            monitor_info = {
                "x": geometry.x,
                "y": geometry.y,
                "width": geometry.width,
                "height": geometry.height,
            }
            monitors.append(monitor_info)
        return monitors



monitor_settings = MonitorSettings()
print(monitor_settings.get_monitors())

















































# class MyWindow(Gtk.Window):
#     def __init__(self):
#         Gtk.Window.__init__(self, title="MultiWall Ubuntu")
#         self.btn = Gtk.Button(label="Press Me")
#         self.btn.connect("clicked", self.btn_pressed)
#         self.add(self.btn)

#     def btn_pressed(self, widget):
#         print("Button was pressed!")


# win = MyWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()