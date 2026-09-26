"""Standalone, candle-driven XAUUSD EMA/RSI/ATR + Fibonacci market-structure strategy."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Optional, Sequence


STRATEGY_NAME = "XAUUSD_EMA_RSI_ATR_STRUCTURE_FIB"


@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class StrategyConfig:
    emaFast: int = 20
    emaSlow: int = 50
    rsiPeriod: int = 14
    atrPeriod: int = 14
    atrSLMultiplier: float = 1.5
    riskReward: float = 2.0
    swingLookback: int = 3
    minimumStructureDistance: float = 0.2  # ATR units
    enableSpreadFilter: bool = True
    maxSpread: float = 0.5
    minimumConfidence: int = 70
    rangingAtrFraction: float = 0.15
    crossoverLookback: int = 8
    maxCrossovers: int = 2
    pullbackLookback: int = 8
    pullbackAtrTolerance: float = 0.35
    maxExtensionAtr: float = 1.0
    strongCloseFraction: float = 0.75
    fibRetracementShallow: float = 0.382
    fibRetracementEntry1: float = 0.500
    fibRetracementEntry2: float = 0.618
    fibRetracementInvalidation: float = 0.786
    fibExtension1: float = 1.272
    fibExtension2: float = 1.618


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NO SIGNAL"


@dataclass
class Signal:
    symbol: str
    signal: str
    strategy: str
    timeframe: str
    confirmation: str
    entry: Optional[float]
    sl: Optional[float]
    tp: Optional[float]
    rr: float
    ema20: Optional[float]
    ema50: Optional[float]
    rsi: Optional[float]
    atr: Optional[float]
    trend: str
    marketStructure: str
    confidence: int
    timestamp: datetime
    signalId: str
    reason: str
    m5Status: str = "unknown"
    pullback: bool = False
    fib382: Optional[float] = None
    fib500: Optional[float] = None
    fib618: Optional[float] = None
    fib786: Optional[float] = None
    activeFibZone: str = "n/a"
    fibExt1272: Optional[float] = None
    fibExt1618: Optional[float] = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result["timestamp"] = self.timestamp.isoformat()
        return result


def ema(values: Sequence[float], period: int) -> list[float]:
    if period <= 0:
        raise ValueError("EMA period must be positive")
    if len(values) < period:
        return []
    alpha = 2.0 / (period + 1)
    result = [sum(values[:period]) / period]
    for value in values[period:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return [float("nan")] * (period - 1) + result


def rsi(candles: Sequence[Candle], period: int) -> list[float]:
    closes = [c.close for c in candles]
    if period <= 0:
        raise ValueError("RSI period must be positive")
    if len(closes) <= period:
        return []
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(x, 0.0) for x in changes]
    losses = [max(-x, 0.0) for x in changes]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    values = [float("nan")] * period

    def value(gain: float, loss: float) -> float:
        if loss == 0:
            return 100.0 if gain else 50.0
        return 100 - 100 / (1 + gain / loss)

    values.append(value(avg_gain, avg_loss))
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        values.append(value(avg_gain, avg_loss))
    return values


def atr(candles: Sequence[Candle], period: int) -> list[float]:
    if period <= 0:
        raise ValueError("ATR period must be positive")
    if len(candles) <= period:
        return []
    ranges = [max(c.high - c.low, abs(c.high - candles[i - 1].close),
                  abs(c.low - candles[i - 1].close)) for i, c in enumerate(candles)]
    values = [float("nan")] * period
    current = sum(ranges[1:period + 1]) / period
    values.append(current)
    for tr in ranges[period + 1:]:
        current = (current * (period - 1) + tr) / period
        values.append(current)
    return values


def _swings(candles: Sequence[Candle], lookback: int) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    highs, lows = [], []
    for i in range(lookback, len(candles) - lookback):
        window = candles[i - lookback:i + lookback + 1]
        if candles[i].high == max(c.high for c in window) and sum(c.high == candles[i].high for c in window) == 1:
            highs.append((i, candles[i].high))
        if candles[i].low == min(c.low for c in window) and sum(c.low == candles[i].low for c in window) == 1:
            lows.append((i, candles[i].low))
    return highs, lows


def fibonacci_levels(high: float, low: float, cfg: StrategyConfig) -> dict[str, float]:
    rng = high - low
    if rng <= 0:
        return {}
    # BUY orientation (retracement from high down): level = high - fib * rng
    # For reporting generically we provide both interpretations via same math;
    # caller interprets according to direction.
    return {
        "0.382": high - cfg.fibRetracementShallow * rng,
        "0.500": high - cfg.fibRetracementEntry1 * rng,
        "0.618": high - cfg.fibRetracementEntry2 * rng,
        "0.786": high - cfg.fibRetracementInvalidation * rng,
    }


def fibonacci_levels_for_direction(high: float, low: float, cfg: StrategyConfig, direction: Direction) -> dict[str, float]:
    rng = high - low
    if rng <= 0:
        return {}
    if direction == Direction.BUY:
        return {
            "0.382": high - cfg.fibRetracementShallow * rng,
            "0.500": high - cfg.fibRetracementEntry1 * rng,
            "0.618": high - cfg.fibRetracementEntry2 * rng,
            "0.786": high - cfg.fibRetracementInvalidation * rng,
        }
    if direction == Direction.SELL:
        return {
            "0.382": low + cfg.fibRetracementShallow * rng,
            "0.500": low + cfg.fibRetracementEntry1 * rng,
            "0.618": low + cfg.fibRetracementEntry2 * rng,
            "0.786": low + cfg.fibRetracementInvalidation * rng,
        }
    return {}


def fibonacci_extensions(high: float, low: float, cfg: StrategyConfig, direction: Direction) -> dict[str, float]:
    rng = high - low
    if rng <= 0:
        return {}
    if direction == Direction.BUY:
        # extensions beyond high
        return {
            "1.272": low + cfg.fibExtension1 * rng,
            "1.618": low + cfg.fibExtension2 * rng,
        }
    if direction == Direction.SELL:
        return {
            "1.272": high - cfg.fibExtension1 * rng,
            "1.618": high - cfg.fibExtension2 * rng,
        }
    return {}


class XAUUSDEmaRsiAtrStructure:
    """Evaluate completed M5/M15 candles. No network/feed or synthetic data is used."""

    def __init__(self, config: StrategyConfig = StrategyConfig()):
        self.config = config
        self.emitted: list[dict] = []
        self._seen_candles: set[tuple[str, str, datetime]] = set()

    def evaluate(self, m5: Sequence[Candle], m15: Sequence[Candle], *,
                 symbol: str = "XAUUSD", spread: Optional[float] = None) -> Signal:
        cfg = self.config
        timestamp = m5[-1].timestamp if m5 else datetime.now(timezone.utc)
        empty = Signal(symbol, Direction.NONE.value, STRATEGY_NAME, "M5", "M15", None, None, None,
                       cfg.riskReward, None, None, None, None, "unknown", "unclear", 0,
                       timestamp, "", "Insufficient candle history.")
        required5 = max(cfg.emaSlow, cfg.rsiPeriod + 1, cfg.atrPeriod + 1, cfg.swingLookback * 2 + 3)
        if len(m5) < required5 or len(m15) < cfg.emaSlow + 1:
            return empty
        if cfg.enableSpreadFilter and (spread is None or spread > cfg.maxSpread or spread < 0):
            empty.reason = "Spread unavailable or above configured maximum."
            return empty

        closes5, closes15 = [c.close for c in m5], [c.close for c in m15]
        e20_5, e50_5 = ema(closes5, cfg.emaFast), ema(closes5, cfg.emaSlow)
        e20_15, e50_15 = ema(closes15, cfg.emaFast), ema(closes15, cfg.emaSlow)
        rsi_values, atr_values = rsi(m5, cfg.rsiPeriod), atr(m5, cfg.atrPeriod)
        e20, e50, value_rsi, value_atr = e20_5[-1], e50_5[-1], rsi_values[-1], atr_values[-1]
        trend_gap = e20_15[-1] - e50_15[-1]
        trend_atr_values = atr(m15, cfg.atrPeriod)
        trend_atr = trend_atr_values[-1] if trend_atr_values else 0.0
        crossovers = sum((e20_15[i] - e50_15[i]) * (e20_15[i - 1] - e50_15[i - 1]) <= 0
                         for i in range(max(1, len(e20_15) - cfg.crossoverLookback), len(e20_15)))
        if abs(trend_gap) <= max(trend_atr * cfg.rangingAtrFraction, 1e-12) or crossovers >= cfg.maxCrossovers:
            trend, direction = "ranging", Direction.NONE
        else:
            direction = Direction.BUY if trend_gap > 0 else Direction.SELL
            trend = "bullish" if direction == Direction.BUY else "bearish"

        highs, lows = _swings(m5[:-1], cfg.swingLookback)
        structure = "unclear"
        if len(highs) >= 2 and len(lows) >= 2:
            # evaluate most recent structure with required separation
            hh = highs[-1][1] > highs[-2][1] and highs[-1][1] - highs[-2][1] >= cfg.minimumStructureDistance * value_atr
            hl = lows[-1][1] > lows[-2][1] and lows[-1][1] - lows[-2][1] >= cfg.minimumStructureDistance * value_atr
            lh = highs[-1][1] < highs[-2][1] and highs[-2][1] - highs[-1][1] >= cfg.minimumStructureDistance * value_atr
            ll = lows[-1][1] < lows[-2][1] and lows[-2][1] - lows[-1][1] >= cfg.minimumStructureDistance * value_atr
            if hh and hl:
                structure = "bullish"
            elif lh and ll:
                structure = "bearish"

        bar = m5[-1]
        aligned = (e20 > e50 and bar.close > e50) if direction == Direction.BUY else (e20 < e50 and bar.close < e50) if direction != Direction.NONE else False
        recent_start = max(0, len(m5) - 1 - cfg.pullbackLookback)
        pullback = any(c.low <= max(e20_5[i], e50_5[i]) + cfg.pullbackAtrTolerance * value_atr and
                       c.high >= min(e20_5[i], e50_5[i]) - cfg.pullbackAtrTolerance * value_atr
                       for i, c in enumerate(m5[recent_start:], recent_start))
        rsi_ok = (value_rsi > 50 if direction == Direction.BUY else value_rsi < 50) if direction != Direction.NONE else False
        rsi_ok = rsi_ok and abs(value_rsi - 50) >= 2

        # --- Fibonacci anchor from confirmed swings ---
        fib_anchor_high: Optional[float] = None
        fib_anchor_low: Optional[float] = None
        fib_levels: dict[str, float] = {}
        fib_ext: dict[str, float] = {}
        fib_valid_anchor = False
        fib_in_entry_zone = False
        fib_shallow_zone = False
        fib_invalidated = False
        active_zone = "n/a"

        if direction != Direction.NONE and highs and lows:
            # Search most recent valid swing pair: BUY low -> high, SELL high -> low
            if direction == Direction.BUY:
                for hi, hv in reversed(highs):
                    for li, lv in reversed(lows):
                        if li < hi:
                            rng = hv - lv
                            if rng >= cfg.minimumStructureDistance * value_atr and rng > 0:
                                fib_anchor_high, fib_anchor_low = hv, lv
                                fib_valid_anchor = True
                                fib_levels = fibonacci_levels_for_direction(fib_anchor_high, fib_anchor_low, cfg, direction)
                                fib_ext = fibonacci_extensions(fib_anchor_high, fib_anchor_low, cfg, direction)
                            break
                    if fib_valid_anchor:
                        break
            elif direction == Direction.SELL:
                for li, lv in reversed(lows):
                    for hi, hv in reversed(highs):
                        if hi < li:
                            rng = hv - lv
                            if rng >= cfg.minimumStructureDistance * value_atr and rng > 0:
                                fib_anchor_high, fib_anchor_low = hv, lv
                                fib_valid_anchor = True
                                fib_levels = fibonacci_levels_for_direction(fib_anchor_high, fib_anchor_low, cfg, direction)
                                fib_ext = fibonacci_extensions(fib_anchor_high, fib_anchor_low, cfg, direction)
                            break
                    if fib_valid_anchor:
                        break

        if fib_valid_anchor:
            # Entry zone is a pullback area that should have been visited
            # recently; the breakout bar itself is above/below the swing and
            # therefore not expected to close inside the zone.
            eps = 1e-9
            fib_window = m5[max(0, len(m5) - 1 - cfg.pullbackLookback - 6): len(m5) - 1]
            if direction == Direction.BUY:
                upper = fib_levels["0.500"]
                lower = fib_levels["0.618"]
                shallow_upper = fib_levels["0.382"]
                invalid_level = fib_levels["0.786"]
                def _in_entry(c: Candle) -> bool:
                    return (lower - eps) <= c.close <= (upper + eps) or (lower - eps) <= c.low <= (upper + eps)
                def _in_shallow(c: Candle) -> bool:
                    return (lower - eps) <= c.close <= (shallow_upper + eps) or (lower - eps) <= c.low <= (shallow_upper + eps)
                fib_in_entry_zone = any(_in_entry(c) for c in fib_window)
                fib_shallow_zone = any(_in_shallow(c) for c in fib_window)
                fib_invalidated = any(c.close < invalid_level - eps for c in fib_window) or bar.close < invalid_level - eps
                if fib_in_entry_zone and not fib_invalidated:
                    active_zone = "0.500-0.618"
                elif fib_shallow_zone and not fib_invalidated:
                    active_zone = "0.382 (shallow)"
                elif fib_invalidated:
                    active_zone = "invalid (>0.786 deep)"
                else:
                    active_zone = "outside fib zone"
            elif direction == Direction.SELL:
                lower = fib_levels["0.500"]
                upper = fib_levels["0.618"]
                shallow_low = fib_levels["0.382"]
                invalid_level = fib_levels["0.786"]
                def _in_entry_s(c: Candle) -> bool:
                    return (lower - eps) <= c.close <= (upper + eps) or (lower - eps) <= c.high <= (upper + eps)
                def _in_shallow_s(c: Candle) -> bool:
                    return (shallow_low - eps) <= c.close <= (upper + eps) or (shallow_low - eps) <= c.high <= (upper + eps)
                fib_in_entry_zone = any(_in_entry_s(c) for c in fib_window)
                fib_shallow_zone = any(_in_shallow_s(c) for c in fib_window)
                fib_invalidated = any(c.close > invalid_level + eps for c in fib_window) or bar.close > invalid_level + eps
                if fib_in_entry_zone and not fib_invalidated:
                    active_zone = "0.500-0.618"
                elif fib_shallow_zone and not fib_invalidated:
                    active_zone = "0.382 (shallow)"
                elif fib_invalidated:
                    active_zone = "invalid (>0.786 deep)"
                else:
                    active_zone = "outside fib zone"

        # Structure breakout & confirmation & SL
        if direction == Direction.BUY:
            broke = bool(highs and bar.close > highs[-1][1] and m5[-2].close <= highs[-1][1])
            structure_ok = structure == "bullish" and bool(lows)
            confirmation = self._bullish_confirmation(m5[-1], m5[-2], cfg.strongCloseFraction)
            swing = lows[-1][1] if lows else bar.low
            sl_atr = bar.close - cfg.atrSLMultiplier * value_atr
            # SL considers swing and invalidation; take most protective (lowest)
            candidates = [swing, sl_atr]
            if fib_valid_anchor and "0.786" in fib_levels:
                # invalidation slightly beyond fib786
                candidates.append(fib_levels["0.786"] - 0.1 * (fib_anchor_high - fib_anchor_low) if fib_anchor_high else fib_levels["0.786"])
            sl = min(candidates)
        elif direction == Direction.SELL:
            broke = bool(lows and bar.close < lows[-1][1] and m5[-2].close >= lows[-1][1])
            structure_ok = structure == "bearish" and bool(highs)
            confirmation = self._bearish_confirmation(m5[-1], m5[-2], cfg.strongCloseFraction)
            swing = highs[-1][1] if highs else bar.high
            sl_atr = bar.close + cfg.atrSLMultiplier * value_atr
            candidates = [swing, sl_atr]
            if fib_valid_anchor and "0.786" in fib_levels:
                candidates.append(fib_levels["0.786"] + 0.1 * (fib_anchor_high - fib_anchor_low) if fib_anchor_high else fib_levels["0.786"])
            sl = max(candidates)
        else:
            broke = structure_ok = confirmation = False
            sl = None

        extension = abs(bar.close - e20) <= cfg.maxExtensionAtr * value_atr
        # fib gate: require valid anchor, in entry zone, not invalidated
        fib_gate = fib_valid_anchor and fib_in_entry_zone and not fib_invalidated

        # Confidence breakdown per spec
        # M15 20, M5 align 15, Pullback 10, Fib 15, RSI 10, Structure 15, Candle 10, Break 5 =100
        fib_score = 15 if fib_in_entry_zone and not fib_invalidated else (7 if fib_shallow_zone and not fib_invalidated else 0)
        scores = [
            20 if direction != Direction.NONE else 0,
            15 if aligned else 0,
            10 if pullback else 0,
            fib_score,
            10 if rsi_ok else 0,
            15 if structure_ok and broke else 0,
            10 if confirmation else 0,
            5 if broke else 0,
        ]
        confidence = sum(scores)
        same_candle = (symbol, "M5", timestamp)
        stop_valid = sl is not None and ((direction == Direction.BUY and sl < bar.close) or (direction == Direction.SELL and sl > bar.close))

        # Mandatory conditions (fib gate is mandatory)
        conditions = [direction != Direction.NONE, aligned, pullback, rsi_ok, structure_ok, broke, confirmation, extension, fib_gate, stop_valid]
        reasons = []
        if direction == Direction.NONE:
            reasons.append("M15 trend ranging")
        if not aligned:
            reasons.append("M5 belum searah M15")
        if not pullback:
            reasons.append("pullback ke EMA belum terjadi")
        if not fib_valid_anchor:
            reasons.append("Fibonacci anchor tidak valid")
        elif fib_invalidated:
            reasons.append("Retracement melewati 0.786")
        elif not fib_in_entry_zone:
            if fib_shallow_zone:
                reasons.append("Harga di shallow 0.382 belum di 0.500-0.618")
            else:
                reasons.append("Harga tidak berada pada area retracement yang valid")
        if not rsi_ok:
            reasons.append("RSI belum menunjukkan momentum")
        if not structure_ok or not broke:
            reasons.append("Market structure belum confirmed / breakout belum valid")
        if not confirmation:
            reasons.append("candle confirmation belum terbentuk")
        if not extension:
            reasons.append("harga terlalu jauh dari EMA setelah breakout")
        if not stop_valid:
            reasons.append("ATR/swing stop tidak valid")
        if confidence < cfg.minimumConfidence:
            reasons.append("confidence di bawah minimum")

        valid = all(conditions) and confidence >= cfg.minimumConfidence and same_candle not in self._seen_candles
        entry = bar.close if valid else None
        take_profit = None
        if valid and sl is not None:
            if direction == Direction.BUY:
                take_profit = entry + (entry - sl) * cfg.riskReward  # type: ignore
            else:
                take_profit = entry - (sl - entry) * cfg.riskReward  # type: ignore

        signal = Signal(symbol, direction.value if valid else Direction.NONE.value, STRATEGY_NAME,
                        "M5", "M15", entry, sl if valid else None, take_profit, cfg.riskReward,
                        e20, e50, value_rsi, value_atr, trend, structure, confidence, timestamp,
                        "", "Conditions confirmed." if valid else "NO SIGNAL — " + "; ".join(reasons),
                        "aligned" if aligned else "opposed", pullback,
                        fib_levels.get("0.382"), fib_levels.get("0.500"), fib_levels.get("0.618"), fib_levels.get("0.786"),
                        active_zone, fib_ext.get("1.272"), fib_ext.get("1.618"))
        if valid:
            self._seen_candles.add(same_candle)
            identity = f"{symbol}|M5|{timestamp.isoformat()}|{signal.signal}|{entry:.8f}|{sl:.8f}|{take_profit:.8f}|{STRATEGY_NAME}"
            signal.signalId = hashlib.sha256(identity.encode()).hexdigest()[:20]
            self.emitted.append({"signalId": signal.signalId, "symbol": symbol, "timeframe": "M5",
                                 "timestamp": timestamp.isoformat(), "direction": signal.signal,
                                 "entry": entry, "SL": sl, "TP": take_profit,
                                 "strategyName": STRATEGY_NAME})
        return signal

    @staticmethod
    def _bullish_confirmation(current: Candle, previous: Candle, fraction: float) -> bool:
        span = current.high - current.low
        if span <= 0:
            return False
        engulf = current.close > current.open and previous.close < previous.open and current.close >= previous.open and current.open <= previous.close
        rejection = current.close > current.open and min(current.open, current.close) - current.low >= abs(current.close - current.open)
        strong = current.close > current.open and (current.close - current.low) / span >= fraction
        return engulf or rejection or strong

    @staticmethod
    def _bearish_confirmation(current: Candle, previous: Candle, fraction: float) -> bool:
        span = current.high - current.low
        if span <= 0:
            return False
        engulf = current.close < current.open and previous.close > previous.open and current.close <= previous.open and current.open >= previous.close
        rejection = current.close < current.open and current.high - max(current.open, current.close) >= abs(current.close - current.open)
        strong = current.close < current.open and (current.high - current.close) / span >= fraction
        return engulf or rejection or strong


__all__ = ["Candle", "Direction", "Signal", "StrategyConfig", "XAUUSDEmaRsiAtrStructure",
           "STRATEGY_NAME", "ema", "rsi", "atr", "fibonacci_levels", "fibonacci_levels_for_direction", "fibonacci_extensions"]
