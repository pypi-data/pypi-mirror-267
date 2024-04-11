from PySide6.QtWidgets import QDialog, QTableView, QLabel, QVBoxLayout

from qtlink.table.table_controller import TableController


def show_dialog_table_display(text: str, table_data: list[dict], show_or_exec: str = 'exec'):
    dialog = DialogTableDisplay(text, table_data=table_data)
    if show_or_exec == 'exec':
        dialog.exec()
    else:
        dialog.show()


class DialogTableDisplay(QDialog):
    def __init__(self, text: str,
                 table_data: list[dict],
                 parent=None):
        super().__init__(parent)
        self.v_layout = QVBoxLayout()
        label = QLabel(text, self)
        label.setWordWrap(True)
        self.tableview = QTableView(self)
        self.v_layout.addWidget(label)
        self.v_layout.addWidget(self.tableview)

        self.setLayout(self.v_layout)
        self.table_controller = TableController(tableview=self.tableview)
        self.update_table_data(table_data)

    def update_table_data(self, table_data):
        self.table_controller.update_table_data(table_data=table_data)
