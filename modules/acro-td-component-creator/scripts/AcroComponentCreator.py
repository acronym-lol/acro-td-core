import os
import re
import traceback

from jinja2 import Environment, FileSystemLoader, Template

from CallbacksExt import CallbacksExt
from AcroVersionExt import AcroVersionExt
from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

class AcroComponentCreator(CallbacksExt, AcroVersionExt):
    """
    AcroComponentCreator description
    """
    def __init__(self, ownerComp):
        # the component to which this extension is attached
        self.ownerComp = ownerComp
        # the component to which data is stored
        self.dataComp = ownerComp.op('data')

        self.createDialog = ownerComp.op('createDialog')

        self.connection_offset = 0
        self.connection_node_offset = 150

        self.callbacksTemplatesPath = os.path.join(var('ACRO_TD_COMPONENT_CREATOR'), 'scripts', 'CallbacksTemplates')

        # init callbacks
        self.callbackDat = self.ownerComp.par.Callbackdat.eval()
        try:
            CallbacksExt.__init__(self, ownerComp)
        except:
            self.ownerComp.addScriptError(traceback.format_exc() + \
                    "Error in CallbacksExt __init__. See textport.")
            print()
            print("Error initializing callbacks - " + self.ownerComp.path)
            print(traceback.format_exc())
        # run onInit callback
        try:
            self.DoCallback('onInit', {'exampleExt':self})
        except:
            self.ownerComp.addScriptError(traceback.format_exc() + \
                    "Error in custom onInit callback. See textport.")
            print(traceback.format_exc())

        # stored items (persistent across saves and re-initialization):
        storedItems = [
            # Only 'name' is required...
            {'name': 'Data', 'default': None, 'readOnly': False,
                                     'property': True, 'dependable': True},
        ]
        self.stored = StorageManager(self, self.dataComp, storedItems)

        # Initialize version tracking
        AcroVersionExt.__init__(self, ownerComp)

        # Register hotkeys
        if hasattr(op, 'HOTKEYMANAGER') and op.HOTKEYMANAGER:
            op.HOTKEYMANAGER.Register('ctrl+alt+shift+n', self.OpenCreateDialog, description='Open Component Creator')

    # do something in the future
    def _future(self, attrib, args=(), group_name=None, delayMilliSeconds=0, delayFrames=0):
        if group_name == None:
            group_name = self.ownerComp.name
        self.ownerComp.op('future').run(attrib, args, group=group_name, delayFrames=delayFrames, delayMilliSeconds=delayMilliSeconds)

    # kill all runs with group name
    def _killRuns(self, group_name):
        for r in runs:
            if r.group == group_name:
                r.kill()

    # -------------------------------------------------------------------------
    # Settings constructors
    # -------------------------------------------------------------------------

    def DefaultSettings(self):
        """Return a dict with all component creation settings at their defaults."""
        return {
            'Classname': '',
            'Docstring': '',
            'Shortcut': '',
            'Opshortcut': False,
            'Comptype': 'base',
            'Samenameasclass': True,
            'Compname': '',
            'Toxext': False,
            'Versionext': False,
            'Examples': False,
            'Path': '/',
            'Posx': 0,
            'Posy': 0,
            'Mqtt': False,
            'Oscin': False,
            'Oscout': False,
            'Tcpclient': False,
            'Tcpserver': False,
            'Udpin': False,
            'Udpout': False,
            'Webclient': False,
            'Webserver': False,
            'Websocket': False,
        }

    def _dialogSettings(self):
        """Read all dialog parameters into a settings dict."""
        cdpar = self.createDialog.par
        return {
            'Classname': cdpar.Classname.eval(),
            'Docstring': cdpar.Docstring.eval(),
            'Shortcut': cdpar.Shortcut.eval(),
            'Opshortcut': cdpar.Opshortcut.eval(),
            'Comptype': cdpar.Comptype.eval(),
            'Samenameasclass': cdpar.Samenameasclass.eval(),
            'Compname': cdpar.Compname.eval(),
            'Toxext': cdpar.Toxext.eval(),
            'Versionext': cdpar.Versionext.eval(),
            'Examples': cdpar.Examples.eval(),
            'Path': cdpar.Path.eval(),
            'Posx': cdpar.Posx.eval(),
            'Posy': cdpar.Posy.eval(),
            'Mqtt': cdpar.Mqtt.eval(),
            'Oscin': cdpar.Oscin.eval(),
            'Oscout': cdpar.Oscout.eval(),
            'Tcpclient': cdpar.Tcpclient.eval(),
            'Tcpserver': cdpar.Tcpserver.eval(),
            'Udpin': cdpar.Udpin.eval(),
            'Udpout': cdpar.Udpout.eval(),
            'Webclient': cdpar.Webclient.eval(),
            'Webserver': cdpar.Webserver.eval(),
            'Websocket': cdpar.Websocket.eval(),
        }

    # -------------------------------------------------------------------------
    # Dialog
    # -------------------------------------------------------------------------

    # open create dialog
    def OpenCreateDialog(self):

        # get current pane
        cur_pane = ui.panes.current

        # if current pane is network editor
        if cur_pane.type == PaneType.NETWORKEDITOR:
            # set dialog params
            self.createDialog.par.Path = ui.panes.current.owner
            self.createDialog.par.Posx = cur_pane.x
            self.createDialog.par.Posy = cur_pane.y

            # set default comp params
            self.createDialog.par.Classname = ''
            self.createDialog.par.Docstring = ''
            self.createDialog.par.Shortcut = ''
            self.createDialog.par.Opshortcut = False
            self.createDialog.par.Comptype = 'base'
            self.createDialog.par.Samenameasclass = True
            self.createDialog.par.Compname = ''
            self.createDialog.par.Examples = False
            self.createDialog.par.Mqtt = False
            self.createDialog.par.Oscin = False
            self.createDialog.par.Oscout = False
            self.createDialog.par.Tcpclient = False
            self.createDialog.par.Tcpserver = False
            self.createDialog.par.Udpin = False
            self.createDialog.par.Udpout = False
            self.createDialog.par.Webclient = False
            self.createDialog.par.Webserver = False
            self.createDialog.par.Websocket = False
            self.createDialog.par.Toxext = False
            self.createDialog.par.Versionext = False

            # open the dialog
            self.createDialog.par.Open.pulse()

    def getCompType(self, comp_type):
        if comp_type == 'base':
            return baseCOMP
        else:
            return containerCOMP

    def cancel(self):
        self.createDialog.par.Close.pulse()
        return

    # check for upper camel name with re
    def checkLegalClassName(self, name):
        return bool(re.match(r'^[A-Z]+(?:[A-Za-z0-9]+)*$', name))

    def checkLegalShortcutName(self, name):
        return bool(re.match(r'^[A-Z][A-Z0-9_]+$', name))

    # -------------------------------------------------------------------------
    # Component creation — dialog handler
    # -------------------------------------------------------------------------

    def createComponent(self):
        """Dialog button handler — validates with messageBox, closes dialog,
        then delegates to CreateComponent()."""
        settings = self._dialogSettings()

        if not self.checkLegalClassName(settings['Classname']):
            ui.messageBox('Warning', 'Class name must be upper camel case.', buttons=['OK'])
            return

        if not self.checkLegalShortcutName(settings['Shortcut']):
            ui.messageBox('Warning', 'Shortcut must be at least 2 characters.', buttons=['OK'])
            return

        self.createDialog.par.Close.pulse()
        self.CreateComponent(settings)

    # -------------------------------------------------------------------------
    # Component creation — public API
    # -------------------------------------------------------------------------

    def CreateComponent(self, settings=None):
        """Create a new component from a settings dict.

        If settings is None, reads current values from the dialog parameters.
        Use DefaultSettings() to get a dict with all defaults, modify it,
        and pass it here.

        Raises ValueError if Classname or Shortcut are invalid.
        """
        if settings is None:
            settings = self._dialogSettings()

        # validate
        if not self.checkLegalClassName(settings['Classname']):
            raise ValueError('Class name must be upper camel case.')
        if not self.checkLegalShortcutName(settings['Shortcut']):
            raise ValueError('Shortcut must be at least 2 characters.')

        self.connection_offset = 0
        offset = 0
        node_offset = 150

        path = settings['Path']
        op_type = self.getCompType(settings['Comptype'])

        # set component name
        name = settings['Compname']
        if settings['Samenameasclass']:
            name = settings['Classname']

        # create component
        comp = op(path).create(op_type, name)
        comp.nodeCenterX = settings['Posx']
        comp.nodeCenterY = settings['Posy']

        # create data storage
        data_comp = comp.create(baseCOMP, 'data')
        data_comp.nodeX = node_offset + offset
        offset += node_offset + 30

        # create examine data
        examine_dat = comp.create(examineDAT, 'examineData')
        examine_dat.par.op = 'data'
        examine_dat.nodeX = node_offset + offset
        offset += node_offset
        if op_type == baseCOMP:
            comp.par.opviewer = './examineData'

        # get shortcut
        shortcut = settings['Shortcut']

        # set parent shortcut
        comp.par.parentshortcut = shortcut

        # set global op shortcut
        if settings['Opshortcut']:
            comp.par.opshortcut = shortcut

        # add tag
        comp.tags.add('component')

        # add controls page
        controls_page = comp.appendCustomPage('Controls')
        if settings['Examples']:
            controls_page.appendPulse('Start', label='Start')

        # add settings page
        settings_page = comp.appendCustomPage('Settings')
        settings_page.appendPulse('Editextension', label='Edit Extension')

        # create extension
        self._createExtension(comp, settings)

        # add mixin module references
        include_versionext = settings['Versionext']
        include_toxext = settings['Toxext'] or include_versionext  # versionext implies toxext
        if include_toxext:
            toxext_ref = comp.create(textDAT, 'AcroToxExt')
            toxext_ref.nodeX = -300
            toxext_ref.nodeY = -150
            toxext_ref.par.file.expr = "var('ACRO_TD_VERSION_MANAGER') + '/scripts/AcroToxExt.py'"
            toxext_ref.par.syncfile = True
        if include_versionext:
            versionext_ref = comp.create(textDAT, 'AcroVersionExt')
            versionext_ref.nodeX = -300
            versionext_ref.nodeY = -300
            versionext_ref.par.file.expr = "var('ACRO_TD_VERSION_MANAGER') + '/scripts/AcroVersionExt.py'"
            versionext_ref.par.syncfile = True

        # add parameter execute dat
        self.addParExecutes(comp, shortcut)

        # add callbacks
        self.addCallbacks(comp, settings['Examples'], offset, node_offset)

        # add included connections
        self._addConnections(comp, settings_page, shortcut, settings)

        # reinit extensions
        comp.par.reinitextensions.pulse()

    def addParExecutes(self, comp, shortcut):
        # create parameter execute dat
        par_execute = comp.create(parameterexecuteDAT, 'parExecutes')
        par_execute.nodeX = -300
        par_execute.par.op = '..'
        par_execute.par.pars = '*'
        par_execute.par.valuechange = True
        par_execute.par.onpulse = True

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('PulseParExecuteTemplate.py.j2')

        # add parameter execute callbacks
        callbacks_code = template.render(shortcut=shortcut)
        par_execute.text = callbacks_code
        par_execute.par.language = 'python'
        return

    def _createExtension(self, comp, settings):
        # Specify the directory where your templates are stored
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('ComponentTemplate.py.j2')

        class_name = settings['Classname']
        include_versionext = settings['Versionext']
        include_toxext = settings['Toxext'] or include_versionext  # versionext implies toxext

        # Render the template with your data
        extclass_code = template.render(
            class_name=class_name,
            docstring=settings['Docstring'],
            include_examples=settings['Examples'],
            include_mqtt=settings['Mqtt'],
            include_oscin=settings['Oscin'],
            include_oscout=settings['Oscout'],
            include_tcpclient=settings['Tcpclient'],
            include_tcpserver=settings['Tcpserver'],
            include_udpin=settings['Udpin'],
            include_udpout=settings['Udpout'],
            include_webclient=settings['Webclient'],
            include_webserver=settings['Webserver'],
            include_websocket=settings['Websocket'],
            include_toxext=include_toxext,
            include_versionext=include_versionext,
        )

        # create extension dat
        ext_dat = comp.create(textDAT, class_name)
        ext_dat.text = extclass_code
        ext_dat.par.language = 'python'

        # save extension to file and sync
        # Write file directly instead of ext_dat.save() to avoid TD cook
        # timing issues when called programmatically (e.g. via AcroMCP)
        script_filepath = 'scripts/' + class_name + '.py'
        abs_path = os.path.join(project.folder, script_filepath)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', newline='\n') as f:
            f.write(extclass_code)
        ext_dat.par.file = script_filepath
        ext_dat.par.syncfile = True

        # add extension to extensions
        comp.par.ext0object = f'op(\'./{class_name}\').module.{class_name}(me)'
        comp.par.ext0name = settings['Shortcut']
        comp.par.ext0promote = True
        return

    # add callbacks pars and ops
    def addCallbacks(self, comp, include_examples, offset, node_offset):
        # add callbacks module
        callbacks_ext = comp.create(selectDAT, 'CallbacksExt')
        callbacks_ext.nodeX = -node_offset
        callbacks_ext.par.dat.expr = 'op.TDModules.op(\'TDCallbacksExt\')'

        # add parameter page and pars
        callbacks_page = comp.appendCustomPage('Callbacks')
        cbd = callbacks_page.appendDAT('Callbackdat', label='Callback DAT')
        cbd.val = comp.name + '_callbacks'
        callbacks_page.appendPulse('Editcallbackdat', label='Edit Callback DAT')
        callbacks_page.appendToggle('Printcallbacks', label='Print Callbacks')

        # add callback dat
        callbacks_dat = comp.parent().create(textDAT, comp.name + '_callbacks')
        callbacks_dat.nodeX = comp.nodeX
        callbacks_dat.nodeY = comp.nodeY - node_offset
        callbacks_dat.dock = comp

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        callbacks_template = env.get_template('ComponentCallbacksTemplate.py.j2')

        callbacks_dat.text = callbacks_template.render(
            include_examples=include_examples
        )
        callbacks_dat.par.language = 'python'
        callbacks_dat.par.edit.expr = 'me.dock.par.Editcallbackdat'

        # add callback backup dat
        callbacks_backup_dat = comp.create(textDAT, 'callbacksBackup')
        callbacks_backup_dat.nodeX = node_offset + offset
        callbacks_backup_dat.par.language = 'python'
        callbacks_backup_dat.text = callbacks_dat.text

        # add dat execute dat to watch for changes
        dat_execute = comp.create(datexecuteDAT, 'datExecute')
        dat_execute.nodeX = node_offset + offset
        dat_execute.nodeY = 110
        dat_execute.par.dat.expr = 'parent().par.Callbackdat'

        dat_execute_callbacks_template = env.get_template('DatExecuteDatCallbacksTemplate.py.j2')
        dat_execute.text = dat_execute_callbacks_template.render()

        # add execute dat to check for callbacks dat on create
        execute_dat = comp.create(executeDAT, 'execute')
        execute_dat.nodeX = node_offset + offset
        execute_dat.nodeY = 220
        execute_dat.par.create = True

        execute_dat_callbacks_template = env.get_template('ExecuteDatCallbacksTemplate.py.j2')
        execute_dat.text = execute_dat_callbacks_template.render()

        # add opexec to watch for name changes
        opexec_dat = comp.create(opexecuteDAT, 'opExecCallbacks')
        opexec_dat.nodeX = node_offset + offset
        opexec_dat.nodeY = 330
        opexec_dat.par.namechange = True
        opexec_dat.par.op = '..'

        opexec_dat_callbacks_template = env.get_template('OpExecCallbacksTemplate.py.j2')
        opexec_dat.text = opexec_dat_callbacks_template.render()
        return

    # -------------------------------------------------------------------------
    # Connections
    # -------------------------------------------------------------------------

    def _addConnections(self, comp, pars_page, shortcut, settings):
        if settings['Mqtt']:
            self.addMQTT(comp, pars_page, shortcut)

        if settings['Oscin']:
            self.addOSCIn(comp, pars_page, shortcut)
        if settings['Oscout']:
            self.addOSCOut(comp, pars_page, shortcut)

        if settings['Tcpclient']:
            self.addTCPClient(comp, pars_page, shortcut)
        if settings['Tcpserver']:
            self.addTCPServer(comp, pars_page, shortcut)

        if settings['Udpin']:
            self.addUDPIn(comp, pars_page, shortcut)
        if settings['Udpout']:
            self.addUDPOut(comp, pars_page, shortcut)

        if settings['Webclient']:
            self.addWebClient(comp, pars_page, shortcut)

        if settings['Webserver']:
            self.addWebServer(comp, pars_page, shortcut)

        if settings['Websocket']:
            self.addWebsocket(comp, pars_page, shortcut)

        return

    # add mqtt
    def addMQTT(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Mqtt', label='MQTT')
        header.startSection = True
        pars_page.appendToggle('Mqttactive', label='Active')
        net_addr = pars_page.appendStr('Mqttnetaddress', label='Net Address')
        net_addr.default = '127.0.0.1'
        pars_page.appendStr('Mqttusername', label='Username')
        pars_page.appendStr('Mqttpassword', label='Password')

        # add mqtt dat
        mqtt_dat = comp.create(mqttclientDAT, 'mqtt')
        mqtt_dat.nodeY = -150
        mqtt_dat.nodeX = self.connection_offset


        # bind parameters
        mqtt_dat.par.active.bindExpr = f'parent.{shortcut}.par.Mqttactive'
        mqtt_dat.par.netaddress.bindExpr = f'parent.{shortcut}.par.Mqttnetaddress'
        mqtt_dat.par.username.bindExpr = f'parent.{shortcut}.par.Mqttusername'
        mqtt_dat.par.password.bindExpr = f'parent.{shortcut}.par.Mqttpassword'

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('MQTTCallbacksTemplate.py.j2')

        # add mqtt callbacks
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('mqtt_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300
        self.connection_offset += self.connection_node_offset
        return

    def addOSCIn(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Oscin', label='OSC In')
        header.startSection = True
        pars_page.appendToggle('Oscinactive', label='Active')
        pars_page.appendInt('Oscinport', label='Port')
        pars_page.appendStr('Oscinlocaladdress', label='Local Address')

        # add osc in dat
        osc_dat = comp.create(oscinDAT, 'oscin')
        osc_dat.nodeY = -150
        osc_dat.nodeX = self.connection_offset

        # bind parameters
        osc_dat.par.active.bindExpr = f'parent.{shortcut}.par.Oscinactive'
        osc_dat.par.port.bindExpr = f'parent.{shortcut}.par.Oscinport'
        osc_dat.par.localaddress.bindExpr = f'parent.{shortcut}.par.Oscinlocaladdress'

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)
        template = env.get_template('OSCCallbacksTemplate.py.j2')
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('oscin_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addOSCOut(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Oscout', label='OSC Out')
        header.startSection = True
        pars_page.appendToggle('Oscoutactive', label='Active')
        pars_page.appendStr('Oscoutnetaddress', label='Net Address')
        pars_page.appendInt('Oscoutport', label='Port')
        pars_page.appendStr('Oscoutlocaladdress', label='Local Address')

        # add osc out dat
        osc_dat = comp.create(oscoutDAT, 'oscout')
        osc_dat.nodeY = -150
        osc_dat.nodeX = self.connection_offset

        # bind parameters
        osc_dat.par.active.bindExpr = f'parent.{shortcut}.par.Oscoutactive'
        osc_dat.par.address.bindExpr = f'parent.{shortcut}.par.Oscoutnetaddress'
        osc_dat.par.port.bindExpr = f'parent.{shortcut}.par.Oscoutport'
        osc_dat.par.localaddress.bindExpr = f'parent.{shortcut}.par.Oscoutlocaladdress'

        self.connection_offset += self.connection_node_offset
        return

    def addTCPClient(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Tcpclient', label='TCP Client')
        header.startSection = True
        pars_page.appendToggle('Tcpclientactive', label='Active')
        pars_page.appendStr('Tcpclientnetaddress', label='Net Address')
        pars_page.appendInt('Tcpclientport', label='Port')

        # add tcp client dat
        tcp_dat = comp.create(tcpipDAT, 'tcpclient')
        tcp_dat.nodeY = -150
        tcp_dat.nodeX = self.connection_offset

        # bind parameters
        tcp_dat.par.active.bindExpr = f'parent.{shortcut}.par.Tcpclientactive'
        tcp_dat.par.address.bindExpr = f'parent.{shortcut}.par.Tcpclientnetaddress'
        tcp_dat.par.port.bindExpr = f'parent.{shortcut}.par.Tcpclientport'

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)
        template = env.get_template('TCPIPClientCallbacksTemplate.py.j2')
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('tcpclient_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addTCPServer(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Tcpserver', label='TCP Server')
        header.startSection = True
        pars_page.appendToggle('Tcpserveractive', label='Active')
        pars_page.appendStr('Tcpservernetaddress', label='Net Address')
        pars_page.appendInt('Tcpserverport', label='Port')
        pars_page.appendStr('Tcpserverlocaladdress', label='Local Address')

        # add tcp server dat
        tcp_dat = comp.create(tcpipDAT, 'tcpserver')
        tcp_dat.par.mode = 'server'
        tcp_dat.nodeY = -150
        tcp_dat.nodeX = self.connection_offset

        # bind parameters
        tcp_dat.par.active.bindExpr = f'parent.{shortcut}.par.Tcpserveractive'
        tcp_dat.par.address.bindExpr = f'parent.{shortcut}.par.Tcpservernetaddress'
        tcp_dat.par.port.bindExpr = f'parent.{shortcut}.par.Tcpserverport'
        tcp_dat.par.localaddress.bindExpr = f'parent.{shortcut}.par.Tcpserverlocaladdress'

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)
        template = env.get_template('TCPIPServerCallbacksTemplate.py.j2')
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('tcpserver_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addUDPIn(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Udpin', label='UDP In')
        header.startSection = True
        pars_page.appendToggle('Udpinactive', label='Active')
        pars_page.appendInt('Udpinport', label='Port')
        pars_page.appendStr('Udpinlocaladdress', label='Local Address')

        # add udp in dat
        udp_dat = comp.create(udpinDAT, 'udpin')
        udp_dat.nodeY = -150
        udp_dat.nodeX = self.connection_offset

        # bind parameters
        udp_dat.par.active.bindExpr = f'parent.{shortcut}.par.Udpinactive'
        udp_dat.par.port.bindExpr = f'parent.{shortcut}.par.Udpinport'
        udp_dat.par.localaddress.bindExpr = f'parent.{shortcut}.par.Udpinlocaladdress'

        # generate callbacks from template
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)
        template = env.get_template('UDPCallbacksTemplate.py.j2')
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('udpin_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addUDPOut(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Udpout', label='UDP Out')
        header.startSection = True
        pars_page.appendToggle('Udpoutactive', label='Active')
        pars_page.appendStr('Udpoutnetaddress', label='Net Address')
        pars_page.appendInt('Udpoutport', label='Port')
        pars_page.appendStr('Udpoutlocaladdress', label='Local Address')

        # add udp out dat
        udp_dat = comp.create(udpoutDAT, 'udpout')
        udp_dat.nodeY = -150
        udp_dat.nodeX = self.connection_offset

        # bind parameters
        udp_dat.par.active.bindExpr = f'parent.{shortcut}.par.Udpoutactive'
        udp_dat.par.address.bindExpr = f'parent.{shortcut}.par.Udpoutnetaddress'
        udp_dat.par.port.bindExpr = f'parent.{shortcut}.par.Udpoutport'
        udp_dat.par.localaddress.bindExpr = f'parent.{shortcut}.par.Udpoutlocaladdress'

        self.connection_offset += self.connection_node_offset
        return

    def addWebClient(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Webclient', label='Webclient')
        header.startSection = True
        pars_page.appendToggle('Webclientactive', label='Active')
        pars_page.appendStr('Webclienturl', label='URL')

        # add webclient dat
        webclient_dat = comp.create(webclientDAT, 'webclient')
        webclient_dat.nodeY = -150
        webclient_dat.nodeX = self.connection_offset

        # bind parameters
        webclient_dat.par.active.bindExpr = f'parent.{shortcut}.par.Webclientactive'
        webclient_dat.par.url.bindExpr = f'parent.{shortcut}.par.Webclienturl'

        # add webclient callbacks
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('WebclientCallbacksTemplate.py.j2')

        # add webclient callbacks
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('webclient_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addWebServer(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Webserver', label='Webserver')
        header.startSection = True
        pars_page.appendToggle('Webserveractive', label='Active')
        pars_page.appendInt('Webserverport', label='Port')

        # add webserver dat
        webserver_dat = comp.create(webserverDAT, 'webserver')
        webserver_dat.nodeY = -150
        webserver_dat.nodeX = self.connection_offset

        # bind parameters
        webserver_dat.par.active.bindExpr = f'parent.{shortcut}.par.Webserveractive'
        webserver_dat.par.port.bindExpr = f'parent.{shortcut}.par.Webserverport'

        # add webserver callbacks
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('WebServerCallbacksTemplate.py.j2')

        # add webserver callbacks
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('webserver_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return

    def addWebsocket(self, comp, pars_page, shortcut):
        # add parameters
        header = pars_page.appendHeader('Websocket', label='Websocket')
        header.startSection = True
        pars_page.appendToggle('Websocketactive', label='Active')
        pars_page.appendStr('Websocketnetaddress', label='Net Address')
        pars_page.appendInt('Websocketport', label='Port')

        # add websocket dat
        websocket_dat = comp.create(websocketDAT, 'websocket')
        websocket_dat.nodeY = -150
        websocket_dat.nodeX = self.connection_offset

        # bind parameters
        websocket_dat.par.active.bindExpr = f'parent.{shortcut}.par.Websocketactive'
        websocket_dat.par.netaddress.bindExpr = f'parent.{shortcut}.par.Websocketnetaddress'
        websocket_dat.par.port.bindExpr = f'parent.{shortcut}.par.Websocketport'

        # add websocket callbacks
        file_loader = FileSystemLoader(self.callbacksTemplatesPath)
        env = Environment(loader=file_loader)

        # Load the template file
        template = env.get_template('WebsocketCallbacksTemplate.py.j2')

        # add websocket callbacks
        callbacks_code = template.render(shortcut=shortcut)
        callbacks_dat = comp.op('websocket_callbacks')
        callbacks_dat.text = callbacks_code
        callbacks_dat.nodeX = self.connection_offset
        callbacks_dat.nodeY = -300

        self.connection_offset += self.connection_node_offset
        return


    # example pulse parameter handler
    def pulse_Editextension(self):
        self.ownerComp.op('AcroComponentCreator').par.edit.pulse()
