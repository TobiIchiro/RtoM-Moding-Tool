from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox,
    QGroupBox, QRadioButton, QButtonGroup, QCompleter, QCheckBox, QGridLayout
)
from PySide6.QtCore import Qt
import sys

from jsonHandler import (loadJson, saveJson)
from armorModUtils import (missingArmorRecipes, DTItemRecipesHandle)

import os

class ArmorAdderUI(QWidget):
    def __init__(self, execDir, scriptDir, items, unlockRequirementsItemsConstructions):
        super().__init__()
        self.setWindowTitle("More Armor Mod Updater")
        self.setMinimumWidth(500)
        self.setMaximumWidth(500)

        self.scriptDir = scriptDir
        self.execDir = execDir

        self.missingArmor = missingArmorRecipes(self.scriptDir)

        self.items = items
        self.materialsWidgets = []
        self.craftingStations = {
            "CraftingStation_BasicForge": "Forge",
            "CraftingStation_AdvancedForge": "Khuzdul Forge",
            "CraftingStation_Workbench": "Workbench",
            "CraftingStation_LegendayElvishForge": "Great Forge of Narvi",
            "CraftingStation_FloodedForge": "Great Belegost Forge",
            "CraftingStation_NogrodForge": "Great Forge of Nogrod",
            "CraftingStation_DurinForge": "Great Forge of Durin",
            "CraftingStation_MithrilForge": "Greaf Mithril Forge"
        }
        
        self.unlockType = "UnlockRequiredItems"

        self.unlockRequirements = unlockRequirementsItemsConstructions
        
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        self.ArmorComboBox = QComboBox()
        self.ArmorComboBox.setToolTip("Select the armor you want to add a recipe for")
        self.ArmorComboBox.addItems([list(d.keys())[0] for d in self.missingArmor])

        # Crafting Stations
        self.CraftingStationsGroup = QGroupBox("Crafting Stations")
        self.CraftingStationsGroup.setToolTip("Select the crafting stations where the armor can be crafted")
        self.CraftingStationsLayout = QGridLayout()

        self.craftingStationsCheckBoxes = []
        
        for index, (tag, displayName) in enumerate(self.craftingStations.items()):
            checkBox = QCheckBox(displayName)
            self.craftingStationsCheckBoxes.append(checkBox)
            row = index // 2
            col = index % 2
            self.CraftingStationsLayout.addWidget(checkBox, row, col)

        self.CraftingStationsGroup.setLayout(self.CraftingStationsLayout)

        
        # Required Materials
        self.materialsLayout = QVBoxLayout()

        buttonsLayout = QHBoxLayout()
        self.addMaterialButton = QPushButton("Add Material")
        self.addMaterialButton.setToolTip("Add a new material to the armor recipe")
        self.removeMaterialButton = QPushButton("Remove Material")
        self.removeMaterialButton.setToolTip("Remove the last added material from the armor recipe")
        
        self.addMaterialButton.clicked.connect(self.addMaterial)
        self.removeMaterialButton.clicked.connect(self.removeMaterial)

        buttonsLayout.addWidget(self.addMaterialButton)
        buttonsLayout.addWidget(self.removeMaterialButton)

        # Unlocked conditions
        self.unlockTConditionsGroupBox = QGroupBox("Unlock Conditions")
        self.unlockTConditionsGroupBox.setToolTip("Select the unlock conditions for the armor")
        self.unlockConditionsLayout = QVBoxLayout()
        self.unlockButtonsLayout = QHBoxLayout()

        self.unlockConditionsButtonGroup = QButtonGroup()

        self.constructionRadioButton = QRadioButton("Discover Construction")
        self.constructionRadioButton.clicked.connect(self.updateUnlockConstructionRequirements)
        self.constructionRadioButton.setToolTip("Unlock the armor by building a construction in game")
        self.materialRadioButton = QRadioButton("Discover Item")
        self.materialRadioButton.clicked.connect(self.updateUnlockItemsRequirements)
        self.materialRadioButton.setToolTip("Unlock the armor by discovering an item in game")
        
        self.materialRadioButton.setChecked(True)

        self.unlockConditionsButtonGroup.addButton(self.materialRadioButton)
        self.unlockConditionsButtonGroup.addButton(self.constructionRadioButton)

        self.unlockRequirementInput = QComboBox()
        self.unlockRequirementInput.addItems(self.unlockRequirements.get(self.unlockType,[]))

        #Save Button
        self.saveButton = QPushButton("Save Armor")
        self.saveButton.clicked.connect(self.saveArmor)
        self.saveButton.setToolTip("Save the armor recipe with the provided details")


        formLayout = QFormLayout()
        formLayout.addRow(QLabel("Armor Name:"), self.ArmorComboBox)
        formLayout.addRow(self.CraftingStationsGroup)

        layout.addLayout(formLayout)
        layout.addWidget(QLabel("Materials (max 6):"))
        layout.addLayout(self.materialsLayout)
        layout.addLayout(buttonsLayout)
        

        self.unlockButtonsLayout.addWidget(self.materialRadioButton)
        self.unlockButtonsLayout.addWidget(self.constructionRadioButton)
        self.unlockConditionsLayout.addLayout(self.unlockButtonsLayout)
        self.unlockConditionsLayout.addWidget(self.unlockRequirementInput)
        self.unlockTConditionsGroupBox.setLayout(self.unlockConditionsLayout)

        layout.addWidget(self.unlockTConditionsGroupBox)

        layout.addWidget(self.saveButton)

        self.setLayout(layout)

        self.addMaterial()  # Add the first material input by default
        self.updateUnlockItemsRequirements()  # Initialize unlock requirements
    
    def addMaterial(self):
        if len(self.materialsWidgets) >= 6:
            QMessageBox.warning(self, "Reached Limit", "You can only add up to 6 materials")
            return
        
        materialLayout = QHBoxLayout()

        materialCategoryInput = QComboBox()
        materialCategoryInput.addItems(list(self.items.keys()))

        materialNameInput = QComboBox()
        materialNameInput.setEditable(True)

        visibleToTag = {}

        def updateItemList(category):
            tags = self.items.get(category, {})
            materialNameInput.clear()
            visibleToTag.clear()

            displayNames = []
            for tag, name in tags.items():
                visibleToTag[name] = tag
                displayNames.append(name)
            
            displayNames.sort()  #Sort alphabetically
            materialNameInput.addItems(displayNames)

            completer = QCompleter(displayNames)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            materialNameInput.setCompleter(completer)

        materialCategoryInput.currentTextChanged.connect(updateItemList)
        updateItemList(materialCategoryInput.currentText())
        

        countInput = QSpinBox()
        countInput.setMinimum(1)
        countInput.setMaximum(999)

        materialLayout.addWidget(materialCategoryInput)
        materialLayout.addWidget(materialNameInput)
        materialLayout.addWidget(QLabel("x"))
        materialLayout.addWidget(countInput)

        self.materialsLayout.addLayout(materialLayout)
        self.materialsWidgets.append((materialNameInput,countInput, visibleToTag))
    
    def removeMaterial(self):
        if len(self.materialsWidgets) <= 1:
            QMessageBox.warning(self, "Minimum Materials", "You must have at least one material")
            return
        lastMaterialIndex = self.materialsLayout.count() - 1
        lastLayoutItem = self.materialsLayout.itemAt(lastMaterialIndex)
        
        if lastLayoutItem is not None:
            layout = lastLayoutItem.layout()
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
            self.materialsLayout.removeItem(layout)
        
        self.materialsWidgets.pop()

    def updateUnlockItemsRequirements(self):
        self.unlockType = "UnlockRequiredItems"
        self.unlockRequirementInput.clear()
        self.visibleUnlockTagMap = {}
        tagToName = self.unlockRequirements.get(self.unlockType, {})
        for tag, name in tagToName.items():
            self.visibleUnlockTagMap[name] = tag
            self.unlockRequirementInput.addItem(name)
        

    def updateUnlockConstructionRequirements(self):
        self.unlockType = "UnlockRequiredConstructions"
        self.unlockRequirementInput.clear()
        self.visibleUnlockTagMap = {}
        tagToName = self.unlockRequirements.get(self.unlockType, {})
        for tag, name in tagToName.items():
            self.visibleUnlockTagMap[name] = tag
            self.unlockRequirementInput.addItem(name)
    
    def saveArmor(self):
        if not any(cb.isChecked() for cb in self.craftingStationsCheckBoxes):
            QMessageBox.warning(self, "No Crafting Station Selected", "Please select at least one crafting station.")
            return
        armorName = self.ArmorComboBox.currentText()
        armorTag = self.missingArmor[self.ArmorComboBox.currentIndex()].get(armorName, None)

        materials = []
        for nameWidget, countWidget, visibleToTag in self.materialsWidgets:
            if isinstance(nameWidget,QComboBox):
                visibleName = nameWidget.currentText().strip()
                materialName = visibleToTag.get(visibleName, visibleName)
                count = countWidget.value()

                '''
                if materialName not in itemlist
                    QMessageBox.warning(self,"Invalid Material", "f"'{materialName}' is not a valid material)
                '''
                materials.append((materialName,count))
        
        craftingStations = [
            tag for tag, name in self.craftingStations.items()
            if any(cb.isChecked() and cb.text() == name for cb in self.craftingStationsCheckBoxes)
        ]
        selectedName = self.unlockRequirementInput.currentText()
        unlockRequirement = self.visibleUnlockTagMap.get(selectedName, selectedName)

        DTItemRecipesHandle(self.execDir, self.scriptDir, armorTag, craftingStations, materials, self.unlockType, unlockRequirement)


        self.missingArmor = missingArmorRecipes(self.scriptDir)
        self.ArmorComboBox.clear()
        self.ArmorComboBox.addItems([list(d.keys())[0] for d in self.missingArmor])
        