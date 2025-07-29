from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox,
    QGroupBox, QRadioButton, QButtonGroup, QCompleter
)
from PySide6.QtCore import Qt
import sys

from jsonHandler import (loadJson, saveJson)

import os

class ArmorUpdaterUI(QWidget):
    def __init__(self, scriptDir):
        super().__init__()
        self.setWindowTitle("More Armor Mod Updater")
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.scriptDir = scriptDir
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()

        self.restoreBWGButton = QPushButton()
        self.restoreBWGButton.setText("Restore Shayar, Amzul and Masharuz armors")
        self.restoreBWGButton.setFixedSize(300,150)
        self.restoreBWGButton.setEnabled(True)
        self.restoreBWGButton.setToolTip("This button will restore the recipes for Shayar, Amzul and Masharuz armors.")
        self.restoreBWGButton.clicked.connect(self.restoreBWG)

        self.SandboxToCampaignButton = QPushButton("Sandbox to Campaign Items")
        self.SandboxToCampaignButton.setFixedSize(300,150)
        self.SandboxToCampaignButton.setEnabled(False)
        self.SandboxToCampaignButton.setToolTip("This button will unlock the Sandbox exclusive items recipes in Campaign mode.")
        #self.SandboxToCampaignButton.clicked.connect(self.sandboxToCampaign)

        self.addCosmeticArmorsButton = QPushButton("Add Cosmetic Armors")
        self.addCosmeticArmorsButton.setFixedSize(300,150)
        self.addCosmeticArmorsButton.setEnabled(False)
        #self.addCosmeticArmorsButton.clicked.connect(self.addCosmeticArmors)
        self.addCosmeticArmorsButton.setToolTip("This button will add the cosmetic armor recipes to the game.")

        layout.addWidget(QLabel("This tab is under construction, please wait for updates."), alignment=Qt.AlignHCenter)
        
        layout.addWidget(self.restoreBWGButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.SandboxToCampaignButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.addCosmeticArmorsButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def restoreBWG(self):
        """
        Restore the Shayar, Amzul and Masharuz armors.
        This function is not implemented yet.
        """
        QMessageBox.information(self, "Info", "This feature is not implemented yet.")