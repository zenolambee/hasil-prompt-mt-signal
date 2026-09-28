Phase 05 selesai — 1 perubahan pola entry, no optimization, indikator tetap.

1. Pola baru retestMode=True
xauusd_strategy.py:StrategyConfig tambah retestMode=False, retestWindow=15, retestToleranceAtr=0.5. Saat True, broke bukan bar close tembus highs/lows tapi retest_found: breakout dalam window 15 bar terakhir + retest (low/close ∈ [lvl±0.5ATR] BUY, high/close SELL) sebelum entry. SL/structure/confirmation/M15 trend/RSI/Fib/RR1:2 tetap, mirrored BUY/SELL.
backtest_xauusd.py tambah _run_backtest_retest_fast (precompute EMA/RSI/ATR, incremental swings, early-exit trending/aligned/RSI/structure, scan O(window) per bar). Routing if retestMode -> _run_backtest_retest_fast.
test_retest_pattern.py 8 test: baseline emits, breakout tanpa retest = NO SIGNAL (BUY/SELL), breakout+retest+confirmation = SIGNAL (BUY/SELL), retest gagal = NO SIGNAL, mirrored, no look-ahead. 45 tests PASS (37 lama + 8 baru).
Walk-forward no look-ahead: m5[:N] + m15 ts ≤ m5[N].ts, validate_no_lookahead PASS.
2. Walk-forward full 212625 M5 / 70892 M15 (2023-08-28→2026-08-26)
Baseline (retestMode=False)	Retest (retestMode=True 15/0.5)	Δ
Trades	35	149	+114
TP / SL	9 / 26	50 / 99	+41 / +73
Win rate	25.71%	33.56%	+7.85pp
Total R	-8.0	+1.0	+9.0R
PF	0.6923	1.0101	+0.32
MaxDD	13.0R	30.0R	+17R
Max consec loss/win	10 / 3	11 / 5	—
BUY	5 TP / 18 SL (21.7%)	30 TP / 56 SL (34.9%)	—
SELL	4 TP / 8 SL (33.3%)	20 TP / 43 SL (31.7%)	—
Per tahun — baseline: 2023 7 (-1R 28.6%), 2024 10 (+5R 50%), 2025 11 (-5R 18.2%), 2026 7 (-7R 0%); retest: 2023 17 (+1R 35.3%), 2024 54 (+6R 37%), 2025 47 (+4R 36.2%), 2026 31 (-10R 22.6%). Elapsed baseline 78.3s, retest 289.4s.

Retest naikkan WR/PF/total R ke breakeven (+1R) tapi DD memburuk & trade 4× — perbaikan marjinal, belum edge kuat; 2026 whipsaw di kedua mode.

3. File & commit
phase/phase-05-entry-retest.md (117 line, 7 section: pola, hasil, perubahan kode, validasi, interpretasi, file, reproduksi)
results/ gitignored: backtest_retest_phase05.json + backtest_retest_trades.csv (149 trade) + backtest_baseline_phase05_ref.json (35 ref)
run_phase05_backtest.py (baseline vs retest runner)
Commit mt-signal = 5a36332 feat: Phase 05 retest-after-breakout pattern (baseline 35/-8R 25.7% vs retest 149/+1R 33.6%) — ahead origin by 1, git push origin main timeout (ChildProcess.kill powershell, intermittent network) — ulangi manual git push di E:\Repo Github\mt-signal.
Commit hasil-prompt-mt-signal (temp C:\Users\ACER\AppData\Local\Temp\hasil-phase) = 2d6bb65 docs: add Phase 05... — ahead origin by 1, sama timeout — ulangi git push di temp.
Cara reproduksi: python -m unittest -v (45) → python run_phase05_backtest.py → python backtest_xauusd.py --m5 data/XAUUSD_m_M5.csv --m15 data/XAUUSD_m_M15.csv --outdir results
