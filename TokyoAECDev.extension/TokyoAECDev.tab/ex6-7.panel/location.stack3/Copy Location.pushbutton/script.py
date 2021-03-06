# -*- coding: utf-8 -*-
from Autodesk.Revit import DB, UI
import pickle
import os
from tempfile import gettempdir

uiapp = __revit__ # noqa F821
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document


class CustomISelectionFilter(UI.Selection.ISelectionFilter):
    def __init__(self, nom_class):
        self.nom_class = nom_class

    def AllowElement(self, e):
        if isinstance(e, self.nom_class):
            return True
        else:
            return False


def main():
    tempfile = os.path.join(gettempdir(), "ViewPort")
    source_vp_reference = uidoc.Selection.PickObject(
        UI.Selection.ObjectType.Element,
        CustomISelectionFilter(DB.Viewport),
        "Select Source Viewport")
    source_vp = doc.GetElement(source_vp_reference.ElementId)
    source_vp_xyz = source_vp.GetBoxCenter()
    point = (source_vp_xyz.X, source_vp_xyz.Y, source_vp_xyz.Z)
    with open(tempfile, "wf") as fp:
        pickle.dump(point, fp)


if __name__ == "__main__":
    main()
