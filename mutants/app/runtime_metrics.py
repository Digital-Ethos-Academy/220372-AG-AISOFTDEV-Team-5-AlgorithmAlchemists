"""In-memory runtime metrics aggregator."""
from __future__ import annotations

import threading
import time
from inspect import signature as _mutmut_signature
from typing import Annotated, Callable, ClassVar, Dict

MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class _Aggregator:
    def xǁ_Aggregatorǁ__init____mutmut_orig(self) -> None:
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = {}
        self._durations: Dict[str, list[float]] = {}
        self._start_time = time.time()
    def xǁ_Aggregatorǁ__init____mutmut_1(self) -> None:
        self._lock = None
        self._counts: Dict[str, int] = {}
        self._durations: Dict[str, list[float]] = {}
        self._start_time = time.time()
    def xǁ_Aggregatorǁ__init____mutmut_2(self) -> None:
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = None
        self._durations: Dict[str, list[float]] = {}
        self._start_time = time.time()
    def xǁ_Aggregatorǁ__init____mutmut_3(self) -> None:
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = {}
        self._durations: Dict[str, list[float]] = None
        self._start_time = time.time()
    def xǁ_Aggregatorǁ__init____mutmut_4(self) -> None:
        self._lock = threading.Lock()
        self._counts: Dict[str, int] = {}
        self._durations: Dict[str, list[float]] = {}
        self._start_time = None
    
    xǁ_Aggregatorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁ_Aggregatorǁ__init____mutmut_1': xǁ_Aggregatorǁ__init____mutmut_1, 
        'xǁ_Aggregatorǁ__init____mutmut_2': xǁ_Aggregatorǁ__init____mutmut_2, 
        'xǁ_Aggregatorǁ__init____mutmut_3': xǁ_Aggregatorǁ__init____mutmut_3, 
        'xǁ_Aggregatorǁ__init____mutmut_4': xǁ_Aggregatorǁ__init____mutmut_4
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁ_Aggregatorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁ_Aggregatorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁ_Aggregatorǁ__init____mutmut_orig)
    xǁ_Aggregatorǁ__init____mutmut_orig.__name__ = 'xǁ_Aggregatorǁ__init__'

    def xǁ_Aggregatorǁrecord__mutmut_orig(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_1(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = None
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_2(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) - 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_3(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(None, 0) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_4(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, None) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_5(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(0) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_6(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, ) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_7(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 1) + 1
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_8(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 2
            self._durations.setdefault(path, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_9(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(path, []).append(None)

    def xǁ_Aggregatorǁrecord__mutmut_10(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(None, []).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_11(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(path, None).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_12(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault([]).append(duration_ms)

    def xǁ_Aggregatorǁrecord__mutmut_13(self, path: str, duration_ms: float) -> None:
        with self._lock:
            self._counts[path] = self._counts.get(path, 0) + 1
            self._durations.setdefault(path, ).append(duration_ms)
    
    xǁ_Aggregatorǁrecord__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁ_Aggregatorǁrecord__mutmut_1': xǁ_Aggregatorǁrecord__mutmut_1, 
        'xǁ_Aggregatorǁrecord__mutmut_2': xǁ_Aggregatorǁrecord__mutmut_2, 
        'xǁ_Aggregatorǁrecord__mutmut_3': xǁ_Aggregatorǁrecord__mutmut_3, 
        'xǁ_Aggregatorǁrecord__mutmut_4': xǁ_Aggregatorǁrecord__mutmut_4, 
        'xǁ_Aggregatorǁrecord__mutmut_5': xǁ_Aggregatorǁrecord__mutmut_5, 
        'xǁ_Aggregatorǁrecord__mutmut_6': xǁ_Aggregatorǁrecord__mutmut_6, 
        'xǁ_Aggregatorǁrecord__mutmut_7': xǁ_Aggregatorǁrecord__mutmut_7, 
        'xǁ_Aggregatorǁrecord__mutmut_8': xǁ_Aggregatorǁrecord__mutmut_8, 
        'xǁ_Aggregatorǁrecord__mutmut_9': xǁ_Aggregatorǁrecord__mutmut_9, 
        'xǁ_Aggregatorǁrecord__mutmut_10': xǁ_Aggregatorǁrecord__mutmut_10, 
        'xǁ_Aggregatorǁrecord__mutmut_11': xǁ_Aggregatorǁrecord__mutmut_11, 
        'xǁ_Aggregatorǁrecord__mutmut_12': xǁ_Aggregatorǁrecord__mutmut_12, 
        'xǁ_Aggregatorǁrecord__mutmut_13': xǁ_Aggregatorǁrecord__mutmut_13
    }
    
    def record(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁ_Aggregatorǁrecord__mutmut_orig"), object.__getattribute__(self, "xǁ_Aggregatorǁrecord__mutmut_mutants"), args, kwargs, self)
        return result 
    
    record.__signature__ = _mutmut_signature(xǁ_Aggregatorǁrecord__mutmut_orig)
    xǁ_Aggregatorǁrecord__mutmut_orig.__name__ = 'xǁ_Aggregatorǁrecord'

    def xǁ_Aggregatorǁsnapshot__mutmut_orig(self) -> Dict[str, dict]:
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

    def xǁ_Aggregatorǁsnapshot__mutmut_1(self) -> Dict[str, dict]:
        with self._lock:
            data = None
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

    def xǁ_Aggregatorǁsnapshot__mutmut_2(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = None
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

    def xǁ_Aggregatorǁsnapshot__mutmut_3(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(None, [])
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

    def xǁ_Aggregatorǁsnapshot__mutmut_4(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, None)
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

    def xǁ_Aggregatorǁsnapshot__mutmut_5(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get([])
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

    def xǁ_Aggregatorǁsnapshot__mutmut_6(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, )
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

    def xǁ_Aggregatorǁsnapshot__mutmut_7(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = None
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

    def xǁ_Aggregatorǁsnapshot__mutmut_8(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(None, 2) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_9(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), None) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_10(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(2) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_11(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), ) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_12(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) * len(durations), 2) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_13(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(None) / len(durations), 2) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_14(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 3) if durations else 0.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_15(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 1.0
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

    def xǁ_Aggregatorǁsnapshot__mutmut_16(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = None
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_17(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 1.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_18(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = None
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_19(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(None)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_20(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = None
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_21(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) + 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_22(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(None) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_23(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) / 0.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_24(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 1.95) - 1
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_25(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 2
                    p95 = sorted_d[max(idx, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_26(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = None
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_27(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(None, 0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_28(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, None)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_29(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(0)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_30(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, )]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_31(self) -> Dict[str, dict]:
        with self._lock:
            data = {}
            for path, count in self._counts.items():
                durations = self._durations.get(path, [])
                avg = round(sum(durations) / len(durations), 2) if durations else 0.0
                p95 = 0.0
                if durations:
                    sorted_d = sorted(durations)
                    idx = int(len(sorted_d) * 0.95) - 1
                    p95 = sorted_d[max(idx, 1)]
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_32(self) -> Dict[str, dict]:
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
                data[path] = None
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_33(self) -> Dict[str, dict]:
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
                data[path] = {"XXcountXX": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_34(self) -> Dict[str, dict]:
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
                data[path] = {"COUNT": count, "avg_ms": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_35(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "XXavg_msXX": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_36(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "AVG_MS": avg, "p95_ms": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_37(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "XXp95_msXX": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_38(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "P95_MS": round(p95, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_39(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(None, 2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_40(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, None)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_41(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(2)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_42(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, )}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_43(self) -> Dict[str, dict]:
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
                data[path] = {"count": count, "avg_ms": avg, "p95_ms": round(p95, 3)}
            return {
                "uptime_seconds": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_44(self) -> Dict[str, dict]:
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
                "XXuptime_secondsXX": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_45(self) -> Dict[str, dict]:
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
                "UPTIME_SECONDS": round(time.time() - self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_46(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(None, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_47(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(time.time() - self._start_time, None),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_48(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_49(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(time.time() - self._start_time, ),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_50(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(time.time() + self._start_time, 2),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_51(self) -> Dict[str, dict]:
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
                "uptime_seconds": round(time.time() - self._start_time, 3),
                "endpoints": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_52(self) -> Dict[str, dict]:
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
                "XXendpointsXX": data,
            }

    def xǁ_Aggregatorǁsnapshot__mutmut_53(self) -> Dict[str, dict]:
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
                "ENDPOINTS": data,
            }
    
    xǁ_Aggregatorǁsnapshot__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁ_Aggregatorǁsnapshot__mutmut_1': xǁ_Aggregatorǁsnapshot__mutmut_1, 
        'xǁ_Aggregatorǁsnapshot__mutmut_2': xǁ_Aggregatorǁsnapshot__mutmut_2, 
        'xǁ_Aggregatorǁsnapshot__mutmut_3': xǁ_Aggregatorǁsnapshot__mutmut_3, 
        'xǁ_Aggregatorǁsnapshot__mutmut_4': xǁ_Aggregatorǁsnapshot__mutmut_4, 
        'xǁ_Aggregatorǁsnapshot__mutmut_5': xǁ_Aggregatorǁsnapshot__mutmut_5, 
        'xǁ_Aggregatorǁsnapshot__mutmut_6': xǁ_Aggregatorǁsnapshot__mutmut_6, 
        'xǁ_Aggregatorǁsnapshot__mutmut_7': xǁ_Aggregatorǁsnapshot__mutmut_7, 
        'xǁ_Aggregatorǁsnapshot__mutmut_8': xǁ_Aggregatorǁsnapshot__mutmut_8, 
        'xǁ_Aggregatorǁsnapshot__mutmut_9': xǁ_Aggregatorǁsnapshot__mutmut_9, 
        'xǁ_Aggregatorǁsnapshot__mutmut_10': xǁ_Aggregatorǁsnapshot__mutmut_10, 
        'xǁ_Aggregatorǁsnapshot__mutmut_11': xǁ_Aggregatorǁsnapshot__mutmut_11, 
        'xǁ_Aggregatorǁsnapshot__mutmut_12': xǁ_Aggregatorǁsnapshot__mutmut_12, 
        'xǁ_Aggregatorǁsnapshot__mutmut_13': xǁ_Aggregatorǁsnapshot__mutmut_13, 
        'xǁ_Aggregatorǁsnapshot__mutmut_14': xǁ_Aggregatorǁsnapshot__mutmut_14, 
        'xǁ_Aggregatorǁsnapshot__mutmut_15': xǁ_Aggregatorǁsnapshot__mutmut_15, 
        'xǁ_Aggregatorǁsnapshot__mutmut_16': xǁ_Aggregatorǁsnapshot__mutmut_16, 
        'xǁ_Aggregatorǁsnapshot__mutmut_17': xǁ_Aggregatorǁsnapshot__mutmut_17, 
        'xǁ_Aggregatorǁsnapshot__mutmut_18': xǁ_Aggregatorǁsnapshot__mutmut_18, 
        'xǁ_Aggregatorǁsnapshot__mutmut_19': xǁ_Aggregatorǁsnapshot__mutmut_19, 
        'xǁ_Aggregatorǁsnapshot__mutmut_20': xǁ_Aggregatorǁsnapshot__mutmut_20, 
        'xǁ_Aggregatorǁsnapshot__mutmut_21': xǁ_Aggregatorǁsnapshot__mutmut_21, 
        'xǁ_Aggregatorǁsnapshot__mutmut_22': xǁ_Aggregatorǁsnapshot__mutmut_22, 
        'xǁ_Aggregatorǁsnapshot__mutmut_23': xǁ_Aggregatorǁsnapshot__mutmut_23, 
        'xǁ_Aggregatorǁsnapshot__mutmut_24': xǁ_Aggregatorǁsnapshot__mutmut_24, 
        'xǁ_Aggregatorǁsnapshot__mutmut_25': xǁ_Aggregatorǁsnapshot__mutmut_25, 
        'xǁ_Aggregatorǁsnapshot__mutmut_26': xǁ_Aggregatorǁsnapshot__mutmut_26, 
        'xǁ_Aggregatorǁsnapshot__mutmut_27': xǁ_Aggregatorǁsnapshot__mutmut_27, 
        'xǁ_Aggregatorǁsnapshot__mutmut_28': xǁ_Aggregatorǁsnapshot__mutmut_28, 
        'xǁ_Aggregatorǁsnapshot__mutmut_29': xǁ_Aggregatorǁsnapshot__mutmut_29, 
        'xǁ_Aggregatorǁsnapshot__mutmut_30': xǁ_Aggregatorǁsnapshot__mutmut_30, 
        'xǁ_Aggregatorǁsnapshot__mutmut_31': xǁ_Aggregatorǁsnapshot__mutmut_31, 
        'xǁ_Aggregatorǁsnapshot__mutmut_32': xǁ_Aggregatorǁsnapshot__mutmut_32, 
        'xǁ_Aggregatorǁsnapshot__mutmut_33': xǁ_Aggregatorǁsnapshot__mutmut_33, 
        'xǁ_Aggregatorǁsnapshot__mutmut_34': xǁ_Aggregatorǁsnapshot__mutmut_34, 
        'xǁ_Aggregatorǁsnapshot__mutmut_35': xǁ_Aggregatorǁsnapshot__mutmut_35, 
        'xǁ_Aggregatorǁsnapshot__mutmut_36': xǁ_Aggregatorǁsnapshot__mutmut_36, 
        'xǁ_Aggregatorǁsnapshot__mutmut_37': xǁ_Aggregatorǁsnapshot__mutmut_37, 
        'xǁ_Aggregatorǁsnapshot__mutmut_38': xǁ_Aggregatorǁsnapshot__mutmut_38, 
        'xǁ_Aggregatorǁsnapshot__mutmut_39': xǁ_Aggregatorǁsnapshot__mutmut_39, 
        'xǁ_Aggregatorǁsnapshot__mutmut_40': xǁ_Aggregatorǁsnapshot__mutmut_40, 
        'xǁ_Aggregatorǁsnapshot__mutmut_41': xǁ_Aggregatorǁsnapshot__mutmut_41, 
        'xǁ_Aggregatorǁsnapshot__mutmut_42': xǁ_Aggregatorǁsnapshot__mutmut_42, 
        'xǁ_Aggregatorǁsnapshot__mutmut_43': xǁ_Aggregatorǁsnapshot__mutmut_43, 
        'xǁ_Aggregatorǁsnapshot__mutmut_44': xǁ_Aggregatorǁsnapshot__mutmut_44, 
        'xǁ_Aggregatorǁsnapshot__mutmut_45': xǁ_Aggregatorǁsnapshot__mutmut_45, 
        'xǁ_Aggregatorǁsnapshot__mutmut_46': xǁ_Aggregatorǁsnapshot__mutmut_46, 
        'xǁ_Aggregatorǁsnapshot__mutmut_47': xǁ_Aggregatorǁsnapshot__mutmut_47, 
        'xǁ_Aggregatorǁsnapshot__mutmut_48': xǁ_Aggregatorǁsnapshot__mutmut_48, 
        'xǁ_Aggregatorǁsnapshot__mutmut_49': xǁ_Aggregatorǁsnapshot__mutmut_49, 
        'xǁ_Aggregatorǁsnapshot__mutmut_50': xǁ_Aggregatorǁsnapshot__mutmut_50, 
        'xǁ_Aggregatorǁsnapshot__mutmut_51': xǁ_Aggregatorǁsnapshot__mutmut_51, 
        'xǁ_Aggregatorǁsnapshot__mutmut_52': xǁ_Aggregatorǁsnapshot__mutmut_52, 
        'xǁ_Aggregatorǁsnapshot__mutmut_53': xǁ_Aggregatorǁsnapshot__mutmut_53
    }
    
    def snapshot(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁ_Aggregatorǁsnapshot__mutmut_orig"), object.__getattribute__(self, "xǁ_Aggregatorǁsnapshot__mutmut_mutants"), args, kwargs, self)
        return result 
    
    snapshot.__signature__ = _mutmut_signature(xǁ_Aggregatorǁsnapshot__mutmut_orig)
    xǁ_Aggregatorǁsnapshot__mutmut_orig.__name__ = 'xǁ_Aggregatorǁsnapshot'


aggregator = _Aggregator()