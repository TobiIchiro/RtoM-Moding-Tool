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

        self.scripDir = scriptDir

        self.setUpUI()

    def setUpUI(self):
        layout = QVBoxLayout()

        self.updaterButton = QPushButton()
        self.updaterButton.setText("Update Mod")
        self.updaterButton.setFixedSize(300,150)
        self.updaterButton.clicked.connect(self.updateMod)

        layout.addWidget(self.updaterButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def updateMod(self):
        #Vanila files from update
        architecturePath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","Architecture.json"))
        DT_ConstructionRecipesPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","DT_ConstructionRecipes.json"))
        DT_ConstructionsPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","DT_Constructions.json"))

        architectureJson = loadJson(architecturePath)
        DT_ConstructionRecipesJson = loadJson(DT_ConstructionRecipesPath)
        DT_ConstructionsJson = loadJson(DT_ConstructionsPath)

        #Files containing new constructions
        newArchitecturePath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","newObjects","MoreBuildings","Architecture.json"))
        newDT_ConstructionRecipesPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","newObjects","MoreBuildings","DT_ConstructionRecipes.json"))
        newDT_ConstructionsPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","newObjects","MoreBuildings","DT_Constructions.json"))

        newArchitectureJson = loadJson(newArchitecturePath)
        newDT_ConstructionRecipesJson = loadJson(newDT_ConstructionRecipesPath)
        newDT_ConstructionsJson = loadJson(newDT_ConstructionsPath)
        

        #Apend Architecture
        for architecture in newArchitectureJson["Exports"][0]["Table"]["Value"]:
            architectureJson["Exports"][0]["Table"]["Value"].append(architecture)
        #Apend Constructions
        for nameMap in newDT_ConstructionsJson["NameMap"]:
            DT_ConstructionsJson["NameMap"].append(nameMap)
        for construction in newDT_ConstructionsJson["Exports"][0]["Table"]["Data"]:
            DT_ConstructionsJson["Exports"][0]["Table"]["Data"].append(construction)
        for importObject in newDT_ConstructionsJson["Imports"]:
            DT_ConstructionsJson["Imports"].append(importObject)
        
        #Append ConstructionRecipes
        for nameMap in newDT_ConstructionRecipesJson["NameMap"]:
            DT_ConstructionRecipesJson["NameMap"].append(nameMap)
        for constructionRecipe in newDT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"]:
            DT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"].append(constructionRecipe)

        #Generated Mod Files
        architectureModPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","moded","Architecture.json"))
        DT_ConstructionRecipesModPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","moded","DT_ConstructionRecipes.json"))
        DT_ConstructionsModPath = os.path.abspath(os.path.join(self.scripDir,"..","Saves","UpdateMods","MoreBuildings","moded","DT_Constructions.json")) 
        
        saveJson(architectureModPath,architectureJson)
        saveJson(DT_ConstructionRecipesModPath,DT_ConstructionRecipesJson)
        saveJson(DT_ConstructionsModPath,DT_ConstructionsJson)



