import flet as ft
from i18n import t
from screens.widgets import language_toggle_button
from ui_constants import (
    SPACING_SM, SPACING_LG, SPACING_XL,
    BUTTON_HEIGHT_LG, BUTTON_WIDTH_LG,
    TEXT_SIZE_LG, TEXT_SIZE_XL
)


def home_screen(page: ft.Page, on_start, on_toggle_language=None):
    """Render the home screen.

    Args:
        page: The Flet page object
        on_start: Callback function to navigate to monster selection
        on_toggle_language: Optional callback to switch the UI language
    """
    content = ft.Column(
        [
            ft.Container(height=SPACING_XL * 2),  # Spacer
            ft.Icon(
                name=ft.Icons.CASTLE,
                size=120,
                color=ft.Colors.RED_400,
            ),
            ft.Container(height=SPACING_LG),
            ft.Text(
                t("app_title"),
                size=48,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED_400,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=SPACING_SM),
            ft.Text(
                t("subtitle"),
                size=TEXT_SIZE_LG,
                color=ft.Colors.RED_300,
                text_align=ft.TextAlign.CENTER,
                italic=True,
            ),
            ft.Container(height=SPACING_XL),
            ft.Container(
                content=ft.Text(
                    t("home_tagline"),
                    size=TEXT_SIZE_XL,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                width=600,
            ),
            ft.Container(height=SPACING_XL * 2),
            ft.ElevatedButton(
                t("view_monsters_btn"),
                width=BUTTON_WIDTH_LG,
                height=BUTTON_HEIGHT_LG,
                on_click=on_start,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_700,
                    color=ft.Colors.WHITE,
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Language toggle pinned to the top-right corner.
    stack_controls = [ft.Container(content=content, expand=True)]
    if on_toggle_language:
        stack_controls.append(
            ft.Container(
                content=language_toggle_button(on_toggle_language),
                top=SPACING_LG,
                right=SPACING_LG,
            )
        )

    return ft.Container(
        content=ft.Stack(stack_controls, expand=True),
        expand=True,
    )
