import tkinter as tk
from tkinter import messagebox, ttk
from spleeter.separator import Separator
import webbrowser
import threading
import pystray
from PIL import Image

# Initialize Spleeter for real-time music removal (2 stems: vocals + music)
separator = Separator('spleeter:2stems')

# Global app status
app_running = False

# Function to process real-time audio (remove music using Spleeter)
def process_audio():
    global app_running
    if app_running:
        print("Processing audio...")  # Placeholder for actual processing logic
        # Dummy audio data processing (You will use real captured audio here)
        # separator.separate_and_return(audio_data)

# Start the real-time processing
def start_app():
    global app_running
    if not app_running:
        app_running = True
        process_audio()  # Start audio processing
        status_label.config(text="Status: Running", foreground="green")
        print("App started.")

# Stop the real-time processing
def stop_app():
    global app_running
    if app_running:
        app_running = False
        status_label.config(text="Status: Stopped", foreground="red")
        print("App stopped.")

# Handle start/stop with confirmation dialog
def toggle_app():
    if app_running:
        if messagebox.askyesno("Stop", "Do you want to stop the app?"):
            stop_app()
    else:
        if messagebox.askyesno("Start", "Do you want to start the app?"):
            start_app()

# Donation button functionality
def donate():
    webbrowser.open("https://your-donation-link.com")

# Create an icon for the system tray
def create_tray_icon():
    icon = pystray.Icon("RealTimeMusicRemover", Image.open("icon.ico"), "Real Time Music Remover", menu=pystray.Menu(
        pystray.MenuItem("Open", show_window),
        pystray.MenuItem("Quit", quit_app)
    ))
    icon.run()

# Show the main window
def show_window(icon, item):
    root.deiconify()
    icon.stop()  # Stop the tray icon when the window is shown

# Quit the application
def quit_app(icon, item):
    stop_app()  # Ensure the app stops processing
    icon.stop()
    root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Real Time Music Remover")
root.geometry("300x200")
root.resizable(False, False)

# Apply modern style
style = ttk.Style()
style.configure("TFrame", background="#2E2E2E")
style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=10, background="#003366", foreground="white", borderwidth=0, relief="flat")
style.map("TButton", background=[("active", "#0056b3")])  # Change color on active

# Main Frame
main_frame = ttk.Frame(root)
main_frame.pack(expand=True, fill='both')

# UI Elements
status_label = ttk.Label(main_frame, text="Status: Stopped", foreground="red")  # Set initial status color to red
status_label.pack(pady=20)

# Create buttons with the same width
button_width = 15  # Set a fixed width for all buttons

toggle_button = ttk.Button(main_frame, text="Start/Stop", command=toggle_app, width=button_width)
toggle_button.pack(pady=10)

donate_button = ttk.Button(main_frame, text="Donate", command=donate, width=button_width)
donate_button.pack(pady=10)

# Function to run app on reboot (auto-start, to be set via system methods)
def add_to_startup():
    pass  # Implement registry or task scheduler to auto-start app

# Override the close button behavior
def on_closing():
    root.withdraw()  # Hide the window
    threading.Thread(target=create_tray_icon).start()  # Run tray icon in a separate thread


root.protocol("WM_DELETE_WINDOW", on_closing)  # Set the close button behavior

# Main loop
root.configure(background="#2E2E2E")  # Set the background color
root.mainloop()
