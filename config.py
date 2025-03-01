import os
from binance.client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
Coin_M_C_API = os.getenv('Coin_Market_cap_Api_key')
Telegram_chat_id =  os.getenv('TELEGRAM_CHAT_ID')
Telegram_bot_token= os.getenv('TELEGRAM_BOT_TOKEN')
# Initialize Binance Client
client = Client(API_KEY, API_SECRET)
# Giriş boyut dosya yolu
INPUT_SHAPE_FILE = "input_shape.json"
_MODEL_PATH="lstm_model.keras"
_INPUT_SHAPE_FILE= "input_shape.json"
_MODEL_PATH_PPO="ppo_trading_finrl.zip"
lightgbm_model_path_c="lightgbm_model.txt"

#main.py
DEFAULT_INTERVALS = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d']
MARGIN_AMOUNT = 1
MAX_OPEN_POSITIONS = 5
LEVERAGE = 75
__confidence=0.35
tahmin_ortalamasi=-5      # Karar (Son 5 tahminin ortalaması)
risk_percentage_open_position=0.01
#Model.py Settings
_epochs = 50
_batch_size = 128
_learning_rate = 0.00082857
_class_weight= {0: 2.0, 1: 1.0}
_validation_split=0.25
threshold_esigi=0.3 #Eğer tahmin edilen değer (predictions) 0.3'ten büyükse, 1 olarak işaretlenir. 1 çıktığında long/short pozisyon açabilir.0 çıktığında işlem açmaz veya mevcut işlemi kapatabilir.
PPO_total_timesteps=50000
train_rl_finrl_time_reward_scaling=1e-4
norm1_TransformBlok_LayerNormalization=1e-6
norm2_TransformBlok_LayerNormalization=1e-6
calculate_turbulence_historial_prices="5m"
Model_ProgressData_features = [
    'rsi', 'rsi_slope', 'macd', 'macd_signal', 'macd_slope', 'adx', 'adx_slope',
    'ema_5', 'ema_10', 'ema_20', 'bb_high', 'bb_low', 'bb_middle',
    'bollinger_bandwidth', 'bollinger_percent_b', 'obv', 'obv_slope', 'mfi',
    'volume_ratio_5m', 'volume_ratio_15m', 'delta_volume', 'atr', 'atr_slope',
    'vwap', 'vwap_delta', 'williams_r',
    'stochastic_rsi', 'stochastic_oscillator', 'chop', 'momentum', 'roc', 'cci',
    'bar_portion', 'bar_position', 'stick_length', 'buy_volume_portion',
    'orderflow_imbalance', 'liquidity_sweep', 'parabolic_sar', 'vw_atr',
    'volume_oscillator', 'cumulative_delta_volume', 'hma_9',
    'pivot', 'support_1', 'support_2', 'resistance_1', 'resistance_2'
] # Bu değerleri değiştirirsen makinayı baştan öğretmen gerekecek... .teras dosyasını silmen lazım.

Model_ProgressData_required_columns= ['open_1m', 'high_1m', 'low_1m', 'close_1m', 'volume_1m']
_intervals_c= DEFAULT_INTERVALS
train_rl_model_indicators_c= ["macd_5m", "rsi_5m", "adx_5m"]
train_rl_finrl_time_interval=calculate_turbulence_historial_prices
train_rl_finrl_historical_prices=calculate_turbulence_historial_prices
Model_ProgressData_price_change_merged_data_high='high_1m'
Model_ProgressData_price_change_merged_data_low='low_1m'
Model_ProgressData_price_change_merged_data_close='close_1m'
Model_ProgressData_price_change_merged_data_open='open_1m'

#data_fetcher.py
_incelenecek_mum_sayisi = 500
_required_columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
_data_c=['open', 'high', 'low', 'close', 'volume']
min_volume_c=25000000


#mutasyon.py
MUTATION_KEYS_c = Model_ProgressData_features
Mutasyon_REQUIRED_COLUMNS_c = ['open_1m', 'high_1m', 'low_1m', 'close_1m', 'volume_1m']
intervals_mutasyon_c=('1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d')
evolutionary_data_optimization_merged_data_y='close_1m'
evolutionary_data_optimization_train_ratio=0.8
mutation_rate_c= 0.1
generations_mutasyon_c= 10
mutasyon_symbols_c = [
    'BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT',
    'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'DASHUSDT', 'BNBUSDT', 'ATOMUSDT', 'VETUSDT', 'ALGOUSDT',
    'ZRXUSDT', 'COMPUSDT', 'DOGEUSDT', 'SXPUSDT', 'MKRUSDT', 'DOTUSDT', 'CRVUSDT', 'RUNEUSDT',
    'EGLDUSDT', 'SOLUSDT', 'UNIUSDT', 'AVAXUSDT', 'NEARUSDT', 'AAVEUSDT', 'FILUSDT', 'RSRUSDT',
    'ZENUSDT', 'SKLUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'CHRUSDT', 'HBARUSDT', 'ONEUSDT',
    'HOTUSDT', '1000SHIBUSDT', 'GTCUSDT', 'DYDXUSDT', '1000XECUSDT', 'GALAUSDT', 'CELOUSDT',
    'ARUSDT', 'CTSIUSDT', 'LPTUSDT', 'PEOPLEUSDT', 'ROSEUSDT', 'DUSKUSDT', 'FLOWUSDT', 'APEUSDT',
    'OPUSDT', 'INJUSDT', 'LUNA2USDT', 'LDOUSDT', 'ICPUSDT', 'APTUSDT', 'QNTUSDT', 'FETUSDT',
    'MAGICUSDT', 'CFXUSDT', 'SSVUSDT', 'CKBUSDT', 'TRUUSDT', 'IDUSDT', 'ARBUSDT', 'JOEUSDT',
    'RDNTUSDT', 'XVSUSDT', 'SUIUSDT', '1000PEPEUSDT', '1000FLOKIUSDT', 'UMAUSDT', 'MAVUSDT',
    'WLDUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'SEIUSDT', 'BICOUSDT', 'BIGTIMEUSDT', 'TIAUSDT',
    'CAKEUSDT', 'MEMEUSDT', 'ORDIUSDT', 'BEAMXUSDT', '1000BONKUSDT', 'PYTHUSDT', 'SUPERUSDT',
    'ETHWUSDT', 'JTOUSDT', '1000SATSUSDT', 'WIFUSDT', 'ONDOUSDT', 'ALTUSDT', 'JUPUSDT', 'ZETAUSDT',
    'PIXELUSDT', 'STRKUSDT', 'TONUSDT', 'AXLUSDT', 'BOMEUSDT', 'ETHFIUSDT', 'ENAUSDT', 'WUSDT',
    'TNSRUSDT', 'SAGAUSDT', 'TAOUSDT', 'NOTUSDT', 'TURBOUSDT', 'IOUSDT', 'ZKUSDT', 'MEWUSDT',
    'ZROUSDT', 'RENDERUSDT', 'BANANAUSDT', 'RAREUSDT', 'SUNUSDT', 'VIDTUSDT', 'NULSUSDT',
    'DOGSUSDT', 'MBOXUSDT', 'CHESSUSDT', 'FLUXUSDT', 'BSWUSDT', 'QUICKUSDT', 'RPLUSDT',
    'AERGOUSDT', 'POLUSDT', 'UXLINKUSDT', '1MBABYDOGEUSDT', 'NEIROUSDT', 'KDAUSDT', 'FIDAUSDT',
    'FIOUSDT', 'CATIUSDT', 'GHSTUSDT', 'LOKAUSDT', 'HMSTRUSDT', 'COSUSDT', 'EIGENUSDT', 'DIAUSDT',
    '1000CATUSDT', 'SCRUSDT', 'SAFEUSDT', 'SANTOSUSDT', 'PONKEUSDT', 'COWUSDT', 'CETUSUSDT',
    '1000000MOGUSDT', 'DRIFTUSDT', 'SWELLUSDT', 'ACTUSDT', 'PNUTUSDT', '1000XUSDT', 'AKTUSDT',
    'SLERFUSDT', 'SCRTUSDT', '1000WHYUSDT', 'THEUSDT', 'MORPHOUSDT', 'KAIAUSDT', 'AEROUSDT',
    'ACXUSDT', 'ORCAUSDT', 'MOVEUSDT', 'RAYSOLUSDT', 'MEUSDT', 'AVAUSDT', 'DEGOUSDT',
    'VELODROMEUSDT', 'PENGUUSDT', 'LUMIAUSDT', 'KMNOUSDT', 'DEXEUSDT', 'PHAUSDT', 'DFUSDT',
    'GRIFFAINUSDT', 'ALCHUSDT', 'SWARMSUSDT', 'SONICUSDT', 'DUSDT', 'PROMUSDT', 'SUSDT',
    'SOLVUSDT', 'VTHOUSDT', 'ANIMEUSDT'
]

# config.py - Risk Yönetimi ve İşlem Ayarları

# 1. Genel Ayarlar
LIVE_MODE = False  # Gerçek işlem yapma modu (True: Gerçek, False: Test)
API_KEY = ''  # API anahtarınız
API_SECRET = ''  # API gizli anahtarınız
POSITION_SIZING = True  # Pozisyon boyutlandırma (True: Açılacak pozisyon büyüklüğü otomatik ayarlanır)
MIN_POSITION_SIZE = 0.01  # Minimum pozisyon büyüklüğü (Örneğin: 0.01 BTC)
MAX_POSITION_SIZE = 1  # Maksimum pozisyon büyüklüğü (Örneğin: 1 BTC)
TIMEZONE = 'Europe/Istanbul'  # Zaman dilimi
USE_LOGGING = True  # İşlem kaydını loglama (True: Evet, False: Hayır)
MAX_REAL_TIME_ORDERS = 5  # Gerçek zamanlı işlem için izin verilen maksimum sipariş sayısı
MAX_PAPER_TRADING_ORDERS = 10  # Paper trading (kağıt üzerinde işlem) için izin verilen maksimum sipariş sayısı
USE_PROFIT_BACKUP = False  # Kâr yedekleme (True: Evet, False: Hayır)
DAILY_PROFIT_REPORT = True  # Günlük kâr zarar raporu gönderme (True: Evet, False: Hayır)

# 2. Kaldıraç Ayarları
USE_DEFAULT_LEVERAGE = True  # Varsayılan kaldıraç kullanımı (True: Evet, False: Hayır)
DEFAULT_LEVERAGE = 10  # Varsayılan kaldıraç değeri (Örneğin: 10x)
DYNAMIC_LEVERAGE = True  # Dinamik kaldıraç kullanımı (True: Evet, False: Hayır)
LOW_VOLATILITY_LEVERAGE = 5  # Düşük volatilite için kaldıraç (Örneğin: 5x)
HIGH_VOLATILITY_LEVERAGE = 15  # Yüksek volatilite için kaldıraç (Örneğin: 15x)

# 3. Giriş Ayarları
USE_PRICE_ENTRY = True  # Fiyat temelli giriş kullanımı (True: Evet, False: Hayır)
USE_INDICATORS = True  # Teknik göstergelere dayalı giriş kullanımı (True: Evet, False: Hayır)
USE_ML_MODEL = False  # Makine öğrenmesi modeli ile giriş tahminleri (True: Evet, False: Hayır)
TREND_FOLLOWING = True  # Trend takip eden strateji kullanımı (True: Evet, False: Hayır)
MEAN_REVERSION = False  # Mean Reversion stratejisi kullanımı (True: Evet, False: Hayır)
BREAKOUT_STRATEGY = True  # Breakout stratejisi kullanımı (True: Evet, False: Hayır)

# 4. Çıkış Ayarları
MULTI_TP = True  # Çoklu Take Profit (TP) noktaları kullanımı (True: Evet, False: Hayır)
TP_COUNT = 3  # TP seviyelerinin sayısı (Örneğin: 3 farklı TP seviyesi)
TP1_PERCENTAGE = 5  # İlk TP seviyesi (Örneğin: %5 kâr)
TP2_PERCENTAGE = 10  # İkinci TP seviyesi (Örneğin: %10 kâr)
TP3_PERCENTAGE = 20  # Üçüncü TP seviyesi (Örneğin: %20 kâr)
FULL_TP = False  # Tam kâr almak için çıkış yapma (True: Evet, False: Hayır)
DYNAMIC_TP = True  # Dinamik TP kullanımı (True: Evet, False: Hayır)
MULTI_SL = True  # Çoklu Stop-Loss (SL) noktaları kullanımı (True: Evet, False: Hayır)
SL1_PERCENTAGE = 3  # Sabit Stop-Loss yüzdesi (Örneğin: %3)
ATR_SL = True  # ATR tabanlı stop-loss kullanımı (True: Evet, False: Hayır)
TRAILING_STOP = True  # Trailing Stop (İzleyen Stop-Loss) kullanımı (True: Evet, False: Hayır)
TRAILING_STOP_PERCENTAGE = 2  # Trailing stop yüzdesi (Örneğin: %2)
PROFIT_LOCK = True  # Kâr yedekleme kullanımı (True: Evet, False: Hayır)
DYNAMIC_PROFIT_LOCK = True  # Dinamik kâr yedekleme kullanımı (True: Evet, False: Hayır)
DYNAMIC_PROFIT_LOCK_OFFSET = 2  # Dinamik profit lock için offset değeri (Örneğin: %2)
DYNAMIC_PROFIT_LOCK_THRESHOLD = 10  # Dinamik profit lock eşiği (Örneğin: %10 kârda)

# 5. Stop-Loss ve Take-Profit Kriterleri
TRIGGER_PERCENTAGE = 1  # Tetikleyici yüzdesi (Örneğin: %1)
STOP_LOSS_TP_THRESHOLD = 5  # Stop-Loss ve Take-Profit limit eşiği (Örneğin: %5)

# 6. Volatilite ve Risk Yönetimi
VOLATILITY_THRESHOLD = 2  # Volatilite eşiği (Örneğin: %2 volatilite)
USE_FIBONACCI_EXIT = False  # Fibonacci düzeltme seviyelerine dayalı çıkış kullanımı (True: Evet, False: Hayır)
FIBO_38_2_EXIT = True  # Fibonacci %38.2 seviyesinde çıkış (True: Evet, False: Hayır)
FIBO_50_EXIT = True  # Fibonacci %50 seviyesinde çıkış (True: Evet, False: Hayır)
FIBO_61_8_EXIT = True  # Fibonacci %61.8 seviyesinde çıkış (True: Evet, False: Hayır)
RSI_EXIT = True  # RSI ile çıkış stratejisi kullanımı (True: Evet, False: Hayır)
RSI_OVERBOUGHT = 70  # RSI aşırı alım seviyesi (Örneğin: 70)
RSI_OVERSOLD = 30  # RSI aşırı satım seviyesi (Örneğin: 30)
MACD_EXIT = False  # MACD ile çıkış stratejisi kullanımı (True: Evet, False: Hayır)
MACD_SIGNAL = 'Bullish'  # MACD sinyali (Örneğin: 'Bullish', 'Bearish')
STOCHASTIC_EXIT = False  # Stokastik ile çıkış stratejisi kullanımı (True: Evet, False: Hayır)
STOCHASTIC_OVERBOUGHT = 80  # Stokastik aşırı alım seviyesi (Örneğin: 80)
STOCHASTIC_OVERSOLD = 20  # Stokastik aşırı satım seviyesi (Örneğin: 20)



