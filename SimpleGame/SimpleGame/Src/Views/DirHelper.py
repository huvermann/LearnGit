import os.path

def getResourceFilePath(resourceName):
    """Returns the file path of the resource"""
    result = None
    if resourceName == "View1.map":
        result = os.path.join(os.getcwd(), "Assets", "Views", "View1", "view1.json")
    elif resourceName == "View1.png":
        result = os.path.join(os.getcwd(), "Assets", "Views", "View1", "view1.png")
    elif recourceName == "View2":
        result = ""

    return result