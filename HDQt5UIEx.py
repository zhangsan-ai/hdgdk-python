from PyQt5.QtWidgets import QTabWidget, QCheckBox,QTabBar


class CheckableTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tabBar().setMovable(True)  # 保持原有特性

        # 存储所有复选框的引用
        self._checkboxes = {}

    def addTab(self, widget, text):
        """重写addTab方法添加复选框"""
        index = super().addTab(widget, text)

        # 创建并嵌入复选框
        checkbox = QCheckBox()
        checkbox.setChecked(False)

        # 将复选框添加到标签左侧
        self.tabBar().setTabButton(index, QTabBar.LeftSide, checkbox)
        self._checkboxes[index] = checkbox

        return index

    def get_checked_tabs(self):
        """获取选中标签的索引列表"""
        return [i for i, cb in self._checkboxes.items() if cb.isChecked()]

