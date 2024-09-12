import requests
import os
import urllib.parse
import json
from colorama import Fore, Style
from datetime import datetime
import time

class Agent301:
    def __init__(self, authorization) -> None:
        self.authorization = authorization.strip()
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Authorization': self.authorization,
            'Cache-Control': 'no-cache',
            'Host': 'api.agent301.org',
            'Origin': 'https://telegram.agent301.org',
            'Pragma': 'no-cache',
            'priority': 'u=1, i',
            'Referer': 'https://telegram.agent301.org/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Agent301 - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def load_data(self, auth):
        try:
            decoded_string = urllib.parse.unquote(auth)
            query_params = dict(urllib.parse.parse_qsl(decoded_string))
            user_data = json.loads(query_params.get('user', '{}'))
            username = user_data.get('username', 'unknown')

            if 'user' not in query_params:
                self.log(f"{Fore.YELLOW}Skipping: No 'user' parameter found in query.{Style.RESET_ALL}")
                return None
            
            return {
                'username': username,
                'authorization': auth
            }
        except (json.JSONDecodeError, KeyError, IndexError):
            self.log(f"{Fore.RED}Failed to parse query data.{Style.RESET_ALL}")
            return None
        
    def get_me(self):
        url = "https://api.agent301.org/getMe"
        headers = self.headers

        response = self.session.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get('result', {})
            else:
                self.log(f"{Fore.RED + Style.BRIGHT}Failed to retrieve user information.{Style.RESET_ALL}")
                return None
        else:
            self.log(
                f"{Fore.RED + Style.BRIGHT}HTTP ERROR: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{response.status_code}{Style.RESET_ALL}"
            )

            return None
        
    def get_tasks(self):
        url = "https://api.agent301.org/getTasks"
        headers = self.headers

        response = self.session.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get('result', {})
            else:
                self.log(f"{Fore.RED + Style.BRIGHT}Failed to retrieve user information.{Style.RESET_ALL}")
                return None
        else:
            self.log(
                f"{Fore.RED + Style.BRIGHT}HTTP ERROR: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{response.status_code}{Style.RESET_ALL}"
            )
            
            return None



    def complete_task(self, task_type, title):
        url = "https://api.agent301.org/completeTask"
        headers = self.headers
        data = {
            "type": task_type
        }

        response = self.session.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                result = data.get('result', {})
                is_completed = result.get('is_completed', False)
                reward = result.get('reward', 0)
                balance = result.get('balance', 0)

                if is_completed:
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{title} {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}completed!{Style.RESET_ALL}"
                    )
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{title} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}| {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Reward ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{reward} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}| {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ New Balance ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{balance}{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.YELLOW + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{title} {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}not yet completed{Style.RESET_ALL}"
                    )
                return is_completed
            else:
                self.log(
                    f"{Fore.RED + Style.BRIGHT}[ Task ] Failed to complete task {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                )
                return False
        else:
            self.log(
                f"{Fore.RED + Style.BRIGHT}HTTP ERROR: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{response.status_code}{Style.RESET_ALL}"
            )
            return False
        
    def load_wheel(self):
        url = "https://api.agent301.org/wheel/load"
        headers = self.headers

        response = self.session.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get('result', {})
            else:
                self.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to retrieve load wheel.{Style.RESET_ALL}")
                return None
        else:
            self.log(
                f"{Fore.RED + Style.BRIGHT}HTTP ERROR: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{response.status_code}{Style.RESET_ALL}"
            )
            return None
        
    def spin_wheel(self):
        url = "https://api.agent301.org/wheel/spin"
        headers = self.headers

        response = self.session.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                return data.get('result', {})
            else:
                self.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to retrieve spin wheel.{Style.RESET_ALL}")
                return None
        else:
            self.log(
                f"{Fore.RED + Style.BRIGHT}HTTP ERROR: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{response.status_code}{Style.RESET_ALL}"
            )
            return None

def main():
    try: 
        with open('query.txt', 'r') as file:
            authorizations = [line.strip() for line in file if line.strip()]

        if not authorizations:
            print(f"{Fore.RED + Style.BRIGHT}Warning: File 'query.txt' kosong. Harap isi dengan query data.{Style.RESET_ALL}")
            return
        
        while True:

            for auth in authorizations:
                auth = auth.strip()

                if auth:
                    client = Agent301(auth)

                    client.clear_terminal()
                    time.sleep(1)
                    client.welcome()

                    client.log(
                        f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}{len(authorizations)}{Style.RESET_ALL}"
                    )
                    client.log(f"{Fore.BLUE + Style.BRIGHT}--------------------------------------------------------{Style.RESET_ALL}")

                    data = client.load_data(auth)

                    if data:
                        client.log(
                            f"{Fore.GREEN + Style.BRIGHT}[ Username ] {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{data['username']}{Style.RESET_ALL}"
                        )

                    info = client.get_me()
                    if info:
                        balance = info.get("balance", 0)
                        tickets = info.get("tickets", 0)
                        daily_streak = info.get("daily_streak", {}).get("day", 0)

                        client.log(
                            f"{Fore.GREEN + Style.BRIGHT}[ Balance ] {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{balance}{Style.RESET_ALL}"
                        )
                        client.log(
                            f"{Fore.GREEN + Style.BRIGHT}[ Tickets ] {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{tickets}{Style.RESET_ALL}"
                        )
                        client.log(
                            f"{Fore.GREEN + Style.BRIGHT}[ Streak  ] {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{daily_streak}{Style.RESET_ALL}"
                        )

                    result = client.get_tasks()
                    if result:

                        tasks = result.get("data", [])
                        for task in tasks:
                            task_type = task.get("type")
                            title = task.get("title")
                            is_claimed = task.get("is_claimed", False)
                            count = task.get("count", 0)
                            max_count = task.get("max_count")

                            if max_count is None and not is_claimed:
                                client.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                                )
                                time.sleep(1)
                                client.complete_task(task_type, title)

                            elif task_type == "video" and count < max_count:
                                while count < max_count:
                                    client.log(
                                        f"{Fore.GREEN + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}[ Progress ]: {Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT}{count}{Style.RESET_ALL}"
                                        f"{Fore.CYAN + Style.BRIGHT}/{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT}{max_count}{Style.RESET_ALL}"
                                    )
                                    time.sleep(1)
                                    if client.complete_task(task_type, title):
                                        count += 1
                                    else:
                                        break

                            elif not is_claimed and count >= max_count:
                                client.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Task ] {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{task_type.upper()} {Style.RESET_ALL}"
                                    f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                                )
                                time.sleep(1)
                                client.complete_task(task_type, title)

                        while tickets > 0:
                            load = client.load_wheel()
                            
                            if load:
                                spin = client.spin_wheel()

                                if spin:
                                    reward = spin.get("reward", "N/A")
                                    toncoin = spin.get("toncoin", 0)
                                    notcoin = spin.get("notcoin", 0)
                                    current_balance = spin.get("balance", 0)
                                    current_ticket = spin.get("tickets", 0)

                                    client.log(f"{Fore.BLUE + Style.BRIGHT}[ Spin Wheel ] Mencoba melakukan spin wheel...{Style.RESET_ALL}")
                                    time.sleep(5)

                                    tickets = current_ticket

                                    if tickets > 0:
                                        client.log(
                                            f"{Fore.GREEN + Style.BRIGHT}[ Rewards ] {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}{reward}{Style.RESET_ALL}"
                                        )
                                        client.log(
                                            f"{Fore.GREEN + Style.BRIGHT}[   TON   ] {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}{toncoin}{Style.RESET_ALL}"
                                        )
                                        client.log(
                                            f"{Fore.GREEN + Style.BRIGHT}[   NOT   ] {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}{notcoin}{Style.RESET_ALL}"
                                        )
                                        client.log(
                                            f"{Fore.GREEN + Style.BRIGHT}[ Balance ] {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}{current_balance}{Style.RESET_ALL}"
                                        )
                                        client.log(
                                            f"{Fore.GREEN + Style.BRIGHT}[ Tickets ] {Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT}{current_ticket}{Style.RESET_ALL}"
                                        )
                                    else:
                                        client.log(f"{Fore.YELLOW + Style.BRIGHT}[ Spin Wheel ] Tidak ada ticket tersisa untuk melakukan spin wheel{Style.RESET_ALL}")
                                        break
                                else:
                                    client.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to spin the wheel.{Style.RESET_ALL}")
                                    break
                            else:
                                client.log(f"{Fore.RED + Style.BRIGHT}[ Spin Wheel ] Failed to load the wheel.{Style.RESET_ALL}")
                                break

                    client.log(f"{Fore.WHITE + Style.BRIGHT}----------------------------------------------{Style.RESET_ALL}")

                time.sleep(1)

            client.log(f"{Fore.YELLOW + Style.BRIGHT}Waiting for 1 hours before starting over...{Style.RESET_ALL}")
            time.sleep(3600)

    except KeyboardInterrupt:
        client.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Agent301 - BOT.{Style.RESET_ALL}")
    except Exception as e:
        client.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()