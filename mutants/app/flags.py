"""Simple feature flag registry with env overrides."""
from __future__ import annotations

import os

_DEFAULT_FLAGS = {
    "REC_DISABLE": "0",  # set to '1' to disable recommendation endpoint
    "QUIZ_DISABLE": "0",  # set to '1' to disable quiz endpoints
}
from inspect import signature as _mutmut_signature
from typing import Annotated, Callable, ClassVar

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

def x_is_enabled__mutmut_orig(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, "0"))
    return val != "1"

def x_is_enabled__mutmut_1(name: str) -> bool:
    val = None
    return val != "1"

def x_is_enabled__mutmut_2(name: str) -> bool:
    val = os.getenv(None, _DEFAULT_FLAGS.get(name, "0"))
    return val != "1"

def x_is_enabled__mutmut_3(name: str) -> bool:
    val = os.getenv(name, None)
    return val != "1"

def x_is_enabled__mutmut_4(name: str) -> bool:
    val = os.getenv(_DEFAULT_FLAGS.get(name, "0"))
    return val != "1"

def x_is_enabled__mutmut_5(name: str) -> bool:
    val = os.getenv(name, )
    return val != "1"

def x_is_enabled__mutmut_6(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(None, "0"))
    return val != "1"

def x_is_enabled__mutmut_7(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, None))
    return val != "1"

def x_is_enabled__mutmut_8(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get("0"))
    return val != "1"

def x_is_enabled__mutmut_9(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, ))
    return val != "1"

def x_is_enabled__mutmut_10(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, "XX0XX"))
    return val != "1"

def x_is_enabled__mutmut_11(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, "0"))
    return val == "1"

def x_is_enabled__mutmut_12(name: str) -> bool:
    val = os.getenv(name, _DEFAULT_FLAGS.get(name, "0"))
    return val != "XX1XX"

x_is_enabled__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_enabled__mutmut_1': x_is_enabled__mutmut_1, 
    'x_is_enabled__mutmut_2': x_is_enabled__mutmut_2, 
    'x_is_enabled__mutmut_3': x_is_enabled__mutmut_3, 
    'x_is_enabled__mutmut_4': x_is_enabled__mutmut_4, 
    'x_is_enabled__mutmut_5': x_is_enabled__mutmut_5, 
    'x_is_enabled__mutmut_6': x_is_enabled__mutmut_6, 
    'x_is_enabled__mutmut_7': x_is_enabled__mutmut_7, 
    'x_is_enabled__mutmut_8': x_is_enabled__mutmut_8, 
    'x_is_enabled__mutmut_9': x_is_enabled__mutmut_9, 
    'x_is_enabled__mutmut_10': x_is_enabled__mutmut_10, 
    'x_is_enabled__mutmut_11': x_is_enabled__mutmut_11, 
    'x_is_enabled__mutmut_12': x_is_enabled__mutmut_12
}

def is_enabled(*args, **kwargs):
    result = _mutmut_trampoline(x_is_enabled__mutmut_orig, x_is_enabled__mutmut_mutants, args, kwargs)
    return result 

is_enabled.__signature__ = _mutmut_signature(x_is_enabled__mutmut_orig)
x_is_enabled__mutmut_orig.__name__ = 'x_is_enabled'
