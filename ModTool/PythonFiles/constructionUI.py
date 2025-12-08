from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox,
    QGroupBox, QRadioButton, QButtonGroup, QCompleter
)
from PySide6.QtCore import Qt
import sys

from modUtils import (
    architectureHandle, DTConstructionsHandle, DTConstructionRecipesHandle
)

class ConstructionAdderUI(QWidget):
    def __init__(self, execDir, dataDir, Items, categoryTagsData, unlockRequirementsItemsConstructions):
        super().__init__()
        self.setWindowTitle("New Construction Adder")
        self.setMinimumWidth(500)

        self.execDir = execDir
        self.dataDir = dataDir
        
        self.items = Items
        self.materialsWidgets = []

        self.categoryTagsRaw = categoryTagsData
        self.mainCategories = sorted(set(k.split('.')[0] for k in categoryTagsData.keys()))
        self.subCategories = {}

        self.unlockType = "UnlockRequiredItems"

        for key in categoryTagsData.keys():
            main, sub = key.split('.')
            if main not in self.subCategories:
                self.subCategories[main] = []
            self.subCategories[main].append(sub)

        self.unlockRequirements = unlockRequirementsItemsConstructions

        self.setupUi()

    def updateSubCategories(self, mainCategory):
        self.categorySubInput.clear()
        self.categorySubInput.addItems(self.subCategories.get(mainCategory, []))
    
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

    def setupUi(self):
        layout = QVBoxLayout()

        # Text Fields
        self.userNameInput = QLineEdit()
        self.userNameInput.setToolTip("Enter the requester user name")
        self.userNameInput.setPlaceholderText("Enter your user name (e.g., Tobi)")
        self.nameInput = QLineEdit(maxLength=30)
        self.nameInput.setToolTip("Enter the construction name (30 characters max)")
        self.nameInput.setPlaceholderText("Enter the construction name (e.g., Dark Wood Floor)")
        self.constructionTag = QLineEdit()
        self.constructionTag.setEnabled(False)
        self.constructionTag.setPlaceholderText("")
        self.descriptionInput = QLineEdit(maxLength=60)
        self.descriptionInput.setToolTip("Enter the construction description (60 characters max)")
        self.descriptionInput.setPlaceholderText("Enter the construction description (e.g., A floor made of dark wood)")
        self.assetPathInput = QLineEdit()
        self.assetPathInput.setPlaceholderText("/Game/Items/Breakables/BreakableContainers/BP_BrewContainer")
        self.assetPathInput.setToolTip("Enter the asset path")

        # Category tags
        self.categoryMainInput = QComboBox()
        self.categoryMainInput.addItems(self.mainCategories)
        self.categoryMainInput.currentTextChanged.connect(self.updateSubCategories)
        self.categoryMainInput.setToolTip("Select the main category (e.g., Wood & Stone, Granite, etc.)")

        self.categorySubInput = QComboBox()
        self.updateSubCategories(self.categoryMainInput.currentText())
        self.categorySubInput.setToolTip("Select the sub category (e.g., Floors, Walls, etc.)")

        # Required Materials
        self.materialsLayout = QVBoxLayout()

        buttonsLayout = QHBoxLayout()
        self.addMaterialButton = QPushButton("Add Material")
        self.addMaterialButton.setToolTip("Add a new material to the construction")
        self.removeMaterialButton = QPushButton("Remove Material")
        self.removeMaterialButton.setToolTip("Remove the selected material from the construction")

        self.addMaterialButton.clicked.connect(self.addMaterial)
        self.removeMaterialButton.clicked.connect(self.removeMaterial)

        buttonsLayout.addWidget(self.addMaterialButton)
        buttonsLayout.addWidget(self.removeMaterialButton)

        # Unlocked conditions
        self.unlockTConditionsGroupBox = QGroupBox("Unlock Conditions")
        self.unlockTConditionsGroupBox.setToolTip("Select the unlock conditions for the construction")
        self.unlockConditionsLayout = QVBoxLayout()
        self.unlockButtonsLayout = QHBoxLayout()

        self.unlockConditionsButtonGroup = QButtonGroup()

        self.constructionRadioButton = QRadioButton("Discover Construction")
        self.constructionRadioButton.clicked.connect(self.updateUnlockConstructionRequirements)
        self.constructionRadioButton.setToolTip("Unlock the construction by building a construction in game")
        self.materialRadioButton = QRadioButton("Discover Item")
        self.materialRadioButton.clicked.connect(self.updateUnlockItemsRequirements)
        self.materialRadioButton.setToolTip("Unlock the construction by discovering an item in game")
        self.materialRadioButton.setChecked(True)

        self.unlockConditionsButtonGroup.addButton(self.materialRadioButton)
        self.unlockConditionsButtonGroup.addButton(self.constructionRadioButton)

        self.unlockRequirementInput = QComboBox()
        self.unlockRequirementInput.addItems(self.unlockRequirements.get(self.unlockType,[]))
        #self.unlockRequiredConstruction = QComboBox()

        #self.updateUnlockRequirements()

        # Buttons
        self.saveButton = QPushButton("Save Construction")
        self.saveButton.clicked.connect(self.saveConstruction)
        self.saveButton.setToolTip("Save the construction recipe with the provided details")

        # Form Layout
        formLayout = QFormLayout()
        formLayout.addRow("User Name",self.userNameInput)
        formLayout.addRow("Name", self.nameInput)
        formLayout.addRow("Name Tag", self.constructionTag)
        formLayout.addRow("Description", self.descriptionInput)
        formLayout.addRow("Asset Path", self.assetPathInput)
        formLayout.addRow("Main Category", self.categoryMainInput)
        formLayout.addRow("Sub Category", self.categorySubInput)

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
        self.addMaterial()
        self.updateUnlockItemsRequirements()
  
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
        
    def saveConstruction(self):
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
        
        userName = self.userNameInput.text().strip()
        name = self.nameInput.text().strip()
        description = self.descriptionInput.text().strip()
        assetPath = self.assetPathInput.text().strip()
        categoryKey = f"{self.categoryMainInput.currentText()}.{self.categorySubInput.currentText()}"
        categoryTag = self.categoryTagsRaw.get(categoryKey,"")

        if not name or not description or not assetPath:
            QMessageBox.warning(self,"Empty Fields","Please fill the empty fields")
            return

        tag = userName + "Pack_" + name.title().replace(" ","")

        #Generate Unique tag and save Architecture.json for generating Mod and mantain for future updates
        uniqueTag = architectureHandle(tag, name, description, self.execDir)
        self.constructionTag.setText(uniqueTag)
        
        DTConstructionsHandle(uniqueTag, assetPath, categoryTag, self.execDir, self.dataDir, userName)
        selectedName = self.unlockRequirementInput.currentText()
        unlockRequirement = self.visibleUnlockTagMap.get(selectedName, selectedName)

        DTConstructionRecipesHandle(uniqueTag, self.execDir, self.dataDir, categoryKey, materials, self.unlockType, unlockRequirement)
        
    



