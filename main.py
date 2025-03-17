from decimal import Decimal
from fastapi import FastAPI, HTTPException, Depends
import schedule
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from BASE.database import engine, Base, get_db
from BASE.config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN_KEY, FETCH_TIME
from models import Target, PriceHistory
from routers import site
import time
from contextlib import asynccontextmanager
import threading
from sqlalchemy.orm import Session
import telepot
import asyncio

app = FastAPI(title="FastAPI with MySQL & SQLAlchemy")


Base.metadata.create_all(bind=engine)


app.include_router(site.router)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

def send_telegram_message(message):
    bot = telepot.Bot(TELEGRAM_TOKEN_KEY)
    bot.sendMessage(TELEGRAM_CHAT_ID, message)

async def fetch_prices(db: Session):
    targets = db.query(Target).all()
    for target in targets:
        url = target.url
        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")

            price_element = soup.find("h4", class_="finalPrice")
            if price_element:
                price = Decimal(str(float(price_element.text.strip().replace("R$", "").replace(".", "").replace(",", "."))))
                
                price_history = db.query(PriceHistory)
                last_price = price_history.filter(PriceHistory.target_id == target.id).order_by(PriceHistory.price_date.desc(), PriceHistory.id.desc()).first()
                lowest_price = price_history.order_by(PriceHistory.price.asc()).first()

                if last_price:
                    if price < last_price.price:
                        message = f"🔥 Price Drop Alert! {target.title} is now R$ {price}!\nCheck here: {url}"
                        send_telegram_message(message)
                
                new_price = PriceHistory(
                    target_id=target.id,
                    price_date=datetime.now().date(),
                    price=price
                )
                db.add(new_price)
                db.commit()
        except Exception as e:
            print(f"Error fetching price for {url}: {e}")



async def async_fetch_prices():
    with Session(engine) as db:
        await fetch_prices(db)

def sync_fetch_prices():
    asyncio.run(async_fetch_prices())

# ✅ Correct way to schedule the function
schedule.every().day.at(FETCH_TIME).do(sync_fetch_prices)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait 1 minute before checking again

def start_scheduler():
    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()

# Start the scheduler when FastAPI app starts
@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get('/')
def ping():
    return {"msg": "Pong"}

@app.get("/targets/")
async def get_targets(db: Session = Depends(get_db)):
    await fetch_prices(db)
    return {"message": "fetch_prices executed successfully"}

