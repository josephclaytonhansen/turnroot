from ui_layout_helpers import *
import dearpygui.dearpygui as d

class Tooltips():
    unit_editor = {
    #Colon separates text from image path - text:image_path
    "Unit name":"Set this unit's displayed name.",
    "Current class":"Create and edit classes in the Class Editor.\nClick the Edit button (the pencil icon) to open the Class Editor",
    "Portrait button": "Create and edit portraits and sprites in the Portrait Editor.\nClick to open the Portrait Editor.\nIf a Portrait has been set for this unit, this button will display their default/neutral potrait.",
    "Compare stats": "See on a graph how this unit's base stats stack up against other created units.",
    "All growth stats": "See these stats in combination with class stats, to determine the true base stats"
}
    
def make_tooltip(source, query, parent):
    tt = source[query].split(":")
    d.add_text(tt[0])
    if len(tt) > 1:
        d.add_image(ImageToTexture(tt[1]))