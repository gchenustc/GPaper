import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QMenu
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个主窗口
        self.tree_view = QTreeView(self)
        self.setCentralWidget(self.tree_view)

        # 创建一个标准项模型
        model = QStandardItemModel()
        self.tree_view.setModel(model)

        # 创建根节点
        root_item = model.invisibleRootItem()

        # 添加父节点
        parent_item = QStandardItem('Parent Item')
        parent_item.setDropEnabled(False)
        root_item.appendRow(parent_item)

        # 添加子节点
        child_item = QStandardItem('Child Item')
        parent_item.appendRow(child_item)

        # 设置树形列表的展开模式
        self.tree_view.setExpandsOnDoubleClick(False)
        self.tree_view.expandAll()

        # 创建上下文菜单
        context_menu = QMenu(self.tree_view)

        # 创建菜单项
        action1 = QAction("Action 1", self)
        action2 = QAction("Action 2", self)

        # 将菜单项添加到上下文菜单中
        context_menu.addAction(action1)
        context_menu.addAction(action2)

        # 设置树形列表的上下文菜单策略
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(lambda pos: context_menu.exec(self.tree_view.mapToGlobal(pos))) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())