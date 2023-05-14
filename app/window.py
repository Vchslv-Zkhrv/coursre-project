from typing import TypedDict

from .abstract_windows import AbstractWindow
from . import shorts
from . import events
from . import dialogs
from . import forms
from . import groups
from .config import FORMS
from .toolbar import ToolBar
from . import personalization as pers


class WindowForms(TypedDict):

    auth: forms.AuthForm
    main: forms.MainForm
    nofile: forms.OpenSuggestion



class Window(AbstractWindow):

    """
    Main application window /
    Главное окно приложения
    """

    forms: WindowForms

    def __init__(self):
        AbstractWindow.__init__(self, "main")

        self.signals.close.connect(self.on_close)
        self.signals.maximize.connect(self.on_maximize)
        self.signals.minimize.connect(self.showMinimized)

        self.auth_signals = events.AuthorizationSignals()
        self.auth_signals.correct.connect(lambda: self.show_form("nofile"))
        self.auth_signals.incorrect.connect(lambda count: self._show_log_in_error(count))
        self.auth_signals.suspicious.connect(self._show_suspisious_error)

        self.setMinimumSize(720, 480)
        shorts.GLayout(self.content)

        self.forms = WindowForms()
        self.forms["auth"] = forms.AuthForm()
        self.forms["main"] = forms.MainForm()
        self.forms["nofile"] = forms.OpenSuggestion(self)

        self._draw_interface()

    def _show_suspisious_error(self):
        d = dialogs.AlertDialog(
            "suspisuous log in attempt",
            self,
            "Данные неверны.\n\nПревышено максимальное количество попыток.\nПриложение будет закрыто.")
        d.show()
        d.rejected.connect(self.close())

    def on_close(self):
        d = dialogs.YesNoDialog("window closer", self, "Закрыть приложение?")
        d.island.setFixedHeight(200)
        d.accepted.connect(self.close)
        d.show()

    def on_maximize(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def _show_log_in_error(self, attempt_count: int):
        if attempt_count in (2, 3):
            message = f"Осталось {attempt_count} попытки"
        elif attempt_count == 1:
            message = "Осталась последняя попытка"
        dialog = dialogs.AlertDialog(
            "wrong log in alert",
            self,
            f"Данные неверны.\n\n{message}")
        dialog.show()

    def _draw_interface(self):

        self.toolbar = ToolBar(self)
        self.title_bar.layout().addWidget(self.toolbar)
        self.toolbar.signals.button_clicked.connect(
            lambda name: self._on_toolbar_button_click(name))

        self.second_titlebar = groups.SecondToolbar(self)
        self.content.layout().addWidget(self.second_titlebar, 0, 0, 1, 1)

        self.container = groups.Group()
        self.container.setSizePolicy(shorts.ExpandingPolicy())
        self.content.layout().addWidget(self.container, 1, 0, 1, 1)
        layout = shorts.GLayout(self.container)

        layout.addWidget(self.forms["auth"], 0, 0, 1, 1)
        layout.addWidget(self.forms["main"], 0, 0, 1, 1)
        layout.addWidget(self.forms["nofile"], 0, 0, 1, 1)
        self.show_form(None)

    def show_form(self, name: FORMS):
        for name_, form in self.forms.items():
            if name == name_:
                form.show()
            else:
                form.hide()
        if name == "auth":
            self.second_titlebar.hide()
            self.toolbar.hide()
        else:
            self.second_titlebar.show()
            self.toolbar.show()

    def _on_toolbar_button_click(self, name: str):
        self.signals.button_click.emit(name)

    def show_help(self, mode: FORMS):
        if mode == "auth":
            dialog = dialogs.AlertDialog(
                "info-auth",
                self,
                "Введите данные вашей учетной записи, чтобы продолжить")
            dialog.title.setText("Подсказка")
            dialog.show()
