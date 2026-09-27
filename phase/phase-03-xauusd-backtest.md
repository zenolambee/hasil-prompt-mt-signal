# Phase 03 — Backtest XAUUSD (Historis Nyata)

**Tujuan:** walk-forward replay candle-by-candle untuk mengukur performa `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` apa adanya (tidak optimasi).

**Source:** https://github.com/zenolambee/mt-signal  
**Engine:** `backtest_xauusd.py` + `candle_data.py` (`load_csv`, `resample_m15`, `validate_candles`, fast walk-forward O(N))  
**Strategy params (tetap):** EMA20/50, RSI14, ATR14 ×1.5, RR 1:2, Fib `0.382/0.500/0.618/0.786`, ext `1.272/1.618`, confidence 70, `swingLookback 3`, `minimumStructureDistance 0.2×ATR`, `maxExtensionAtr 1.0`  
**Tanggal:** 2026-09-27  
**Commit source:** `7ff5ed6` + loader/backtest fixes (historical CSV `;` delimiter, timestamp `%Y.%m.%d %H:%M`)

## Dataset

- **Files deteksi otomatis:** `data/XAUUSD_m_M5.csv` (212.625 M5), `data/XAUUSD_m_M15.csv` (70.892 M15), `data/XAUUSD_M5_history.csv` (10.000 M5, subset 2026-07–08)
- **Validasi:** `validate_candles` — duplicates 0, out_of_order 0, invalid OHLC 0 untuk M5 & M15; dedup by timestamp, sort ascending; gaps >10min ~ tear waktu libur (787 untuk M5)
- **Format:** auto-detect `,` vs `;`, header `time`/`Time`/`timestamp` + `open/high/low/close` case-insensitive, timestamp `YYYY.MM.DD HH:MM` (MT5) / `YYYY-MM-DD HH:MM:SS` / ISO
- **M15:** nyata tersedia → dipakai langsung (tidak resample sintetis). Data `XAUUSD_M5_history` tidak dipakai karena subset dari M5 utama
- **Backtest utama:** `data/XAUUSD_m_M5.csv` + `data/XAUUSD_m_M15.csv` → `results/`

## Metode walk-forward

- Loop `idx` 0..`len(m5)-1`, slice `m5[:idx+1]`, `m15` via pointer `m15_ptr` advancing by `timestamp ≤ m5[idx].timestamp` — **tidak ada look-ahead**
- Swings dari `m5[:-1]` via incremental `_swings` prefix, fib window `m5[-1-lookback-6 : -1]` (exclude entry bar), break `m5[-1]/m5[-2]`
- `OPEN` blok signal baru sampai resolve; `backtest_results.csv` simpan semua trade termasuk `OPEN`

## Aturan entry / SL / TP / ambiguous

- Entry `close` signal, SL `min(swingLow, close−1.5×ATR, fib786−0.1×range)` BUY / `max(...)` SELL, TP `entry ± |entry−SL|×2.0` (RR 1:2)
- Forward scan setelah entry (entry candle tidak dicek): `high ≥ TP` → TP_HIT (+2R), `low ≤ SL` → SL_HIT (−1R), keduanya → AMBIGUOUS (0R, konservatif)

## Hasil Historis Nyata

**Periode:** 2023-08-28 01:00 UTC → 2026-08-26 23:55 UTC (M5), M15 01:00 → 23:45  
**Candle:** M5 212.625, M15 70.892, evaluated signals 211.214 (min history 50 M5 / 51 M15)

| Metric | Value |
|---|---|
| Total signals | 211.214 |
| BUY / SELL / NO SIGNAL | 23 / 12 / 211.179 |
| Total trades | 35 |
| TP hit / SL hit / AMBIGUOUS / OPEN | 9 / 26 / 0 / 0 |
| BUY TP/SL | 5 / 18 |
| SELL TP/SL | 4 / 8 |
| Win rate (closed) | 25.71% |
| Total R | −8.0 |
| Average R | −0.2286 |
| Profit factor | 0.6923 |
| Max drawdown | 13.0 R |
| Max consecutive wins / losses | 3 / 10 |
| Largest win / loss | +2.0 / −1.0 |

**Daily breakdown (hari dengan trade):** `2023-09-26 +2R`, `2023-12-27 +2R`, `2024-04-02 +2R`, `2024-07-08 +2R`, `2024-10-21 +2R`, `2024-11-06 +2R`, `2024-12-23 +2R`, `2025-04-03 +2R`, `2025-09-30 +2R` (9 hari TP); sisanya −1R per hari (26 hari SL). Full breakdown di `results/backtest_summary.json → daily_breakdown`.

**Outputs:** `results/backtest_results.csv` (35 baris), `results/backtest_signal_log.csv` (211k baris, ~85MB), `results/backtest_summary.json` — tidak di-commit ke git (`.gitignore` `results/`), tapi tersedia lokal untuk evaluasi. CLI: `python backtest_xauusd.py --m5 data/XAUUSD_m_M5.csv --m15 data/XAUUSD_m_M15.csv --outdir results`

## Engine validation (fixture, bukan market)

`test_backtest_xauusd.py` 14 test: BUY→TP/SL, SELL→TP/SL, AMBIGUOUS, OPEN duplicate, RR 1:2, M5→M15 resample, empty, invalid CSV skip, sequential/drawdown, R, no look-ahead, no optimization params — **PASS**

## CLI

```sh
python backtest_xauusd.py --m5 data/XAUUSD_m_M5.csv --m15 data/XAUUSD_m_M15.csv --outdir results
python backtest_xauusd.py --m5 data/XAUUSD_m_M5.csv --outdir results  # M15 resampled
```

CSV: `timestamp,open,high,low,close` (atau `time` / `;` delimiter MT5, `Time;Open;High;Low;Close;TickVolume;Spread;RealVolume` juga didukung).

## Test

- `test_backtest_xauusd.py` 14 + `test_validate_candles.py` 4 + `test_xauusd_strategy.py` 19
- **Total: `python -m unittest -v` 37 PASS / 0 FAIL**, `python -m py_compile` ok

## Limitation

- Profit/drawdown dalam `R` (RR 1:2), bukan nominal; belum biaya/komisi/slippage.
- Gap libur tidak diisi; `OPEN` tidak ada di run ini (semua trade close sebelum akhir dataset).
- `results/` di-ignore git — hasil dibagikan via Phase docs / snapshot, bukan commit 85MB log.
- Tidak optimasi — tujuan hanya mengukur strategy saat ini.
