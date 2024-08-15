import gi
import time
import board
import adafruit_dht
import adafruit_hcsr04
import adafruit_tsl2561
import digitalio

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton

class RPiSensorActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.max_participants = 1

        # Toolbar
        toolbar_box = ToolbarBox()
        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        self.show_all()

        # Set up sensors
        self.setup_sensors()

        # Create GUI elements
        self.create_gui()

        # Update sensor readings every 2 seconds
        GLib.timeout_add_seconds(2, self.update_readings)

    def setup_sensors(self):
        # Initialize the DHT11 sensor
        self.dht_sensor = adafruit_dht.DHT11(board.D4)

        # Initialize the HC-SR04 Ultrasonic sensor
        self.distance_sensor = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6)

        # Initialize the TSL2561 Light Sensor
        self.light_sensor = adafruit_tsl2561.TSL2561(board.I2C())

        # Initialize the PIR Motion Sensor
        self.pir_sensor = digitalio.DigitalInOut(board.D7)
        self.pir_sensor.direction = digitalio.Direction.INPUT

    def create_gui(self):
        # Main container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_box.set_halign(Gtk.Align.CENTER)
        self.main_box.set_valign(Gtk.Align.CENTER)
        self.main_box.set_margin_start(30)
        self.main_box.set_margin_end(30)
        self.main_box.set_margin_top(30)
        self.main_box.set_margin_bottom(30)
        self.main_box.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        self.set_canvas(self.main_box)

        # Container for sensor labels
        sensor_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        sensor_box.set_halign(Gtk.Align.CENTER)
        sensor_box.set_valign(Gtk.Align.CENTER)
        sensor_box.set_margin_start(30)
        sensor_box.set_margin_end(30)
        sensor_box.set_margin_top(30)
        sensor_box.set_margin_bottom(30)

        # Load CSS
        self.load_css()

        # Humidity label
        self.humidity_label = Gtk.Label()
        self.humidity_label.get_style_context().add_class("sensor-label")
        sensor_box.pack_start(self.humidity_label, False, False, 0)

        # Distance label
        self.distance_label = Gtk.Label()
        self.distance_label.get_style_context().add_class("sensor-label")
        sensor_box.pack_start(self.distance_label, False, False, 0)

        # Light label
        self.light_label = Gtk.Label()
        self.light_label.get_style_context().add_class("sensor-label")
        sensor_box.pack_start(self.light_label, False, False, 0)

        # Motion label
        self.motion_label = Gtk.Label()
        self.motion_label.get_style_context().add_class("sensor-label")
        sensor_box.pack_start(self.motion_label, False, False, 0)

        # Add sensor box to the main container
        self.main_box.pack_start(sensor_box, True, True, 0)
        self.main_box.show_all()

    def load_css(self):
        css = b"""
        .sensor-label {
            background-color: #4a90e2; /* Blue background for labels */
            border-radius: 10px;
            padding: 20px;
            font-family: monospace;
            font-size: 24px;
            color: #ffffff; /* White text color */
            margin: 10px;
            border: 2px solid #2a70b1; /* Darker blue border */
        }

        .main-box {
            background-color: #ffffff; /* White background for the main container */
            border-radius: 25px; /* Rounded corners for the main container */
            padding: 20px; /* Padding inside the container */
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_readings(self):
        try:
            # Read humidity
            humidity = self.dht_sensor.humidity
            if humidity is not None:
                self.humidity_label.set_text(f"Humidity: {humidity:.1f} %")
            else:
                self.humidity_label.set_text("Humidity: Error reading")
        except RuntimeError as e:
            self.humidity_label.set_text(f"Humidity: Error reading ({str(e)})")

        try:
            # Read distance
            distance = self.distance_sensor.distance
            self.distance_label.set_text(f"Distance: {distance:.1f} cm")
        except RuntimeError as e:
            self.distance_label.set_text(f"Distance: Error reading ({str(e)})")

        try:
            # Read light intensity
            light = self.light_sensor.lux
            self.light_label.set_text(f"Light: {light:.1f} lux")
        except RuntimeError as e:
            self.light_label.set_text(f"Light: Error reading ({str(e)})")

        try:
            # Read motion detection
            motion = self.pir_sensor.value
            self.motion_label.set_text(f"Motion: {'Detected' if motion else 'Not detected'}")
        except RuntimeError as e:
            self.motion_label.set_text(f"Motion: Error reading ({str(e)})")

        return True  # Continue to call this function

if __name__ == "__main__":
    activity = RPiSensorActivity(None)
    Gtk.main()
