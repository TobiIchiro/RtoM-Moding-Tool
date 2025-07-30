from jsonHandler import (
    loadJson, saveJson
)
import os

import copy


def missingArmorRecipes(scriptDir, execDir):
    """
    Check if the armor recipes are missing in the DT_ItemRecipes.json file.
    Returns:
        list: A list of missing armor recipes.
    """
    dtItemRecipesPath = os.path.join(execDir, "..", "Saves", "UpdateMods","MoreArmor", "DT_ItemRecipes.json")
    newDtItemRecipesPath = os.path.join(execDir, "..", "Saves", "newObjects", "MoreArmor", "DT_ItemRecipes.json")
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
    craftingStationArray = craftingStationsArrayHandler(craftingStations, craftingStationTemplate)
    itemRecipeTemplate["Value"][3]["Value"] = craftingStationArray 

    #Handle required materials to craft
    itemArray = craftingMaterialsHandler(materials, requiredMaterialTemplate)
    itemRecipeTemplate["Value"][8]["Value"] = itemArray

    #Handle unlock conditions
    unlockConditionsHandler(itemRecipeTemplate, unlockOption, unlockRequirement, unlockRequirementsStructs, dummyStructs)

    #Add the new item recipe to the DT_ItemRecipes
    newDT_ItemRecipes["NameMap"].append(armorTag)
    newDT_ItemRecipes["NameMap"].append(f'Armor.{armorTag}')
    newDT_ItemRecipes["Exports"][0]["Table"]["Data"].append(itemRecipeTemplate)

    saveJson(newArmorRecipesPath, newDT_ItemRecipes)

def craftingStationsArrayHandler(craftingStations, craftingStationTemplate):
    """
    Creates a crafting stations list
    Args:
        craftingStations (list): craftingStations where item or armor can be crafted
        craftingStationTemplate (dict): Template for CraftingStation
    """
    craftingStationArray = []
    for craftingStation in craftingStations:
        newCraftingStation = copy.deepcopy(craftingStationTemplate)
        newCraftingStation["Value"][0]["Value"] = craftingStation
        craftingStationArray.append(newCraftingStation)
    
    return craftingStationArray

def craftingMaterialsHandler(materials, requiredMaterialTemplate):
    """
    Creates a list of required materials for crafting item or armor
    Args: 
        materials (list): required materials for crafting item or armor
        requiredMaterialTemplate (dict): Template of the structure for the required material
    """
    itemArray = []
    for item in materials:
        newItem = copy.deepcopy(requiredMaterialTemplate)
        newItem["Value"][0]["Value"][0]["Value"] = item[0]
        newItem["Value"][2]["Value"] = item[1]
        itemArray.append(newItem)
    
    return itemArray

def unlockConditionsHandler(itemRecipeTemplate, unlockOption, unlockRequirement, unlockRequirementsStructs, dummyStructs):
    """
    Modifies unlock conditions based on selected option
    Args:
        itemRecipeTemplate (dict): Template to modify
        unlockOption (str): UnlockRequiredItems" or "UnlockRequiredConstructions"
        unlockRequirement (str): Requieremnt to unlock, can be Item or Construction
        dummyStructs (dict): Empty Structs for not used fields
    """
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


def sandboxExclusiveItemsListHandler():
    sandboxExclusiveItemsList = [
            {"Tag":"Spear_1h_t1_TU2", "UnlockOption":"UnlockRequiredConstructions", "UnlockRequirement":"CraftingStation_BasicForge"}, #Iron Spear
            {"Tag":"WarAxe_1h_t2", "UnlockOption":"", "UnlockRequirement":""}, #Steel War Axe
            {"Tag":"WarAxe_1h_t3", "UnlockOption":"", "UnlockRequirement":""}, #First Age Battle Axe
            {"Tag":"Battleaxe_2h_t2", "UnlockOption":"", "UnlockRequirement":""}, #Belegost War Axe
            {"Tag":"Halberd_2h_t2", "UnlockOption":"", "UnlockRequirement":""}, #Khazâd Army Halberd
            {"Tag":"Sword_2h_t2", "UnlockOption":"", "UnlockRequirement":""}, #Khazâd Army Greatsword
            {"Tag":"Battleaxe_2h_t4", "UnlockOption":"", "UnlockRequirement":""}, #Barôkamlut
            {"Tag":"FamousElvenSword", "UnlockOption":"", "UnlockRequirement":""}, #Dagamarth
            {"Tag":"Amazing_Set_HelmetArmor", "UnlockOption":"", "UnlockRequirement":""}, #Gatherer’s Hat
            {"Tag":"Wonderful_Set_HelmetArmor", "UnlockOption":"", "UnlockRequirement":""}, #Wolf Skin Hat
            {"Tag":"SouthernmostFireProof_Set_HelmetArmor", "UnlockOption":"", "UnlockRequirement":""}, #Spiked Helmet
            {"Tag":"BlueMountainsHunter_Set_TorsoArmor", "UnlockOption":"", "UnlockRequirement":""}, #Blue Mountains Hunter's Armor
            {"Tag":"BlueMountainsHunter_Set_BootsArmor", "UnlockOption":"", "UnlockRequirement":""}, #Blue Mountains Hunter’s Boots
            {"Tag":"RangeBonus_Set_GlovesArmor", "UnlockOption":"", "UnlockRequirement":""}, #Blue Mountains Hunter’s Gloves
            {"Tag":"AntiColdTorso", "UnlockOption":"", "UnlockRequirement":""}, #Grey Mountain Overcoat
            {"Tag":"AntiColdBoots", "UnlockOption":"", "UnlockRequirement":""}, #Grey Mountains Boots
            {"Tag":"AntiColdGloves", "UnlockOption":"", "UnlockRequirement":""}, #Grey Mountain Gloves
            {"Tag":"AntiColdHelm", "UnlockOption":"", "UnlockRequirement":""}, #Grey Mountain Helmet
            {"Tag":"Nogrod_Set_TorsoArmor", "UnlockOption":"", "UnlockRequirement":""}, #Nogrod Armor,
            {"Tag":"Nogrod_Set_GlovesArmor", "UnlockOption":"", "UnlockRequirement":""} #Nogrod Gloves
        ]
    return sandboxExclusiveItemsList