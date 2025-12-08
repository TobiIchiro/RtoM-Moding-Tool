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

class ConstructionRestoreUI(QWidget):
    def __init__(self, scriptDir):
        super().__init__()
        self.setWindowTitle("Restore Constructions")
        self.setMinimumWidth(500)
        self.scriptDir = scriptDir

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.updaterButton = QPushButton()
        self.updaterButton.setText("Restore Constructions")
        self.updaterButton.setFixedSize(300,150)
        self.updaterButton.clicked.connect(self.restoreConstructions)

        layout.addWidget(self.updaterButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def restoreConstructions(self):
        DT_ConstructionRecipesPath = os.path.abspath(os.path.join(self.scriptDir,"..","Saves","mods","MoreBuildings","DT_ConstructionRecipes.json"))

        data = loadJson(DT_ConstructionRecipesPath)

        constructions = [
            "Elder_Archway_A",
            "Advanced_Column_Wood_A",
            "Advanced_Column_Wood_D",
            "Advanced_Fence_Wood_1m",
            "Advanced_Fence_Wood",
            "Crude_Column",
            "Elder_Wall_E",
            "Scaffolding_Platform_Open",
            "Elder_Wall_A_Crown",
            "Elder_Wall_Short_A",
            "Elder_Window_B",
            "Elder_Window_A",
            "Elder_Wall_Thin_A_Crown",
            "Elder_Wall_Thin_B",
            "Elder_Archway_C",
            "Elder_Wall_B_Crown",
            "Elder_Wall_D",
            "Advanced_Column_Wood_B",
            "Elder_Wall_E_Crown",
            "Elder_Archway_Corner",
            "Scaffolding_Platform_1x1x3",
            "Elder_Wall_Short_B",
            "Elder_Wall_B",
            "Elder_Window_C",
            "Elder_Wall_A",
            "Elder_Wall_C",
            "Elder_Wall_Thin_A",
            "Scaffolding_Platform_1x3x3",
            "Elder_Archway_Vertical",
            "Elder_Archway_Horizontal_Large",
            "Elder_Wall_Corner_Crown",
            "Advanced_Stairs_Railing_1m_V2"
        ]

        recipeList = data["Exports"][0]["Table"]["Data"]
        modifiedCount = 0

        for recipe in recipeList:
            name = recipe.get("Name")
            if name in constructions:
                try:
                    recipe["Value"][20]["Value"][0]["Value"] = "EMorRecipeUnlockType::DiscoverDependencies"
                except (KeyError, IndexError, TypeError):
                    continue
        
        saveJson(DT_ConstructionRecipesPath, data)