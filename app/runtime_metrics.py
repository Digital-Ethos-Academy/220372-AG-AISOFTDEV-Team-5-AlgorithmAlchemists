"""In-memory runtime metrics aggregator."""
from __future__ import annotations

import threading
import time
from typing import Dict


class _Aggregator:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = {}
        self._durations: Dict[str, list[float]] = {}
        self._start_time = time.time()

    def record(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def snapshot(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }


aggregator = _Aggregator()