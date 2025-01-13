import customtkinter
import os
from integrate_with_calendar import create_google_calendar_event

from datetime import datetime
import pytz

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()


        self.title("App")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)


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

        # folder opening button
        self.open_folder_button = customtkinter.CTkButton(self, text="Otwórz Folder", command=self.open_folder)
        self.open_folder_button.grid(row=1, column=2, padx=20, pady=20)

        # create event window button
        self.create_event_window_button = customtkinter.CTkButton(self, text="Utwórz wydarzenie", command=self.open_event_window)
        self.create_event_window_button.grid(row=2, column=2, padx=20, pady=20)


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

    def open_event_window(self):
        # Create a new top-level window
        self.event_window = customtkinter.CTkToplevel(self)
        self.event_window.title("Nowe wydarzenie")
        self.event_window.geometry(f"{500}x400")
        self.event_window.resizable(False, False)

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
        self.create_event_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

    def create_event(self):
        title = self.event_title_entry.get()
        description = self.event_description_entry.get()
        location = self.event_location_entry.get()
        start_time_str = self.start_time_entry.get()
        end_time_str = self.end_time_entry.get()


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
            "end_time": end_time.isoformat()
        }

        event_link = create_google_calendar_event(event_data)
        if event_link:
            print(f"Wydarzenie zostało utworzone: {event_link}")
        else:
            print("Nie udało się utworzyć wydarzenia.")

if __name__ == "__main__":
    app = App()
    app.mainloop()