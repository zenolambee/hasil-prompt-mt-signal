# mt-signal

## XAUUSD EMA/RSI/ATR + Fibonacci market-structure module

`xauusd_strategy.py` is an independent strategy module (strategy `XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB`). It consumes completed M5 and M15 `Candle` sequences from the caller — no mock feed or broker connection.

```python
from xauusd_strategy import Candle, StrategyConfig, XAUUSDEmaRsiAtrStructure

strategy = XAUUSDEmaRsiAtrStructure(StrategyConfig())
result = strategy.evaluate(m5_candles, m15_candles, symbol="XAUUSD", spread=0.25)
print(result.to_dict())
# result fields include fib382/fib500/fib618/fib786, activeFibZone, fibExt1272/fibExt1618
```

**Configurable** via `StrategyConfig`: `emaFast/emaSlow`, `rsiPeriod`, `atrPeriod`, `atrSLMultiplier`, `riskReward`, `swingLookback`, `minimumStructureDistance`, `enableSpreadFilter`/`maxSpread`, `minimumConfidence`, ranging/crossover/pullback thresholds, and Fibonacci params `fibRetracementShallow` (0.382), `fibRetracementEntry1` (0.500), `fibRetracementEntry2` (0.618), `fibRetracementInvalidation` (0.786), `fibExtension1` (1.272), `fibExtension2` (1.618).

**Fibonacci anchor** comes from confirmed swing High/Low (completed pivots only). Entry requires price to have visited 0.500–0.618 in the recent pullback window; 0.382 is shallow (confidence boost only); beyond 0.786 invalidates. Extensions 1.272/1.618 are reported for reference; TP remains RR-based. Confidence = M15 20 + M5 15 + Pullback 10 + Fib 15 + RSI 10 + Structure 15 + Candle 10 + Break 5 = 100; high score never overrides a failed mandatory gate.

Signal is emitted only when all gates pass (`M15 trend + M5 alignment + structure + fib gate + RSI + candle confirmation + break + ATR/SL`); otherwise `NO SIGNAL` with a specific reason. Successful signals are recorded in `strategy.emitted` and duplicate candle evaluations are blocked (persist the list if needed across restarts).

Run tests:

```sh
python -m unittest -v
```
