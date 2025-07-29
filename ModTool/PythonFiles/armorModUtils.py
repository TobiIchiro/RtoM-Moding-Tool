from jsonHandler import (
    loadJson, saveJson
)
import os

import copy


def missingArmorRecipes(scriptDir):
    """
    Check if the armor recipes are missing in the DT_ItemRecipes.json file.
    Returns:
        list: A list of missing armor recipes.
    """
    dtItemRecipesPath = os.path.join(scriptDir, "..", "Saves", "UpdateMods","MoreArmor", "DT_ItemRecipes.json")
    newDtItemRecipesPath = os.path.join(scriptDir, "..", "Saves", "newObjects", "MoreArmor", "DT_ItemRecipes.json")
    dtArmorPath = os.path.join(scriptDir, "..", "Data", "MoreArmor", "Armor.json")
    missingArmorList = []

    dtItemRecipes = loadJson(dtItemRecipesPath)
    newDtItemRecipes = loadJson(newDtItemRecipesPath)
    dtArmor = loadJson(dtArmorPath)

    itemRecipes = (
        dtItemRecipes.get("Exports",[{}])[0]
        .get("Table",{})
        .get("Data",[])
    )

    newItemRecipes = (
        newDtItemRecipes.get("Exports",[{}])[0]
        .get("Table",{})
        .get("Data",[])
    )

    recipeNames = {recipe.get("Name") for recipe in itemRecipes}
    newRecipesNames = {recipe.get("Name") for recipe in newItemRecipes}

    for armorTag, armorName in dtArmor.items():
        if armorTag not in recipeNames and armorTag not in newRecipesNames:
            missingArmorList.append({armorName: armorTag})


    return missingArmorList

def DTItemRecipesHandle(path, dataDir, armorTag, craftingStations, materials, unlockOption, unlockRequirement):
    """
    Handle the creation of a new item recipe in the DT_ItemRecipes.json file.
    """

    itemRecipePath = os.path.abspath(os.path.join(dataDir,"MoreArmor", "ItemRecipeTemplate.json"))
    craftingStationPath = os.path.abspath(os.path.join(dataDir, "MoreArmor", "CraftingStationTemplate.json"))
    requiredMaterialPath = os.path.abspath(os.path.join(dataDir, "MoreArmor", "RequiredMaterialTemplate.json"))
    dummyStructsPath = os.path.abspath(os.path.join(dataDir, "MoreArmor", "DumyStructs.json"))
    unlockRequirementsPath = os.path.abspath(os.path.join(dataDir,"MoreArmor","UnlockRequirementsStructs.json"))

    itemRecipeTemplate = loadJson(itemRecipePath)
    craftingStationTemplate = loadJson(craftingStationPath)
    requiredMaterialTemplate = loadJson(requiredMaterialPath)
    dummyStructs = loadJson(dummyStructsPath)
    unlockRequirementsStructs = loadJson(unlockRequirementsPath)

    newArmorRecipesPath = os.path.abspath(os.path.join(path,"..", "Saves", "newObjects", "MoreArmor", "DT_ItemRecipes.json"))
    
    newDT_ItemRecipes = loadJson(newArmorRecipesPath)


    itemRecipeTemplate["Name"] = armorTag
    itemRecipeTemplate["Value"][0]["Value"][0]["Value"] = f'Armor.{armorTag}'
    
    #Handle crafting stations
    craftingStationArray = []
    for craftingStation in craftingStations:
        newCraftingStation = copy.deepcopy(craftingStationTemplate)
        newCraftingStation["Value"][0]["Value"] = craftingStation
        craftingStationArray.append(newCraftingStation)

    itemRecipeTemplate["Value"][3]["Value"] = craftingStationArray

    #Handle required materials to craft
    itemArray = []
    for item in materials:
        newItem = copy.deepcopy(requiredMaterialTemplate)
        newItem["Value"][0]["Value"][0]["Value"] = item[0]
        newItem["Value"][2]["Value"] = item[1]
        itemArray.append(newItem)

    itemRecipeTemplate["Value"][8]["Value"] = itemArray

    #Handle unlock conditions
    if unlockOption == "UnlockRequiredItems":
        unlockRequiredItems = unlockRequirementsStructs["UnlockRequiredItems"].copy()
        unlockRequiredItems["Value"][0]["Value"][0]["Value"] = unlockRequirement
        itemRecipeTemplate["Value"][12]["Value"][3] = unlockRequiredItems
        itemRecipeTemplate["Value"][12]["Value"][4] = dummyStructs["UnlockRequiredConstructions"]
    else:
        unlockRequiredConstruction = unlockRequirementsStructs["UnlockRequiredConstructions"].copy()
        unlockRequiredConstruction["Value"][0]["Value"][0]["Value"] = unlockRequirement
        itemRecipeTemplate["Value"][12]["Value"][3] = dummyStructs["UnlockRequiredItems"]
        itemRecipeTemplate["Value"][12]["Value"][4] = unlockRequiredConstruction

    #Add the new item recipe to the DT_ItemRecipes
    newDT_ItemRecipes["NameMap"].append(armorTag)
    newDT_ItemRecipes["NameMap"].append(f'Armor.{armorTag}')
    newDT_ItemRecipes["Exports"][0]["Table"]["Data"].append(itemRecipeTemplate)

    saveJson(newArmorRecipesPath, newDT_ItemRecipes)