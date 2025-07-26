from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox,
    QGroupBox, QRadioButton, QButtonGroup, QCompleter
)
from PySide6.QtCore import Qt
import sys
import os

from jsonHandler import (
        loadJson, saveJson
)

class ConstructionUpdaterUI(QWidget):
    def __init__(self, scriptDir):
        super().__init__()
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)

        self.scriptDir = scriptDir

        self.setUpUI()

    def setUpUI(self):
        layout = QVBoxLayout()

        self.updaterButton = QPushButton()
        self.updaterButton.setText("Update Mod")
        self.updaterButton.setFixedSize(300,150)
        self.updaterButton.setEnabled(True)
        self.updaterButton.clicked.connect(self.updateMod)

        layout.addWidget(self.updaterButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def buildPath(self, category, fileName):
        base = {
            "vanilla": os.path.join(self.scriptDir,"..","Saves","UpdateMods","MoreBuildings"),
            "new": os.path.join(self.scriptDir,"..","Saves","newObjects","MoreBuildings"),
            "moded": os.path.join(self.scriptDir,"..","Saves","UpdateMods","MoreBuildings","moded")
        }[category]
        return os.path.abspath(os.path.join(base, fileName))

    def updateMod(self):

        #Vanila files from update
        architectureJson = loadJson(self.buildPath("vanilla", "Architecture.json"))
        DT_ConstructionRecipesJson = loadJson(self.buildPath("vanilla", "DT_ConstructionRecipes.json"))
        DT_ConstructionsJson = loadJson(self.buildPath("vanilla", "DT_Constructions.json"))

        #Files containing new constructions
        newArchitectureJson = loadJson(self.buildPath("new", "Architecture.json"))
        newDT_ConstructionRecipesJson = loadJson(self.buildPath("new", "DT_ConstructionRecipes.json"))
        newDT_ConstructionsJson = loadJson(self.buildPath("new", "DT_Constructions.json"))
        

        #Apend Architecture
        architectureJson["Exports"][0]["Table"]["Value"].extend(newArchitectureJson["Exports"][0]["Table"]["Value"])
        
        #Apend Constructions
        vanillaImportsLength = len(DT_ConstructionsJson["Imports"])
        #Updating imports 2DTextures OuterIndex
        for i, importObj in enumerate(newDT_ConstructionsJson["Imports"]):
            if importObj["OuterIndex"] < 0:
                importObj["OuterIndex"] = -(vanillaImportsLength + abs(importObj["OuterIndex"]) - 1005)

        #Updating icon reference 
        for construction in newDT_ConstructionsJson["Exports"][0]["Table"]["Data"]:
            for prop in construction["Value"]:
                if prop["$type"] == "UAssetAPI.PropertyTypes.Objects.ObjectPropertyData, UAssetAPI":
                    if isinstance(prop.get("Value"), int) and prop["Value"] < 0:
                        prop["Value"] = -(vanillaImportsLength + abs(prop["Value"]) - 1006)
        
        DT_ConstructionsJson["NameMap"].extend(newDT_ConstructionsJson["NameMap"])
        DT_ConstructionsJson["Exports"][0]["Table"]["Data"].extend(newDT_ConstructionsJson["Exports"][0]["Table"]["Data"])
        DT_ConstructionsJson["Imports"].extend(newDT_ConstructionsJson["Imports"])
        
        #Append ConstructionRecipes
        DT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"].extend(newDT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"])

        #Generated Mod Files 
        saveJson(self.buildPath("moded", "Architecture.json"), architectureJson)
        saveJson(self.buildPath("moded", "DT_ConstructionRecipes.json"), DT_ConstructionRecipesJson)
        saveJson(self.buildPath("moded", "DT_Constructions.json"),DT_ConstructionsJson)



