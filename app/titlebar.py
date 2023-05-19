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
            widgets.TextButton("Профили"),
            "toolbar-profile",
            dd_button("user-pen", "Аккаунт", "user-account", "Ctrl+A"),
            dd_button("user-cross", "Выйти", "user-exit", "Ctrl+Alt+A"),
            dd_button("users-three", "Профили", "user-accounts", "Ctrl+Shift+A")
        )
        self.add_button(
            widgets.TextButton("Файл"),
            "toolbar-file",
            dd_button("folder", "Открыть проект", "file-folder", "Ctrl+Shift+O"),
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
            dd_button("square-grid", "+ таблица", "database-create", "Ctrl+Alt+="),
            dd_button("square", "- таблица", "database-drop", "Ctrl+Alt+-"),
            dd_button("square-plus", "+ столбец", "database-column", "Ctrl+Shift+="),
            dd_button("square-minus", "- столбец", "database-alter", "Ctrl+Shift+-")
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
            dd_button("document-check", "Режим работы", "settings-mode", "Ctrl+`"),
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
            "background-color: !back!;"
        )
        gwm.set_style(
            toolbar_button_name,
            "hover",
            "background-color: !highlight2!;"
        )

        dropdown = Dropdown(
            f"{toolbar_button_name}-dropdown",
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
        layout.setContentsMargins(int(GAP/2), 0, GAP, 0)
        self.normal_document_icon = dynamic.DynamicSvg("document", "black")
        self.unknown_document_icon = dynamic.DynamicSvg("document-search", "black")
        self.path = widgets.Label("Файл не выбран", gui.main_family.font())
        self.empty_commit_icon = dynamic.DynamicSvg("git-commit", "black")
        self.filled_commit_icon = dynamic.DynamicSvg("git-commit-filled", "black")
        self.commit = widgets.Label("Изменений нет", gui.main_family.font())
        self.empty_branch_icon = dynamic.DynamicSvg("git-branch", "black")
        self.filled_branch_icon = dynamic.DynamicSvg("git-branch-filled", "black")
        self.branch = widgets.Label("Не синронизировано", gui.main_family.font())

        self.path.setStyleSheet(self.styleSheet())
        self.commit.setStyleSheet(self.styleSheet())
        self.branch.setStyleSheet(self.styleSheet())

        layout.addWidget(self.normal_document_icon)
        layout.addWidget(self.unknown_document_icon)
        layout.addWidget(self.path)
        layout.addWidget(shorts.Spacer(width=8))
        layout.addWidget(self.empty_commit_icon)
        layout.addWidget(self.filled_commit_icon)
        layout.addWidget(self.commit)
        layout.addWidget(shorts.Spacer(width=8))
        layout.addWidget(self.empty_branch_icon)
        layout.addWidget(self.filled_branch_icon)
        layout.addWidget(self.branch)

        self.normal_document_icon.hide()
        self.filled_branch_icon.hide()
        self.filled_commit_icon.hide()

    def _set_status(
            self,
            icon0: dynamic.DynamicSvg,
            icon1: dynamic.DynamicSvg,
            label: widgets.Label,
            status: bool,
            message: str):

        label.setText(message)
        if status:
            icon1.show()
            icon0.hide()
        else:
            icon1.hide()
            icon0.show()

    def set_commit_status(self, status: bool, message: str):
        return self._set_status(
            self.empty_commit_icon,
            self.filled_commit_icon,
            self.commit,
            status,
            message
        )

    def set_branch_status(self, status: bool, message: str):
        return self._set_status(
            self.empty_branch_icon,
            self.filled_branch_icon,
            self.branch,
            status,
            message
        )

    def set_file_status(self, status: bool, message: str):
        return self._set_status(
            self.unknown_document_icon,
            self.normal_document_icon,
            self.path,
            status,
            message
        )
