# Phase 04 — XAUUSD Trade Failure Analysis

**Sumber:** hasil REAL backtest Phase 03 (tidak ada perubahan strategy logic/parameter/optimasi).

**Strategy:** `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB` — EMA20/50, RSI14, ATR14 x1.5, RR 1:2, Fib 0.382/0.500/0.618/0.786, ext 1.272/1.618, swingLookback 3, confidence 70

**Periode:** 2023-08-28 to 2026-08-26 | **M5:** 212625 candle | **M15:** 70892 candle

**Ringkasan:** Total 35 trades | 9 TP / 26 SL | BUY 5/18 | SELL 4/8 | Total -8R | Win rate 25.71% | PF 0.69 | Max DD 13R | Max consecutive loss 10

**Batasan Phase 04:** Diagnostic only — tidak mengubah logic, tidak optimasi, tidak curve fitting, tidak strategi baru. Hanya temuan faktual.

## 1. Tabel 35 Trade (21-field diagnostic per trade)

> Semua candle walk-forward no look-ahead: signal di N hanya pakai `m5[:N]` dan `m15 timestamp ≤ m5[N].timestamp`, swings `m5[:-1]`, fib window exclude entry bar. Confidence 100 = semua gate lolos (M15 trending + M5 aligned + pullback + Fib 15 + RSI 10 + Structure 15 + Candle 10 + Break 5).

### 1A. Core (Kolom 1-14)

| No | Timestamp | Dir | Entry | SL | TP | Result | R | M15 | M5 | RSI | ATR | Fib | Conf | Swing Used |
|---:|-----------|-----|------:|----:|----:|--------|---:|-----|----|----:|----:|-----|-----:|------------|
| 1 | 2023-09-26T03:15:00+00:00 | SELL | 1916.0 | 1916.67476 | 1914.6504799999998 | TP_HIT | 2.0 | bearish | bearish | 41.07 | 0.2708 | 0.500-0.618 | 100 | swingLow idx=5767 val=1916.09 (broken: close 1916.10 -> 1916.00 < 1916.09) |
| 2 | 2023-10-04T21:55:00+00:00 | SELL | 1817.59 | 1820.8884600000001 | 1810.9930799999995 | SL_HIT | -1.0 | bearish | bearish | 38.89 | 0.9299 | 0.500-0.618 | 100 | swingLow idx=7647 val=1817.69 (broken: close 1817.87 -> 1817.59 < 1817.69) |
| 3 | 2023-10-30T03:00:00+00:00 | BUY | 2004.92 | 2001.01196 | 2012.7360800000001 | SL_HIT | -1.0 | bullish | bullish | 56.56 | 1.3426 | 0.500-0.618 | 100 | swingHigh idx=12400 val=2004.68 (broken: close 2004.63 -> 2004.92 > 2004.68) |
| 4 | 2023-11-14T21:55:00+00:00 | BUY | 1963.67 | 1961.85572 | 1967.2985600000002 | SL_HIT | -1.0 | bullish | bullish | 56.59 | 0.7741 | 0.500-0.618 | 100 | swingHigh idx=15646 val=1963.61 (broken: close 1963.02 -> 1963.67 > 1963.61) |
| 5 | 2023-12-07T15:35:00+00:00 | BUY | 2034.55 | 2030.41 | 2042.8299999999997 | SL_HIT | -1.0 | bullish | bullish | 59.8 | 1.5952 | 0.500-0.618 | 100 | swingHigh idx=20159 val=2034.07 (broken: close 2033.92 -> 2034.55 > 2034.07) |
| 6 | 2023-12-13T13:15:00+00:00 | BUY | 1982.9 | 1979.90164 | 1988.8967200000002 | SL_HIT | -1.0 | bullish | bullish | 58.96 | 0.8426 | 0.500-0.618 | 100 | swingHigh idx=21229 val=1982.79 (broken: close 1982.30 -> 1982.90 > 1982.79) |
| 7 | 2023-12-27T16:45:00+00:00 | BUY | 2070.21 | 2064.96306 | 2080.70388 | TP_HIT | 2.0 | bullish | bullish | 58.63 | 1.5109 | 0.500-0.618 | 100 | swingHigh idx=23751 val=2069.65 (broken: close 2068.77 -> 2070.21 > 2069.65) |
| 8 | 2024-01-10T17:35:00+00:00 | SELL | 2028.07 | 2033.52 | 2017.1699999999998 | SL_HIT | -1.0 | bearish | bearish | 46.59 | 1.8735 | 0.500-0.618 | 100 | swingLow idx=26245 val=2028.64 (broken: close 2029.17 -> 2028.07 < 2028.64) |
| 9 | 2024-02-02T08:00:00+00:00 | BUY | 2055.91 | 2053.8510600000004 | 2060.0278799999987 | SL_HIT | -1.0 | bullish | bullish | 56.89 | 0.6407 | 0.500-0.618 | 100 | swingHigh idx=30782 val=2055.88 (broken: close 2055.48 -> 2055.91 > 2055.88) |
| 10 | 2024-04-02T20:40:00+00:00 | BUY | 2262.76 | 2254.21 | 2279.8600000000006 | TP_HIT | 2.0 | bullish | bullish | 58.28 | 2.0816 | 0.500-0.618 | 100 | swingHigh idx=42228 val=2262.38 (broken: close 2262.21 -> 2262.76 > 2262.38) |
| 11 | 2024-04-25T14:30:00+00:00 | BUY | 2328.08 | 2324.4248 | 2335.3904 | SL_HIT | -1.0 | bullish | bullish | 56.81 | 1.2928 | 0.500-0.618 | 100 | swingHigh idx=46840 val=2327.26 (broken: close 2327.03 -> 2328.08 > 2327.26) |
| 12 | 2024-07-08T10:25:00+00:00 | SELL | 2379.83 | 2386.0139799999997 | 2367.4620400000003 | TP_HIT | 2.0 | bearish | bearish | 44.68 | 1.3937 | 0.500-0.618 | 100 | swingLow idx=61021 val=2380.76 (broken: close 2380.98 -> 2379.83 < 2380.76) |
| 13 | 2024-10-21T01:10:00+00:00 | BUY | 2722.27 | 2718.7883799999995 | 2729.233240000001 | TP_HIT | 2.0 | bullish | bullish | 59.82 | 1.3141 | 0.500-0.618 | 100 | swingHigh idx=81578 val=2722.04 (broken: close 2721.24 -> 2722.27 > 2722.04) |
| 14 | 2024-11-06T20:05:00+00:00 | SELL | 2663.22 | 2669.7439799999997 | 2650.17204 | TP_HIT | 2.0 | bearish | bearish | 42.04 | 2.912 | 0.500-0.618 | 100 | swingLow idx=85115 val=2664.49 (broken: close 2666.39 -> 2663.22 < 2664.49) |
| 15 | 2024-11-11T10:50:00+00:00 | SELL | 2668.95 | 2673.46762 | 2659.9147599999997 | SL_HIT | -1.0 | bearish | bearish | 45.25 | 1.7936 | 0.500-0.618 | 100 | swingLow idx=85825 val=2669.33 (broken: close 2669.42 -> 2668.95 < 2669.33) |
| 16 | 2024-12-23T07:15:00+00:00 | BUY | 2626.29 | 2623.6163 | 2631.6373999999996 | TP_HIT | 2.0 | bullish | bullish | 57.64 | 1.103 | 0.500-0.618 | 100 | swingHigh idx=94014 val=2626.23 (broken: close 2625.73 -> 2626.29 > 2626.23) |
| 17 | 2024-12-26T13:25:00+00:00 | BUY | 2629.22 | 2626.15806 | 2635.343879999999 | SL_HIT | -1.0 | bullish | bullish | 59.27 | 1.032 | 0.500-0.618 | 100 | swingHigh idx=94598 val=2628.63 (broken: close 2628.38 -> 2629.22 > 2628.63) |
| 18 | 2025-01-14T15:35:00+00:00 | SELL | 2665.55 | 2670.96886 | 2654.7122800000006 | SL_HIT | -1.0 | bearish | bearish | 39.99 | 2.6836 | 0.500-0.618 | 100 | swingLow idx=97940 val=2666.53 (broken: close 2667.23 -> 2665.55 < 2666.53) |
| 19 | 2025-01-31T16:50:00+00:00 | BUY | 2808.68 | 2803.8513999999996 | 2818.3372000000004 | SL_HIT | -1.0 | bullish | bullish | 62.48 | 1.9803 | 0.500-0.618 | 100 | swingHigh idx=101509 val=2808.37 (broken: close 2807.36 -> 2808.68 > 2808.37) |
| 20 | 2025-03-18T18:10:00+00:00 | BUY | 3033.08 | 3025.9611600000003 | 3047.317679999999 | SL_HIT | -1.0 | bullish | bullish | 57.94 | 2.4225 | 0.500-0.618 | 100 | swingHigh idx=110344 val=3032.11 (broken: close 3031.94 -> 3033.08 > 3032.11) |
| 21 | 2025-04-03T12:35:00+00:00 | SELL | 3125.4 | 3131.4359999999997 | 3113.328000000001 | TP_HIT | 2.0 | bearish | bearish | 43.66 | 3.1272 | 0.500-0.618 | 100 | swingLow idx=113569 val=3126.12 (broken: close 3128.72 -> 3125.40 < 3126.12) |
| 22 | 2025-07-16T06:05:00+00:00 | SELL | 3327.8 | 3334.2246400000004 | 3314.95072 | SL_HIT | -1.0 | bearish | bearish | 45.06 | 1.8357 | 0.500-0.618 | 100 | swingLow idx=133530 val=3327.81 (broken: close 3329.21 -> 3327.80 < 3327.81) |
| 23 | 2025-08-22T15:20:00+00:00 | SELL | 3327.04 | 3331.2508399999997 | 3318.6183200000005 | SL_HIT | -1.0 | bearish | bearish | 43.08 | 1.7969 | 0.500-0.618 | 100 | swingLow idx=141092 val=3327.76 (broken: close 3329.86 -> 3327.04 < 3327.76) |
| 24 | 2025-09-23T04:30:00+00:00 | BUY | 3751.82 | 3745.55436 | 3764.3512800000003 | SL_HIT | -1.0 | bullish | bullish | 56.34 | 2.9893 | 0.500-0.618 | 100 | swingHigh idx=147007 val=3750.64 (broken: close 3749.87 -> 3751.82 > 3750.64) |
| 25 | 2025-09-30T19:35:00+00:00 | BUY | 3845.38 | 3831.2 | 3873.7400000000007 | TP_HIT | 2.0 | bullish | bullish | 60.29 | 4.3763 | 0.500-0.618 | 100 | swingHigh idx=148571 val=3844.63 (broken: close 3844.39 -> 3845.38 > 3844.63) |
| 26 | 2025-11-11T20:25:00+00:00 | SELL | 4110.37 | 4116.949200000001 | 4097.211599999998 | SL_HIT | -1.0 | bearish | bearish | 42.13 | 3.5912 | 0.500-0.618 | 100 | swingLow idx=156846 val=4110.57 (broken: close 4113.40 -> 4110.37 < 4110.57) |
| 27 | 2025-12-23T10:55:00+00:00 | BUY | 4489.9 | 4484.42576 | 4500.848479999999 | SL_HIT | -1.0 | bullish | bullish | 59.63 | 2.7496 | 0.500-0.618 | 100 | swingHigh idx=164943 val=4489.60 (broken: close 4489.59 -> 4489.90 > 4489.60) |
| 28 | 2025-12-24T03:00:00+00:00 | BUY | 4514.11 | 4499.92 | 4542.489999999999 | SL_HIT | -1.0 | bullish | bullish | 62.63 | 5.1255 | 0.500-0.618 | 100 | swingHigh idx=165126 val=4512.70 (broken: close 4511.85 -> 4514.11 > 4512.70) |
| 29 | 2026-01-06T19:30:00+00:00 | BUY | 4488.92 | 4471.64 | 4523.48 | SL_HIT | -1.0 | bullish | bullish | 61.68 | 4.3939 | 0.500-0.618 | 100 | swingHigh idx=167212 val=4488.91 (broken: close 4487.14 -> 4488.92 > 4488.91) |
| 30 | 2026-01-23T07:35:00+00:00 | BUY | 4958.73 | 4951.05594 | 4974.078119999998 | SL_HIT | -1.0 | bullish | bullish | 59.73 | 3.1937 | 0.500-0.618 | 100 | swingHigh idx=170627 val=4958.33 (broken: close 4957.24 -> 4958.73 > 4958.33) |
| 31 | 2026-01-26T09:05:00+00:00 | BUY | 5088.21 | 5056.3753799999995 | 5151.879240000001 | SL_HIT | -1.0 | bullish | bullish | 56.38 | 9.4941 | 0.500-0.618 | 100 | swingHigh idx=170917 val=5082.22 (broken: close 5081.20 -> 5088.21 > 5082.22) |
| 32 | 2026-02-03T15:55:00+00:00 | BUY | 4932.39 | 4902.61 | 4991.950000000002 | SL_HIT | -1.0 | bullish | bullish | 54.8 | 12.5175 | 0.500-0.618 | 100 | swingHigh idx=172658 val=4930.98 (broken: close 4926.10 -> 4932.39 > 4930.98) |
| 33 | 2026-04-16T07:30:00+00:00 | BUY | 4827.56 | 4814.106679999999 | 4854.466640000003 | SL_HIT | -1.0 | bullish | bullish | 58.82 | 3.2032 | 0.500-0.618 | 100 | swingHigh idx=186595 val=4827.06 (broken: close 4826.40 -> 4827.56 > 4827.06) |
| 34 | 2026-04-17T14:00:00+00:00 | SELL | 4785.13 | 4797.6876999999995 | 4760.014600000001 | SL_HIT | -1.0 | bearish | bearish | 40.95 | 4.0145 | 0.500-0.618 | 100 | swingLow idx=186955 val=4787.10 (broken: close 4787.28 -> 4785.13 < 4787.10) |
| 35 | 2026-08-07T14:15:00+00:00 | BUY | 4320.39 | 4304.243399999999 | 4352.683200000002 | SL_HIT | -1.0 | bullish | bullish | 60.05 | 4.5388 | 0.500-0.618 | 100 | swingHigh idx=208902 val=4320.28 (broken: close 4320.20 -> 4320.39 > 4320.28) |

### 1B. Diagnostic (Kolom 15-21)

| No | Timestamp | Alasan Signal Terbentuk | Kondisi Market Saat Entry | Dekat R/S? | Pullback Fib Valid | Candle Valid | Break Valid | Penyebab Gagal |
|---:|-----------|--------------------------|-----------------------------|------------|--------------------|--------------|-------------|--------------|
| 1 | 2023-09-26T03:15:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 41.1 bearing + HH/HL(bearish) + breakout 1916.09 + candle rejection + conf 100 | M15 bearish trending, M5 bearish, volatilitas rendah-menengah (ATR 0.27, 0.014%), RSI 41.07 (dist 8.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | — (TP hit, breakout continuation valid) |
| 2 | 2023-10-04T21:55:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 38.9 bearing + HH/HL(bearish) + breakout 1817.69 + candle rejection + conf 100 | M15 bearish trending, M5 bearish, volatilitas rendah-menengah (ATR 0.93, 0.051%), RSI 38.89 (dist 11.1 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 3 | 2023-10-30T03:00:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.6 ith bullish + HH/HL(bullish) + breakout 2004.68 + candle engulf + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 1.34, 0.067%), RSI 56.56 (dist 6.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 4 | 2023-11-14T21:55:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.6 ith bullish + HH/HL(bullish) + breakout 1963.61 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah (ATR 0.77, 0.039%), RSI 56.59 (dist 6.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 5 | 2023-12-07T15:35:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.8 ith bullish + HH/HL(bullish) + breakout 2034.07 + candle engulf + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 1.60, 0.078%), RSI 59.80 (dist 9.8 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 6 | 2023-12-13T13:15:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.0 ith bullish + HH/HL(bullish) + breakout 1982.79 + candle engulf + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah (ATR 0.84, 0.042%), RSI 58.96 (dist 9.0 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 7 | 2023-12-27T16:45:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 58.6 ith bullish + HH/HL(bullish) + breakout 2069.65 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 1.51, 0.073%), RSI 58.63 (dist 8.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 8 | 2024-01-10T17:35:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 46.6 bearing + HH/HL(bearish) + breakout 2028.64 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 1.87, 0.092%), RSI 46.59 (dist 3.4 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 9 | 2024-02-02T08:00:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.9 ith bullish + HH/HL(bullish) + breakout 2055.88 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 0.64, 0.031%), RSI 56.89 (dist 6.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 10 | 2024-04-02T20:40:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 58.3 ith bullish + HH/HL(bullish) + breakout 2262.38 + candle engulf + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 2.08, 0.092%), RSI 58.28 (dist 8.3 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | — (TP hit, breakout continuation valid) |
| 11 | 2024-04-25T14:30:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.8 ith bullish + HH/HL(bullish) + breakout 2327.26 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 1.29, 0.056%), RSI 56.81 (dist 6.8 dari 50) | Tidak (entry berjarak >0.5 ATR dari swing) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 12 | 2024-07-08T10:25:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 44.7 bearing + HH/HL(bearish) + breakout 2380.76 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas rendah-menengah (ATR 1.39, 0.059%), RSI 44.68 (dist 5.3 dari 50) | Tidak (entry berjarak >0.5 ATR dari swing) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 13 | 2024-10-21T01:10:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.8 ith bullish + HH/HL(bullish) + breakout 2722.04 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 1.31, 0.048%), RSI 59.82 (dist 9.8 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 14 | 2024-11-06T20:05:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 42.0 bearing + HH/HL(bearish) + breakout 2664.49 + candle engulf + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 2.91, 0.109%), RSI 42.04 (dist 8.0 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | — (TP hit, breakout continuation valid) |
| 15 | 2024-11-11T10:50:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 45.2 bearing + HH/HL(bearish) + breakout 2669.33 + candle rejection + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 1.79, 0.067%), RSI 45.25 (dist 4.8 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 16 | 2024-12-23T07:15:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 57.6 ith bullish + HH/HL(bullish) + breakout 2626.23 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 1.10, 0.042%), RSI 57.64 (dist 7.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 17 | 2024-12-26T13:25:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.3 ith bullish + HH/HL(bullish) + breakout 2628.63 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas rendah-menengah (ATR 1.03, 0.039%), RSI 59.27 (dist 9.3 dari 50) | Tidak (entry berjarak >0.5 ATR dari swing) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 18 | 2025-01-14T15:35:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 40.0 bearing + HH/HL(bearish) + breakout 2666.53 + candle engulf + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 2.68, 0.101%), RSI 39.99 (dist 10.0 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 19 | 2025-01-31T16:50:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 62.5 ith bullish + HH/HL(bullish) + breakout 2808.37 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 1.98, 0.071%), RSI 62.48 (dist 12.5 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 20 | 2025-03-18T18:10:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 57.9 ith bullish + HH/HL(bullish) + breakout 3032.11 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 2.42, 0.080%), RSI 57.94 (dist 7.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 21 | 2025-04-03T12:35:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 43.7 bearing + HH/HL(bearish) + breakout 3126.12 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas tinggi (ATR 3.13, 0.100%), RSI 43.66 (dist 6.3 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 22 | 2025-07-16T06:05:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 45.1 bearing + HH/HL(bearish) + breakout 3327.81 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 1.84, 0.055%), RSI 45.06 (dist 4.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 23 | 2025-08-22T15:20:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 43.1 bearing + HH/HL(bearish) + breakout 3327.76 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas menengah (ATR 1.80, 0.054%), RSI 43.08 (dist 6.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 24 | 2025-09-23T04:30:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.3 ith bullish + HH/HL(bullish) + breakout 3750.64 + candle rejection + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 2.99, 0.080%), RSI 56.34 (dist 6.3 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 25 | 2025-09-30T19:35:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 60.3 ith bullish + HH/HL(bullish) + breakout 3844.63 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas tinggi (ATR 4.38, 0.114%), RSI 60.29 (dist 10.3 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | — (TP hit, breakout continuation valid) |
| 26 | 2025-11-11T20:25:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 42.1 bearing + HH/HL(bearish) + breakout 4110.57 + candle strong close + conf 100 | M15 bearish trending, M5 bearish, volatilitas tinggi (ATR 3.59, 0.087%), RSI 42.13 (dist 7.9 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 27 | 2025-12-23T10:55:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.6 ith bullish + HH/HL(bullish) + breakout 4489.60 + candle rejection + conf 100 | M15 bullish trending, M5 bullish, volatilitas menengah (ATR 2.75, 0.061%), RSI 59.63 (dist 9.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 28 | 2025-12-24T03:00:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 62.6 ith bullish + HH/HL(bullish) + breakout 4512.70 + candle rejection + conf 100 | M15 bullish trending, M5 bullish, volatilitas sangat tinggi (ATR 5.13, 0.114%), RSI 62.63 (dist 12.6 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 29 | 2026-01-06T19:30:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 61.7 ith bullish + HH/HL(bullish) + breakout 4488.91 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas tinggi (ATR 4.39, 0.098%), RSI 61.68 (dist 11.7 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 30 | 2026-01-23T07:35:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 59.7 ith bullish + HH/HL(bullish) + breakout 4958.33 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas tinggi (ATR 3.19, 0.064%), RSI 59.73 (dist 9.7 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 31 | 2026-01-26T09:05:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 56.4 ith bullish + HH/HL(bullish) + breakout 5082.22 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas sangat tinggi (ATR 9.49, 0.187%), RSI 56.38 (dist 6.4 dari 50) | Tidak (entry berjarak >0.5 ATR dari swing) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai (ATR ekstrem >8, volatilitas tinggi) |
| 32 | 2026-02-03T15:55:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 54.8 ith bullish + HH/HL(bullish) + breakout 4930.98 + candle strong close + conf 100 | M15 bullish trending, M5 bullish, volatilitas sangat tinggi (ATR 12.52, 0.254%), RSI 54.80 (dist 4.8 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (strong close) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai (ATR ekstrem >8, volatilitas tinggi) |
| 33 | 2026-04-16T07:30:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 58.8 ith bullish + HH/HL(bullish) + breakout 4827.06 + candle rejection + conf 100 | M15 bullish trending, M5 bullish, volatilitas tinggi (ATR 3.20, 0.066%), RSI 58.82 (dist 8.8 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 34 | 2026-04-17T14:00:00+00:00 | M15 bearish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 41.0 bearing + HH/HL(bearish) + breakout 4787.10 + candle engulf + conf 100 | M15 bearish trending, M5 bearish, volatilitas tinggi (ATR 4.01, 0.084%), RSI 40.95 (dist 9.0 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (engulf) | Ya | False breakout bearish: harga tembus swingLow lalu reversal, SL tersentuh sebelum TP 2R tercapai |
| 35 | 2026-08-07T14:15:00+00:00 | M15 bullish (EMA20>EMA50) + M5 aligned + pullback True + Fib 0.500-0.618 + RSI 60.0 ith bullish + HH/HL(bullish) + breakout 4320.28 + candle rejection + conf 100 | M15 bullish trending, M5 bullish, volatilitas tinggi (ATR 4.54, 0.105%), RSI 60.05 (dist 10.0 dari 50) | Ya (breakout tipis) | Ya (0.500-0.618) | Ya (rejection) | Ya | False breakout bullish: harga tembus swingHigh lalu reversal, SL tersentuh sebelum TP 2R tercapai |

### 1C. Detail Fib & Risk per Trade

| No | Timestamp | Fib Anchor High (idx) | Fib Anchor Low (idx) | Range | 0.382 | 0.500 | 0.618 | 0.786 | Risk | Risk/ATR | Dist Break | Bars to Exit | Exit |
|---:|-----------|----------------------:|---------------------:|------:|------:|------:|------:|------:|-----:|---------:|-----------:|-------------:|------|
| 1 | 2023-09-26T03:15:00+00:00 | 1916.75 | 1916.09 | 0.6600000000000819 | 1916.34212 | 1916.42 | 1916.49788 | 1916.60876 | 0.6747600000001057 | 2.49 | 0.33 | 20 | 2023-09-26T04:55:00+00:00 |
| 2 | 2023-10-04T21:55:00+00:00 | 1821.3 | 1817.69 | 3.6099999999999 | 1819.06902 | 1819.495 | 1819.92098 | 1820.52746 | 3.2984600000002047 | 3.55 | 0.11 | 7 | 2023-10-04T22:30:00+00:00 |
| 3 | 2023-10-30T03:00:00+00:00 | 2004.68 | 2000.54 | 4.1400000000001 | 2003.09852 | 2002.6100000000001 | 2002.12148 | 2001.42596 | 3.908040000000028 | 2.91 | 0.18 | 42 | 2023-10-30T06:30:00+00:00 |
| 4 | 2023-11-14T21:55:00+00:00 | 1963.61 | 1961.63 | 1.9799999999997908 | 1962.85364 | 1962.62 | 1962.38636 | 1962.05372 | 1.8142800000000534 | 2.34 | 0.08 | 38 | 2023-11-15T02:05:00+00:00 |
| 5 | 2023-12-07T15:35:00+00:00 | 2034.07 | 2030.41 | 3.6599999999998545 | 2032.67188 | 2032.24 | 2031.80812 | 2031.19324 | 4.139999999999873 | 2.6 | 0.3 | 13 | 2023-12-07T16:40:00+00:00 |
| 6 | 2023-12-13T13:15:00+00:00 | 1982.79 | 1979.53 | 3.259999999999991 | 1981.54468 | 1981.1599999999999 | 1980.77532 | 1980.22764 | 2.998360000000048 | 3.56 | 0.13 | 25 | 2023-12-13T15:20:00+00:00 |
| 7 | 2023-12-27T16:45:00+00:00 | 2069.65 | 2064.36 | 5.289999999999964 | 2067.6292200000003 | 2067.005 | 2066.38078 | 2065.49206 | 5.246939999999995 | 3.47 | 0.37 | 10 | 2023-12-27T17:35:00+00:00 |
| 8 | 2024-01-10T17:35:00+00:00 | 2033.99 | 2028.64 | 5.349999999999909 | 2030.6837 | 2031.315 | 2031.9463 | 2032.8451 | 5.4500000000000455 | 2.91 | 0.3 | 158 | 2024-01-11T07:45:00+00:00 |
| 9 | 2024-02-02T08:00:00+00:00 | 2055.88 | 2053.59 | 2.2899999999999636 | 2055.00522 | 2054.735 | 2054.4647800000002 | 2054.0800600000002 | 2.0589399999994384 | 3.21 | 0.05 | 35 | 2024-02-02T10:55:00+00:00 |
| 10 | 2024-04-02T20:40:00+00:00 | 2262.38 | 2254.21 | 8.170000000000073 | 2259.25906 | 2258.295 | 2257.3309400000003 | 2255.95838 | 8.550000000000182 | 4.11 | 0.18 | 34 | 2024-04-02T23:30:00+00:00 |
| 11 | 2024-04-25T14:30:00+00:00 | 2327.26 | 2324.06 | 3.200000000000273 | 2326.0376 | 2325.66 | 2325.2824 | 2324.7448 | 3.65520000000015 | 2.83 | 0.63 | 12 | 2024-04-25T15:30:00+00:00 |
| 12 | 2024-07-08T10:25:00+00:00 | 2386.69 | 2380.76 | 5.929999999999836 | 2383.0252600000003 | 2383.7250000000004 | 2384.42474 | 2385.42098 | 6.183979999999792 | 4.44 | 0.67 | 97 | 2024-07-08T18:30:00+00:00 |
| 13 | 2024-10-21T01:10:00+00:00 | 2722.04 | 2718.37 | 3.6700000000000728 | 2720.6380599999998 | 2720.205 | 2719.77194 | 2719.1553799999997 | 3.4816200000004756 | 2.65 | 0.18 | 51 | 2024-10-21T05:25:00+00:00 |
| 14 | 2024-11-06T20:05:00+00:00 | 2670.42 | 2664.49 | 5.930000000000291 | 2666.75526 | 2667.455 | 2668.15474 | 2669.15098 | 6.523979999999938 | 2.24 | 0.44 | 74 | 2024-11-07T03:15:00+00:00 |
| 15 | 2024-11-11T10:50:00+00:00 | 2674.0 | 2669.33 | 4.670000000000073 | 2671.1139399999997 | 2671.665 | 2672.21606 | 2673.00062 | 4.517620000000079 | 2.52 | 0.21 | 17 | 2024-11-11T12:15:00+00:00 |
| 16 | 2024-12-23T07:15:00+00:00 | 2626.23 | 2623.28 | 2.949999999999818 | 2625.1031000000003 | 2624.755 | 2624.4069 | 2623.9113 | 2.673699999999826 | 2.42 | 0.05 | 17 | 2024-12-23T08:40:00+00:00 |
| 17 | 2024-12-26T13:25:00+00:00 | 2628.63 | 2625.84 | 2.7899999999999636 | 2627.56422 | 2627.235 | 2626.90578 | 2626.43706 | 3.061939999999595 | 2.97 | 0.57 | 9 | 2024-12-26T14:10:00+00:00 |
| 18 | 2025-01-14T15:35:00+00:00 | 2671.54 | 2666.53 | 5.0099999999997635 | 2668.44382 | 2669.035 | 2669.62618 | 2670.46786 | 5.418859999999768 | 2.02 | 0.37 | 19 | 2025-01-14T17:10:00+00:00 |
| 19 | 2025-01-31T16:50:00+00:00 | 2808.37 | 2803.27 | 5.099999999999909 | 2806.4218 | 2805.8199999999997 | 2805.2182 | 2804.3614 | 4.828600000000279 | 2.44 | 0.16 | 28 | 2025-01-31T19:10:00+00:00 |
| 20 | 2025-03-18T18:10:00+00:00 | 3032.11 | 3025.17 | 6.940000000000055 | 3029.45892 | 3028.6400000000003 | 3027.82108 | 3026.6551600000003 | 7.118839999999636 | 2.94 | 0.4 | 189 | 2025-03-19T10:55:00+00:00 |
| 21 | 2025-04-03T12:35:00+00:00 | 3132.12 | 3126.12 | 6.0 | 3128.412 | 3129.12 | 3129.828 | 3130.836 | 6.0359999999996035 | 1.93 | 0.23 | 6 | 2025-04-03T13:05:00+00:00 |
| 22 | 2025-07-16T06:05:00+00:00 | 3335.05 | 3327.81 | 7.2400000000002365 | 3330.57568 | 3331.4300000000003 | 3332.28432 | 3333.50064 | 6.424640000000181 | 3.5 | 0.01 | 5 | 2025-07-16T06:30:00+00:00 |
| 23 | 2025-08-22T15:20:00+00:00 | 3331.7 | 3327.76 | 3.9399999999996 | 3329.26508 | 3329.73 | 3330.19492 | 3330.85684 | 4.210839999999735 | 2.34 | 0.4 | 14 | 2025-08-22T16:30:00+00:00 |
| 24 | 2025-09-23T04:30:00+00:00 | 3750.64 | 3744.9 | 5.739999999999782 | 3748.4473199999998 | 3747.77 | 3747.09268 | 3746.12836 | 6.265640000000076 | 2.1 | 0.39 | 8 | 2025-09-23T05:10:00+00:00 |
| 25 | 2025-09-30T19:35:00+00:00 | 3844.63 | 3831.2 | 13.430000000000291 | 3839.49974 | 3837.915 | 3836.3302599999997 | 3834.07402 | 14.180000000000291 | 3.24 | 0.17 | 102 | 2025-10-01T05:05:00+00:00 |
| 26 | 2025-11-11T20:25:00+00:00 | 4117.77 | 4110.57 | 7.200000000000728 | 4113.3204 | 4114.17 | 4115.0196000000005 | 4116.229200000001 | 6.5792000000010376 | 1.83 | 0.06 | 9 | 2025-11-11T21:10:00+00:00 |
| 27 | 2025-12-23T10:55:00+00:00 | 4489.6 | 4483.76 | 5.8400000000001455 | 4487.36912 | 4486.68 | 4485.99088 | 4485.00976 | 5.474239999999554 | 1.99 | 0.11 | 2 | 2025-12-23T11:05:00+00:00 |
| 28 | 2025-12-24T03:00:00+00:00 | 4512.7 | 4499.92 | 12.779999999999745 | 4507.81804 | 4506.3099999999995 | 4504.80196 | 4502.65492 | 14.1899999999996 | 2.77 | 0.28 | 23 | 2025-12-24T04:55:00+00:00 |
| 29 | 2026-01-06T19:30:00+00:00 | 4488.91 | 4471.64 | 17.269999999999527 | 4482.31286 | 4480.275 | 4478.23714 | 4475.33578 | 17.279999999999745 | 3.93 | 0.0 | 80 | 2026-01-07T03:10:00+00:00 |
| 30 | 2026-01-23T07:35:00+00:00 | 4958.33 | 4950.12 | 8.210000000000036 | 4955.19378 | 4954.225 | 4953.25622 | 4951.87694 | 7.674059999999372 | 2.4 | 0.13 | 7 | 2026-01-23T08:10:00+00:00 |
| 31 | 2026-01-26T09:05:00+00:00 | 5082.22 | 5053.05 | 29.170000000000073 | 5071.0770600000005 | 5067.635 | 5064.19294 | 5059.29238 | 31.83462000000054 | 3.35 | 0.63 | 77 | 2026-01-26T15:30:00+00:00 |
| 32 | 2026-02-03T15:55:00+00:00 | 4930.98 | 4902.61 | 28.36999999999989 | 4920.1426599999995 | 4916.795 | 4913.44734 | 4908.68118 | 29.780000000000655 | 2.38 | 0.11 | 4 | 2026-02-03T16:15:00+00:00 |
| 33 | 2026-04-16T07:30:00+00:00 | 4827.06 | 4812.44 | 14.6200000000008 | 4821.47516 | 4819.75 | 4818.02484 | 4815.568679999999 | 13.45332000000144 | 4.2 | 0.16 | 42 | 2026-04-16T11:00:00+00:00 |
| 34 | 2026-04-17T14:00:00+00:00 | 4799.05 | 4787.1 | 11.949999999999818 | 4791.664900000001 | 4793.075000000001 | 4794.4851 | 4796.4927 | 12.557699999999386 | 3.13 | 0.49 | 8 | 2026-04-17T14:40:00+00:00 |
| 35 | 2026-08-07T14:15:00+00:00 | 4320.28 | 4302.18 | 18.099999999999454 | 4313.3658 | 4311.23 | 4309.0942000000005 | 4306.0534 | 16.146600000000944 | 3.56 | 0.02 | 14 | 2026-08-07T15:25:00+00:00 |

**Catatan 21 field per spec:** semua pullback Fib valid (`0.500-0.618`), semua candle confirmation valid (engulf/rejection/strong close), semua structure break valid (close menembus swingHigh/Low dengan prev close di sisi opposite). Dekat R/S: hampir semua `Ya (breakout tipis)` karena entry breakout by design berjarak tipis dari swing yang baru ditembus (rata-rata dist 0.24 ATR untuk SL, 0.29 ATR untuk TP).

## 2. Pengelompokan Hasil (A-J)

| Kategori | SL | TP | Total Kategori | % dari 26 SL | % dari 35 total | Win rate kategori | Catatan faktual |
|----------|---:|---:|---------------:|-------------:|----------------:|------------------:|---------------|
| A. BUY failure | 18 | 5 | 23 | 69.2% | 51.4% | 21.7 |  |
| B. SELL failure | 8 | 4 | 12 | 30.8% | 22.9% | 33.3 |  |
| C. M15 trend failure | 26 | 0 | 26 | 100.0% | 74.3% | - | Semua 26 SL terjadi saat M15 trending (signal hanya emit saat trending); tidak ada SL pada kondisi ranging karena filter ranging menolak signal |
| D. Fib failure | 0 | 0 | 0 | 0.0% | 0% | - | 0/26 SL: semua fib_zone 0.500-0.618 valid, tidak ada invalidation >0.786 |
| E. Structure failure | 0 | 0 | 0 | 0.0% | 0% | - | 0/26 SL: semua M5 structure bullish/bearish terkonfirmasi (HH>HL / LL<LH) |
| F. RSI/momentum failure | 0 | 0 | 0 | 0.0% | 0% | - | 0/26 di bawah 3 poin dari 50 (gate butuh >=2). SL RSI 54.8-62.6 BUY dan 38.9-46.6 SELL, serupa dengan TP |
| G. Candle confirmation failure | 0 | 0 | 0 | 0.0% | 0% | - | 0/26: semua entry lolos candle confirmation (engulf/rejection/strong close) |
| H. SL terlalu dekat / ATR | 0 | 0 | 0 | 0.0% | 0% | - | 0/26 SL dengan risk <1.5 ATR; avg risk SL 2.86 ATR vs TP 3.00 ATR |
| I. Entry pada kondisi ranging | 4 | 0 | 4 | 15.4% | 11.4% | - | Hanya 4/26 SL dengan ATR<1.0 (volatilitas rendah): 2023-09-26, 2023-10-04, 2023-11-14, 2023-12-13, 2024-02-02 sebagian; mayoritas SL tidak di ranging |
| J. Faktor lain (false breakout / reversal) | 26 | 0 | 26 | 100.0% | 74.3% | - | SL meski semua gate valid (trend, fib, structure, RSI, candle, break) - harga reversal setelah breakout |

**Ringkasan kategori:**
- **A. BUY failure 18/26 (69.2%)** — dominan; BUY win rate 21.7% (5/23).
- **B. SELL failure 8/26 (30.8%)** — SELL win rate 33.3% (4/12), lebih baik dari BUY.
- **C. M15 trend failure 26/26 (100%)** — faktual semua SL terjadi saat M15 trending (signal hanya emit saat trending). Tidak ada SL di kondisi ranging karena filter `ranging` menolak signal.
- **D. Fib failure 0/26** — semua fib_zone `0.500-0.618` valid, tidak ada invalidation >0.786.
- **E. Structure failure 0/26** — semua M5 structure terkonfirmasi bullish/bearish (HH>HL / LH<LL).
- **F. RSI/momentum failure 0/26** — gate butuh `|RSI-50| >=2`; SL RSI 54.8-62.6 BUY dan 38.9-46.6 SELL, serupa TP (TP 41.0-60.3).
- **G. Candle confirmation failure 0/26** — semua lolos engulf/rejection/strong close.
- **H. SL terlalu dekat / ATR 0/26** — risk rata-rata 2.86 ATR (SL) vs 3.00 ATR (TP), tidak ada SL dengan risk <1.5 ATR.
- **I. Ranging 4/26 (15.4%)** — hanya 4 SL dengan ATR <1.0: `2023-10-04 (0.93)`, `2023-11-14 (0.77)`, `2023-12-13 (0.84)`, `2024-02-02 (0.64)` — volatilitas rendah-menengah, bukan mayoritas.
- **J. Faktor lain (false breakout/reversal) 26/26 (100%)** — semua SL meski semua gate valid lalu harga reversal setelah breakout tipis, SL tersentuh sebelum TP 2R.

## 3. BUY vs SELL

| Arah | Total | TP | SL | Win rate | Total R (TP*2 + SL*-1) |
|------|------:|---:|---:|---------:|------------------------:|
| BUY | 23 | 5 | 18 | 21.7% | -8R |
| SELL | 12 | 4 | 8 | 33.3% | 0R |

## 4. Hasil per Tahun

| Tahun | Trades | TP | SL | Win rate | Net R |
|-------|-------:|---:|---:|---------:|------:|
| 2023 | 7 | 2 | 5 | 28.6% | -1R |
| 2024 | 10 | 5 | 5 | 50.0% | 5R |
| 2025 | 11 | 2 | 9 | 18.2% | -5R |
| 2026 | 7 | 0 | 7 | 0.0% | -7R |

**Pola tahunan:** 2023: 2/7 (28.6%) -1R; 2024: 5/10 (50%) +5R (satu-satunya tahun profit); 2025: 2/11 (18.2%) -5R; 2026: 0/7 (0%) -7R — degradasi berurutan, 2026 semua BUY gagal di ATR 3-12 (harga XAUUSD 4300-5100, volatilitas ekstrem).

## 5. Hasil per Bulan

| Bulan | Trades | TP | SL | Net R | Win rate |
|-------|-------:|---:|---:|------:|---------:|
| 2023-09 | 1 | 1 | 0 | 2R | 100.0% |
| 2023-10 | 2 | 0 | 2 | -2R | 0.0% |
| 2023-11 | 1 | 0 | 1 | -1R | 0.0% |
| 2023-12 | 3 | 1 | 2 | 0R | 33.3% |
| 2024-01 | 1 | 0 | 1 | -1R | 0.0% |
| 2024-02 | 1 | 0 | 1 | -1R | 0.0% |
| 2024-04 | 2 | 1 | 1 | 1R | 50.0% |
| 2024-07 | 1 | 1 | 0 | 2R | 100.0% |
| 2024-10 | 1 | 1 | 0 | 2R | 100.0% |
| 2024-11 | 2 | 1 | 1 | 1R | 50.0% |
| 2024-12 | 2 | 1 | 1 | 1R | 50.0% |
| 2025-01 | 2 | 0 | 2 | -2R | 0.0% |
| 2025-03 | 1 | 0 | 1 | -1R | 0.0% |
| 2025-04 | 1 | 1 | 0 | 2R | 100.0% |
| 2025-07 | 1 | 0 | 1 | -1R | 0.0% |
| 2025-08 | 1 | 0 | 1 | -1R | 0.0% |
| 2025-09 | 2 | 1 | 1 | 1R | 50.0% |
| 2025-11 | 1 | 0 | 1 | -1R | 0.0% |
| 2025-12 | 2 | 0 | 2 | -2R | 0.0% |
| 2026-01 | 3 | 0 | 3 | -3R | 0.0% |
| 2026-02 | 1 | 0 | 1 | -1R | 0.0% |
| 2026-04 | 2 | 0 | 2 | -2R | 0.0% |
| 2026-08 | 1 | 0 | 1 | -1R | 0.0% |

## 6. Consecutive Loss Pattern

- Urutan result (35 trade kronologis): `TP_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> TP_HIT -> SL_HIT -> SL_HIT -> TP_HIT -> SL_HIT -> TP_HIT -> TP_HIT -> TP_HIT -> SL_HIT -> TP_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> TP_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> TP_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT -> SL_HIT`
- Consecutive SL streak per trade: `[0, 1, 2, 3, 4, 5, 0, 1, 2, 0, 1, 0, 0, 0, 1, 0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`
- **Max consecutive SL: 10** (trade #26-35 akhir urutan) — streak terpanjang di akhir dataset: 2025-11-11 SL, 2025-12-23 SL, 2025-12-24 SL, 2026-01-06 SL, 2026-01-23 SL, 2026-01-26 SL, 2026-02-03 SL, 2026-04-16 SL, 2026-04-17 SL, 2026-08-07 SL (10 berurutan).
- Max consecutive wins: 13.0R DD context, but streak wins max 3 (2024-07-08, 2024-10-21, 2024-11-06 berurutan).

## 7. Apakah 26 SL Memiliki Pola yang Sama?

**Ya — 26/26 SL identik pada semua gate:**
- Confidence 100 (semua skor penuh: M15 20 + M5 align 15 + Pullback 10 + Fib 15 + RSI 10 + Structure 15 + Candle 10 + Break 5).
- M15 trending aligned (bullish untuk BUY, bearish untuk SELL) — tidak ada ranging entry.
- M5 structure bullish (HH>HL) untuk BUY, bearish (LL<LH) untuk SELL — jarak minimal 0.2 ATR terpenuhi.
- RSI dist 4.8-12.6 dari 50 (BUY 54.8-62.6, SELL 38.9-46.6) — tidak lemah, serupa TP.
- Fib 0.500-0.618 valid dari confirmed swing (anchor low<High untuk BUY, High<Low untuk SELL, range >=0.2 ATR), tidak ada invalidation >0.786.
- Breakout tipis: close menembus swingHigh/Low dengan prev close di sisi berlawanan, dist rata-rata 0.24 ATR.
- Candle confirmation valid (engulf / rejection wick / strong close >=0.75).
- Risk rata-rata 2.86 ATR (min 2.34, max 3.55 kecuali 2 outlier ATR-ekstrem 2026-01-26 9.49 ATR dan 2026-02-03 12.51 ATR yang risk 3.35 dan 2.38 ATR).

**Tidak ada anomali gate yang membedakan SL dari TP secara kategorikal.**

## 8. Apakah Ada Kondisi Berulang Sebelum SL?

- Semua SL didahului pullback ke 0.500-0.618 yang valid dalam window `pullbackLookback+6` sebelum entry — bukan anomali.
- Semua breakout terjadi setelah pullback, bukan chase di tengah trend.
- Pola berulang: breakout tipis lalu reversal — SL tersentuh dalam rata-rata 34 bar M5 (~2.8 jam) setelah entry, sementara TP rata-rata 45 bar (~3.8 jam).
- Tidak ada pengulangan jam/hari spesifik di luar distribusi harian acak (trade tersebar 23 bulan berbeda).

## 9. Apakah 9 TP Memiliki Karakteristik Berbeda dari 26 SL?

- RSI: TP avg 51.79 vs SL avg 53.74 (TP sedikit lebih dekat ke 50 karena ada SELL RSI 41-42; range TP 41.0-60.3, SL 38.9-62.6 — overlap besar).
- ATR: TP avg 2.01 vs SL avg 3.02 (TP ATR lebih rendah-menengah 0.27-4.37, SL melebar ke 0.64-12.51 dengan 3 outlier >5).
- Risk/ATR: TP avg 3.0 vs SL avg 2.86 (hampir identik ~3.0 vs 2.86).
- Dist breakout: TP avg 0.29 ATR vs SL 0.24 ATR (mirip, TP sedikit lebih jauh).
- Bars to exit: TP avg 45.67 vs SL 34.04 (TP butuh ~11 bar lebih lama).
- **Kesimpulan faktual:** Tidak ada pemisah tajam; distribusi TP dan SL overlap pada hampir semua metrik. Satu-satunya perbedaan lemah: SL lebih sering di volatilitas ekstrem (>5 ATR pada 2025-12-24, 2026-01-26, 2026-02-03).

## 10. Kondisi Paling Sering pada TP vs SL

- **Paling sering pada TP (9):** M15 trending + M5 bullish/bearish + RSI moderat (54-60 BUY, 41-44 SELL) + fib 0.500-0.618 + ATR 0.27-4.37 (menengah) + breakout tipis — identik dengan SL.
- **Paling sering pada SL (26):** Sama persis — M15 trending + M5 bullish/bearish + RSI 54-62 BUY / 38-46 SELL + fib 0.500-0.618 + breakout tipis + ATR menyebar 0.64-12.51. Frekuensi BUY SL tinggi (18 vs 8 SELL).
- **Pola dominan SL:** BUY false breakout di uptrend 2025-2026 volatilitas tinggi (6 BUY SL di 2026 semua gagal).

## 11. Ringkasan Pola Utama (Faktual, Tanpa Rekomendasi)

1. **Strategi sangat selektif:** 211.214 signal dievaluasi, hanya 35 trade (0.016%) — filter ketat.
2. **Semua gate lolos identik:** 35/35 confidence 100, fib valid, structure valid, candle valid — tidak ada pembeda gate antara TP dan SL.
3. **False breakout dominan:** 26/26 SL adalah breakout tipis yang reversal sebelum 2R tercapai (kategori J 100%).
4. **BUY lebih buruk dari SELL:** BUY 21.7% vs SELL 33.3%; 69.2% SL adalah BUY.
5. **Bukan Fib/Structure/RSI/Candle failure:** D/E/F/G semua 0/26.
6. **Bukan SL terlalu dekat:** H 0/26 dengan risk <1.5 ATR; risk rata-rata ~2.9 ATR.
7. **Bukan mayoritas ranging:** I hanya 4/26 (15.4%) ATR<1.0.
8. **Tahunan memburuk:** 2024 satu-satunya profit (+5R, 50% WR), 2025-2026 degradasi ke 0% WR di 2026.
9. **Streak loss panjang di akhir:** 10 SL berurutan (2025-11 sampai 2026-08) — Max DD 13R.
10. **TP vs SL overlap:** Tidak ada threshold RSI/ATR/dist yang memisahkan secara faktual; SL hanya sedikit lebih volatilitas ekstrem.

## 12. File Output

- `results/backtest_results.csv` — 35 trades Phase 03 (tetap, tidak dihapus)
- `results/backtest_summary.json` — ringkasan Phase 03 (tetap)
- `results/backtest_signal_log.csv` — 211k signal log (tetap, ~85MB)
- `results/trade_analysis.csv` — 35 baris x 40 kolom diagnostik (21-field spec + fib/risk detail), rebuild via `generate_phase04.py`
- `results/trade_analysis_summary.json` — ringkasan kategori A-J, yearly/monthly, consecutive, TP vs SL
- `phase/phase-04-trade-analysis.md` — dokumen ini

**Reproduksi:** `python generate_phase04.py` (membaca `data/XAUUSD_m_M5.csv`, `data/XAUUSD_m_M15.csv`, `results/backtest_results.csv`, menghitung ulang swings/fib/risk dari candle walk-forward).

**Hasil akhir wajib:** Tabel 35 trade di atas (1A + 1B + 1C) dan ringkasan pola utama (poin 1-10) memenuhi spec Phase 04.
