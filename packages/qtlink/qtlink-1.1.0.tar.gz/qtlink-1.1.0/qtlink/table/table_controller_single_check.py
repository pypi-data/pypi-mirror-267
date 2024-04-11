# -*- coding:utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem

from qtlink.table.table_controller import TableController
from qtlink.util import create_signal


class TableControllerSingleCheck(TableController):
    def __init__(self, tableview):
        super().__init__(tableview)
        self.model.itemChanged.connect(self.on_item_changed)
        self.signal_checked_rows = create_signal(list)

    def update_table_data(self, table_data: list[dict], hide_columns: list[str] = None):
        # 断开信号连接
        self.model.itemChanged.disconnect(self.on_item_changed)

        self.before_update_table_data(table_data)
        if hide_columns is None:
            hide_columns = []
        for data in table_data:
            items = [QStandardItem(str(data.get(column, None)) if data.get(column, None) is not None else '')
                     for column in self.table_columns
                     if column not in hide_columns]
            items[0].setCheckable(True)
            self.model.appendRow(items)

        self.set_table()
        # 重新连接信号
        self.model.itemChanged.connect(self.on_item_changed)
        self.on_item_changed()

    def on_item_changed(self, item: QStandardItem = None):
        if item is None or item.checkState() != Qt.Checked:
            return

        for row in range(self.model.rowCount()):
            if self.model.item(row, 0) != item:
                self.model.item(row, 0).setCheckState(Qt.Unchecked)
        checked_rows = self.get_checked_rows()
        self.signal_checked_rows.signal.emit(checked_rows)

    def get_checked_rows(self) -> list[dict]:
        for row in range(self.model.rowCount()):
            item = self.model.item(row, 0)  # 勾选框在第一列
            if item.checkState() == Qt.Checked:
                return [self.raw_data[row], ]
