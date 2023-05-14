from typing import Any


from .personalization import personalization
from . import widgets
from . import config as cfg
from . import shorts
from . import gui
from . import connector


class AbstractTableNav(widgets.RadioGroup):

    """
    widgets providing navigation between database table /
    виджет, обеспечивающий навигацию по таблицам базы данных
    """

    def __init__(self):
        widgets.RadioGroup.__init__(self, "h", True)
        self.verticalScrollBar().setDisabled(True)
        self.setFixedHeight(cfg.HEAD_FONTSIZE + cfg.GAP)
        self.area.layout().setSpacing(cfg.GAP*2)

    def fill(self, tablenames: tuple[str]):
        self.drop_radios()
        radios = tuple(widgets.getRadioButton(name) for name in tablenames)
        self.add_radios(*radios)


@personalization((
    """
        outline: none;
        border: none;
        border-radius: 0px;
    """,
    {
        "background-color": "back"
    }
))
class TableNav(AbstractTableNav):
    pass


class AbstactCell(widgets.AbstractLabel):

    def __init__(self, text: str):
        widgets.AbstractLabel.__init__(self, text, gui.mono_family.font())
        self.setSizePolicy(shorts.ExpandingPolicy())
        self.setWordWrap(False)
        self.setMinimumHeight(self.font().pixelSize()*2)
        self.setMinimumWidth(100)


@personalization((
    f"""
        border: none;
        border-radius: 0px;
        padding-right: {cfg.GAP}px;
        padding-left: {cfg.GAP}px;
    """,
    {
        "color": "fore",
        "background-color": "back"
    }
))
class Cell(AbstactCell):
    pass


@personalization((
    f"""
        border: none;
        border-radius: 0px;
        padding-right: {cfg.GAP}px;
        padding-left: {cfg.GAP}px;
    """,
    {
        "color": "fore",
        "background-color": "highlight2"
    }
))
class HeaderCell(AbstactCell):

    def __init__(self, text: str):
        super().__init__(text)


class AbstractTable(widgets.ScrollArea):

    """
    Table widget. Can be connected directly to connector.SQL /
    Виджет таблицы. Может быть подключен напрямую к connector.SQL
    """

    database: connector.SQL
    table: connector.Table
    cells: list[list[AbstactCell]]

    def __init__(self):
        widgets.ScrollArea.__init__(self)
        layout = shorts.GLayout(self.area)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 1, 1, 1)
        self.cells = []
        self.setSizePolicy(shorts.MinimumPolicy())

    def connect(self, connector: connector.SQL):
        self.database = connector

    def draw_table(self, tablename: str):
        self.table = self.database.tables[tablename]
        try:
            values = self.database.get_rows(tablename, 1, 20, True)
            hheaders = ["#"]
            hheaders.extend(column.name for column in self.table.columns)
            self.fill(hheaders, *values)
        except connector.EmptySet:
            print("empty")

    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.hide()
        self.cells = []

    def fill(self, *rows: tuple[Any]):
        self.clear()
        layout = self.area.layout()
        for i, row in enumerate(rows):
            self.cells.append([])
            for j, value in enumerate(row):
                if i == 0 or j == 0:
                    cell = HeaderCell(str(value))
                else:
                    cell = Cell(str(value))
                if j == 0:
                    cell.setFixedWidth(50)
                if i == 0:
                    cell.setFixedHeight(cell.font().pixelSize()*3)
                self.cells[-1].append(cell)
                layout.addWidget(cell, i, j, 1, 1)


@personalization((
    """
        border-radius: 0px;
    """,
    {
        "background-color": "highlight1"
    }
))
class Table(AbstractTable):
    pass
