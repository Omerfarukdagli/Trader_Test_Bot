import random

import pandas as pd
from binance import Client
from config import client, _incelenecek_mum_sayisi, _intervals_c, _required_columns, _data_c, min_volume_c
import logging

# Global değişkenler



# Logging ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_all_symbols(min_volume=min_volume_c):
    """
    Binance Futures'taki tüm USDT çiftlerini getirir ve minimum hacme göre filtreler.
    """
    try:
        # Binance API'den sembol bilgisi al
        tickers = client.futures_ticker()
        usdt_symbols = []

        for ticker in tickers:
            if ticker['symbol'].endswith('USDT') and float(ticker['quoteVolume']) > min_volume:
                usdt_symbols.append(ticker['symbol'])

        usdt_symbols = sorted(usdt_symbols, key=lambda x: float(client.futures_ticker(symbol=x)['quoteVolume']), reverse=True)
        random.shuffle(usdt_symbols)
        logging.info(f"Fetched {len(usdt_symbols)} symbols with minimum volume {min_volume}.")
        return usdt_symbols
    except Exception as e:
        logging.error(f"Error fetching symbols: {e}")
        return []

def gpt__fetch_all_symbols():
    """
    Binance Futures'taki tüm USDT çiftlerini getirir.
    """
    try:
        exchange_info = client.futures_exchange_info()
        usdt_symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['symbol'].endswith('USDT')]
        logging.info(f"Fetched {len(usdt_symbols)} symbols.")
        return usdt_symbols
    except Exception as e:
        logging.error(f"Error fetching symbols: {e}")
        return []

def fetch_historical_data(symbol, intervals=_intervals_c, limit=_incelenecek_mum_sayisi):
    """Belirli bir sembol için farklı zaman dilimlerinden geçmiş verileri getirir."""
    all_data = {}
    try:
        for interval in intervals:
            klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
            data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                                 'close_time', 'quote_asset_volume', 'number_of_trades',
                                                 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
                                                 'ignore'])
            # Gerekli sütunları kontrol edin
            required_columns = _required_columns
            if not all(col in data.columns for col in required_columns):
                logging.error(f"Missing required columns in data for {symbol} with interval {interval}.")
                continue

            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            data = data[_data_c].astype(float)
            all_data[interval] = data

        return all_data
    except Exception as e:
        logging.error(f"Error fetching historical data for {symbol}: {e}")
        return None

def merge_timeframes(data_dict):
    """
    Farklı zaman dilimlerinden gelen verileri birleştirir.
    :param data_dict: {'1m': DataFrame, '15m': DataFrame, '4h': DataFrame}
    :return: Birleştirilmiş DataFrame
    """
    try:
        merged = None
        for interval, data in data_dict.items():
            if data is None or data.empty:
                logging.warning(f"Data for interval {interval} is missing or empty. Skipping...")
                continue

            # Debug: Her interval için orijinal DataFrame'in boyutunu loglayın.

            # Sütun isimlerine interval suffix ekleyin
            data_with_suffix = data.add_suffix(f"_{interval}")


            if merged is None:
                merged = data_with_suffix

            else:
                merged = merged.join(data_with_suffix, how="outer")


        if merged is not None:
            # Önce ileri doldurma (ffill) uygulayıp, ardından NaN içeren satırları kaldırıyoruz
            merged_filled = merged.ffill().dropna(thresh=int(merged.shape[1] * 1))

            return merged_filled
        else:
            logging.error("No valid data to merge.")
            return None
    except Exception as e:
        logging.error(f"Error merging timeframes: {e}")
        return None


def fetch_data_and_add_indicators(symbol):
    """Sembol için geçmiş verileri alır ve teknik indikatörleri ekler."""
    from indicators import add_indicators  # İndikatör fonksiyonlarını içeren modül

    try:
        data = fetch_historical_data(symbol)
        if data is not None:
            data_with_indicators = {}
            for interval, df in data.items():
                if df is not None:
                    data_with_indicators[interval] = add_indicators(df)
            logging.info(f"Added indicators for {symbol}.")
            return data_with_indicators
        else:
            logging.warning(f"No data to process for {symbol}.")
            return None
    except Exception as e:
        logging.error(f"Error adding indicators for {symbol}: {e}")
        return None


import requests


def fetch_bitcoin_dominance_coingecko():
    """
    CoinGecko API'den Bitcoin Dominance değerini çeker.
    """
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url)

        # Yanıtı JSON formatında çözümle
        data = response.json()

        # Yanıtı ekrana yazdırarak içeriği kontrol edelim
        print("CoinGecko Yanıtı:", data)

        # 'data' anahtarını kontrol edelim
        if "data" in data and "market_cap_percentage" in data["data"] and "btc" in data["data"][
            "market_cap_percentage"]:
            btc_dominance = data["data"]["market_cap_percentage"]["btc"]
            return btc_dominance
        else:
            print("Hata: CoinGecko yanıtında beklenen veri bulunamadı.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"CoinGecko API isteğinde hata oluştu: {e}")
        return None
    except Exception as e:
        print(f"Genel hata: {e}")
        return None


# Örnek kullanım
if __name__ == "__main__":
    symbols = fetch_all_symbols()
    if symbols:
        symbol = symbols[0]  # İlk sembolü seç
        data_with_indicators = fetch_data_and_add_indicators(symbol)
        if data_with_indicators is not None:
            merged_data = merge_timeframes(data_with_indicators)
            if merged_data is not None:
                print(merged_data.head())
            else:
                logging.error("Merged data is invalid or empty.")