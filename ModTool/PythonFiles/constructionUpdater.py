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

        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore Constructions")
        self.restoreButton.setFixedSize(300,150)
        self.restoreButton.clicked.connect(self.restoreConstructions)
        self.restoreButton.setEnabled(True)
        self.restoreButton.setToolTip("This button will restore the constructions removed in the 1.2 update.")

        self.updaterButton = QPushButton()
        self.updaterButton.setText("Update Mod")
        self.updaterButton.setFixedSize(300,150)
        self.updaterButton.setEnabled(False)
        self.updaterButton.clicked.connect(self.updateMod)
        self.updaterButton.setToolTip("This button will update the mod with the new constructions.")

        layout.addWidget(self.restoreButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.updaterButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)
    
    def buildPath(self, category, fileName):
        base = {
            "vanilla": os.path.join(self.scriptDir,"..","Saves","UpdateMods","MoreBuildings"),
            "new": os.path.join(self.scriptDir,"..","Saves","newObjects","MoreBuildings"),
            "moded": os.path.join(self.scriptDir,"..","Saves","UpdateMods","MoreBuildings","moded")
        }[category]
        return os.path.abspath(os.path.join(base, fileName))
    
    def restoreConstructions(self):
        #Vanila files from update
        data = loadJson(self.buildPath("vanilla", "DT_ConstructionRecipes.json"))

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
            "Advanced_Stairs_Railing_1m_V2",
            "Advanced_Bannister_Post_Stone"
        ]

        recipeList = data["Exports"][0]["Table"]["Data"]

        for recipe in recipeList:
            name = recipe.get("Name")
            if name in constructions:
                try:
                    recipe["Value"][20]["Value"][0]["Value"] = "EMorRecipeUnlockType::DiscoverDependencies"
                except (KeyError, IndexError, TypeError):
                    continue

        saveJson(self.buildPath("moded", "DT_ConstructionRecipes.json"), data)
        QMessageBox.information(self, "Restoration Complete", "Constructions removed in 1.2 have been restored.")
        self.restoreButton.setEnabled(False)
        self.updaterButton.setEnabled(True)

    def updateMod(self):

        #Moded files after restoring constructions
        architectureJson = loadJson(self.buildPath("vanilla", "Architecture.json"))
        DT_ConstructionRecipesJson = loadJson(self.buildPath("moded", "DT_ConstructionRecipes.json"))
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
                importObj["OuterIndex"] = -(vanillaImportsLength + abs(importObj["OuterIndex"]))

        #Updating icon reference 
        for construction in newDT_ConstructionsJson["Exports"][0]["Table"]["Data"]:
            for prop in construction["Value"]:
                if prop["$type"] == "UAssetAPI.PropertyTypes.Objects.ObjectPropertyData, UAssetAPI":
                    if isinstance(prop.get("Value"), int) and prop["Value"] < 0:
                        prop["Value"] = -(vanillaImportsLength + abs(prop["Value"]))
        
        DT_ConstructionsJson["NameMap"].extend(newDT_ConstructionsJson["NameMap"])
        DT_ConstructionsJson["Exports"][0]["Table"]["Data"].extend(newDT_ConstructionsJson["Exports"][0]["Table"]["Data"])
        DT_ConstructionsJson["Imports"].extend(newDT_ConstructionsJson["Imports"])
        
        #Append ConstructionRecipes
        for nameMap in newDT_ConstructionRecipesJson["NameMap"]:
            if nameMap not in DT_ConstructionRecipesJson["NameMap"]:
                DT_ConstructionRecipesJson["NameMap"].append(nameMap)
        DT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"].extend(newDT_ConstructionRecipesJson["Exports"][0]["Table"]["Data"])

        #Generated Mod Files 
        saveJson(self.buildPath("moded", "Architecture.json"), architectureJson)
        saveJson(self.buildPath("moded", "DT_ConstructionRecipes.json"), DT_ConstructionRecipesJson)
        saveJson(self.buildPath("moded", "DT_Constructions.json"),DT_ConstructionsJson)



