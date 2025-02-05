import customtkinter
import os
from integrate_with_calendar import create_google_calendar_event, list_google_calendar_events, delete_google_calendar_event
from record_audio import start_recording, stop_recording_threads
from screen_capture import take_screenshot, get_monitor_area, calculate_similarity_ssim
from datetime import datetime, timezone
import time
import threading
import ctypes
import shutil


from speech_summary import process_audio_file

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.current_meeting_folder = None

        self.title("App")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)
        self.events_window = None
        self.event_window = None
        
        self.records_thread = None
        self.screenshot_thread = None
        self.stop_screenshot = threading.Event()

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        for i in range(5):  # Przyjmując, że masz 5 wierszy w sidebar_frame
            self.sidebar_frame.grid_rowconfigure(i, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ustawienia", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Platforma Label and OptionMenu
        self.platforma_label = customtkinter.CTkLabel(self.sidebar_frame, text="Platforma:", anchor="w")
        self.platforma_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.platforma_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Teams", "Zoom", "Google Meet",], command=self.sidebar_button_event)
        self.platforma_optionmenu.grid(row=2, column=0, padx=20, pady=10)

        self.dodatkowe_ustawienia_label = customtkinter.CTkLabel(self.sidebar_frame, text="Dodatkowe ustawienia", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.dodatkowe_ustawienia_label.grid(row=6, column=0, padx=20, pady=(20, 0))
        
        # Język Label and OptionMenu
        self.jezyk_label = customtkinter.CTkLabel(self.sidebar_frame, text="Język:", anchor="w")
        self.jezyk_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.jezyk_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Polski", "English", "Espanol", "Francais", "Deutsch"], command=self.sidebar_button_event)
        self.jezyk_optionmenu.grid(row=5, column=0, padx=20, pady=10)

        # Appearance Mode Label and OptionMenu
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(30, 20))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        # UI Scaling Label and OptionMenu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))

        # create buttons in the middle
        self.platforma_optionmenu.set("Teams")
        self.jezyk_optionmenu.set("Polski")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.start_label = customtkinter.CTkLabel(self, text="Nagrywanie spotkania", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.start_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 10))

        self.start_button = customtkinter.CTkButton(self, text="Start", command=self.toggle_start_stop, fg_color="green", hover_color="darkgreen")
        self.start_button.grid(row=1, column=1, padx=10, pady=10)

        # folder opening button
        self.open_folder_button = customtkinter.CTkButton(self, text="Przeglądaj spotkania", command=self.open_folder)
        self.open_folder_button.grid(row=3, column=1, padx=10, pady=10)

        self.calendar_label = customtkinter.CTkLabel(self, text="Integracja z kalendarzem", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.calendar_label.grid(row=0, column=2,columnspan=2 ,padx=(20, 0), pady=(20, 10))

        # email input fields
        self.email_label = customtkinter.CTkLabel(self, text="Adres e-mail kalendarza:", anchor="w")
        self.email_label.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

        self.email_entry = customtkinter.CTkEntry(self, width=300)
        self.email_entry.grid(row=1, column=3, padx=(0, 5), pady=(5, 0))

        # create event window button
        self.create_event_window_button = customtkinter.CTkButton(self, text="Utwórz wydarzenie", command=self.open_event_window)
        self.create_event_window_button.grid(row=2, column=2,columnspan=2, padx=10, pady=10)

        # list events button
        self.list_events_button = customtkinter.CTkButton(self, text="Wyświetl/Usuń wydarzenia", command=self.list_and_delete_events)
        self.list_events_button.grid(row=3, column=2,columnspan=2, padx=10, pady=10)

        # schedule recording button
        self.schedule_recording_button = customtkinter.CTkButton(self, text="Zaplanowanie nagrywania", command=self.open_schedule_recording_window)
        self.schedule_recording_button.grid(row=4, column=2,columnspan=2, padx=10, pady=10)

    def toggle_start_stop(self):
        if self.start_button.cget("text") == "Start":
            project_path = self.find_project_root()

            if project_path is None:
                print("Nie znaleziono katalogu projektu!")
                return

            database_path = os.path.join(project_path, "Database")

            if not os.path.exists(database_path):
                os.makedirs(database_path)
                print(f"Folder utworzony w: {database_path}")

            # Make a timestamped meeting folder
            timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
            self.current_meeting_folder = os.path.join(database_path,f"Spotkanie_{timestamp}")

            # Create meeting folder
            if not os.path.exists(self.current_meeting_folder):
                os.makedirs(self.current_meeting_folder)
                print(f"📁 Created folder: {self.current_meeting_folder}")

            self.start_button.configure(text="Stop", fg_color="red", hover_color="darkred")
            self.records_thread = start_recording()
            self.stop_screenshot.clear()
            self.screenshot_thread = threading.Thread(target=self.capture_screenshots, args=(self.platforma_optionmenu.get(),))
            self.screenshot_thread.start()


        else:
            self.start_button.configure(text="Start", fg_color="green", hover_color="darkgreen")
            stop_recording_threads(self.records_thread)
            self.stop_screenshot.set()
            self.screenshot_thread.join()

            # Move audio_file.wav to Dataabse folder 
            merged_audio_path = os.path.join(self.current_meeting_folder, "audio_file.wav")
            shutil.move("audio_file.wav", merged_audio_path)
            print(f"Audio file moved to: {merged_audio_path}")

            transcription_file = os.path.join(self.current_meeting_folder, "transcription.txt")
            summary_file = os.path.join(self.current_meeting_folder, "summary.txt")

            language_map = {
                "Polski": "pl",
                "English": "en",
                "Espanol": "es",
                "Francais": "fr",
                "Deutsch": "de"

            }
            language = language_map.get(self.jezyk_optionmenu.get())  # Change based on user selection if necessary

            print(f"🎤 Processing audio for transcription & summary in: {self.current_meeting_folder}")
            # Process and save transcription + summary in the meeting folder
            recorded_file = merged_audio_path
            process_audio_file(recorded_file, language, transcription_file, summary_file)

            print(f"✅ Transcription & summary saved in: {self.current_meeting_folder}")

    def capture_screenshots(self, app_name):
        ctypes.windll.user32.SetProcessDPIAware()
        monitor_area = get_monitor_area(app_name)
        
        if monitor_area is None:
            print("Unable to find the application window. Exiting.")
            return

        previous_image = None

        while not self.stop_screenshot.is_set():
            current_image = take_screenshot(monitor_area)
            
            if previous_image is not None:
                similarity = calculate_similarity_ssim(previous_image, current_image)
                print(f"SSIM Similarity: {similarity:.2f}")

                if similarity > 0.9:
                    print("Screenshots are similar. Skipping save.")
                    time.sleep(5)
                    continue

            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = os.path.join(self.current_meeting_folder, f"screenshot_{current_time}.png")
            current_image.save(file_name)
            print(f"Screenshot saved as {file_name}")

            previous_image = current_image
            time.sleep(5)    
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self, value=None):
        if value:
            print(f"Wybrano opcję: {value}")
        else:
            print("sidebar_button click")

    def find_project_root(self,project_name="software-engineering-project"):
        current_path = os.path.abspath(__file__)  # Pobiera pełną ścieżkę do skryptu
        while True:
            if os.path.basename(current_path) == project_name:
                return current_path
            parent = os.path.dirname(current_path)
            if parent == current_path:  # Dotarliśmy do głównego katalogu systemowego
                return None
            current_path = parent  # Przechodzimy do folderu wyżej


    def open_folder(self):
        project_path = self.find_project_root()
        
        if project_path is None:
            print("Nie znaleziono katalogu projektu!")
            return
        
        database_path = os.path.join(project_path, "Database")

        if not os.path.exists(database_path):
            os.makedirs(database_path)
            print(f"Folder utworzony w: {database_path}")

        os.startfile(database_path)

    def list_and_delete_events(self):

        user_email = self.email_entry.get().strip()

        if not user_email:
            print("Proszę podać adres e-mail.")
            return
        
        if not user_email.endswith("@gmail.com"):
            print("Nieprawidłowy adres e-mail.")
            return

        events = list_google_calendar_events(user_email)

        if not events:
            print("Brak wydarzeń do wyświetlenia.")
            return
        
        self.email_entry.configure(state="disabled")

        # Events window
        self.events_window = customtkinter.CTkToplevel(self)
        self.events_window.title("Lista wydarzeń i usuwanie")
        self.events_window.geometry(f"{600}x{500}")
        self.events_window.resizable(False, False)
        self.events_window.attributes("-topmost", True)

        def on_close_event_window():
            self.email_entry.configure(state="normal")
            self.events_window.destroy()

        self.events_window.protocol("WM_DELETE_WINDOW", on_close_event_window)

        # Event list
        self.events_list_label = customtkinter.CTkLabel(self.events_window, text="Wydarzenia:", anchor="w")
        self.events_list_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.events_textbox = customtkinter.CTkTextbox(self.events_window, width=500, height=300)
        self.events_textbox.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        self.event_id_mapping = {}

        # Texbox with events
        for idx, event in enumerate(events, start=1):
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            self.events_textbox.insert("end", f"{idx}. {event['summary']} (Start: {start_time})\n")
            self.event_id_mapping[str(idx)] = event['id']

        self.events_textbox.configure(state="disabled")

        # Delete event input fields
        self.event_number_label = customtkinter.CTkLabel(self.events_window, text="Numer wydarzenia do usunięcia:", anchor="w")
        self.event_number_label.grid(row=2, column=0, padx=20, pady=(20, 5))

        self.event_number_entry = customtkinter.CTkEntry(self.events_window, width=300)
        self.event_number_entry.grid(row=2, column=1, padx=20, pady=(20, 5))

        # Button to delete event
        self.delete_event_button = customtkinter.CTkButton(
            self.events_window,
            text="Usuń wydarzenie",
            command=self.delete_event_by_number
        )
        self.delete_event_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def delete_event_by_number(self):
        event_number = self.event_number_entry.get().strip()

        if not event_number.isdigit() or event_number not in self.event_id_mapping:
            print("Nieprawidłowy numer wydarzenia.")
            return

        event_id = self.event_id_mapping[event_number]
        user_email = self.email_entry.get().strip()

        if not user_email:
            print("Proszę podać adres e-mail.")
            return
        if not user_email.endswith("@gmail.com"):
            print("Nieprawidłowy adres e-mail.")
            return

        success = delete_google_calendar_event(event_id, user_email)
        if success:
            print(f"Wydarzenie zostało usunięte.")
            self.events_window.destroy()
        else:
            print(f"Nie udało się usunąć wydarzenia.")

    def open_event_window(self):

        if not self.email_entry.get().strip():
            print("Proszę podać adres e-mail.")
            return
        if not self.email_entry.get().strip().endswith("@gmail.com"):
            print("Nieprawidłowy adres e-mail.")
            return

        self.email_entry.configure(state="disabled")


        # Create a new top-level window
        self.event_window = customtkinter.CTkToplevel(self)
        self.event_window.title("Nowe wydarzenie")
        self.event_window.geometry(f"{700}x{300}")
        self.event_window.resizable(False, False)
        self.event_window.attributes("-topmost", True)

        def on_close_event_window():
            self.email_entry.configure(state="normal")
            self.event_window.destroy()

        self.event_window.protocol("WM_DELETE_WINDOW", on_close_event_window)

        # Calendar event input fields
        self.event_title_label = customtkinter.CTkLabel(self.event_window, text="Tytuł wydarzenia:", anchor="w")
        self.event_title_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.event_title_entry = customtkinter.CTkEntry(self.event_window, width=300)
        self.event_title_entry.grid(row=0, column=1, padx=20, pady=(20, 5))

        self.event_description_label = customtkinter.CTkLabel(self.event_window, text="Opis wydarzenia:", anchor="w")
        self.event_description_label.grid(row=1, column=0, padx=20, pady=5)
        self.event_description_entry = customtkinter.CTkEntry(self.event_window, width=300)
        self.event_description_entry.grid(row=1, column=1, padx=20, pady=5)

        self.event_location_label = customtkinter.CTkLabel(self.event_window, text="Lokalizacja:", anchor="w")
        self.event_location_label.grid(row=2, column=0, padx=20, pady=5)
        self.event_location_entry = customtkinter.CTkEntry(self.event_window, width=300)
        self.event_location_entry.grid(row=2, column=1, padx=20, pady=5)

        self.start_time_label = customtkinter.CTkLabel(self.event_window, text="Data i czas rozpoczęcia (YYYY-MM-DD HH:MM):", anchor="w")
        self.start_time_label.grid(row=3, column=0, padx=20, pady=5)
        self.start_time_entry = customtkinter.CTkEntry(self.event_window, width=300)
        self.start_time_entry.grid(row=3, column=1, padx=20, pady=5)

        self.end_time_label = customtkinter.CTkLabel(self.event_window, text="Data i czas zakończenia (YYYY-MM-DD HH:MM):", anchor="w")
        self.end_time_label.grid(row=4, column=0, padx=20, pady=5)
        self.end_time_entry = customtkinter.CTkEntry(self.event_window, width=300)
        self.end_time_entry.grid(row=4, column=1, padx=20, pady=5)

        # Button to create event
        self.create_event_button = customtkinter.CTkButton(self.event_window, text="Utwórz wydarzenie", command=self.create_event)
        self.create_event_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

    def create_event(self):
        title = self.event_title_entry.get()
        description = self.event_description_entry.get()
        location = self.event_location_entry.get()
        start_time_str = self.start_time_entry.get()
        end_time_str = self.end_time_entry.get()
        calendar_email = self.email_entry.get().strip()

        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Błędny format daty lub godziny. Użyj formatu: YYYY-MM-DD HH:MM")
            return
        
        event_data = {
            "summary": title,
            "description": description,
            "location": location,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }

        user_email = calendar_email
        event_link = create_google_calendar_event(event_data,user_email ,calendar_id=calendar_email)

        if event_link:
            print(f"Wydarzenie zostało utworzone: {event_link}")
            self.email_entry.configure(state="normal")
            self.event_window.destroy()
        else:
            print("Nie udało się utworzyć wydarzenia.")

    def open_schedule_recording_window(self):
        user_email = self.email_entry.get().strip()

        if not user_email:
            print("Proszę podać adres e-mail.")
            return
        
        if not user_email.endswith("@gmail.com"):
            print("Nieprawidłowy adres e-mail.")
            return

        events = list_google_calendar_events(user_email)

        if not events:
            print("Brak wydarzeń do wyświetlenia.")
            return

        self.email_entry.configure(state="disabled")

        # Schedule recording window
        self.schedule_window = customtkinter.CTkToplevel(self)
        self.schedule_window.title("Zaplanowanie nagrywania")
        self.schedule_window.geometry(f"{600}x{500}")
        self.schedule_window.resizable(False, False)
        self.schedule_window.attributes("-topmost", True)

        def on_close_schedule_window():
            self.email_entry.configure(state="normal")
            self.schedule_window.destroy()

        self.schedule_window.protocol("WM_DELETE_WINDOW", on_close_schedule_window)

        self.schedule_list_label = customtkinter.CTkLabel(self.schedule_window, text="Wydarzenia:", anchor="w")
        self.schedule_list_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.schedule_textbox = customtkinter.CTkTextbox(self.schedule_window, width=500, height=300)
        self.schedule_textbox.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        self.schedule_event_mapping = {}

        for idx, event in enumerate(events, start=1):
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            self.schedule_textbox.insert("end", f"{idx}. {event['summary']} (Start: {start_time})\n")
            self.schedule_event_mapping[str(idx)] = event

        self.schedule_textbox.configure(state="disabled")

        self.schedule_event_number_label = customtkinter.CTkLabel(self.schedule_window, text="Numer wydarzenia do zaplanowania:", anchor="w")
        self.schedule_event_number_label.grid(row=2, column=0, padx=20, pady=(20, 5))

        self.schedule_event_number_entry = customtkinter.CTkEntry(self.schedule_window, width=300)
        self.schedule_event_number_entry.grid(row=2, column=1, padx=20, pady=(20, 5))

        self.set_schedule_button = customtkinter.CTkButton(
            self.schedule_window,
            text="Zaplanuj nagrywanie",
            command=self.set_recording_schedule
        )
        self.set_schedule_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def set_recording_schedule(self):
        selected_event_number = self.schedule_event_number_entry.get().strip()

        if not selected_event_number.isdigit() or selected_event_number not in self.schedule_event_mapping:
            print("Nieprawidłowy numer wydarzenia.")
            return

        event = self.schedule_event_mapping[selected_event_number]
        user_email = self.email_entry.get().strip()

        if not user_email:
            print("Proszę podać adres e-mail.")
            return
        if not user_email.endswith("@gmail.com"):
            print("Nieprawidłowy adres e-mail.")
            return

        event_start_time = event['start'].get('dateTime', event['start'].get('date'))
        event_start_time = datetime.fromisoformat(event_start_time)

        event_start_time = event_start_time.replace(tzinfo=None)
        time_diff = event_start_time - datetime.now()

        if time_diff.total_seconds() > 0:
            print(f"Nagrywanie zaplanowane na rozpoczęcie o {event_start_time}")
            self.after(int(time_diff.total_seconds() * 1000), self.toggle_start_stop)

            self.schedule_window.destroy()
        else:
            print("Wydarzenie już się rozpoczęło!")



if __name__ == "__main__":
    app = App()
    app.mainloop()