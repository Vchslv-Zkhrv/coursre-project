from typing import Any

from PyQt6 import QtGui

from . import widgets
from . import config as cfg
from . import shorts
from . import gui
from . import connector


class TableNav(widgets.RadioGroup):

    """
    widgets providing navigation between database table /
    виджет, обеспечивающий навигацию по таблицам базы данных
    """

    def __init__(self):
        widgets.RadioGroup.__init__(self, "h", True)
        self.verticalScrollBar().setDisabled(True)
        self.setFixedHeight(cfg.HEAD_FONTSIZE + cfg.GAP)
        self.area.layout().setSpacing(cfg.GAP*2)
        QtGui.QShortcut("Ctrl+Tab", self, self.tab)

    def tab(self):
        index = 0
        for i, radio in enumerate(self.radios):
            if radio.active:
                index = i
        self.radios[index-1].button1.click()

    def fill(self, tablenames: tuple[str]):
        self.drop_radios()
        radios = tuple(widgets.getRadioButton(name) for name in tablenames)
        self.add_radios(*radios)


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
