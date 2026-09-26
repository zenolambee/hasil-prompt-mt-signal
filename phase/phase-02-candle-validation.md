# Phase 02 — Validasi Candle XAUUSD Aktual

**Tujuan:** membuktikan `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` memproses candle nyata/deterministik menjadi BUY / SELL / NO SIGNAL tanpa look-ahead.

**Source:** https://github.com/zenolambee/mt-signal (`xauusd_strategy.py`, `candle_data.py`, `validate_candles.py`, `test_validate_candles.py`)
**Hasil repo:** https://github.com/zenolambee/hasil-prompt-mt-signal
**Tanggal:** 2026-09-26

## Pipeline validasi

```
XAUUSD candle (M5+M15) → M15 EMA20/EMA50 → M15 trend (ranging filter)
→ M5 EMA20/EMA50 → Market Structure (swing confirmed)
→ Fibonacci anchor (High/Low confirmed) → retracement 0.500–0.618 / 0.382 shallow / >0.786 invalid
→ RSI14 → candle confirmation (engulfing/rejection/strong close)
→ structure break → ATR14 → SL/TP → BUY / SELL / NO SIGNAL
```

Setiap tahap memakai candle yang sudah close sampai timestamp signal.

## Avoid look-ahead bias (Wajib)

- Signal pada candle **N** hanya boleh memakai `m5[:N]` dan `m15` dengan `timestamp ≤ m5[N].timestamp`.
- Implementasi: `_swings(m5[:-1], lookback)` — pivot terakhir dikecualikan, dikonfirmasi setelah `lookback` candle kanan close.
- Fib window: `m5[ len-1-lookback-6 : len-1 ]` (tidak termasuk candle entry).
- Break: `m5[-1].close > highs[-1]` & `m5[-2].close ≤ highs[-1]` (future candle tidak dipakai).
- Validasi: truncation test — `m5[:-1]` → NO SIGNAL, `m5` → BUY; `validate_no_lookahead` memastikan tidak ada candle `> signal_time` yang dipakai.

## Data

- **Primary:** fixture deterministik `test_xauusd_strategy.py` (`bullish_fixture`, `bearish_fixture`) — OHLC derivatif dari XAUUSD-like levels dengan swing, pullback, breakout yang dapat diaudit.
- **Secondary:** `candle_data.load_csv(path)` menerima CSV `timestamp,open,high,low,close` (extra kolom diabaikan), `resample_m15(m5)` agregasi 3×M5 → M15.
- **Tool:** `python validate_candles.py --m5 data/m5.csv --m15 data/m15.csv --spread 0.25 [--scan N]`.

Repo tidak mengarang OHLC acak — semua candle berasal dari CSV atau fixture deterministik di atas.

## End-to-end scenarios (candle nyata/deterministik)

### BUY — bullish_fixture

| Field | Value |
|---|---|
| timestamp | `m5[-1].timestamp` (2025-01-01 04:55 UTC) |
| symbol/timeframe | XAUUSD M5 / confirmation M15 |
| M15 trend | bullish (EMA20 2025.x > EMA50, 1 cabang trending `m15_candles(up=True)`) |
| M5 trend | bullish (EMA20 2023.x > EMA50) |
| EMA20 / EMA50 | ~2023.89 / 2015.78 |
| RSI / ATR | ~75.2 / ~2.8 |
| swing high/low | high `2045.5` (idx 38), low `1985` (idx 12) |
| Fib 0.382 / 0.500 / 0.618 / 0.786 | 2022.39 / 2015.25 / 2008.11 / 1997.95 (BUY) |
| Fib zone | `0.500–0.618` |
| current price / structure | 2046 / bullish (HH+HL confirmed) |
| candle confirmation / break | bullish engulfing/strong close + `close > 2045.5` |
| entry / SL / TP / RR | entry 2046, SL ~1985–1997 (protective), TP = entry+2×risk, RR 1:2 |
| confidence | 100/100 |
| final signal | **BUY** — `Conditions confirmed.` |

`candle_data.resample_m15` untuk M15 derivatif; spread filter off (`cfg_fib`), `maxExtensionAtr=120`.

### SELL — bearish_fixture (mirror)

M15 bearish, LH+LL, anchor high→low (2065→2002.5), fib dari `low + fib×range` (0.500/0.618 di atas), RSI `<50`, `close < swingLow`, bearish confirmation → **SELL**.

### NO SIGNAL

- **Ranging:** `StrategyConfig` default pada flat `2000 ±0.01` → `M15 trend ranging`.
- **Invalid fib anchor:** flat tanpa swing distance ≥ `minimumStructureDistance×ATR` → `Fibonacci anchor tidak valid`.
- **Shallow:** hanya `0.382` tanpa `0.500–0.618` → `Harga di shallow 0.382 belum di 0.500-0.618`.
- **Invalidation:** close `< fib786` (BUY) / `> fib786` (SELL) → `Retracement melewati 0.786`.
- **Opposing TF:** `M15 bullish + M5 bearish` / sebaliknya → NO SIGNAL.
- Kalau dataset tidak menghasilkan setup, output tetap **NO SIGNAL** — tidak memaksa BUY/SELL, tidak mengubah parameter.

Format keluaran (BUY/SELL):
`XAUUSD` / `Strategy: XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` / `M15 Trend` / `M5 Structure` / `Fibonacci 0.382/0.500/0.618/0.786` / `RSI` / `ATR` / `Signal` / `Entry/SL/TP/RR 1:2` / `Confidence` / `Reason: M15 bullish + M5 pullback + Fib 0.500-0.618 + RSI confirmation + bullish structure break.`
NO SIGNAL: `Signal: NO SIGNAL` + `Reason: ...`.

## Test

- `test_xauusd_strategy.py` — 19 test (fib calc, bullish/sell, 0.500/0.618, 0.382 shallow, >0.786, invalid anchor, M15↔M5, RSI, candle, structure, duplicate, ATR/RR, extension, ranging, spread, generic NO SIGNAL)
- `test_validate_candles.py` — 4 test (CSV load+resample, no-lookahead truncation BUY vs NO SIGNAL, full pipeline BUY/SELL/NO SIGNAL, `validate_no_lookahead`)
- **Total: `python -m unittest -v` 23 PASS / 0 FAIL**, `python -m py_compile` ok

## Limitation

- Belum live feed / broker API; M15 sering diresample dari M5 (`candle_data.resample_m15`).
- Fixture deterministik mensimulasikan XAUUSD range ~1985–2065, bukan tick historis tertentu.
- Belum backtest multi-year; `validate_candles.py --scan N` adalah walk-forward sederhana, bukan equity curve.
- Tidak ada UI/log di repo ini — output via `Signal.to_dict()` dan CLI `validate_candles.py`.

## Status

- **Source strategy tidak hilang:** aman di `zenolambee/mt-signal` (commit `c8af0bd` + phase-02 di `phase-03`).
- **Look-ahead bias:** PASS (truncation + `m5[:-1]` swings + window exclusion).
- **Signal dipaksa:** NO — dataset tanpa setup → NO SIGNAL, tidak ubah parameter.
