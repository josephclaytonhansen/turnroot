from ui_layout_helpers import *
import dearpygui.dearpygui as d

class Tooltips():
    unit_editor = {
    #Colon separates text from image path - text:image_path
    "Unit name":"Set this unit's displayed name.",
    "Current class":"Create and edit classes in the Class Editor.\nClick the Edit button (the pencil icon) to open the Class Editor",
    "Portrait button": "Create and edit portraits and sprites in the Portrait Editor.\nClick to open the Portrait Editor.\nIf a Portrait has been set for this unit, this button will display their default/neutral potrait.",
    "Compare stats": "See on a graph how this unit's base stats stack up against other created units.",
    "All growth stats": "See these stats in combination with class stats, to determine the true base stats",
    "Avatar/Player Character":"Avatar/Player Character: A unit with customizable name and appearance.\nThe unit name will be used as the default.",
    "Generic Unit":"Generic Unit: A templated unit meant to be copy-and-pasted; for example, a Soldier or a Ruffian.\nGeneric units can have random variation in base stats, classes, skills, and items",
    "Unique Unit":"Unique Unit: A named unit- there can be only one.\nFor team members, bosses, etc.",
    "NPC": "NPC: A unit that does not appear in combat, and has no stats/items/classes as a result.\nFor merchants and background characters",
}
    
def make_tooltip(source, query, parent):
    tt = source[query].split(":")
    d.add_text(tt[0])
    if len(tt) > 1:
        d.add_image(ImageToTexture(tt[1]))