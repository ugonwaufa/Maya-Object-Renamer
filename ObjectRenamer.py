from maya import cmds
# This Autodesk Maya Script Identifies objects selected or all objects in the scene if nothing is selected and renames them
# according to their object type e.g pCube1 gets renamed to pCube1_geo since it's a mesh

### Dictionary ###
#This is a dictionary where suffixes can be assigned according to object types
SUFFIXES = {
    "mesh": "geo",
    "joint": "jnt",
    "camera": None,
    "ambientLight": "lgt"
}
#Objects that aren't assigned in the dictionary are assumed to be groups "grp"
DEFAULT_SUFFIX = "grp"

### Rename Function ###
def rename(selection=False):

    """
    This function will rename any object to have the correct suffix
    Args:
        selection: Whether or not we use the correct selection

    Returns:
        A list of all the objects we operated on
    """
    objects = cmds.ls(selection=selection, dag=True, long=True)

    # This function cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You don't have anything selected! Try selecting something")

    objects.sort(key=len, reverse=True)

    for obj in objects:
        shortName = obj.split("|")[-1]

        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        suffix = SUFFIXES.get(objType, DEFAULT_SUFFIX)

        if not suffix:
            continue

        if obj.endswith('_'+suffix):
            continue

        newName = "%s_%s" % (shortName, suffix)
        cmds.rename(obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName, newName)

    return objects
