import requests
import time
import json
import logging
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

class AutoVote:
    def __init__(self, config_path="config.json"):
        self.api_url = "https://loliland.ru/apiv2/bonus/give"
        self.config_path = Path(config_path)
        self.config = None
        self.session = requests.Session()
        self.next_vote_time = {}
        
        self._init_logger()

    def _init_logger(self):
        self.logger = logging.getLogger('AutoVote')
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        file_handler = logging.FileHandler('vote.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                self.config = json.load(file)
            self.logger.info("Configuration loaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Config loading error: {e}")
            return False

    def _get_random_delay(self):
        min_delay = self.config.get("min_delay", 5)
        max_delay = self.config.get("max_delay", 15)
        return random.uniform(min_delay, max_delay)

    def _parse_wait_time(self, error_message):
        pattern = r"(\d+) часа (\d+) минут (\d+) секунд"
        match = re.search(pattern, error_message)
        
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return None

    def send_vote(self, account: dict):
        account_id = account.get("access_id")
        account_name = account.get("name", account_id[:6] + "...")

        if account_id in self.next_vote_time and datetime.now() < self.next_vote_time[account_id]:
            wait_time = self.next_vote_time[account_id] - datetime.now()
            self.logger.info(f"{account_name} | Next vote available in {wait_time}")
            return False

        headers = {
            "User-Agent": self.config.get("user-agent", ""),
            "accept": "*/*",
            "accept-language": "ru",
            "access-id": account_id,
            "access-token": account.get("access_token"),
            "Referer": "https://loliland.ru/ru/cabinet/bonus",
        }

        try:
            response = self.session.post(
                self.api_url,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.next_vote_time[account_id] = datetime.now() + timedelta(hours=24)
                self.logger.info(f"{account_name} | Success! Response: {response.json()}")
                return True
            elif response.status_code == 403:
                try:
                    error_data = response.json()
                    if error_data.get("error_code") == -9:
                        wait_time = self._parse_wait_time(error_data["details"]["description"])
                        if wait_time:
                            self.next_vote_time[account_id] = datetime.now() + wait_time
                            self.logger.info(f"{account_name} | Waiting required: {wait_time}")
                        else:
                            self.next_vote_time[account_id] = datetime.now() + timedelta(hours=24)
                except:
                    self.next_vote_time[account_id] = datetime.now() + timedelta(hours=24)
                
                self.logger.warning(f"{account_name} | Error: {response.text}")
                return False
            else:
                self.logger.warning(f"{account_name} | HTTP Error {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{account_name} | Request error: {str(e)}")
            return False

    def run(self):
        if not self.load_config():
            return

        accounts = self.config.get("accounts", [])
        self.logger.info(f"Accounts found: {len(accounts)}")
        
        while True:
            for account in accounts:
                self.send_vote(account)
                delay = self._get_random_delay()
                self.logger.info(f"Waiting {delay:.1f} seconds...")
                time.sleep(delay)
            
            if self.next_vote_time:
                next_vote = min(self.next_vote_time.values())
                now = datetime.now()
                
                if next_vote > now:
                    wait_seconds = (next_vote - now).total_seconds()
                    self.logger.info(f"All accounts voted. Waiting {wait_seconds/3600:.2f} hours...")
                    time.sleep(wait_seconds)
                else:
                    self.logger.info("Continuing voting cycle")
            else:
                self.logger.info("No voting time data available. Continuing...")

if __name__ == "__main__":
    voter = AutoVote()
    voter.run()