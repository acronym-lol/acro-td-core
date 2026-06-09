import os
import traceback
from pprint import pprint

from CallbacksExt import CallbacksExt
from TDStoreTools import StorageManager
from AcroVersionExt import AcroVersionExt
TDF = op.TDModules.mod.TDFunctions

class AcroCore(CallbacksExt, AcroVersionExt):
    """
    AcroCore description
    """
    def __init__(self, ownerComp):
        # the component to which this extension is attached
        self.ownerComp = ownerComp
        # the component to which data is stored
        self.dataComp = ownerComp.op('data')

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

        # properties
        # TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
        # 				   readOnly=False)

        # stored items (persistent across saves and re-initialization):
        storedItems = [
            {'name': 'Data', 'default': None, 'readOnly': False,
                                     'property': True, 'dependable': True},
        ]
        self.stored = StorageManager(self, self.dataComp, storedItems)

        # Initialize version tracking mixin (creates Version param page if needed)
        AcroVersionExt.__init__(self, ownerComp)

        # refresh UI colors via colors component
        # self.ownerComp.op('colors').Refresh()

        # Register hotkeys
        if hasattr(op, 'HOTKEYMANAGER') and op.HOTKEYMANAGER:
            op.HOTKEYMANAGER.Register('ctrl+alt+shift+u', self.ToggleUI, description='Toggle AcroCore UI')
            op.HOTKEYMANAGER.Register('ctrl+alt+shift+t', self.ToggleTimeline, description='Toggle TD Timeline')

            if op('/tdPyEnvManager'):
                op.HOTKEYMANAGER.Register('ctrl+alt+shift+e', op('/tdPyEnvManager').OpenCli, description='Open tdPyEnvManager CLI')

    def ToggleUI(self):
        # if ui is open, close it
        if 'acrocoreui' in [p.name for p in ui.panes]:
            self.ownerComp.op('ui').par.w.mode = ParMode.CONSTANT
            self.ownerComp.op('ui').par.h.mode = ParMode.CONSTANT
            p = ui.panes['acrocoreui']
            p.close()
            return
        # if ui is closed, open it
        else:
            p = ui.panes[0].splitLeft()
            #p = ui.panes[1]
            p.ratio = .25
            p.name = 'acrocoreui'
            p.owner = op('/AcroCore/ui')
            p.changeType(PaneType.PANEL)
            

            self.ownerComp.op('ui').par.w.expr = "ui.panes['acrocoreui'].topRight.x - ui.panes['acrocoreui'].bottomLeft.x"
            self.ownerComp.op('ui').par.h.expr = "ui.panes['acrocoreui'].topRight.y - ui.panes['acrocoreui'].bottomLeft.y"
            self.CookUI()
            self.ownerComp.op('eval1').cook(force=True)
            
    def ToggleTimeline(self):
        timeline = op('/ui/dialogs/timeline')
        timeline_height = timeline.par.h
        if timeline_height.val > 0:
            timeline.par.h = 0
        else:
            timeline.par.h = 70

    def copyPlaybar(self):
        # copy the playbar component to mainmenu and wire it to emptypanel
        mainmenu = op('/ui/dialogs/mainmenu')
        emptypanel = mainmenu.op('emptypanel') if mainmenu else None
        if mainmenu and emptypanel and not mainmenu.op('playbar'):
            playbar = mainmenu.copy(self.ownerComp.op('playbar'), name='playbar')
            playbar.par.clone.expr = "op.AcroCore.op('playbar')"
            # wire playbar output to emptypanel input
            playbar.inputCOMPConnectors[0].connect(emptypanel.outputCOMPConnectors[0])

    def hideLinks(self):
        mainmenu = op('/ui/dialogs/mainmenu')
        mainmenu.op('wiki').par.display = False
        mainmenu.op('forum').par.display = False
        mainmenu.op('tutorials').par.display = False

    def hideGPU(self):
        mainmenu = op('/ui/dialogs/mainmenu')
        mainmenu.op('gpuUsage').par.display = False

    def CookUI(self):
        # cooks the ui to force the display to update
        children = self.ownerComp.op('ui').findChildren(tags=['widgetcontainer'])
        
        for c in children:
            c.cook(force=True)

    def onStart(self):
        self.printStartupBanner()
        run(self.checkProjectSaved, delayFrames=1)

        self.copyPlaybar()
        self.hideLinks()
        self.hideGPU()
        return

    def printStartupBanner(self):
        """Print ASCII art startup banner to textport"""
        version_str = self.VersionString

        banner = r"""
 __/\\\\\\\\\\\\\\\___/\\\\\\\\\\\\_____/\\\\\\\\\\\\_____/\\\\\\\\\\\\\___
  _\///////\\\/////___\/\\\////////\\\__\/\\\////////\\\__\/\\\/////////\\\_
   _______\/\\\________\/\\\______\//\\\_\/\\\______\//\\\_\/\\\_______\/\\\_
    _______\/\\\________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\\\/__
     _______\/\\\________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\/////////____
      _______\/\\\________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_____________
       _______\/\\\________\/\\\_______/\\\__\/\\\_______/\\\__\/\\\_____________
        _______\/\\\________\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\/___\/\\\_____________
         _______\///_________\////////////_____\////////////_____\///______________
"""
        print(banner)
        print(f"  VTProDesign                                                  {version_str}")
        print("================================================================================")

    def checkProjectSaved(self):
        # check to see if the project has been saved once
        if 'NewProject' in project.name:
            r = ui.messageBox('Warning', 'Please save your project before using the default project.', buttons=['OK', 'Cancel'])
            if r == 1:
                return
            o = ui.chooseFile(load=False, fileTypes=['toe'], title='Save Project As')
            project.save(o)
    
    def updateAlpackaYml(self):
        """Create or update `alpacka.yml` alongside the .toe file.

        Launcher-owned fields at the top level (name, description, template,
        kind, tags, created, schema) are setdefault'd — only written when
        absent. AcroCore-owned fields live under `kind_data.touchdesigner.*`
        (toe_file + alternate_toe_files setdefault; td_version + td_major
        always refreshed). `last_opened` is a top-level shared "last writer
        wins" field, refreshed every save.

        YAML I/O prefers `ruamel.yaml` (round-trip — preserves comments,
        ordering, quotes) and falls back to `PyYAML`. If neither is
        installed in TD's Python, this is a no-op with a textport notice;
        the next launcher save will rewrite the file from its in-memory
        Project, so AcroCore-owned fields just stay stale until then.
        """
        from datetime import datetime

        backend, yaml_mod = self._loadYamlBackend()
        if backend is None:
            print(
                "AcroCore: neither ruamel.yaml nor PyYAML is available in TD's "
                "Python — skipping alpacka.yml update. Install one with "
                "`pip install ruamel.yaml` from TD's bundled Python to "
                "re-enable on-save metadata refresh."
            )
            return

        info_path = os.path.join(project.folder, 'alpacka.yml')
        data = None
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    if backend == 'ruamel':
                        data = yaml_mod.load(f)
                    else:
                        data = yaml_mod.safe_load(f)
            except Exception:
                data = None

        if not isinstance(data, dict):
            data = self._newMapping(backend)

        now = datetime.now().isoformat(timespec='seconds')

        # Launcher-owned scalars — setdefault so user edits via the
        # launcher's Edit Details survive every TD save.
        data.setdefault('schema', 1)
        data.setdefault('name', project.name)
        data.setdefault('description', '')
        data.setdefault('template', '')
        data.setdefault('kind', 'touchdesigner')
        data.setdefault('tags', [])
        data.setdefault('created', now)

        # kind_data.touchdesigner — AcroCore-owned section. The launcher
        # accesses these via the toe_file / td_version compatibility
        # accessors that read/write through `kind_data["touchdesigner"]`.
        kind_data = data.get('kind_data')
        if not isinstance(kind_data, dict):
            kind_data = self._newMapping(backend)
            data['kind_data'] = kind_data

        td = kind_data.get('touchdesigner')
        if not isinstance(td, dict):
            td = self._newMapping(backend)
            kind_data['touchdesigner'] = td

        # `project.name` is the TD project name without extension (e.g.
        # "MyProject"); the .toe file on disk is `<name>.toe`. Setdefault
        # so a user-renamed `toe_file` in alpacka.yml survives TD saves.
        td.setdefault('toe_file', '{}.toe'.format(project.name))
        td.setdefault('alternate_toe_files', [])
        # Always refresh — this is what TD knows authoritatively.
        td['td_version'] = str(project.saveBuild)
        td['td_major'] = str(project.saveVersion)

        # Shared field — last writer wins.
        data['last_opened'] = now

        # Atomic write: write to a sibling temp and replace, mirroring how
        # the launcher's project.save() avoids partial-write corruption.
        tmp_path = info_path + '.tmp'
        try:
            with open(tmp_path, 'w', encoding='utf-8', newline='\n') as f:
                if backend == 'ruamel':
                    yaml_mod.dump(data, f)
                else:
                    yaml_mod.safe_dump(
                        data, f, default_flow_style=False, sort_keys=False,
                        allow_unicode=True,
                    )
            os.replace(tmp_path, info_path)
        except OSError as e:
            print('AcroCore: failed to write alpacka.yml: {}'.format(e))
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return

    def _loadYamlBackend(self):
        """Return ('ruamel'|'pyyaml'|None, yaml_module).

        Cached on the instance so repeated saves don't re-import. Ruamel
        is preferred — it round-trips comments and field ordering so
        users' hand edits survive a save cycle. PyYAML is a working
        fallback; TD's Python on most installs has neither out of the
        box, so the caller surfaces a clear notice when both fail.
        """
        cached = getattr(self, '_yamlBackendCache', None)
        if cached is not None:
            return cached
        try:
            from ruamel.yaml import YAML
            y = YAML(typ='rt')
            y.preserve_quotes = True
            y.indent(mapping=2, sequence=4, offset=2)
            self._yamlBackendCache = ('ruamel', y)
            return self._yamlBackendCache
        except ImportError:
            pass
        try:
            import yaml
            self._yamlBackendCache = ('pyyaml', yaml)
            return self._yamlBackendCache
        except ImportError:
            pass
        self._yamlBackendCache = (None, None)
        return self._yamlBackendCache

    def _newMapping(self, backend):
        """Create a yaml-backend-appropriate empty mapping.

        Ruamel's CommentedMap preserves indentation + ordering when
        round-tripped; for PyYAML a plain dict is fine.
        """
        if backend == 'ruamel':
            try:
                from ruamel.yaml.comments import CommentedMap
                return CommentedMap()
            except ImportError:
                return {}
        return {}

    # open the component creator dialog
    def CreateComponent(self):
        self.ownerComp.op('AcroComponentCreator').OpenCreateDialog()

    # on project save
    def onSave(self):
        # Pure-Python project bootstrapping (folder structure, .gitignore,
        # .mcp.json, CLAUDE.md, Claude skills) now runs in the launcher at
        # project-creation time, driven by the repo's template.yml. The only
        # thing onSave needs to do is refresh alpacka.yml with fields that
        # require TD's runtime API (project.saveBuild / saveVersion).
        # Version bumping happens separately via VersionManager.onSaveStart().
        self.updateAlpackaYml()
        return

    def onExit(self):
        """Called when TD is closing - clean up MCP registry."""
        acromcp = self.ownerComp.op('AcroMCP')
        if acromcp and hasattr(acromcp, 'onExit'):
            acromcp.onExit()

    # PULSE HANDLERS

    def pulse_Editextension(self):
        """Edit extension pulse handler"""
        self.ownerComp.op('AcroCore').par.edit.pulse()

    def pulse_Printstartupbanner(self):
        """Print startup banner pulse handler"""
        self.printStartupBanner()
        return

    def pulse_Checkforupdates(self):
        """Manual version check - delegates to VersionManager"""
        vm = self.ownerComp.op('AcroVersionManager')
        if vm:
            vm.CheckAll()
        return
    



