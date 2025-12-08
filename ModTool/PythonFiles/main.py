import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, 
    QWidget, QLabel, QVBoxLayout
    )
from PySide6.QtGui import QIcon
from jsonHandler import loadJson
from constructionUI import ConstructionAdderUI
from constructionUpdater import ConstructionUpdaterUI
from armorAdderUI import ArmorAdderUI
from armorUpdaterUI import ArmorUpdaterUI
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Loading Needed Files
        if getattr(sys, 'frozen', False):
            scriptDir = sys._MEIPASS
            iconPath = os.path.join(scriptDir,"Icon","ToolIcon.ico")
            dataDir = os.path.join(scriptDir, "Data")
            execDir = os.path.dirname(sys.executable)
        else:
            scriptDir = os.path.dirname(os.path.abspath(__file__))
            iconPath = os.path.join(scriptDir,"..","Icon","ToolIcon.ico")
            dataDir = os.path.join(scriptDir,"..","Data")
            execDir = scriptDir
        print(f"ScriptDir: {scriptDir}")
        print(f"ExecDir: {execDir}")
        print(f"IconDir: {iconPath}")
        print(f"DataDir: {dataDir}")
        self.setWindowTitle("TobiIchiro Moding Tool")
        self.setWindowIcon(QIcon(iconPath))

        #Tabs container
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        #DT_Items, Category
        itemsData = loadJson(os.path.abspath(os.path.join(dataDir, "MoreBuildings", "Items.json")))
        categoryTagsData = loadJson(os.path.abspath(os.path.join(dataDir, "MoreBuildings", "CategoryTags.json")))
        unlockRequirementsItemsConstructions = loadJson(os.path.abspath(os.path.join(dataDir, "MoreBuildings", "UnlockRequirementsItemsConstructions.json")))
        unlockRequirementsItemsConstructionsArmor = loadJson(os.path.abspath(os.path.join(dataDir, "MoreArmor", "UnlockRequirementsItemsConstructions.json")))

        #Tab 1: UI Adding New Construction Recipes
        constructRecipeAdderTab = ConstructionAdderUI(execDir, dataDir, itemsData, categoryTagsData, unlockRequirementsItemsConstructions)
        self.tabs.addTab(constructRecipeAdderTab, "New Construction Adder")

        #Tab 2: UI More Buildings Mantain Mod
        moreBuildingMantainModTab = ConstructionUpdaterUI(execDir)
        self.tabs.addTab(moreBuildingMantainModTab, "More Buildings Mantain Mod")

        #Tab 3: UI Adding New Armor Recipes
        armorAdderTab = ArmorAdderUI(execDir, dataDir, itemsData, unlockRequirementsItemsConstructionsArmor)
        self.tabs.addTab(armorAdderTab, "New Armor Adder")

        #Tab 4: Custom Armor Recipes Mantain Mod
        armorUpdaterTab = ArmorUpdaterUI(execDir, dataDir)
        self.tabs.addTab(armorUpdaterTab, "Armor Recipes Mantain Mod")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())