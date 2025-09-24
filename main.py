import os
# Set an environment variable to avoid a Kivy startup issue on some systems
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from datetime import datetime
import pytz

# --- Configuration ---
TIMEZONES = {
    "ph": {"name": "Philippines", "tz": "Asia/Manila"},
    "nyc": {"name": "New York, USA", "tz": "America/New_York"},
    "lon": {"name": "London, UK", "tz": "Europe/London"},
    "ruh": {"name": "Riyadh, Saudi Arabia", "tz": "Asia/Riyadh"},
    "syd": {"name": "Sydney, Australia", "tz": "Australia/Sydney"},
}

class WorldClockLayout(BoxLayout):
    # This class is the root widget of our app, defined in the .kv file.
    # Kivy will automatically link this class to the <WorldClockLayout> rule.
    pass

class WorldClockApp(App):
    def build(self):
        # The build method returns the root widget of the application.
        # Kivy automatically loads the 'worldclock.kv' file.
        self.layout = WorldClockLayout()
        # Schedule the update_times function to run every second.
        Clock.schedule_interval(self.update_times, 1)
        return self.layout

    def update_times(self, dt):
        """This function is called every second to update the time and date."""
        ph_tz = pytz.timezone('Asia/Manila')
        ph_now = datetime.now(ph_tz)
        ph_offset = ph_now.utcoffset()

        for key, data in TIMEZONES.items():
            try:
                tz = pytz.timezone(data["tz"])
                now = datetime.now(tz)

                # Format the strings
                time_str = now.strftime("%I:%M:%S %p")
                date_str = now.strftime("%A, %B %d, %Y")

                # Calculate the offset
                diff_hours = (now.utcoffset() - ph_offset).total_seconds() / 3600
                offset_str = ""
                if diff_hours == 0:
                    offset_str = "Philippine Standard Time"
                elif diff_hours > 0:
                    offset_str = f"{int(diff_hours)} hours ahead of PH"
                else:
                    offset_str = f"{int(abs(diff_hours))} hours behind PH"

                # Update the labels in the .kv file using their 'id'
                self.layout.ids[f'{key}_time'].text = time_str
                self.layout.ids[f'{key}_date'].text = date_str
                self.layout.ids[f'{key}_offset'].text = offset_str

            except Exception as e:
                self.layout.ids[f'{key}_time'].text = "Error"
                print(f"Error updating {data['name']}: {e}")

if __name__ == '__main__':
    WorldClockApp().run()