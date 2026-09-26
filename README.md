# hasil-prompt-mt-signal

Repositori **hasil/dokumentasi prompt** - bukan source code utama.

- **Source code utama:** https://github.com/zenolambee/mt-signal (`xauusd_strategy.py`, `test_xauusd_strategy.py`)
- **Isi repo ini:** ringkasan phase & hasil validasi (`phase/`). Tidak menyimpan API key / secret / `.env`.

## Phase

- **Phase 01 - XAUUSD EMA/RSI/ATR + Fibonacci:** `phase/phase-01-xauusd-ema-rsi-atr-fibonacci.md` - `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` (EMA20/50 + RSI14 + ATR14 + Market Structure + Fibonacci `0.382/0.500/0.618/0.786`, extension `1.272/1.618`), M15 confirmation / M5 entry, ATR SL `1.5xATR`, RR `1:2`, confidence `100`, 19 test PASS.
- **Phase 02 - Validasi candle XAUUSD aktual:** `phase/phase-02-candle-validation.md` - pipeline candle, BUY/SELL/NO SIGNAL, look-ahead audit, dataset & limitation.

## Struktur

```
hasil-prompt-mt-signal/
├── README.md
└── phase/
    ├── phase-01-xauusd-ema-rsi-atr-fibonacci.md
    └── phase-02-candle-validation.md
```
