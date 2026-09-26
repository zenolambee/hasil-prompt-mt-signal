# Phase 03 — Backtest XAUUSD

**Tujuan:** walk-forward replay candle-by-candle untuk mengukur performa `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` apa adanya (tidak optimasi).

**Source:** https://github.com/zenolambee/mt-signal  
**Engine:** `backtest_xauusd.py` + `candle_data.py` (`load_csv`, `resample_m15`)  
**Strategy params (tetap):** EMA20/50, RSI14, ATR14 ×1.5, RR 1:2, Fib `0.382/0.500/0.618/0.786`, ext `1.272/1.618`, confidence 70, `swingLookback 3`, `minimumStructureDistance 0.2×ATR`, `maxExtensionAtr 1.0`  
**Tanggal:** 2026-09-26

## Dataset

- **Historical nyata belum tersedia di repo.** Tidak ada `data/xauusd_m5.csv` / `data/xauusd_m15.csv` yang ter-commit. Tidak ada API key / `.env` yang disimpan.
- **Metode data:** `backtest_xauusd.py` menerima CSV `timestamp,open,high,low,close` (extra kolom `volume`/`spread` diabaikan). Jika `--m15` tidak diberikan, M15 diresample dari M5 via `candle_data.resample_m15` (agregasi 3×M5). Jika file tidak ada, engine mencetak instruksi dan tidak mengarang data.
- **Fixture untuk engine test:** `test_backtest_xauusd.py` memakai `bullish_fixture`/`bearish_fixture` deterministik (60 M5 + 70 M15) hanya untuk membuktikan mesin bekerja, bukan sebagai dataset utama backtest.
- **Periode dataset historis nyata:** — (belum ada)  
- **Jumlah candle historis nyata:** — (belum ada)

## Metode walk-forward

- Loop `idx` 0..`len(m5)-1`, slice `m5[:idx+1]`, `m15` difilter `timestamp ≤ m5[idx].timestamp` (atau proporsional `//3` bila M15 diresample) — **tidak ada look-ahead**.
- Swings dari `m5[:-1]` saja, fib window `m5[-1-lookback-6 : -1]` (exclude entry bar), break pakai `m5[-1]/m5[-2]`.
- Evaluasi via `XAUUSDEmaRsiAtrStructure.evaluate(m5_slice, m15_slice, spread)` per candle.
- Duplikasi/OPEN: jika trade masih `OPEN`, signal baru tidak dibuka sampai trade resolve (per spec default). `OPEN` tetap di `backtest_results.csv` dengan `r_multiple 0`.

## Aturan entry / SL / TP / ambiguous

- **Entry:** `close` candle signal (field `Signal.entry`).
- **SL:** paling protektif dari `min(swingLow, close−1.5×ATR, fib786−0.1×range)` BUY / `max(...)` SELL.
- **TP:** `entry ± |entry−SL|×2.0` (RR 1:2 dari SL aktual).
- **Hasil trade:** scan forward candles setelah entry (entry candle tidak dicek). Jika `high ≥ TP` → `TP_HIT` (+2R), `low ≤ SL` → `SL_HIT` (−1R). Jika **satu candle** menyentuh **keduanya** → `AMBIGUOUS` (0R, konservatif, tidak asumsi urutan intrabar).

## Hasil metrics (historical nyata)

> **Backtest historical belum dijalankan karena dataset XAUUSD historis belum tersedia.**  
> Engine + test hanya memvalidasi pipeline; belum ada `backtest_results.csv` / `backtest_summary.json` historis yang dapat dilaporkan sebagai hasil market nyata. Jangan menganggap fixture sebagai backtest market.

## Hasil metrics (fixture engine validation — bukan market)

Untuk memastikan mesin sehat, `run_backtest` pada fixture deterministik (`bullish_fixture` 60 M5, `bearish_fixture` 60 M5, 14 backtest tests):

- `BUY → TP`, `BUY → SL`, `SELL → TP`, `SELL → SL` — PASS
- `AMBIGUOUS` candle (high & low hit) → `AMBIGUOUS` 0R — PASS
- `OPEN` memblok duplicate — PASS
- `RR 1:2` (`|TP−entry| == 2×|entry−SL|`) — PASS
- Sequential, drawdown, R calculation, M5→M15 resample, empty/invalid CSV — PASS

Contoh summary shape (dari test harness, bukan market):

```json
{
  "total_candles": 60,
  "total_trades": 1,
  "tp_hits": 0, "sl_hits": 0, "ambiguous": 0, "open_trades": 1,
  "win_rate": 0, "total_r": 0, "average_r": 0,
  "max_drawdown": 0, "profit_factor": 0,
  "ambiguous_rule": "...",
  "lookahead": "Walk-forward: signal at N uses only candles 0..N ..."
}
```

## CLI

```sh
python backtest_xauusd.py --m5 data/xauusd_m5.csv
python backtest_xauusd.py --m5 data/xauusd_m5.csv --m15 data/xauusd_m15.csv --outdir results --spread 0.25
```

Output: `results/backtest_results.csv` (`timestamp,direction,entry,sl,tp,result,r_multiple,confidence,m15_trend,m5_structure,rsi,atr,fib_zone`), `backtest_signal_log.csv`, `backtest_summary.json` (metrics + daily breakdown + params).

CSV historis yang diharapkan:

```
timestamp,open,high,low,close
2025-01-01 00:00:00,2025.10,2026.30,2024.80,2025.90
...
```

M15 boleh `timestamp,open,high,low,close` terpisah; bila tidak ada, akan diresample dari M5.

## Daily breakdown

- Tersedia di `backtest_summary.json → daily_breakdown` per `YYYY-MM-DD`: `{signals, buy, sell, tp, sl, net_r}`. Untuk fixture 2025-01-01: signals 11, buy 1, sell 0, net_r 0 (trade masih OPEN).

## Test

- `test_backtest_xauusd.py` — 14 test (BUY→TP/SL, SELL→TP/SL, AMBIGUOUS, OPEN duplicate, RR, resample, empty, invalid CSV, sequential/drawdown, R, no look-ahead, no optimization, etc.)
- `test_validate_candles.py` — 4 test, `test_xauusd_strategy.py` — 19 test
- **Total: `python -m unittest -v` 37 PASS / 0 FAIL**, `python -m py_compile` ok

## Limitation

- Tidak ada historical XAUUSD nyata di repo — hasil market belum dapat dihitung.
- Tidak optimasi / tidak curve fitting — tujuan phase 03 hanya mengukur performa saat ini.
- Profit factor / drawdown dihitung dari `r_multiple` (+2 / −1 / 0), bukan equity curve nominal.
- M15 dari `resample_m15` (3×M15) bila feed M15 tidak ada — tidak sama dengan M15 broker sebenarnya.
- Belum ada UI / log streaming — output file CSV/JSON.

## Status

- **Source backtest aman:** `backtest_xauusd.py`, `test_backtest_xauusd.py`, `candle_data.py` (fix invalid CSV row skip) — tidak ada indikator baru, tidak ubah params untuk optimasi.
- **Look-ahead:** PASS (truncation + `m5[:-1]` swings)
- **Historical backtest:** belum dijalankan (dataset belum tersedia — jujur, tidak dikarang)
