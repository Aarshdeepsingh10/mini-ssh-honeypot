@'
# Mini SSH Honeypot

A small, educational SSH honeypot written in Python using Paramiko.  
**Purpose:** capture authentication attempts and basic commands in a safe lab VM to learn attacker TTPs.

## Safe usage
- Run the honeypot **only** in an isolated VM or private lab network.
- **Do not** expose this to the public Internet without taking precautions.
- Keep captured logs private and delete or sanitize before sharing.

## Contents
- `honeypot.py` — the honeypot server
- `parse_logs.py` — converts `honeypot.log` to CSV and prints basic stats
- `.gitignore` — prevents logs/keys from being pushed

## How to run (basic)
1. Create a Python venv: `python -m venv venv && .\venv\Scripts\Activate`
2. Install deps: `pip install -r requirements.txt`
3. Start: `python honeypot.py 0.0.0.0 2222`

## License
MIT
'@ > README.md
