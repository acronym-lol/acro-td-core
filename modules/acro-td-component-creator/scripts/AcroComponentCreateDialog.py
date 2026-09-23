class AcroComponentCreateDialog:
    """
    Procedurally creates and manages custom parameters for the
    Component Creator dialog.
    """

    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
        self._ensureControlsPage()
        self._ensureSettingsPage()
        self._ensureConnectionsPage()

    # -----------------------------------------------------------------
    # Controls page - dialog mechanics (Open, Close, Path, Pos)
    # -----------------------------------------------------------------

    def _ensureControlsPage(self):
        comp = self.ownerComp
        page = next((p for p in comp.customPages if p.name == 'Controls'), None)
        if page is not None:
            return
        page = comp.appendCustomPage('Controls')
        page.appendPulse('Open', label='Open')
        page.appendPulse('Close', label='Close')
        page.appendStr('Path', label='Path')
        page.appendXY('Pos', label='Pos')
        page.appendPulse('Rebuilddialog', label='Rebuild Dialog')

    # -----------------------------------------------------------------
    # Settings page - class, comp type, and options
    # -----------------------------------------------------------------

    def _ensureSettingsPage(self):
        comp = self.ownerComp
        page = next((p for p in comp.customPages if p.name == 'Settings'), None)
        if page is not None:
            return
        page = comp.appendCustomPage('Settings')

        # Class section
        page.appendHeader('Class', label='Class')
        page.appendStr('Classname', label='Class Name')
        page.appendStr('Docstring', label='DocString')
        page.appendStr('Shortcut', label='Shortcut (parent, ext)')
        page.appendToggle('Opshortcut', label='Global Op Shortcut')

        # COMP section
        page.appendHeader('Comp', label='COMP')
        comp_type = page.appendMenu('Comptype', label='COMP Type')[0]
        comp_type.menuNames = ['base', 'container']
        comp_type.menuLabels = ['Base', 'Container']
        comp_type.default = 'base'
        page.appendToggle('Samenameasclass', label='Same Name As Class')
        page.appendStr('Compname', label='COMP Name')

        # Mixins section
        page.appendHeader('Mixins', label='Mixins')
        toxext = page.appendToggle('Toxext', label='ToxEXT')[0]
        toxext.default = False
        versionext = page.appendToggle('Versionext', label='VersionEXT')[0]
        versionext.default = False
        toxext.enableExpr = 'not me.par.Versionext'

        # Options section
        page.appendHeader('Options', label='Options')
        page.appendToggle('Examples', label='Examples')

    # -----------------------------------------------------------------
    # Connections page - communication protocol toggles
    # -----------------------------------------------------------------

    def _ensureConnectionsPage(self):
        comp = self.ownerComp
        page = next((p for p in comp.customPages if p.name == 'Connections'), None)
        if page is not None:
            return
        page = comp.appendCustomPage('Connections')
        page.appendToggle('Mqtt', label='MQTT')
        page.appendToggle('Oscin', label='OSC In')
        page.appendToggle('Oscout', label='OSC Out')
        page.appendToggle('Tcpclient', label='TCP Client')
        page.appendToggle('Tcpserver', label='TCP Server')
        page.appendToggle('Udpin', label='UDP In')
        page.appendToggle('Udpout', label='UDP Out')
        page.appendToggle('Webclient', label='Web Client')
        page.appendToggle('Webserver', label='Web Server')
        page.appendToggle('Websocket', label='WebSocket')

    # -----------------------------------------------------------------
    # Configure parameter1 to show both Settings and Connections pages
    # -----------------------------------------------------------------

    def _configureParameterComp(self):
        par_comp = self.ownerComp.op('parameter1')
        if par_comp is None:
            return
        par_comp.par.pagescope = 'Settings Connections'
        par_comp.par.pagenames = True

    # -----------------------------------------------------------------
    # Rebuild - delete and recreate all custom pages
    # -----------------------------------------------------------------

    def RebuildDialog(self):
        """Delete and recreate all custom parameter pages."""
        comp = self.ownerComp

        # Delete existing custom pages
        for page in list(comp.customPages):
            page.destroy()

        # Recreate all pages
        self._ensureControlsPage()
        self._ensureSettingsPage()
        self._ensureConnectionsPage()
        self._configureParameterComp()

        print(f'AcroComponentCreateDialog: Rebuilt dialog parameters')

    # -----------------------------------------------------------------
    # Pulse handlers
    # -----------------------------------------------------------------

    def pulse_Rebuilddialog(self):
        """Pulse handler for Rebuild Dialog button"""
        self.RebuildDialog()
