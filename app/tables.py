from typing import Any, Literal

from PyQt6 import QtCore
from loguru import logger

from . import widgets
from . import config as cfg
from . import shorts
from . import gui
from . import connector
from .dynamic import global_widget_manager as gwm
from . import dynamic


def scrollbar_stylesheet(direction: Literal["horizontal", "vertical"]):
    return """
    QScrollBar:%s {
        border: none;
        background: !highlight3!;
        background-color: !highlight3!;
        height: %spx;
        background-image: none;
    }
    QScrollBar::add-page:%s, QScrollBar::sub-page:%s {
        background: !highlight3!;
    }
    QScrollBar::handle:%s {
        background-color: !highlight2!;
        background: !highlight2!;
    }
    QScrollBar::add-line:%s {
        border: none;
        background-color: !highlight3!;
        background: !highlight3!;
    }

    QScrollBar::sub-line:%s {
        border: none;
        background: !highlight3!;
        background-color: !highlight3!;
    }
""" % (
        direction,
        cfg.GAP*2,
        direction,
        direction,
        direction,
        direction,
        direction
    )


class TableNav(widgets.RadioGroup):

    """
    widgets providing navigation between database table /
    виджет, обеспечивающий навигацию по таблицам базы данных
    """

    def __init__(self):
        widgets.RadioGroup.__init__(self, "h", True)
        self.setFixedHeight(cfg.HEAD_FONTSIZE + cfg.GAP*2)
        self.area.layout().setSpacing(cfg.GAP*2)
        self.setContentsMargins(cfg.GAP, 0, cfg.GAP, 0)
        gwm.add_widget(self, style_preset="frame")
        gwm.add_shortcut(self.tab_forward, "Ctrl+Tab")
        gwm.add_shortcut(self.tab_backwards, "Ctrl+Shift+Tab")

    def tab_forward(self):
        index = self.radios.index(self.get_choosen_radios()[0])
        index = index + 1 if index + 1 < len(self.radios) else 0
        self.tab(index)

    def tab_backwards(self):
        index = self.radios.index(self.get_choosen_radios()[0])
        index = index - 1 if index >= 0 else len(self.radios) - 1
        self.tab(index)

    def tab(self, index: int):
        self.radios[index].current().click()

    def _add_button_to_gwm(self, button: widgets.TextButton):

        button.dont_translate = True
        gwm.add_widget(button)
        gwm.set_style(button, "always", "border: none; outline: none;")
        gwm.set_style(button, "leave", "color: !fore!;")
        gwm.set_style(button, "hover", "color: !blue!;")

    def _make_radio(self, text: str) -> widgets.RadioButton:

        b0 = widgets.TextButton(text)
        self._add_button_to_gwm(b0)
        b1 = widgets.TextButton(text, gui.main_family.font(size=cfg.HEAD_FONTSIZE))
        self._add_button_to_gwm(b1)

        return widgets.RadioButton(b0, b1)

    def fill(self, tablenames: tuple[str]):

        self.drop_radios()
        self.radios = list(self._make_radio(name) for name in tablenames)
        self.add_radios(*self.radios)


class TableCell(widgets.Label):

    full_text: str

    def __init__(
            self,
            text: str,
            font: gui.Font):

        visible_text = text[:100] if len(text) >= 100 else text
        widgets.Label.__init__(self, visible_text, font)
        self.full_text = text

        self.setWordWrap(False)
        self.dont_translate = True
        self.setSizePolicy(shorts.RowPolicy())
        self.setContentsMargins(*[cfg.GAP, ]*4)

        gwm.add_widget(self)
        gwm.set_style(
            self,
            "always",
            "border-radius: 0px; border: none; outline: none;"
        )
        gwm.set_style(
            self,
            "leave",
            "background-color: !back!; color: !fore!;"
        )


class TableRegularCell(TableCell):

    def __init__(self, text: str):
        TableCell.__init__(self, text, gui.mono_family.font())


class TableHeaderCell(TableCell):

    def __init__(self, text: str):
        TableCell.__init__(self, text, gui.mono_family.font(weight=700))


class Table(widgets.HScrollArea):

    """
    Table widget. Can be connected directly to connector.SQL /
    Виджет таблицы. Может быть подключен напрямую к connector.SQL
    """

    database: connector.SQL = None
    table: connector.Table = None
    cells: list[list[TableRegularCell]]

    def __init__(self):
        widgets.HScrollArea.__init__(self)
        layout = shorts.GLayout(self.area)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        self.cells = []
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        gwm.add_shortcut(self.up, "Up")
        gwm.add_shortcut(self.down, "Down")
        gwm.add_shortcut(self.start, "Ctrl+Up")
        gwm.add_shortcut(self.end, "Ctrl+Down")

        self.hspacer = shorts.ExpandingSpacer()
        self.vspacer = shorts.ExpandingSpacer()

    def up(self):
        rowid = self.get_first_rowid()-1
        self.scroll_table(rowid if rowid >= 1 else 1)

    def down(self):
        self.scroll_table(self.get_first_rowid()+1)

    def end(self):
        self.scroll_table(-1)

    def start(self):
        self.scroll_table(1)

    def connect(self, connector: connector.SQL):
        self.database = connector

    def get_first_rowid(self) -> int:
        rowid = int(self.cells[1][0].text())
        return rowid

    def scroll_table(self, start: int):
        try:
            values = self.database.get_rows(self.table.name, start, 20, True)
            if len(values) < len(self.cells) - 1:
                return
            hheaders = ["#"]
            hheaders.extend(column.name for column in self.table.columns)
            self.fill_cells(hheaders, *values)
        except connector.EmptySet:
            self.clear()

    def draw_table(self, tablename: str):
        self.table = self.database.tables[tablename]
        self.clear()
        try:
            values = self.database.get_rows(self.table.name, 1, 20, True)
            hheaders = ["#"]
            hheaders.extend(column.name for column in self.table.columns)
            self.draw_cells(hheaders, *values)
        except connector.EmptySet:
            self.draw_cells((("", ), ))
            logger.error(f"Table {tablename} has no rows")

    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.hide()
        self.cells = []

    def fill_cells(self, *rows: tuple[Any]):
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.cells[i][j].setText(str(value))

    def draw_cells(self, *rows: tuple[Any]):
        layout = self.area.layout()
        for i, row in enumerate(rows):
            self.cells.append([])
            for j, value in enumerate(row):
                if i == 0 or j == 0:
                    cell = TableHeaderCell(str(value))
                else:
                    cell = TableRegularCell(str(value))
                self.cells[-1].append(cell)
                layout.addWidget(cell, i, j, 1, 1)

        layout.addWidget(self.vspacer, i+1, 0, 1, j)
        layout.addWidget(self.hspacer, 0, j+1, i, 1)
