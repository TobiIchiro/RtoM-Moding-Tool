from jsonHandler import (
        loadJson, saveJson
)
import copy
import os

def genUniqueTag(baseTag, exports):
        from string import ascii_uppercase

        existingEntries = {entry[0] for entry in exports if isinstance(entry, list) and len(entry) == 2}

        for letter in ascii_uppercase:
                newTag = f"{baseTag}_{letter}.Name"
                if newTag not in existingEntries:
                        return letter
        raise ValueError("Could'nt generate a unique name for the base tag '{basTag}' (A-Z deoleated)")

def architectureHandle(tag, name, description, path):

        #File paths
        modPath = os.path.abspath(os.path.join(path,"..","Saves","mods","MoreBuildings","Architecture.json"))
        newPath = os.path.abspath(os.path.join(path,"..","Saves","newObjects","MoreBuildings","Architecture.json"))

        #Loading Files
        architectureModData = loadJson(modPath)
        architectureNewData = loadJson(newPath)

        #Export Lists
        exportsMod = architectureModData["Exports"][0]["Table"]["Value"]
        exportsNew = architectureNewData["Exports"][0]["Table"]["Value"]

        #Get unique tag
        uniqueLetter = genUniqueTag(tag, exportsMod)
        uniqueTag = f"{tag}_{uniqueLetter}"

        #Preapering string arrays
        nameArray = [f"{uniqueTag}.Name", name]
        descriptionArray = [f"{uniqueTag}.Description", description]

        #Adding values
        exportsMod.append(nameArray)
        exportsMod.append(descriptionArray)

        exportsNew.append(nameArray)
        exportsNew.append(descriptionArray)

        #mod
        saveJson(modPath, architectureModData)

        #newConstructions
        saveJson(newPath, architectureNewData)

        return uniqueTag

def DTConstructionsHandle(uniqueTag, assetPath, categoryTag, path, userName):
        #File paths
        modPath = os.path.abspath(os.path.join(path,"..","Saves","mods","MoreBuildings","DT_Constructions.json"))
        newPath = os.path.abspath(os.path.join(path,"..","Saves","newObjects","MoreBuildings","DT_Constructions.json"))

        templatePath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","ConstructionTemplate.json"))
        importTemplatePath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","constructionsImportTemplates.json"))

        DT_ConstructionsModData = loadJson(modPath)
        DT_ConstructionsNewData = loadJson(newPath)

        template = loadJson(templatePath)
        importTemplate = loadJson(importTemplatePath)

        #Get blueprint name
        blueprintName = assetPath.split("/")[-1]

        #Icon infor
        textureName = f"T_UI_BuildIcon_{uniqueTag}"
        iconPath = f"/Game/Mods/{userName}Pack/Constructions/Icons/{textureName}"

        #Edit template
        #Edite name
        template["Name"] = uniqueTag
        #Edit Arqchitecture.json references
        template["Value"][0]["Value"] = f"{uniqueTag}.Name"
        template["Value"][1]["Value"] = f"{uniqueTag}.Description"
        #Edit Actor path
        template["Value"][3]["Value"]["AssetPath"]["AssetName"] = f"{assetPath}.{blueprintName}_C"
        #Edit Backwards Compatibility Actor path
        template["Value"][4]["Value"][0]["Value"][0]["Value"]["AssetPath"]["AssetName"] = f"{assetPath}.{blueprintName}_C"
        template["Value"][5]["Value"][0]["Value"].append(categoryTag)
        #Edit Icon
        packageImportLocation = - 1 - len(DT_ConstructionsModData["Imports"]) #Import Data starts in -1 and decreases 1, last entru should be the length of the array but negative
        #In vanilla file (no edition) of update 1.5.2 length = 1005, so next package should be -1006
        template["Value"][2]["Value"] = packageImportLocation - 1 #Because it appends first package then texture

        DT_ConstructionsModData["NameMap"].extend([
                uniqueTag,
                assetPath,
                f"{assetPath}.{blueprintName}_C",
                textureName,
                iconPath
        ])
        DT_ConstructionsNewData["NameMap"].extend([
                uniqueTag,
                assetPath,
                f"{assetPath}.{blueprintName}_C",
                textureName,
                iconPath
        ])

        DT_ConstructionsModData["Exports"][0]["Table"]["Data"].append(template)
        DT_ConstructionsNewData["Exports"][0]["Table"]["Data"].append(template)

        #imports handler

        packageImport = importTemplate["Package"].copy()
        packageImport["ObjectName"] = iconPath

        textureImport = importTemplate["Texture2D"].copy()
        textureImport["ObjectName"] = textureName
        textureImport["OuterIndex"] = packageImportLocation #Needs to references location of package.



        DT_ConstructionsModData["Imports"].append(packageImport)
        DT_ConstructionsModData["Imports"].append(textureImport)
        DT_ConstructionsNewData["Imports"].append(packageImport)
        DT_ConstructionsNewData["Imports"].append(textureImport)

        saveJson(modPath, DT_ConstructionsModData)
        saveJson(newPath, DT_ConstructionsNewData)

def DTConstructionRecipesHandle(uniqueTag, path, categoryTag, requiredItems, unlockOption, unlockRequirement):
        #Needed Files paths
        recipeTemplatePath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","ConstructionRecipeTemplate.json"))
        itemTemplatePath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","ItemTemplate.json"))
        dummyStructsPath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","DumyStructs.json"))
        flagsPath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","CategoryFlags.json"))
        unlockRequirementsPath = os.path.abspath(os.path.join(path,"..","Data","MoreBuildings","UnlockRequirementsStructs.json"))

        #File paths
        modPath = os.path.abspath(os.path.join(path,"..","Saves","mods","MoreBuildings","DT_ConstructionRecipes.json"))
        newPath = os.path.abspath(os.path.join(path,"..","Saves","newObjects","MoreBuildings","DT_ConstructionRecipes.json"))
        
        #Loading Needes Files
        recipeTemplate = loadJson(recipeTemplatePath)
        itemTemplate = loadJson(itemTemplatePath)
        dummyStructs = loadJson(dummyStructsPath)
        flagData = loadJson(flagsPath)
        unlockRequirementsStructs = loadJson(unlockRequirementsPath)

        #Loading Data tables
        DT_ConstructionRecipesModData = loadJson(modPath)
        DT_ConstructionRecipesNewData = loadJson(newPath)

        DT_ConstructionRecipesNewData["NameMap"].append(uniqueTag)
        DT_ConstructionRecipesModData["NameMap"].append(uniqueTag)

        itemArray = []

        for item in requiredItems:
                newItem = copy.deepcopy(itemTemplate)
                newItem["Value"][0]["Value"][0]["Value"] = item[0]
                newItem["Value"][2]["Value"] = item[1]
                itemArray.append(newItem)
                if item[0] not in DT_ConstructionRecipesModData["NameMap"]:
                        DT_ConstructionRecipesModData["NameMap"].append(item[0])
                        DT_ConstructionRecipesNewData["NameMap"].append(item[0])
        

        flags = flagData.get(categoryTag)
        if not flags and "." in categoryTag:
                _, sub = categoryTag.split(".",1)
                flags = flagData.get(sub)


        #Editing Template
        recipeTemplate["Name"] = uniqueTag #Edit Recipe Name
        recipeTemplate["Value"][0]["Value"][0]["Value"] = uniqueTag #Edit Row Name
        recipeTemplate["Value"][2]["Value"] = flags[0] #Edit LocationRequirement
        recipeTemplate["Value"][3]["Value"] = flags[1] #Edit PlacementType
        recipeTemplate["Value"][4]["Value"] = flags[2] #Edit OnWall
        recipeTemplate["Value"][5]["Value"] = flags[3] #Edit OnFloor
        recipeTemplate["Value"][9]["Value"] = flags[4] #Edit AutoFoundation
        recipeTemplate["Value"][10]["Value"] = flags[5] #Edit InheritAutoFoundationStability
        recipeTemplate["Value"][11]["Value"] = flags[6] #Edit AllowRefunds
        recipeTemplate["Value"][16]["Value"] = itemArray #Edit DefaultRequiredMaterials

        #Handle unlock conditions
        if unlockOption == "UnlockRequiredItems":
               unlockRequiredItems = unlockRequirementsStructs["UnlockRequiredItems"].copy()
               unlockRequiredItems["Value"][0]["Value"][0]["Value"] = unlockRequirement
               recipeTemplate["Value"][20]["Value"][3] = unlockRequiredItems
               recipeTemplate["Value"][20]["Value"][4] = dummyStructs["UnlockRequiredConstructions"]
        else:
               unlockRequiredConstruction = unlockRequirementsStructs["UnlockRequiredConstructions"].copy()
               unlockRequiredConstruction["Value"][0]["Value"][0]["Value"] = unlockRequirement
               recipeTemplate["Value"][20]["Value"][3] = dummyStructs["UnlockRequiredItems"]
               recipeTemplate["Value"][20]["Value"][4] = unlockRequiredConstruction

        #Save data
        DT_ConstructionRecipesModData["Exports"][0]["Table"]["Data"].append(recipeTemplate)
        DT_ConstructionRecipesNewData["Exports"][0]["Table"]["Data"].append(recipeTemplate)
        
        
        #Saving Data tables
        saveJson(modPath, DT_ConstructionRecipesModData)
        saveJson(newPath, DT_ConstructionRecipesNewData)



