"""
Tests for the i18n (internationalization) module.

These cover:
- OS-locale auto-detection of the default language
- Switching / toggling the active language
- Translation lookup, placeholder formatting, and fallbacks
- Translation-table completeness (every key has en + ja)
"""

import pytest
import i18n


@pytest.fixture(autouse=True)
def reset_language():
    """Reset the active language to the default before each test."""
    i18n.set_language(i18n.FALLBACK_LANGUAGE)
    yield
    i18n.set_language(i18n.FALLBACK_LANGUAGE)


class TestLocaleDetection:
    """Auto-detect the default language from the OS locale."""

    def _clear_locale_env(self, monkeypatch):
        for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
            monkeypatch.delenv(var, raising=False)

    @pytest.mark.parametrize("value", ["ja_JP.UTF-8", "ja_JP", "ja", "japanese", "ja:en"])
    def test_japanese_locales_detect_as_ja(self, monkeypatch, value):
        self._clear_locale_env(monkeypatch)
        monkeypatch.setenv("LANG", value)
        assert i18n.detect_default_language() == i18n.JA

    @pytest.mark.parametrize("value", ["en_US.UTF-8", "en_GB", "de_DE", "fr_FR.UTF-8"])
    def test_non_japanese_locales_fall_back_to_en(self, monkeypatch, value):
        self._clear_locale_env(monkeypatch)
        monkeypatch.setenv("LANG", value)
        assert i18n.detect_default_language() == i18n.EN

    def test_lc_all_takes_priority_over_lang(self, monkeypatch):
        self._clear_locale_env(monkeypatch)
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        monkeypatch.setenv("LC_ALL", "ja_JP.UTF-8")
        assert i18n.detect_default_language() == i18n.JA

    def test_init_language_sets_active_language(self, monkeypatch):
        self._clear_locale_env(monkeypatch)
        monkeypatch.setenv("LANG", "ja_JP.UTF-8")
        assert i18n.init_language() == i18n.JA
        assert i18n.get_language() == i18n.JA


class TestLanguageSwitching:
    """Set / toggle the active language."""

    def test_set_language(self):
        i18n.set_language(i18n.JA)
        assert i18n.get_language() == i18n.JA

    def test_set_language_ignores_unsupported(self):
        i18n.set_language(i18n.JA)
        i18n.set_language("xx")
        assert i18n.get_language() == i18n.JA

    def test_toggle_language_flips_both_ways(self):
        i18n.set_language(i18n.EN)
        assert i18n.toggle_language() == i18n.JA
        assert i18n.toggle_language() == i18n.EN

    def test_other_language_and_name(self):
        i18n.set_language(i18n.EN)
        assert i18n.other_language() == i18n.JA
        assert i18n.other_language_name() == "日本語"
        i18n.set_language(i18n.JA)
        assert i18n.other_language_name() == "English"


class TestTranslation:
    """Translate keys into the active language."""

    def test_returns_active_language_string(self):
        i18n.set_language(i18n.EN)
        assert i18n.t("view_monsters_btn") == "View Monsters"
        i18n.set_language(i18n.JA)
        assert i18n.t("view_monsters_btn") == "モンスターを見る"

    def test_placeholder_formatting(self):
        i18n.set_language(i18n.EN)
        assert i18n.t("defense_ac", ac=15) == "Defense (AC): 15"
        i18n.set_language(i18n.JA)
        assert i18n.t("strength_str", str=8) == "筋力 (STR): 8"

    def test_unknown_key_returns_key(self):
        assert i18n.t("not_a_real_key") == "not_a_real_key"


class TestTranslationCompleteness:
    """Every key must be translated into every supported language."""

    def test_all_keys_have_all_languages(self):
        for key, translations in i18n.TRANSLATIONS.items():
            for lang in i18n.SUPPORTED_LANGUAGES:
                assert lang in translations, f"'{key}' missing '{lang}' translation"
                assert translations[lang], f"'{key}' has empty '{lang}' translation"
