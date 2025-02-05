# software-engineering-project

## Jak uruchomić projekt

1. **Sklonowanie repozytorium**:
    ```bash
    git clone https://github.com/tymoteush13/software-engineering-project.git
    ```

2. **Zainstalowanie Pythona**:
    - Wersja Pythona musi być niższa niż 3.13.

3. **Uruchomienie środowiska wirtualnego**:
    ```bash
    python -m venv venv
    ```

4. **Aktywacja środowiska wirtualnego w katalogu projektu**:
    - **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```
    - **MacOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

5. **Instalacja niezbędnych pakietów**:
    ```bash
    pip install -r .\requirements.txt
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

6. **Uruchomienie aplikacji**:
    ```bash
    python app.py
    ```

## Konfiguracja urządzeń audio w systemie Windows

Aby aplikacja poprawnie działała z dźwiękiem, upewnij się, że odpowiednie urządzenia audio są ustawione jako domyślne.

### Instrukcja

1.Otwórz Panel sterowania → Dźwięk.

2. Przejdź do zakładki Odtwarzanie i wybierz urządzenie, które chcesz używać (np. słuchawki, głośniki). Kliknij Ustaw jako domyślne.

3. Przejdź do zakładki Nagrywanie i wykonaj ten sam krok dla mikrofonu, jeśli aplikacja go wymaga.

4. Zapisz zmiany, klikając OK.

Teraz aplikacja będzie korzystać z wybranych urządzeń audio.

    
## Jak połączyć aplikację z kalendarzem Google

1. **Zaloguj się lub utwórz konto Google**:
    - Jeśli jeszcze nie masz konta Google, utwórz je na [stronie rejestracji Google](https://accounts.google.com/signup).
    - Jeśli masz konto, po prostu się zaloguj.

2. **Prześlij adres e-mail do administratora**:
    - Wyślij swój adres e-mail na adres wskazany przez administratora, aby otrzymać dostęp do kalendarza.

3. **Stwórz plik `credentials.json`**:
    - Administrator wygeneruje dla Ciebie dane dostępowe do konta Google i prześle je w postaci pliku `credentials.json`. Umieść ten plik w głównym katalogu projektu.
    - Plik `credentials.json` zawiera dane uwierzytelniające, które pozwalają aplikacji na dostęp do Twojego kalendarza Google.

