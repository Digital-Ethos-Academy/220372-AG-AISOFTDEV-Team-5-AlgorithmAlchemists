"""Lightweight settings loader (avoids pydantic-settings dependency)."""
from __future__ import annotations

import os
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


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


def x__flag__mutmut_orig(name: str, default: str) -> bool:
    return os.getenv(name, default) == "1"


def x__flag__mutmut_1(name: str, default: str) -> bool:
    return os.getenv(None, default) == "1"


def x__flag__mutmut_2(name: str, default: str) -> bool:
    return os.getenv(name, None) == "1"


def x__flag__mutmut_3(name: str, default: str) -> bool:
    return os.getenv(default) == "1"


def x__flag__mutmut_4(name: str, default: str) -> bool:
    return os.getenv(name, ) == "1"


def x__flag__mutmut_5(name: str, default: str) -> bool:
    return os.getenv(name, default) != "1"


def x__flag__mutmut_6(name: str, default: str) -> bool:
    return os.getenv(name, default) == "XX1XX"

x__flag__mutmut_mutants : ClassVar[MutantDict] = {
'x__flag__mutmut_1': x__flag__mutmut_1, 
    'x__flag__mutmut_2': x__flag__mutmut_2, 
    'x__flag__mutmut_3': x__flag__mutmut_3, 
    'x__flag__mutmut_4': x__flag__mutmut_4, 
    'x__flag__mutmut_5': x__flag__mutmut_5, 
    'x__flag__mutmut_6': x__flag__mutmut_6
}

def _flag(*args, **kwargs):
    result = _mutmut_trampoline(x__flag__mutmut_orig, x__flag__mutmut_mutants, args, kwargs)
    return result 

_flag.__signature__ = _mutmut_signature(x__flag__mutmut_orig)
x__flag__mutmut_orig.__name__ = 'x__flag'


class Settings:
    # dynamic properties so tests (monkeypatch env) reflect instantly
    @property
    def poi_tracing(self) -> bool:
        return _flag("POI_TRACING", "0")

    @property
    def poi_observability(self) -> bool:
        return _flag("POI_OBSERVABILITY", "1")

    @property
    def rec_disable(self) -> bool:
        return _flag("REC_DISABLE", "0")

    @property
    def quiz_disable(self) -> bool:
        return _flag("QUIZ_DISABLE", "0")

    @property
    def internal_metrics_enabled(self) -> bool:
        return _flag("POI_INTERNAL_METRICS_ENABLED", "1")

    # --- Provider Availability (never return secret values) ---
    @property
    def openai_enabled(self) -> bool:  # presence only
        return bool(os.getenv("OPENAI_API_KEY"))

    @property
    def anthropic_enabled(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    @property
    def huggingface_enabled(self) -> bool:
        return bool(os.getenv("HUGGINGFACE_API_KEY"))

    @property
    def tavily_enabled(self) -> bool:
        return bool(os.getenv("TAVILY_API_KEY"))

    @property
    def google_enabled(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY"))

    def xǁSettingsǁprovider_status__mutmut_orig(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_1(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "XXopenaiXX": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_2(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "OPENAI": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_3(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "XXanthropicXX": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_4(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "ANTHROPIC": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_5(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "XXhuggingfaceXX": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_6(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "HUGGINGFACE": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_7(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "XXtavilyXX": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_8(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "TAVILY": self.tavily_enabled,
            "google": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_9(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "XXgoogleXX": self.google_enabled,
        }

    def xǁSettingsǁprovider_status__mutmut_10(self) -> dict:
        """Return boolean availability map for AI providers.

        No secret values are exposed; only presence (bool) is reported.
        """
        return {
            "openai": self.openai_enabled,
            "anthropic": self.anthropic_enabled,
            "huggingface": self.huggingface_enabled,
            "tavily": self.tavily_enabled,
            "GOOGLE": self.google_enabled,
        }
    
    xǁSettingsǁprovider_status__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSettingsǁprovider_status__mutmut_1': xǁSettingsǁprovider_status__mutmut_1, 
        'xǁSettingsǁprovider_status__mutmut_2': xǁSettingsǁprovider_status__mutmut_2, 
        'xǁSettingsǁprovider_status__mutmut_3': xǁSettingsǁprovider_status__mutmut_3, 
        'xǁSettingsǁprovider_status__mutmut_4': xǁSettingsǁprovider_status__mutmut_4, 
        'xǁSettingsǁprovider_status__mutmut_5': xǁSettingsǁprovider_status__mutmut_5, 
        'xǁSettingsǁprovider_status__mutmut_6': xǁSettingsǁprovider_status__mutmut_6, 
        'xǁSettingsǁprovider_status__mutmut_7': xǁSettingsǁprovider_status__mutmut_7, 
        'xǁSettingsǁprovider_status__mutmut_8': xǁSettingsǁprovider_status__mutmut_8, 
        'xǁSettingsǁprovider_status__mutmut_9': xǁSettingsǁprovider_status__mutmut_9, 
        'xǁSettingsǁprovider_status__mutmut_10': xǁSettingsǁprovider_status__mutmut_10
    }
    
    def provider_status(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSettingsǁprovider_status__mutmut_orig"), object.__getattribute__(self, "xǁSettingsǁprovider_status__mutmut_mutants"), args, kwargs, self)
        return result 
    
    provider_status.__signature__ = _mutmut_signature(xǁSettingsǁprovider_status__mutmut_orig)
    xǁSettingsǁprovider_status__mutmut_orig.__name__ = 'xǁSettingsǁprovider_status'


settings = Settings()