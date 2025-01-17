import customtkinter
import os
from integrate_with_calendar import create_google_calendar_event, list_google_calendar_events, delete_google_calendar_event
from record_audio import start_recording, stop_recording_threads

from datetime import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("App")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)
        self.events_window = None
        self.event_window = None
        
        self.records_thread = None


        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Ustawienia", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Max miejsce Label and OptionMenu
        self.max_miejsce_label = customtkinter.CTkLabel(self.sidebar_frame, text="Max miejsce:", anchor="w")
        self.max_miejsce_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.max_miejsce_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["2", "4", "6", "8", "10"], command=self.sidebar_button_event)
        self.max_miejsce_optionmenu.grid(row=2, column=0, padx=20, pady=10)
        
        # Jakość Label and OptionMenu
        self.jakosc_label = customtkinter.CTkLabel(self.sidebar_frame, text="Jakość nagrania:", anchor="w")
        self.jakosc_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.jakosc_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["360p", "720p", "1080p", "1440p"], command=self.sidebar_button_event)
        self.jakosc_optionmenu.grid(row=4, column=0, padx=20, pady=10)
        
        # Język Label and OptionMenu
        self.jezyk_label = customtkinter.CTkLabel(self.sidebar_frame, text="Język:", anchor="w")
        self.jezyk_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.jezyk_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Polski", "Angielski"], command=self.sidebar_button_event)
        self.jezyk_optionmenu.grid(row=6, column=0, padx=20, pady=10)

        # Appearance Mode Label and OptionMenu
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        
        # UI Scaling Label and OptionMenu
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # create buttons in the middle
        self.max_miejsce_optionmenu.set("6")
        self.jakosc_optionmenu.set("1080p")
        self.jezyk_optionmenu.set("Polski")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.start_button = customtkinter.CTkButton(self, text="Start", command=self.toggle_start_stop, fg_color="green", hover_color="darkgreen")
        self.start_button.grid(row=0, column=1, padx=10, pady=10)

        self.email_label = customtkinter.CTkLabel(self, text="Adres e-mail kalendarza:", anchor="w")
        self.email_label.grid(row=0, column=2, padx=(5, 0), pady=(5, 0))

        self.email_entry = customtkinter.CTkEntry(self, width=300)
        self.email_entry.grid(row=0, column=3, padx=(0, 5), pady=(5, 0))

        # folder opening button
        self.open_folder_button = customtkinter.CTkButton(self, text="Otwórz Folder", command=self.open_folder)
        self.open_folder_button.grid(row=1, column=3, padx=10, pady=10)

        # create event window button
        self.create_event_window_button = customtkinter.CTkButton(self, text="Utwórz wydarzenie", command=self.open_event_window)
        self.create_event_window_button.grid(row=2, column=3, padx=10, pady=10)

        # list events button
        self.list_events_button = customtkinter.CTkButton(self, text="Wyświetl/Usuń wydarzenia", command=self.list_and_delete_events)
        self.list_events_button.grid(row=3, column=3, padx=10, pady=10)

    def toggle_start_stop(self):
        if self.start_button.cget("text") == "Start":
            self.start_button.configure(text="Stop", fg_color="red", hover_color="darkred")
            self.records_thread = start_recording()
        else:
            self.start_button.configure(text="Start", fg_color="green", hover_color="darkgreen")
            stop_recording_threads(self.records_thread)

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

    def open_folder(self):
        folder_path = "C:/Users/Tymek/software-engineering-project/Database"
        os.startfile(folder_path)

    def list_and_delete_events(self):

        user_email = self.email_entry.get().strip()

        if not user_email:
            print("Proszę podać adres e-mail.")
            return

        events = list_google_calendar_events(user_email)

        if not events:
            print("Brak wydarzeń do wyświetlenia.")
            return

        # Events window
        self.events_window = customtkinter.CTkToplevel(self)
        self.events_window.title("Lista wydarzeń i usuwanie")
        self.events_window.geometry(f"{600}x{500}")
        self.events_window.resizable(False, False)
        self.events_window.attributes("-topmost", True)

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

        success = delete_google_calendar_event(event_id, user_email)
        if success:
            print(f"Wydarzenie zostało usunięte.")
            self.events_window.destroy()
        else:
            print(f"Nie udało się usunąć wydarzenia.")

    def open_event_window(self):
        # Create a new top-level window
        self.event_window = customtkinter.CTkToplevel(self)
        self.event_window.title("Nowe wydarzenie")
        self.event_window.geometry(f"{700}x{300}")
        self.event_window.resizable(False, False)
        self.event_window.attributes("-topmost", True)

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
            self.event_window.destroy()
        else:
            print("Nie udało się utworzyć wydarzenia.")

if __name__ == "__main__":
    app = App()
    app.mainloop()