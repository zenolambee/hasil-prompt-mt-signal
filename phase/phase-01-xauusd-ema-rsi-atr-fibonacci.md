# Phase 01 — XAUUSD EMA/RSI/ATR + Fibonacci

**Strategy:** `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB`  
**Source code:** https://github.com/zenolambee/mt-signal  
**Commit:** `c8af0bdad1803e6b6e15ded93f634d329cf7352d` (hasil repo sync, `cbbd47b` base)  
**Date:** 2026-09-26

## Indikator
- EMA20 / EMA50 (M15 trend, M5 alignment)
- RSI14 (M5, threshold 50 ±2)
- ATR14 (M5, SL/validasi)
- Market Structure — swing High/Low confirmed (`swingLookback=3`, jarak minimum `minimumStructureDistance` × ATR)
- Fibonacci retracement `0.382 / 0.500 / 0.618 / 0.786` + extension `1.272 / 1.618`

## Timeframe
- **M15** confirmation (`EMA20 > EMA50` bullish, `<` bearish, ranging jika `|gap| ≤ ATR×rangingAtrFraction` atau crossovers ≥ max)
- **M5** entry — semua gate M5 dievaluasi pada candle yang sudah close

## Logic BUY (ringkas)
M15 bullish → M5 aligned (EMA20>EMA50 & close>EMA50) → Higher High + Higher Low → Fibonacci anchor valid (low→high, range ≥ `minimumStructureDistance×ATR`) → pullback window menyentuh `0.500–0.618` & tidak melewati `0.786` → pullback EMA window → RSI `>50` → break `close > swingHigh` → candle bullish confirmation (engulfing/rejection/strong close ≥ `strongCloseFraction`) → tidak terlalu jauh dari EMA → SL valid → confidence ≥ `minimumConfidence` → **BUY**

## Logic SELL
Mirror: M15 bearish, LH+LL, anchor high→low, window `0.500–0.618` dihitung dari low, RSI `<50`, break `close < swingLow`, bearish confirmation.

## Logic NO SIGNAL
Ranging, M5 tidak searah, structure tidak confirmed, fib anchor invalid, tidak di zona `0.500–0.618`, melewati `0.786` (`0.382` hanya shallow → `Harga di shallow 0.382 belum di 0.500-0.618`), RSI gagal, break/confirmation gagal, terlalu jauh dari EMA, spread > `maxSpread`, confidence di bawah minimum. Reason per gate.

## Fibonacci
- Anchored hanya dari swing confirmed (tidak pernah candle random/future).
- Entry: `0.500–0.618` harus pernah dikunjungi di window pullback sebelum candle entry.
- `0.382` shallow: confidence +7 tapi tidak lolos gate.
- `>0.786` dalam deep: invalid → NO SIGNAL `Retracement melewati 0.786`.
- Extension `1.272/1.618` dilaporkan di `fibExt1272`/`fibExt1618`; TP tetap RR.

## ATR SL / RR TP
- `atrSLMultiplier=1.5` × ATR M5, kandidat `[swing, close ± ATR×mult, fib786 ±0.1×range]` → paling protektif (BUY `min`, SELL `max`).
- TP = `entry ± |entry−SL|×riskReward` (default `1:2`).

## Confidence (100)
M15 20 + M5 align 15 + Pullback 10 + Fib 15 (shallow 7) + RSI 10 + Structure 15 + Candle 10 + Break 5. Tidak meng-override gate mandatory.

## Test
- File: `test_xauusd_strategy.py` (repo utama)
- Suite: 19 test — `python -m unittest -v` **19 PASS / 0 FAIL** (2026-09-26)
- Cakupan: fib calc, bullish/sell end-to-end dengan fixture deterministik, zona 0.500/0.618, shallow 0.382, invalidation 0.786, invalid anchor, M15 bullish↔M5 bearish & sebaliknya, RSI, candle confirmation, structure, duplicate, ATR SL/RR, extension, ranging, spread filter, NO SIGNAL generik

## Validasi candle aktual
- Pipeline candle aktual dipisahkan ke `phase-02-candle-validation.md` (dataset, BUY/SELL/NO SIGNAL, look-ahead audit, limitation).

## Struktur & penggunaan
\\\python
from xauusd_strategy import Candle, StrategyConfig, XAUUSDEmaRsiAtrStructure
s = XAUUSDEmaRsiAtrStructure()
sig = s.evaluate(m5, m15, spread=0.25)  # Sequence[Candle] yang sudah close
sig.to_dict()  # fib382/fib500/fib618/fib786, activeFibZone, fibExt1272/1618, reason
\\\
Configurable: `emaFast/emaSlow`, `rsiPeriod`, `atrPeriod`, `rangingAtrFraction`, `crossoverLookback/maxCrossovers`, `pullbackLookback/pullbackAtrTolerance`, `maxExtensionAtr`, `strongCloseFraction`, `fib*`, `swingLookback`, `minimumStructureDistance`, `enableSpreadFilter/maxSpread`, `minimumConfidence`.
