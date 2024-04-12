import json
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

def add_items_to_list(list_widget):
    with open('model_name.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, value in data.items():
            # 创建列表项并设置文本和详细描述
            item_text = f"{key} ( {value} )"  # 使用冒号分隔键和值
            item = QListWidgetItem(item_text)
            item.setFont(QFont("Arial", 12))  # 设置字体大小为12
            list_widget.addItem(item)

# 存放主UI所有槽函数

# 默认参数与手动调参互斥
def on_groupBox_clicked(main_window_self):
    # print("GroupBox clicked")
    sender = main_window_self.sender()
    # print(sender)
    if sender.isChecked():
        # print("GroupBox is checked")
        # 如果当前GroupBox被选中，则取消另一个GroupBox的选中状态
        if sender is main_window_self.Main_Box_acq:
            print("主程序信号属性为默认属性")
            main_window_self.Main_Box_manual.setChecked(False)
        else:
            print("主程序信号属为手动更改")
            main_window_self.Main_Box_acq.setChecked(False)


def newfile_clicked(window):
    folder_path = QFileDialog.getExistingDirectory(window, "选择文件夹", "/")
    if folder_path:
        window.folder_path = folder_path  # 将 folder_path 设置为 MainWindow 类的属性
        print("选择了文件",window.folder_path)
        print(window.sample_rate)
        window.Main_textEdit_newfile.setText(f"文件夹：{folder_path}")

def sample_clicked(window):
    sample_rate = window.Main_textEdit_sample.toPlainText()
    window.sample_rate = sample_rate
    print("设置了采样率为", window.sample_rate)
    window.Main_textEdit_sample.setText(f"已设置采样率为 {sample_rate}")



