# Loliland AutoVote Bot 🤖🗳️  

A Python bot for automatic voting on loliland.ru with smart cooldown management and random delays.  

## Features ✨  

- Multiple account support 👥 - Vote from multiple accounts sequentially  
- Smart cooldown system ⏳ - Parses exact wait time from error responses  
- Random delays 🎲 - Configurable random intervals between votes  
- Persistent logging 📝 - Detailed logs in both console and file  
- 24/7 operation 🌙☀️ - Automatically resumes when voting becomes available  

## Installation 🛠️  

1. Clone the repository 
```
git clone https://github.com/helldoodle-dev/loliland-autovote-new.git
cd loliland-autovote-new
```

2. Install dependencies 
```
pip install requests
```

3. Create config file  
Create `config.json` (see Configuration section below)

4. Run the bot `python main.py`

## Configuration ⚙️  

Create `config.json` with following structure:  
```
{
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "min_delay": 5,
    "max_delay": 15,
    "accounts": [
        {
            "name": "account1",
            "access_id": "01812ef3-1092-7ceb-81b2-4791564aab5f",
            "access_token": "95ffaa952dbad379bf60711cf88682b389..."
        },
        {
            "name": "account2",
            "access_id": "01812ef3-1092-7ceb-81b2-47911564aab5f",
            "access_token": "95ffaa952dbad379bf60711cf881682b389..."
        }
    ]
}
```

### Config Options:  

- `user-agent`: Browser user agent string  
- `min_delay`: Minimum delay between votes (seconds)  
- `max_delay`: Maximum delay between votes (seconds)  
- `accounts`: Array of account objects with:  
  - `name`: Account nickname  
  - `access_id`: Account access ID  
  - `access_token`: Account access token  

## Logging 📋  

The bot creates vote.log with all activities:  
```
[2025-04-25 20:50:06] [INFO] Configuration loaded successfully
[2025-04-25 20:50:06] [INFO] Accounts found: 2
[2025-04-25 20:50:06] [INFO] account1 | Success! Response: {'payout': {'coinAmount': 46}}
[2025-04-25 20:50:06] [INFO] Waiting 8.3 seconds...
[2025-04-25 20:50:06] [INFO] account2 | Waiting required: 23:37:28
```

## Important Notes ⚠️  

- Use responsibly and respect website rules  
- Don't share your access tokens  
- The bot may stop working if website API changes  

---

## Support 💬  

For questions or issues, please [open an issue](https://github.com/helldoodle-dev/loliland-autovote-new/issues).  

Happy voting! 🎉
