import os
import flet as ft
from i18n import init_language, toggle_language, t
from screens.home_screen import home_screen
from screens.monster_selection_screen import monster_selection_screen
from screens.cards_screen import cards_screen


def main(page: ft.Page):
    """Main application entry point."""
    # Pick the UI language from the OS locale (Japanese locale -> Japanese,
    # otherwise English). Users can switch live via the in-app toggle.
    init_language()

    page.title = t("app_title")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Dark theme for D&D atmosphere
    page.bgcolor = ft.Colors.GREY_900

    # Desktop screen dimensions
    page.window.width = 1400  # Desktop width
    page.window.height = 900  # Desktop height
    page.window.resizable = True
    page.window.maximizable = True

    # Remember how to rebuild the current screen so the language toggle can
    # re-render it in place after switching languages.
    current_builder = {"build": None}

    def render(build):
        """Render a screen and remember its builder for re-rendering."""
        current_builder["build"] = build
        page.clean()
        page.title = t("app_title")
        page.add(build())
        page.update()

    def handle_toggle_language(e=None):
        """Switch language and re-render the current screen in place."""
        toggle_language()
        if current_builder["build"]:
            render(current_builder["build"])

    # Navigation functions
    def navigate_to_home(e=None):
        """Navigate to the home screen."""
        render(lambda: home_screen(page, navigate_to_monster_selection, handle_toggle_language))

    def navigate_to_monster_selection(e=None):
        """Navigate to the monster selection screen."""
        render(lambda: monster_selection_screen(
            page, navigate_to_home, navigate_to_cards, handle_toggle_language))

    def navigate_to_cards(monster1_index: str, monster2_index: str):
        """Navigate to the cards screen with selected monsters."""
        render(lambda: cards_screen(
            page, monster1_index, monster2_index, navigate_to_monster_selection,
            handle_toggle_language))

    # Start with home screen
    navigate_to_home()


# Local development opens a native desktop window.
# In a container, set FLET_WEB=1 to serve the app over HTTP instead (see Dockerfile).
if os.getenv("FLET_WEB"):
    ft.app(
        main,
        view=None,  # headless: serve as a web app, don't open a desktop window/browser
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
else:
    ft.app(main)
