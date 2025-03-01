import pandas as pd
import ta
import warnings
from ta.volatility import BollingerBands
import numpy as np

from config import _data_c

def add_indicators(data):
    """
    Add technical indicators to the data.
    :param data: DataFrame with OHLCV data
    :return: DataFrame with indicators
    """
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Gerekli sütunların mevcut olduğundan emin olun
    required_cols = _data_c
    if not all(col in data.columns for col in required_cols):
        raise ValueError("Eksik veri sütunları")

    try:
        # Relative Strength Index (RSI)
        data['rsi'] = ta.momentum.RSIIndicator(close=data['close'], window=14).rsi()

        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(close=data['close'], window_slow=26, window_fast=12, window_sign=9)
        data['macd'] = macd.macd()
        data['macd_signal'] = macd.macd_signal()

        # Exponential Moving Averages (Kısa Vadeli)
        data['ema_5'] = ta.trend.EMAIndicator(close=data['close'], window=8).ema_indicator()
        data['ema_10'] = ta.trend.EMAIndicator(close=data['close'], window=13).ema_indicator()
        data['ema'] = ta.trend.EMAIndicator(close=data['close'], window=21).ema_indicator()
        data['ema_20'] = ta.trend.EMAIndicator(close=data['close'], window=20).ema_indicator()

        # Bollinger Bands
        bb = BollingerBands(close=data['close'], window=20, window_dev=2)
        data['bb_middle'] = bb.bollinger_mavg()
        data['bb_high'] = bb.bollinger_hband()
        data['bb_low'] = bb.bollinger_lband()

        # Average Directional Index (ADX)
        adx_indicator = ta.trend.ADXIndicator(high=data['high'], low=data['low'], close=data['close'], window=14)
        data['adx'] = adx_indicator.adx()

        # DMI: +DI ve -DI hesaplamaları
        data['plus_di'] = adx_indicator.adx_pos()
        data['minus_di'] = adx_indicator.adx_neg()

        # Stochastic RSI
        stoch_rsi = ta.momentum.StochRSIIndicator(close=data['close'], window=14, smooth1=3, smooth2=3)
        data['stochastic_rsi'] = stoch_rsi.stochrsi()

        # Commodity Channel Index (CCI)
        data['cci'] = ta.trend.CCIIndicator(high=data['high'], low=data['low'], close=data['close'], window=20).cci()

        # On-Balance Volume (OBV)
        data['obv'] = ta.volume.OnBalanceVolumeIndicator(close=data['close'], volume=data['volume']).on_balance_volume()

        # Average True Range (ATR)
        data['atr'] = ta.volatility.AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=14).average_true_range()
        data['atr_30'] = ta.volatility.AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=30).average_true_range()
        data['atr_50'] = ta.volatility.AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=50).average_true_range()

        # Hacim ağırlıklı ATR
        period = 14
        high = data['high']
        low = data['low']
        close = data['close']

        tr = np.maximum.reduce([high - low, abs(high - close.shift()), abs(low - close.shift())])
        vw_tr = tr * (data['volume'] / 1_000_000)  # Volume milyon cinsinden
        data['vw_atr'] = vw_tr.rolling(window=period).mean()

        # Parabolic SAR
        data['parabolic_sar'] = ta.trend.PSARIndicator(high=data['high'], low=data['low'], close=data['close'], step=0.02, max_step=0.2).psar()

        # Momentum (MOM)
        data['momentum'] = data['close'] - data['close'].shift(10)

        # Rate of Change (ROC)
        data['roc'] = ((data['close'] - data['close'].shift(12)) / data['close'].shift(12)) * 100

        # Volume Weighted Average Price (VWAP)
        data['vwap'] = (data['volume'] * (data['high'] + data['low'] + data['close']) / 3).cumsum() / data['volume'].cumsum()

        # Money Flow Index (MFI)
        data['mfi'] = ta.volume.MFIIndicator(
            high=data['high'], low=data['low'], close=data['close'], volume=data['volume'], window=14
        ).money_flow_index()

        # VWAP Deviation
        data['vwap_deviation'] = data['close'] - data['vwap']

        # Choppiness Index (CHOP)
        data['chop'] = (data['high'] - data['low']).rolling(window=14).mean() / (
            data['close'] - data['open']).rolling(window=14).mean()

        # Volume Oscillator (VO)
        short_window = 5
        long_window = 14
        data['volume_oscillator'] = data['volume'].rolling(window=short_window).mean() - data['volume'].rolling(window=long_window).mean()

        # EK: Ek Hacim/Likidite Göstergesi (örneğin, volume ratio)
        data['volume_ratio'] = data['volume'] / data['volume'].rolling(window=5).mean()

        # Williams %R
        data['williams_r'] = ta.momentum.WilliamsRIndicator(
            high=data['high'], low=data['low'], close=data['close'], lbp=14
        ).williams_r()

        # Stochastic Oscillator
        so = ta.momentum.StochasticOscillator(data["high"], data["low"], data["close"])
        data["stochastic_oscillator"] = so.stoch()

        # Eğimsellikler (Slope)
        data['rsi_slope'] = data['rsi'].diff()
        data['macd_slope'] = data['macd'].diff()
        data['adx_slope'] = data['adx'].diff().fillna(0)
        data['atr_slope'] = data['atr'].diff()
        data['obv_slope'] = data['obv'].diff()

        # Bar Portion (Mum gövde oranı)
        data['bar_portion'] = np.where(
            (data['high'] - data['low']) == 0,
            0,
            (data['close'] - data['open']) / (data['high'] - data['low'])
        )

        # Bar Position (Mumun konumu)
        data['bar_position'] = np.where(
            (data['high'] - data['low']) == 0,
            0,
            ((data['open'] + data['close']) / 2 - data['low']) / (data['high'] - data['low'])
        )

        # Bollinger Bandwidth & %B
        data['bollinger_bandwidth'] = (data['bb_high'] - data['bb_low']) / data['bb_middle']
        data['bollinger_percent_b'] = (data['close'] - data['bb_low']) / (data['bb_high'] - data['bb_low'])

        # Alıcı Hacmi Payı (Buy Volume Portion)
        data['buy_volume_portion'] = data['volume'] / data['volume'].rolling(window=5).sum()

        # Delta Volume
        data['delta_volume'] = data['volume'].diff()

        # Büyük hacimli fiyat hareketlerini tespit eden Liquidity Sweep göstergesi
        data['liquidity_sweep'] = np.where(
            (data['high'] > data['high'].shift(1)) & (data['low'] < data['low'].shift(1)) &
            (data['volume'] > data['volume'].rolling(window=5).mean()), 1, 0
        )

        # Order Flow Imbalance (Alım-Satım dengesizliği)
        data['orderflow_imbalance'] = (data['close'] - data['open']) / (data['high'] - data['low'])


        # Stick Length (Mum uzunluğu, ATR ile normalize)
        data['stick_length'] = (data['high'] - data['low']) / data['atr'].shift(1)

        # Volume Ratio (5m, 15m)
        data['volume_ratio_5m'] = data['volume'] / data['volume'].rolling(window=5).mean()
        data['volume_ratio_15m'] = data['volume'] / data['volume'].rolling(window=15).mean()

        # VWAP Delta (VWAP - Kapanış Fiyatı Farkı)
        data['vwap_delta'] = data['vwap'] - data['close']

        # Hull Moving Average (HMA)
        data['hma_9'] = hma(data, 9)

        # Pivot Noktalarını Ekle
        data = pivot_points(data)

        # Cumulative Delta Volume'u Ekle
        data = cumulative_delta_volume(data)

        data['sma_50'] = ta.trend.SMAIndicator(close=data['close'], window=50).sma_indicator()
        data['sma_200'] = ta.trend.SMAIndicator(close=data['close'], window=200).sma_indicator()

        # Ichimoku göstergesi
        data['ichimoku_conversion_line'] = ichimoku_conversion_line(data, window=9)
        data['ichimoku_base_line'] = ichimoku_base_line(data, window=26)
        data['elder_force_index'] = elders_force_index(data, window=13)

        # Pivot noktalarını ekledikten sonra Fibonacci seviyelerini hesapla
        fib_levels = fibonacci_levels(data)
        for level, value in fib_levels.items():
            # Her satır için aynı değeri kullanarak sabit bir sütun ekliyoruz.
            data[level] = value

        # Eksik değerleri temizle
        data.dropna(subset=['open', 'high', 'low', 'close', 'volume'], inplace=True)

        return data

    except Exception as e:
        print(f"Indicator eklenirken hata: {e}")
        return data

def cumulative_delta_volume(data):
    """Cumulative Delta Volume hesaplama"""
    data['delta_volume'] = data['volume'].diff().fillna(0)
    data['cumulative_delta_volume'] = data['delta_volume'].cumsum()
    return data

def pivot_points(data):
    """Pivot noktalarını hesaplayan fonksiyon"""
    data['pivot'] = (data['high'].shift(1) + data['low'].shift(1) + data['close'].shift(1)) / 3
    data['support_1'] = 2 * data['pivot'] - data['high'].shift(1)
    data['support_2'] = data['pivot'] - (data['high'].shift(1) - data['low'].shift(1))
    data['resistance_1'] = 2 * data['pivot'] - data['low'].shift(1)
    data['resistance_2'] = data['pivot'] + (data['high'].shift(1) - data['low'].shift(1))
    return data

def hma(data, window):
    """Hull Moving Average hesaplama fonksiyonu"""
    wma_half = ta.trend.WMAIndicator(close=data['close'], window=window//2).wma()
    wma_full = ta.trend.WMAIndicator(close=data['close'], window=window).wma()
    hma_sqrt = int(np.sqrt(window))
    hma_calc = ta.trend.WMAIndicator(close=(2 * wma_half - wma_full), window=hma_sqrt).wma()
    return hma_calc

def fibonacci_levels(data, period=14):
    # Yeterli veri olup olmadığını kontrol et
    if len(data) < period:
        return {}

    recent_high = data['high'].rolling(window=period).max().iloc[-1]
    recent_low = data['low'].rolling(window=period).min().iloc[-1]
    diff = recent_high - recent_low

    levels = {}
    from config import FIBO_38_2_EXIT, FIBO_50_EXIT, FIBO_61_8_EXIT

    if FIBO_38_2_EXIT:
        levels['fib_38_2'] = recent_high - 0.382 * diff
    if FIBO_50_EXIT:
        levels['fib_50'] = recent_high - 0.5 * diff
    if FIBO_61_8_EXIT:
        levels['fib_61_8'] = recent_high - 0.618 * diff

    return levels

def ichimoku_conversion_line(data, window=9):
    """
    Ichimoku Conversion Line (Tenkan-sen) hesaplar.
    :param data: DataFrame, en az 'high' ve 'low' sütunlarını içermeli.
    :param window: Hesaplama periyodu (genellikle 9)
    :return: Conversion Line serisi
    """
    high_max = data['high'].rolling(window=window).max()
    low_min = data['low'].rolling(window=window).min()
    return (high_max + low_min) / 2

def ichimoku_base_line(data, window=26):
    """
    Ichimoku Base Line (Kijun-sen) hesaplar.
    :param data: DataFrame, en az 'high' ve 'low' sütunlarını içermeli.
    :param window: Hesaplama periyodu (genellikle 26)
    :return: Base Line serisi
    """
    high_max = data['high'].rolling(window=window).max()
    low_min = data['low'].rolling(window=window).min()
    return (high_max + low_min) / 2

def elders_force_index(data, window=13):
    """
    Elder's Force Index hesaplar.
    :param data: DataFrame, 'close' ve 'volume' sütunlarını içermeli.
    :param window: Hareketli ortalama periyodu (örneğin, 13)
    :return: Elder's Force Index serisi
    """
    efi = (data['close'] - data['close'].shift(1)) * data['volume']
    return efi.rolling(window=window).mean()
def add_indicators_to_all(data_dict):
    """
    Her zaman dilimi için teknik indikatörleri ekler.
    :param data_dict: {'1m': DataFrame, '15m': DataFrame, '4h': DataFrame}
    :return: Güncellenmiş veri sözlüğü
    """
    try:

        for interval, data in data_dict.items():
            if data is not None:
                try:
                    # İlk 5 satırı göster (opsiyonel)
                    data_with_indicators = add_indicators(data)
                    data_dict[interval] = data_with_indicators
                except Exception as inner_e:

                    data_dict[interval] = None
            else:
                print(f"No data available for interval: {interval}")
        print("Finished processing all intervals in add_indicators_to_all.")
        return data_dict
    except Exception as e:
        print(f"Error adding indicators to all timeframes: {e}")
        return None
