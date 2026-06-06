"""Small shared UI widgets used across screens."""

import flet as ft
from i18n import other_language_name


def language_toggle_button(on_toggle) -> ft.Control:
    """Build the language switch button.

    The label shows the language you'd switch *to* (e.g. "日本語" while
    English is active), so it reads as an action. The tooltip is bilingual
    so it makes sense in either language.

    Args:
        on_toggle: Callback invoked when the button is clicked.
    """
    return ft.OutlinedButton(
        text=other_language_name(),
        icon=ft.Icons.LANGUAGE,
        on_click=on_toggle,
        tooltip="Language / 言語",
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
    )
