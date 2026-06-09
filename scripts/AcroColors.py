"""
Extension for managing TouchDesigner UI colors.
"""

class AcroColors:
    """
    Manages color mapping between component parameters and TouchDesigner UI colors.
    """
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp

        self.colorMapping = {
            'Editablebg': 'dat.bg.editable',
            'Editabletext': 'dat.python.editable',
            'Noteditablebg': 'dat.bg.noteditable',
            'Noteditabletext': 'dat.python.noteditable',
            'Editingtext': 'dat.python.editing',
            'Hilitebg': 'dat.bg.hilite',
            'Hilitetext': 'dat.python.hilite',
            'Commenttext': 'dat.comment.fg',
            'Scroll': 'dat.scroll',
            'Linenobg': 'dat.lineno.bg',
            'Linenohilitebg': 'dat.lineno.bg.hilite',
            'Linenotext': 'dat.lineno.fg',
            'Linenotextnodata': 'dat.lineno.fg.nodata',
            'Tableoutline': 'dat.table.outline',
            'Tableselectbg': 'dat.table.select.background',
            'Tableselectoutline': 'dat.table.select.outline',
            'Pythoncomments': 'dat.python.comments',
            'Pythonfunctions': 'dat.python.functions',
            'Pythonkeywords': 'dat.python.keywords',
            'Pythonnumbers': 'dat.python.numbers',
            'Pythonstrings': 'dat.python.strings'
        }

    def Refresh(self):
        """Refresh all UI colors from component parameters"""
        for color_name in self.colorMapping.keys():
            r = getattr(self.ownerComp.par, color_name + 'r').eval()
            g = getattr(self.ownerComp.par, color_name + 'g').eval()
            b = getattr(self.ownerComp.par, color_name + 'b').eval()
            color = str(self.colorMapping[color_name])
            ui.colors[color] = (r, g, b)

    def Update(self, par):
        """Update a single UI color when a parameter changes"""
        color_name = par.name[:-1]
        if color_name in self.colorMapping.keys():
            r = getattr(self.ownerComp.par, color_name + 'r').eval()
            g = getattr(self.ownerComp.par, color_name + 'g').eval()
            b = getattr(self.ownerComp.par, color_name + 'b').eval()
            color = str(self.colorMapping[color_name])
            ui.colors[color] = (r, g, b)
