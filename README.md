# Hardware Monitoring Bot (hw_bot)

This project is a Python/FastAPI application that monitors prices, saves them to a database, and alerts users via Telegram when prices drop by more than 10% from the last recorded value.

## Setup and Installation

### Prerequisites

To run this project, ensure you have the following installed:

- Python 3.13.1
- FastAPI 0.115.11
- MySQL or another compatible database

### Environment Variables

Before running the project, set the following environment variables:
```
  DATABASE_URL=your_database_url
  TELEGRAM_BOT_TOKEN=your_telegram_bot_token
  TELEGRAM_CHAT_ID=your_telegram_chat_id
  FETCH_TIME=your_prefered_price_fetch_time
```

## Installation

1. Clone the repository:
```
  git clone https://github.com/gabriel-torres3077/hw-bot.git
  cd hw-bot
```
2. Create a virtual environment and activate it:

```
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies

```
  pip install -r requirements.txt
```

## Running the Project

1. Start the FastAPI application:
```
  uvicorn app.main:app --reload
```

2. The API will be available at http://127.0.0.1:8000.

## Usage

The bot automatically fetches prices every morning at 08:00, you can update it to any time you want just by updating FETCH_TIME in the [environment variables](#environment-variables).

## To be implemented

- Variable price threshold before send message on telegram (next)
- Telegram bot function to add products
- Form to add/update products list
- Multiple chat integration (maybe)
- Price report

