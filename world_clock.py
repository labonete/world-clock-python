import tkinter as tk
from datetime import datetime
import pytz
import os
import sys
# --- Import ctypes for the AppUserModelID ---
import ctypes

try:
    import winreg
except ImportError:
    winreg = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Configuration ---
TIMEZONES = {
    "Philippines": "Asia/Manila",
    "New York, USA": "America/New_York",
    "London, UK": "Europe/London",
    "Riyadh, Saudi Arabia": "Asia/Riyadh",
    "Sydney, Australia": "Australia/Sydney",
}

# --- Theme Palettes ---
THEMES = {
    "dark": {
        "root_bg": "#2E2E2E", "frame_bg": "#424242", "city_fg": "white",
        "time_fg": "#00FF00", "date_fg": "lightgrey", "offset_fg": "#BBBBBB",
        "menu_bg": "#333333", "menu_fg": "white", "size_fg": "yellow"
    },
    "light": {
        "root_bg": "#F0F0F0", "frame_bg": "#FFFFFF", "city_fg": "black",
        "time_fg": "#006400", "date_fg": "#333333", "offset_fg": "#555555",
        "menu_bg": "SystemButtonFace", "menu_fg": "black", "size_fg": "blue"
    }
}

def get_windows_theme():
    if not winreg: return 'light'
    try:
        key_path = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
        winreg.CloseKey(key)
        return 'light' if value == 1 else 'dark'
    except Exception:
        return 'light'

# --- Application ---
class WorldClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Clock")
        self.root.geometry("360x600")
        self.root.resizable(True, True)

        try:
            icon_path = resource_path("icon.ico")
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Icon not found. Using default icon.")
        
        self.theme_name = get_windows_theme()
        self.theme = THEMES[self.theme_name]
        
        self.timezone_widgets = []
        self.settings_menu = None
        self.size_label = None
        self.canvas = None
        self.scrollable_frame = None

        self._create_menu()
        self._create_widgets()
        self._apply_theme()
        
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Up>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Down>", lambda event: self.canvas.yview_scroll(1, "units"))
        
        self.root.bind("<Configure>", self._on_resize)
        self.update_times()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.settings_menu = tk.Menu(menubar, tearoff=0)
        self.settings_menu.add_command(label="Refresh Theme", command=self.refresh_theme)
        menubar.add_cascade(label="Settings", menu=self.settings_menu)
        self.root.config(menu=menubar)

    def _create_widgets(self):
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        for city in TIMEZONES:
            tz_frame = tk.Frame(self.scrollable_frame, bd=1, relief="solid")
            tz_frame.pack(fill="x", pady=6, ipady=8, padx=10)

            city_label = tk.Label(tz_frame, text=city, font=("Helvetica", 14, "bold"))
            city_label.pack()
            offset_label = tk.Label(tz_frame, font=("Helvetica", 9, "italic"))
            offset_label.pack()
            time_label = tk.Label(tz_frame, font=("Helvetica", 20))
            time_label.pack(pady=(5, 0))
            date_label = tk.Label(tz_frame, font=("Helvetica", 10))
            date_label.pack()
            
            self.timezone_widgets.append({
                "frame": tz_frame, "city": city_label, "offset": offset_label,
                "time": time_label, "date": date_label
            })
        
        self.size_label = tk.Label(self.root, text="", font=("Helvetica", 8))
        self.size_label.pack(side="bottom", anchor="se", padx=5, pady=2)

    def _apply_theme(self):
        self.root.configure(bg=self.theme["root_bg"])
        self.settings_menu.configure(bg=self.theme["menu_bg"], fg=self.theme["menu_fg"])
        self.size_label.configure(bg=self.theme["root_bg"], fg=self.theme["size_fg"])
        self.canvas.configure(bg=self.theme["root_bg"])
        self.scrollable_frame.configure(bg=self.theme["root_bg"])

        for widgets in self.timezone_widgets:
            widgets["frame"].configure(bg=self.theme["frame_bg"])
            widgets["city"].configure(bg=self.theme["frame_bg"], fg=self.theme["city_fg"])
            widgets["offset"].configure(bg=self.theme["frame_bg"], fg=self.theme["offset_fg"])
            widgets["time"].configure(bg=self.theme["frame_bg"], fg=self.theme["time_fg"])
            widgets["date"].configure(bg=self.theme["frame_bg"], fg=self.theme["date_fg"])

    def refresh_theme(self):
        new_theme_name = get_windows_theme()
        if new_theme_name != self.theme_name:
            self.theme_name = new_theme_name
            self.theme = THEMES[self.theme_name]
            self._apply_theme()

    def _on_resize(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.size_label.config(text=f"{width}x{height}")
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    def update_times(self):
        ph_tz = pytz.timezone('Asia/Manila')
        ph_now = datetime.now(ph_tz)
        ph_offset = ph_now.utcoffset()

        for i, (city, tz_name) in enumerate(TIMEZONES.items()):
            widgets = self.timezone_widgets[i]
            try:
                tz = pytz.timezone(tz_name)
                now = datetime.now(tz)
                
                widgets["time"].config(text=now.strftime("%I:%M:%S %p"))
                widgets["date"].config(text=now.strftime("%A, %B %d, %Y"))

                diff_hours = (now.utcoffset() - ph_offset).total_seconds() / 3600
                offset_str = ""
                if diff_hours == 0:
                    offset_str = "Philippine Standard Time"
                elif diff_hours > 0:
                    offset_str = f"{int(diff_hours)} hours ahead of PH"
                else:
                    offset_str = f"{int(abs(diff_hours))} hours behind PH"
                widgets["offset"].config(text=offset_str)

            except Exception as e:
                widgets["time"].config(text="Invalid Timezone")
                print(f"Error updating {city}: {e}")

        self.root.after(1000, self.update_times)

if __name__ == "__main__":
    # --- SET THE UNIQUE APP ID FOR THE TASKBAR ICON ---
    myappid = 'kevinacer.worldclock.app.1' # A unique string for your app
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()