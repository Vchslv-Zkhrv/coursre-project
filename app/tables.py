from typing import Any

from PyQt6 import QtGui

from . import widgets
from . import config as cfg
from . import shorts
from . import gui
from . import connector
from .dynamic import global_widget_manager as gwm


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

    def __init__(self, text: str):
        widgets.Label.__init__(self, text, gui.mono_family.font())
        self.setSizePolicy(shorts.ExpandingPolicy())
        self.setWordWrap(False)
        self.setMinimumHeight(self.font().pixelSize()*2)
        self.setMinimumWidth(100)


class TableHeaderCell(TableCell):

    def __init__(self, text: str):
        super().__init__(text)


class Table(widgets.ScrollArea):

    """
    Table widget. Can be connected directly to connector.SQL /
    Виджет таблицы. Может быть подключен напрямую к connector.SQL
    """

    database: connector.SQL = None
    table: connector.Table = None
    cells: list[list[TableCell]]

    def __init__(self):
        widgets.ScrollArea.__init__(self)
        layout = shorts.GLayout(self.area)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        self.cells = []
        self.setSizePolicy(shorts.MinimumPolicy())

        QtGui.QShortcut("up", self).activated.connect(self.up)
        QtGui.QShortcut("ctrl+up", self).activated.connect(self.start)
        QtGui.QShortcut("down", self).activated.connect(self.down)
        QtGui.QShortcut("ctrl+down", self).activated.connect(self.end)

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
            print("empty")

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
                    cell = TableCell(str(value))
                if j == 0:
                    cell.setFixedWidth(50)
                if i == 0:
                    cell.setFixedHeight(cell.font().pixelSize()*3)
                self.cells[-1].append(cell)
                layout.addWidget(cell, i, j, 1, 1)
