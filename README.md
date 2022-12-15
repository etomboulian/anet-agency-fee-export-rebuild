# anet-agency-fee-export-rebuild

1. Create the .env file with the following params

```
DB_SERVER=127.0.0.1
DB_PORT=1434
DB_NAME=ljsupport12
DB_USER=evan
DB_PASSWORD=evan

SMTP_SERVER=smtp.test.com
SMTP_PORT=25
SMTP_SENDER_EMAIL=test@active.com
SMTP_SENDER_PASSWORD=abc123
SMTP_TARGET_EMAIL=test@example.ca

OUTPUT_PATH=output
```

2. python -m venv .venv
3. pip install -r requirements.txt
4. python main.py
