from typing import List
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox
import pandas as pd
import re
import traceback

class LocWidght(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("排查")

        self.horizontal_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()

        self.risk_button = QPushButton("风险地区文件", parent=self)
        self.risk_button.setProperty("class", "danger")
        self.risk_button.clicked.connect(self.select_risk)

        self.search_button = QPushButton("需排查地区", parent=self)
        self.search_button.setProperty("class", "warning")
        self.search_button.clicked.connect(self.select_search)

        self.horizontal_layout.addWidget(self.risk_button)
        self.horizontal_layout.addWidget(self.search_button)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.submit_button = QPushButton("提交", parent=self)
        self.submit_button.setProperty("class", "success")
        self.submit_button.clicked.connect(self.submit)

        self.vertical_layout.addWidget(self.submit_button)
        self.setLayout(self.vertical_layout)

    def select_risk(self):
        self.risk_file, _ = QFileDialog.getOpenFileName(self, "选取文件", "./", "Excel文件(*.xlsx *.xls)")

    def select_search(self):
        self.search_file, _ = QFileDialog.getOpenFileName(self, "选取文件", "./", "Excel文件(*.xlsx *.xls)")

    def submit(self):
        try:
            risk_file = pd.read_excel(self.risk_file)
            search_file = pd.read_excel(self.search_file)
        except:
            QMessageBox.critical(self, "错误信息", "请选择文件！")
            traceback.print_exc()
            return
        try:
            search_list: List[str] = search_file["地址"].tolist()
            risk_province = risk_file["省份"].tolist()
            risk_loc = risk_file["范围"].tolist()
        except:
            QMessageBox.critical(self, "错误信息", "文件内容错误")
            return

        result = pd.DataFrame(columns=["地址", "疑似排查源（可能归属的排查地点）"])

        for search in search_list:
            for risk in risk_loc:
                if isinstance(risk, str):
                    possible = re.split(r",|、|，", risk)
                    if any(p in search for p in possible):
                        result = pd.concat([result, pd.DataFrame([{
                            "地址": search,
                            "疑似排查源（可能归属的排查地点）": risk
                        }])], ignore_index=True)

        file, _ = QFileDialog.getSaveFileName(self, "文件保存", ".", "Excel文件(*.xlsx)")
        try:
            result.to_excel(file, index=False)
        except:
            QMessageBox.critical(self, "错误信息", "请关闭同名文件后重新保存")
            return

        QMessageBox.information(self, "提示", "成功")