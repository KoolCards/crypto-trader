# python data/fetch_eth_history_cc.py
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd
import requests

API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")  # get one free at cryptocompare.com
PARQUET_PATH = Path(__file__).resolve().parent / "ethereum_price.parquet"
URL = "https://min-api.cryptocompare.com/data/v2/histoday"
SYMBOL, VS = "ETH", "USD"
MAX_LIMIT = 2000  # max per call

def fetch_batch(to_ts: int | None) -> pd.DataFrame:
    params = {
        "fsym": SYMBOL,
        "tsym": VS,
        "limit": MAX_LIMIT,
        "toTs": to_ts,
        "api_key": API_KEY,
    }
    resp = requests.get(URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()["Data"]["Data"]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.date
    df = df.loc[:, ["date", "close"]].rename(columns={"close": "price"})
    return df

def fetch_all() -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    to_ts = int(datetime.now(tz=timezone.utc).timestamp())
    for i in range(2):
        batch = fetch_batch(to_ts)
        frames.append(batch)
        if len(batch) < MAX_LIMIT:
            break
        # go one day before the earliest in this batch
        to_ts = int(batch["date"].min().strftime("%s")) - 86400
    df = pd.concat(frames, ignore_index=True)
    return df.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)

def merge_and_save(new_df: pd.DataFrame) -> None:
    if PARQUET_PATH.exists():
        try:
            existing = pd.read_parquet(PARQUET_PATH)
            existing["date"] = pd.to_datetime(existing["date"]).dt.date
        except Exception:
            existing = pd.DataFrame(columns=["date", "price"])
    else:
        existing = pd.DataFrame(columns=["date", "price"])

    combined = (
        pd.concat([existing, new_df], ignore_index=True)
        .drop_duplicates(subset=["date"], keep="last")
        .sort_values("date")
        .reset_index(drop=True)
    )
    combined.to_parquet(PARQUET_PATH, index=False)
    print(f"Wrote {len(combined)} rows to {PARQUET_PATH}")

if __name__ == "__main__":
    df = fetch_all()
    df = df[df['price'] > 0]
    print(f"Fetched {len(df)} daily rows from CryptoCompare")
    merge_and_save(df)
