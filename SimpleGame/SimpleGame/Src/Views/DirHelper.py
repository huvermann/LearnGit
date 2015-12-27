import os.path

def getResourceFilePath(resourceName):
    """Returns the file path of the resource"""
    result = None
    if resourceName == "View1.map":
        result = os.path.join(os.getcwd(), "Assets", "Views", "View1", "view1.json")
    elif resourceName == "View1.png":
        result = os.path.join(os.getcwd(), "Assets", "Views", "View1", "view1.png")
    elif resourceName == "Level1.map":
        result = os.path.join(os.getcwd(), "Assets", "Views", "Level1", "Level1.json")    
    elif resourceName == "Level1.png":
        result = os.path.join(os.getcwd(), "Assets", "Views", "Level1", "Level1.png")

    return result