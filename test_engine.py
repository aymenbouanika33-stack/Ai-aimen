from app.engine import Candle, analyze, PaperBroker


def make_candles(n=80):
    rows = []
    price = 2000.0
    for i in range(n):
        # Gradual upward drift with small deterministic variation.
        o = price
        price += 0.8
        c = price
        rows.append({"time": f"2026-01-01T00:{i:02d}:00Z", "open": o, "high": c + 0.3, "low": o - 0.2, "close": c, "volume": 10})
    return rows


def test_analyze_waits_for_minimum_history():
    result = analyze(make_candles(20))
    assert result["action"] == "WAIT"


def test_analyze_returns_valid_action():
    result = analyze(make_candles())
    assert result["action"] in {"BUY", "SELL", "WAIT"}
    assert 0 <= result["score"] <= 100


def test_live_trading_is_not_part_of_paper_broker():
    broker = PaperBroker()
    assert broker.status()["live_trading_enabled"] is False


def test_candle_rejects_invalid_ohlc():
    try:
        Candle.from_dict({"time":"x", "open":10, "high":8, "low":9, "close":10})
        assert False, "expected invalid OHLC to fail"
    except ValueError:
        pass
