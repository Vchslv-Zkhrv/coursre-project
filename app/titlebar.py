from . import widgets
from . import shorts
from .dropdowns import Dropdown, get_dropdown_button as dd_button
from . import config as cfg
from .config import GAP
from . import dynamic
from .dynamic import global_widget_manager as gwm
from . import gui


class ToolBar(dynamic.DynamicFrame):

    """
    Toolbar placed on MainWindow titlebar /
    Панель инструментов, расположеная на шапке главного окна
    """

    buttons: tuple[widgets.SvgTextButton, tuple[widgets.SvgTextButton]]

    def __init__(self, window: dynamic.DynamicWindow):
        dynamic.DynamicFrame.__init__(self)
        layout = shorts.HLayout(self)
        layout.setSpacing(8)
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())
        self.window_ = window

        self.add_button(
            widgets.TextButton("Аккаунт"),
            "toolbar-profile",
            dd_button("user-pen", "Аккаунт", "user-account", "Ctrl+A"),
            dd_button("user-cross", "Выйти", "user-exit", "Ctrl+Alt+A"),
            dd_button("users-three", "Пользователи", "user-accounts", "Ctrl+Shift+A")
        )
        self.add_button(
            widgets.TextButton("Файл"),
            "toolbar-file",
            dd_button("folder", "Открыть папку", "file-folder", "Ctrl+Shift+O"),
            dd_button("document-text", "Открыть файл", "file-file", "Ctrl+O"),
            dd_button("floppy-disk", "Сохранить", "file-save", "Ctrl+S"),
            dd_button("share-reverse", "Отменить", "file-undo", "Ctrl+Z"),
            dd_button("share", "Повторить", "file-redo", "Ctrl+Shift+Z")
        )
        self.add_button(
            widgets.TextButton("База данных"),
            "toolbar-database",
            dd_button("filter", "Фильтр", "database-filter", "Ctrl+F"),
            dd_button("sticky-note-pen", "Изменение", "database-edit", "Ctrl+E"),
            dd_button("trash", "Удаление", "database-delete", "Ctrl+-"),
            dd_button("circle-plus", "Добавление", "database-add", "Ctrl+="),
            dd_button("square-grid", "Создать таблицу", "database-create", "Ctrl+Alt+="),
            dd_button("square", "Удалить таблицу", "database-drop", "Ctrl+Alt+-"),
            dd_button("square-plus", "Создать столбец", "database-column", "Ctrl+Shift+="),
            dd_button("square-minus", "Удалить столбец", "database-alter", "Ctrl+Shift+-")
        )
        self.add_button(
            widgets.TextButton("Экспорт"),
            "toolbar-export",
        )
        self.add_button(
            widgets.TextButton("Статистика"),
            "toolbar-statistics",
        )
        self.add_button(
            widgets.TextButton("Настройки"),
            "toolbar-settings",
            dd_button("clock-duration", "Автосохранение", "settings-autosave", "Ctrl+Alt+S"),
            dd_button("document-check", "Режим работы", "settings-mode", "Ctrl+~"),
            dd_button("palette", "Тема", "settings-theme", "Ctrl+T"),
            dd_button("language", "Язык", "settings-language", "Ctrl+L")
        )

    def add_button(
            self,
            toolbar_button: widgets.SvgTextButton,
            toolbar_button_name: str,
            *dropdown_buttons: widgets.SvgTextButton):

        self.layout().addWidget(toolbar_button)
        gwm.add_widget(toolbar_button, toolbar_button_name)
        gwm.set_style(
            toolbar_button_name,
            "always",
            f"""
                padding-right: {GAP*2}px;
                padding-left: {GAP*2}px;
                border: none;
                outline: none;
                border-radius: {cfg.radius()}px;
            """
        )
        gwm.set_style(
            toolbar_button_name,
            "leave",
            "background-color: !back!; color: !fore!;"
        )
        gwm.set_style(
            toolbar_button_name,
            "hover",
            "background-color: !highlight2!; color: !fore!;"
        )

        dropdown = Dropdown(
            self.window_,
            dropdown_buttons)

        toolbar_button.clicked.connect(
            lambda e: self.show_dropdown(toolbar_button, dropdown))

    def show_dropdown(
            self,
            toolbar_button: widgets.SvgTextButton,
            dropdown: Dropdown):

        pos = toolbar_button.geometry().bottomLeft()
        pos.setX(pos.x() + GAP)
        pos.setY(pos.y() + GAP*2)
        dropdown.show_(pos)


def get_statusbar_label(text: str, object_name: str) -> widgets.Label:
    label = widgets.Label(text, gui.main_family.font())
    gwm.add_widget(label, object_name)
    gwm.set_style(
        object_name,
        "always",
        "outline: none; border: none; border-radius: 0px;")
    gwm.set_style(
        object_name,
        "leave",
        "background-color: !highlight3!; color: !fore!;"
    )
    return label


class StatusBar(dynamic.DynamicFrame):

    """
        Statusbar for MainWindow /
        Статусбар для главного кона
    """

    def __init__(self, window: dynamic.DynamicWindow):
        dynamic.DynamicFrame.__init__(self)
        self.window_ = window
        self.setFixedHeight(cfg.BUTTONS_SIZE.height())

        layout = shorts.HLayout(self)
        layout.setSpacing(GAP)

        status = dynamic.DynamicFrame()
        gwm.add_widget(status)
        gwm.set_style(status, "always", dynamic.always % cfg.radius())
        gwm.set_style(status, "leave", "background-color: !highlight3!;")
        status_layout = shorts.HLayout(status)

        file = dynamic.DynamicSvg("document", "black")
        nofile = dynamic.DynamicSvg("document-search", "black")
        self.path_icon = widgets.SvgButton({
            "leave": nofile,
            "active": file
        })
        self.path_label = get_statusbar_label("Файл не выбран", "status-path")
        self.path_label.setWordWrap(False)

        commit = dynamic.DynamicSvg("git-commit-filled", "black")
        nocommit = dynamic.DynamicSvg("git-commit", "black")
        self.commit_icon = widgets.SvgButton({
            "leave": nocommit,
            "active": commit
        })
        self.commit_label = get_statusbar_label("Изменений нет", "status-commit")
        self.commit_label.setWordWrap(False)

        branch = dynamic.DynamicSvg("git-branch-filled", "black")
        nobranch = dynamic.DynamicSvg("git-branch", "black")
        self.branch_icon = widgets.SvgButton({
            "leave": nobranch,
            "active": branch
        })
        self.branch_label = get_statusbar_label("Не синхронизировано", "status-branch")
        self.branch_label.setWordWrap(False)

        status_layout.addWidget(self.path_icon)
        status_layout.addWidget(self.path_label)
        status_layout.addWidget(shorts.Spacer(width=GAP))
        status_layout.addWidget(self.commit_icon)
        status_layout.addWidget(self.commit_label)
        status_layout.addWidget(shorts.Spacer(width=GAP))
        status_layout.addWidget(self.branch_icon)
        status_layout.addWidget(self.branch_label)
        status_layout.addWidget(shorts.Spacer(width=GAP*2))

        self.history_button = widgets.get_regular_button("status-history", "clock-duration")

        russian = dynamic.DynamicSvg("flag-russia", "black", cfg.BUTTONS_SIZE)
        english = dynamic.DynamicSvg("flag-uk", "black", cfg.BUTTONS_SIZE)
        self.language_button = widgets.SwitchingButton(
            ("ru", russian),
            ("en", english)
        )
        self.language_button.signals.triggered.connect(
            lambda trigger: self._on_lang_click(trigger)
        )
        gwm.add_widget(self.language_button, "language-button")
        gwm.copy_style(status, self.language_button)

        theme_icons = []

        theme_icons.append(
            (
                gwm.theme_name,
                dynamic.DynamicSvg(gwm.theme["theme_icon"], "black")
            )
        )
        for theme_name, theme in gwm.themes.items():
            if theme_name == gwm.theme_name:
                continue
            theme_icons.append(
                (
                    theme_name,
                    dynamic.DynamicSvg(theme["theme_icon"], "black")
                )
            )
        self.themes_button = widgets.SwitchingButton(*theme_icons)
        self.themes_button.signals.triggered.connect(
            lambda trigger: self._on_theme_click(trigger))
        gwm.add_widget(self.themes_button, "themes-button")

        settings = dynamic.DynamicFrame()
        gwm.add_widget(settings)
        gwm.copy_style(status, settings)

        settings.setFixedHeight(self.height())
        settings_layout = shorts.HLayout(settings)
        settings_layout.setSpacing(cfg.GAP)
        settings_layout.addWidget(self.language_button)
        settings_layout.addWidget(self.themes_button)

        layout.addWidget(status)
        layout.addWidget(self.history_button)
        layout.addItem(shorts.HSpacer())
        layout.addWidget(settings)

    def _on_lang_click(self, trigger: str):
        if trigger in gwm.languages:
            gwm.switch_language(self.language_button.icon[0])

    def _on_theme_click(self, trigger: str):
        if trigger in gwm.themes:
            theme = self.themes_button.icon[0]
            gwm.switch_theme(theme)

    def set_commit_status(self, status: bool, message: str):
        self.commit_label.setText(message)
        self.commit_icon.signals.triggered.emit("active" if status else "leave")

    def set_branch_status(self, status: bool, message: str):
        self.branch_label.setText(message)
        self.commit_icon.signals.triggered.emit("active" if status else "leave")

    def set_file_status(self, status: bool, message: str):
        self.path_icon.signals.triggered.emit("active" if status else "leave")
        self.path_icon.dont_translate = status
        self.path_label.setText(
            message if status else dynamic.translate(message, gwm.language))
