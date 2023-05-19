from . import shorts
from . import widgets
from . import config as cfg
from .config import GAP
from . import gui
from . import dynamic


class Group(dynamic.DynamicFrame):

    """
    Regular frame without style /
    Обычный фрейм без стиля
    """

    def __init__(self):
        dynamic.DynamicFrame.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)


class StatusBar(Group):

    """
        Statusbar for MainWindow /
        Статусбар для главного кона
    """

    def __init__(self, window: dynamic.DynamicWindow):
        Group.__init__(self)
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


class SecondToolbar(Group):

    """
    Second toolbar placed under the titlebar /
    Вторая полоса инструментов, расположенная под шапкой окна
    """

    def __init__(self, window: dynamic.DynamicWindow):
        Group.__init__(self, "second toolbar")
        self.window_ = window
        self.setFixedHeight(cfg.BUTTONS_SIZE.height() + GAP)
        self.setSizePolicy(shorts.RowPolicy())

        layout = shorts.HLayout(self)
        layout.setContentsMargins(GAP, GAP, GAP, 0)
        layout.setSpacing(GAP)

        self.status_bar = StatusBar(window)
        layout.addWidget(self.status_bar)

        self.history_button = widgets.ShrinkingButton(
            window,
            "git-compare",
            "История",
            100,
            "history"
        )
        dynamic.global_widget_manager.add_shortcut("history", "Crtl+H")
        layout.addWidget(self.history_button)

        layout.addItem(shorts.HSpacer())
