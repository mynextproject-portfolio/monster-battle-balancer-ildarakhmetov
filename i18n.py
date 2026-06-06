"""
Lightweight internationalization (i18n) for the Monster Battle app.

Supports English ("en") and Japanese ("ja"). The active language is chosen
once at startup by auto-detecting the operating system locale (Japanese
locales -> Japanese, everything else -> English) and can then be switched
live from the in-app language toggle.

This module is intentionally free of any UI-framework imports so the
translation logic can be unit-tested on its own.

Usage:
    from i18n import t, init_language, set_language, get_language

    init_language()                # detect OS locale once, at app start
    label = t("view_monsters_btn")
    stat = t("defense_ac", ac=15)  # keys with placeholders accept kwargs
"""

import os
import locale

# Supported language codes
EN = "en"
JA = "ja"
SUPPORTED_LANGUAGES = (EN, JA)
FALLBACK_LANGUAGE = EN

# Human-readable language names (shown on the toggle button)
LANGUAGE_NAMES = {EN: "English", JA: "日本語"}

# All user-facing strings, keyed by a stable identifier.
# Strings with {placeholders} are filled in by t() via str.format.
TRANSLATIONS = {
    # Home screen
    "app_title":            {EN: "Monster Battle",        JA: "モンスターバトル"},
    "subtitle":             {EN: "D&D Monster Viewer",    JA: "D&D モンスタービューアー"},
    "home_tagline":         {EN: "Pick two monsters and compare their stat cards",
                             JA: "2体のモンスターを選んで、ステータスカードを見比べよう"},
    "view_monsters_btn":    {EN: "View Monsters",         JA: "モンスターを見る"},

    # Shared / error states
    "load_monsters_failed": {EN: "Failed to load monsters",
                             JA: "モンスターの読み込みに失敗しました"},
    "load_details_failed":  {EN: "Failed to load monster details",
                             JA: "モンスター情報の読み込みに失敗しました"},
    "check_connection":     {EN: "Please check your internet connection",
                             JA: "インターネット接続を確認してください"},
    "back_btn":             {EN: "← Back",                JA: "← もどる"},

    # Monster selection screen
    "select_monster_1":     {EN: "Select Monster 1",      JA: "モンスター1を選択"},
    "select_monster_2":     {EN: "Select Monster 2",      JA: "モンスター2を選択"},
    "select_two_monsters":  {EN: "Please select two monsters!",
                             JA: "モンスターを2体選んでください！"},
    "back_to_home":         {EN: "Back to home",          JA: "ホームにもどる"},
    "monster_selection_title": {EN: "Monster Selection",  JA: "モンスター選択"},
    "choose_two":           {EN: "Choose two monsters to compare",
                             JA: "見比べる2体のモンスターを選んでください"},
    "monster_1":            {EN: "Monster 1",             JA: "モンスター1"},
    "monster_2":            {EN: "Monster 2",             JA: "モンスター2"},
    "view_cards_btn":       {EN: "🃏 View Cards",          JA: "🃏 カードを見る"},

    # Cards screen
    "monster_cards_title":  {EN: "Monster Cards",         JA: "モンスターカード"},
    "back_to_selection":    {EN: "Back to monster selection",
                             JA: "モンスター選択にもどる"},
    "hp":                   {EN: "HP: {hp}",              JA: "HP: {hp}"},
    "defense_ac":           {EN: "Defense (AC): {ac}",    JA: "防御 (AC): {ac}"},
    "strength_str":         {EN: "Strength (STR): {str}", JA: "筋力 (STR): {str}"},
}

_current_language = FALLBACK_LANGUAGE


def detect_default_language() -> str:
    """Auto-detect the UI language from the operating system locale.

    Japanese locales map to "ja"; everything else falls back to "en".
    Checks the standard locale environment variables first (reliable on
    Linux/macOS), then the C library locale as a backstop.
    """
    code = ""
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        value = os.environ.get(var)
        if value:
            code = value
            break
    if not code:
        try:
            code = locale.getlocale()[0] or ""
        except (ValueError, TypeError):
            code = ""
    return JA if code.lower().startswith("ja") else EN


def init_language() -> str:
    """Set the active language by auto-detecting the OS locale. Returns it."""
    global _current_language
    _current_language = detect_default_language()
    return _current_language


def get_language() -> str:
    """Return the currently active language code."""
    return _current_language


def set_language(lang: str) -> None:
    """Switch the active language. Unsupported codes are ignored."""
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang


def toggle_language() -> str:
    """Flip between the two supported languages and return the new one."""
    set_language(JA if _current_language == EN else EN)
    return _current_language


def other_language() -> str:
    """Return the language code that is NOT currently active."""
    return JA if _current_language == EN else EN


def other_language_name() -> str:
    """Name of the inactive language, for the 'switch to X' toggle button."""
    return LANGUAGE_NAMES[other_language()]


def t(key: str, **kwargs) -> str:
    """Translate a key into the active language.

    Unknown keys return the key itself, so a missing string is visible in
    the UI rather than crashing the app. Placeholders are filled from kwargs.
    """
    translations = TRANSLATIONS.get(key)
    if translations is None:
        return key
    text = translations.get(_current_language) or translations.get(FALLBACK_LANGUAGE, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
