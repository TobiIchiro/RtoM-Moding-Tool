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
import copy
import re

class ArmorUpdaterUI(QWidget):
    def __init__(self, execDir, scriptDir):
        super().__init__()
        self.setWindowTitle("More Armor Mod Updater")
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)
        self.scriptDir = scriptDir
        self.execDir = execDir
        self.setupUI()
    
    def setupUI(self):
        layout = QVBoxLayout()

        self.restoreBWGButton = QPushButton()
        self.restoreBWGButton.setText("Restore Shayar, Amzul and Masharuz armors")
        self.restoreBWGButton.setFixedSize(300,150)
        self.restoreBWGButton.setEnabled(False)
        self.restoreBWGButton.setToolTip("This button will restore the recipes for Shayar, Amzul and Masharuz armors.")
        self.restoreBWGButton.clicked.connect(self.restoreBWG)

        self.SandboxToCampaignButton = QPushButton("Sandbox to Campaign Items")
        self.SandboxToCampaignButton.setFixedSize(300,150)
        self.SandboxToCampaignButton.setEnabled(False)
        self.SandboxToCampaignButton.setToolTip("This button will unlock the Sandbox exclusive items recipes in Campaign mode.")
        self.SandboxToCampaignButton.clicked.connect(self.sandboxToCampaign)

        self.addCosmeticArmorsButton = QPushButton("Add Cosmetic Armors")
        self.addCosmeticArmorsButton.setFixedSize(300,150)
        self.addCosmeticArmorsButton.setEnabled(False)
        self.addCosmeticArmorsButton.clicked.connect(self.addCosmeticArmors)
        self.addCosmeticArmorsButton.setToolTip("This button will add the cosmetic armor recipes to the game.")

        layout.addWidget(QLabel("This tab is under construction, please wait for updates."), alignment=Qt.AlignHCenter)
        
        layout.addWidget(self.restoreBWGButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.SandboxToCampaignButton, alignment=Qt.AlignHCenter)
        layout.addWidget(self.addCosmeticArmorsButton, alignment=Qt.AlignHCenter)

        self.setLayout(layout)
    
    def cleanName(self, name):
        """
        Clean the name by removing _White_, _Black_, and _Gold_.
        """
        return re.sub(r'_(White|Black|Gold)_', '_', name)

    def restoreBWG(self):
        """
        Restore the Shayar, Amzul and Masharuz armors.
        """
        DT_ItemRecipesPath = os.path.join(self.execDir,"..", "Saves", "UpdateMods", "MoreArmor", "DT_ItemRecipes.json")
        templatePath = os.path.join(self.scriptDir,"..", "Data", "MoreArmor", "UnlockRequiredItems.json")
        DT_modedItemRecipesPath = os.path.join(self.execDir, "..", "Saves", "UpdateMods", "MoreArmor", "moded", "DT_ItemRecipes.json")

        DT_ItemRecipes = loadJson(DT_ItemRecipesPath)
        templateObj = loadJson(templatePath)

        exports = DT_ItemRecipes.get("Exports", [])
        if not exports:
            QMessageBox.warning(self, "Warning", "Could not find elements in 'Exports'.")
            return

        tableData = exports[0].get("Table", {}).get("Data", [])

        for item in tableData:
            try:
                rawName = item["Value"][0]["Value"][0]["Value"]
            except (IndexError, KeyError, TypeError):
                print("[Advertencia] No se encontró Value[0].Value[0].Value en un item")
                continue
            if any(color in rawName for color in ["_White_", "_Black_", "_Gold_"]):
                # Paso 1: limpiar nombre
                baseName = self.cleanName(rawName)

                # Paso 2: Cambiar UnlockType si es necesario
                try:
                    unlockType = item["Value"][12]["Value"][0]["Value"]
                    if unlockType == "EMorRecipeUnlockType::Manual":
                        item["Value"][12]["Value"][0]["Value"] = "EMorRecipeUnlockType::DiscoverDependencies"
                except (IndexError, KeyError):
                    QMessageBox.warning(self, "Warning", f"Could not modify UnlockType in {rawName}")

                # Paso 3: Reemplazar posición 3 con JSON de plantilla
                try:
                    newObj = copy.deepcopy(templateObj)
                    newObj["Value"][0]["Value"][0]["Value"] = baseName
                    item["Value"][12]["Value"][3] = newObj
                except (IndexError, KeyError, TypeError):
                    QMessageBox.warning(self, "Warning", f"Could not replace RequiredRecipe in {rawName}")
        
        # Guardar el archivo modificado
        saveJson(DT_modedItemRecipesPath, DT_ItemRecipes)
        QMessageBox.information(self, "Success", "Shayar, Amzul and Masharuz armors have been restored successfully.")

        self.restoreBWGButton.setEnabled(False)
        self.SandboxToCampaignButton.setEnabled(True)

    def sandboxToCampaign(self):
        """
        Unlock the Sandbox exclusive items recipes in Campaign mode.
        This function is not implemented yet.
        """
        sandboxExclusiveItemsList = [
            "Spear_1h_t1_TU2", #Iron Spear
            "WarAxe_1h_t2", #Steel War Axe
            "WarAxe_1h_t3", #First Age Battle Axe
            "Battleaxe_2h_t2", #Belegost War Axe
            "Halberd_2h_t2", #Khazâd Army Halberd
            "Sword_2h_t2", #Khazâd Army Greatsword
            "Battleaxe_2h_t4", #Barôkamlut
            "FamousElvenSword", #Dagamarth
        ]
        sandboxExclusiveArmorList = [
            "Amazing_Set_HelmetArmor", #Gatherer’s Hat
            "Wonderful_Set_HelmetArmor", #Wolf Skin Hat
            "SouthernmostFireProof_Set_HelmetArmor", #Spiked Helmet
            "BlueMountainsHunter_Set_TorsoArmor", #Blue Mountains Hunter's Armor
            "BlueMountainsHunter_Set_BootsArmor", #Blue Mountains Hunter’s Boots
            "RangeBonus_Set_GlovesArmor", #Blue Mountains Hunter’s Gloves
            "AntiColdTorso", #Grey Mountain Overcoat
            "AntiColdBoots", #Grey Mountains Boots
            "AntiColdGloves", #Grey Mountain Gloves
            "AntiColdHelm", #Grey Mountain Helmet
            "Nogrod_Set_TorsoArmor", #Nogrod Armor,
            "Nogrod_Set_GlovesArmor", #Nogrod Gloves
        ]

        #Step 1: Load Json files
        #Step 2: Check for every sandbox exclusive item in the DT_ItemRecipes.json
        #Step 3: check if the item is not in the campaign mode by checking defaultunlocks
        #Step 4: If the the item is not, change the unlock type to DiscoverDependencies
        #Step 5: Add unlock requirements to the item
        #Step 6: Save the modified DT_ItemRacipes.json
        #Step 7: Show a message box with the success message
        #Step 8: Enable the addCosmeticArmorsButton
        QMessageBox.information(self, "Information", "This feature is not implemented yet. Please wait for updates.")
        self.SandboxToCampaignButton.setEnabled(False)
        self.addCosmeticArmorsButton.setEnabled(True)
    
    def addCosmeticArmors(self):
        """
        Add the cosmetic armor recipes to the game.
        This function is not implemented yet.
        """

        #Step 1: Load new armor recipes and vanilla file.
        #Step 2: Extend NameMap with the new armor recipes file NameMap.
        #Step 3: Extend Exports with the new armor recipes file Exports.
        #Step 4: Save the modified DT_ItemRecipes.json
        #Step 5: Show a message box with the success message
        #Step 6: Enable the restoreBWGButton
        QMessageBox.information(self, "Information", "This feature is not implemented yet. Please wait for updates.")
        self.addCosmeticArmorsButton.setEnabled(False)
        self.restoreBWGButton.setEnabled(True)
        