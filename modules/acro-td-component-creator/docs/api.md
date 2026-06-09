# AcroComponentCreator - Component Scaffolding Tool

## Overview

`AcroComponentCreator` is a dialog-based scaffolding tool that generates fully wired TouchDesigner components from a set of user-configurable options. It extends `CallbacksExt` and uses **Jinja2 templates** stored in `scripts/CallbacksTemplates/` to produce Python extension code, callback scripts, parameter execute DATs, and network connection operators.

The tool is designed to eliminate the repetitive boilerplate involved in creating new components. A single dialog interaction produces a complete component with:

- An extension class with `CallbacksExt` inheritance and `StorageManager`
- A callbacks system with external callback DAT, backup, and auto-creation on instantiation
- Custom parameter pages (Controls, Settings, Callbacks, and connection-specific pages)
- Optional network connection operators (MQTT, OSC, TCP/IP, UDP, WebSocket, Web Client, Web Server) with parameters bound to the parent component

---

## Opening the Dialog

The dialog is accessed through the main project extension:

```python
AcroCore.CreateComponent()
```

This calls:

```python
ownerComp.op('AcroComponentCreator').OpenCreateDialog()
```

**Requirements:**

- Must be called from the **Network Editor** pane. The dialog will not open from other pane types.
- The dialog path is set to the current pane's owner component.
- The component position is set from the current cursor location.
- All dialog parameters are reset to their defaults each time the dialog opens.

---

## Dialog Parameters

The dialog presents the following parameters for configuring the new component:

### Identity

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Classname` | `str` | `''` | Extension class name. Must be UpperCamelCase. |
| `Docstring` | `str` | `''` | Class docstring inserted into the generated extension. |
| `Shortcut` | `str` | `''` | Parent shortcut name for the component. Must be 2+ uppercase characters. |
| `Opshortcut` | `toggle` | `False` | Also register the shortcut as a global OP shortcut. |

### Component Type

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Comptype` | `menu` | `base` | Component type: `base` (baseCOMP) or `container` (containerCOMP). |
| `Samenameasclass` | `toggle` | `True` | Use the class name as the component name. |
| `Compname` | `str` | `''` | Custom component name. Only used when `Samenameasclass` is off. |

### Code Generation

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Examples` | `toggle` | `False` | Include example code in generated templates (properties, `Start()` method, callbacks). |
| `Mixins` | `menu` | `none` | Tox/Version mixin to include in the generated extension. Options: `none` (no mixin), `toxext` (AcroToxExt for tox management only), `versionext` (AcroVersionExt for version tracking + tox management). |

When a mixin is selected, the generated extension will inherit from the appropriate class and call its `__init__`. Selecting `versionext` always includes tox management since `AcroVersionExt` inherits from `AcroToxExt`. See [Tox Management](tox-management) and [Version Tracking](version-tracking) for details on what each mixin provides.

### Connection Types

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Mqtt` | `toggle` | `False` | Include an MQTT client DAT. |
| `Oscin` | `toggle` | `False` | Include an OSC receiver DAT. |
| `Oscout` | `toggle` | `False` | Include an OSC sender DAT. |
| `Tcpclient` | `toggle` | `False` | Include a TCP/IP client DAT. |
| `Tcpserver` | `toggle` | `False` | Include a TCP/IP server DAT. |
| `Udpin` | `toggle` | `False` | Include a UDP receiver DAT. |
| `Udpout` | `toggle` | `False` | Include a UDP sender DAT. |
| `Webclient` | `toggle` | `False` | Include a Web Client DAT. |
| `Webserver` | `toggle` | `False` | Include a Web Server DAT. |
| `Websocket` | `toggle` | `False` | Include a WebSocket client DAT. |

---

## Validation

The AcroComponentCreator validates two fields before allowing component creation:

### Class Name

Must match the regex pattern:

```
^[A-Z]+(?:[A-Za-z0-9]+)*$
```

This enforces **UpperCamelCase** naming. Valid examples:

- `MyComponent`
- `OSCController`
- `MQTTBridge2`

Invalid examples:

- `myComponent` -- must start with uppercase
- `my_component` -- underscores not allowed
- `My Component` -- spaces not allowed

### Shortcut

Must match the regex pattern:

```
^[A-Z][A-Z0-9_]+$
```

This requires **2 or more uppercase characters**, with digits and underscores allowed after the first character. Valid examples:

- `MC`
- `MQTT_BRIDGE`
- `OSC2`

Invalid examples:

- `m` -- too short, lowercase
- `Mc` -- second character must be uppercase
- `mc` -- must start with uppercase

---

## What Gets Created

When `createComponent()` runs, it produces the following operator network inside the target location:

### 1. The Component

A `baseCOMP` or `containerCOMP` (based on `Comptype`) placed at the cursor position in the network editor.

### 2. Data Storage

A `baseCOMP` named `data` inside the component, used by `StorageManager` for persistent storage across saves and re-initialization.

### 3. Examine Data

An `examineDAT` inside the component for inspecting stored data.

### 4. Shortcuts

- A **parent shortcut** is set on the component using the `Shortcut` value.
- If `Opshortcut` is enabled, the shortcut is also registered as a **global OP shortcut**.

### 5. Component Tag

The `component` tag is added to the created component.

### 6. Controls Page

A custom parameter page named **Controls** is added to the component. If `Examples` is enabled, a `Start` pulse parameter is included.

### 7. Settings Page

A custom parameter page named **Settings** with an `Editextension` pulse parameter that opens the extension DAT for editing.

### 8. Extension DAT

A `textDAT` generated from `ComponentTemplate.py.j2` containing the full extension class. This DAT is synced to the `scripts/` folder on disk. The generated class includes:

```python
class MyComponent(CallbacksExt):
    """ My component docstring """

    def __init__(self, ownerComp):
        self.ownerComp = ownerComp

        # init callbacks
        self.callbackDat = self.ownerComp.par.Callbackdat.eval()
        try:
            CallbacksExt.__init__(self, ownerComp)
        except:
            # error handling ...

        # run onInit callback
        try:
            self.DoCallback('onInit', {'ownerComp': self.ownerComp})
        except:
            # error handling ...

        # data storage
        self.dataComp = ownerComp.op('data')
        storedItems = [
            {'name': 'Data', 'default': None, 'readOnly': False,
             'property': True, 'dependable': True},
        ]
        self.stored = StorageManager(self, self.dataComp, storedItems)

        # connection references (based on selected options)
        # self.mqttDat = ownerComp.op('mqtt')
        # self.oscInDat = ownerComp.op('oscin')
        # self.oscOutDat = ownerComp.op('oscout')
        # self.tcpClientDat = ownerComp.op('tcpclient')
        # ...
```

### 9. Parameter Execute DAT

Generated from `PulseParExecuteTemplate.py.j2`. Routes pulse and value change events to the extension using naming conventions:

```python
def onPulse(par):
    func = getattr(parent().extensions[0], f'pulse_{par.name}', None)
    if callable(func):
        func()

def onValueChange(par, prev):
    func = getattr(parent().extensions[0], f'par_{par.name}', None)
    if callable(func):
        func(par)
```

### 10. Callbacks System

A complete callbacks infrastructure:

| Operator | Type | Purpose |
|----------|------|---------|
| CallbacksExt select DAT | `selectDAT` | References the CallbacksExt module |
| Callbacks page | Parameter page | Contains `Callbackdat`, `Editcallbackdat`, `Printcallbacks` parameters |
| Callbacks DAT | `textDAT` | External callbacks file (from `ComponentCallbacksTemplate.py.j2`) |
| Callbacks backup | `textDAT` | Backup copy of callbacks for auto-restoration |
| DAT execute | `datexecDAT` | Monitors callbacks DAT for changes (from `DatExecuteDatCallbacksTemplate.py.j2`) |
| Execute DAT | `executeDAT` | Handles `onCreate` to auto-create callbacks when component is instantiated (from `ExecuteDatCallbacksTemplate.py.j2`) |
| opExec | `opexecuteDAT` | Monitors component rename events to keep callback DAT name in sync (from `OpExecCallbacksTemplate.py.j2`) |

The callbacks DAT is generated from `ComponentCallbacksTemplate.py.j2`:

```python
def onInit(info):
    return

# included when Examples is enabled:
def onStart(info):
    return

def onDone(info):
    return
```

### 11. Connection Operators

Based on the selected connection types, the appropriate DAT operators are created with parameters bound to the parent component. See the [Connection Types](#connection-types) section for details.

---

## Connection Types

Each connection type creates a specific DAT operator inside the component, along with custom parameters on the component's parameter page. All connection parameters use `bindExpr` to reference the parent component, following the pattern:

```python
parent.{shortcut}.par.{ParameterName}
```

### MQTT

**Operator:** `mqttclientDAT` named `mqtt`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Mqttactive` | `toggle` | Enable/disable the MQTT connection |
| `Mqttnetaddress` | `str` | Broker network address |
| `Mqttusername` | `str` | Authentication username |
| `Mqttpassword` | `str` | Authentication password |

**Callbacks template:** `MQTTCallbacksTemplate.py.j2` -- delegates all MQTT events to the extension:

```python
def onConnect(dat):
    ext.SHORTCUT.onConnectMQTT(dat)

def onMessage(dat, topic, payload, qos, retained, dup):
    ext.SHORTCUT.onMessageMQTT(dat, topic, payload, qos, retained, dup)
```

**Extension methods added:** `onConnectMQTT`, `onConnectFailureMQTT`, `onConnectionLostMQTT`, `onSubscribeMQTT`, `onSubscribeFailureMQTT`, `onUnsubscribeMQTT`, `onUnsubscribeFailureMQTT`, `onPublishMQTT`, `onMessageMQTT`, `publishMQTT`, `subscribeMQTT`, `unsubscribeMQTT`

---

### OSC In (Receiver)

**Operator:** `oscinDAT` named `oscin`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Oscinactive` | `toggle` | Enable/disable the OSC receiver |
| `Oscinport` | `int` | Listening port |
| `Oscinlocaladdress` | `str` | Local network address |

**Callbacks template:** `OSCCallbacksTemplate.py.j2` -- delegates received OSC messages to the extension:

```python
def onReceiveOSC(dat, rowIndex, message, byteData, timeStamp, address, args, peer):
    ext.SHORTCUT.onReceiveOSC(dat, rowIndex, message, byteData, timeStamp, address, args, peer)
```

**Extension methods added:** `onReceiveOSC`

---

### OSC Out (Sender)

**Operator:** `oscoutDAT` named `oscout`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Oscoutactive` | `toggle` | Enable/disable the OSC sender |
| `Oscoutnetaddress` | `str` | Destination network address |
| `Oscoutport` | `int` | Destination port |
| `Oscoutlocaladdress` | `str` | Local network address |

**Callbacks template:** None (output only).

**Extension methods added:** `sendOSCMsg`

---

### TCP/IP Client

**Operator:** `tcpipDAT` named `tcpclient`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Tcpclientactive` | `toggle` | Enable/disable the TCP client connection |
| `Tcpclientnetaddress` | `str` | Server network address |
| `Tcpclientport` | `int` | Server port |

**Callbacks template:** `TCPIPClientCallbacksTemplate.py.j2` -- delegates TCP client events to the extension:

```python
def onConnect(dat, peer):
    ext.SHORTCUT.onConnectTCP(dat, peer)

def onReceive(dat, rowIndex, message, byteData, peer):
    ext.SHORTCUT.onReceiveTCPMsg(dat, rowIndex, message, byteData, peer)

def onClose(dat, peer):
    ext.SHORTCUT.onCloseTCP(dat, peer)
```

**Extension methods added:** `sendTCPMsg`, `onConnectTCP`, `onReceiveTCPMsg`, `onCloseTCP`

---

### TCP/IP Server

**Operator:** `tcpipDAT` named `tcpserver` (mode set to `server`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `Tcpserveractive` | `toggle` | Enable/disable the TCP server |
| `Tcpservernetaddress` | `str` | Network address |
| `Tcpserverport` | `int` | Listening port |
| `Tcpserverlocaladdress` | `str` | Local address to bind |

**Callbacks template:** `TCPIPServerCallbacksTemplate.py.j2` -- delegates TCP server events to the extension with server-specific method names:

```python
def onConnect(dat, peer):
    ext.SHORTCUT.onConnectTCPServer(dat, peer)

def onReceive(dat, rowIndex, message, byteData, peer):
    ext.SHORTCUT.onReceiveTCPServerMsg(dat, rowIndex, message, byteData, peer)

def onClose(dat, peer):
    ext.SHORTCUT.onCloseTCPServer(dat, peer)
```

**Extension methods added:** `sendTCPServerMsg`, `onConnectTCPServer`, `onReceiveTCPServerMsg`, `onCloseTCPServer`

---

### UDP In (Receiver)

**Operator:** `udpinDAT` named `udpin`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Udpinactive` | `toggle` | Enable/disable the UDP receiver |
| `Udpinport` | `int` | Listening port |
| `Udpinlocaladdress` | `str` | Local network address |

**Callbacks template:** `UDPCallbacksTemplate.py.j2` -- delegates received UDP messages to the extension:

```python
def onReceive(dat, rowIndex, message, byteData, peer):
    ext.SHORTCUT.onReceiveUDPMsg(dat, rowIndex, message, byteData, peer)
```

**Extension methods added:** `onReceiveUDPMsg`

---

### UDP Out (Sender)

**Operator:** `udpoutDAT` named `udpout`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Udpoutactive` | `toggle` | Enable/disable the UDP sender |
| `Udpoutnetaddress` | `str` | Destination network address |
| `Udpoutport` | `int` | Destination port |
| `Udpoutlocaladdress` | `str` | Local network address |

**Callbacks template:** None (output only).

**Extension methods added:** `sendUDPMsg`

---

### Web Client

**Operator:** `webclientDAT` named `webclient`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Webclientactive` | `toggle` | Enable/disable the web client |
| `Webclienturl` | `str` | Target URL |

**Callbacks template:** `WebclientCallbacksTemplate.py.j2` -- delegates HTTP response events to the extension:

```python
def onConnect(webClientDAT, id):
    ext.SHORTCUT.onConnect(webClientDAT, id)

def onDisconnect(webClientDAT, id):
    ext.SHORTCUT.onDisconnect(webClientDAT, id)

def onResponse(webClientDAT, statusCode, headerDict, data, id):
    ext.SHORTCUT.onResponse(webClientDAT, statusCode, headerDict, data, id)
```

**Extension methods added:** `onConnectWebclient`, `onDisconnectWebclient`, `onResponseWebclient`, `webclientRequest`

---

### Web Server

**Operator:** `webserverDAT` named `webserver`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Webserveractive` | `toggle` | Enable/disable the web server |
| `Webserverport` | `str` | Listening port |

**Callbacks template:** `WebserverCallbacksTemplate.py.j2` -- delegates HTTP and WebSocket server events to the extension:

```python
def onHTTPRequest(webServerDAT, request, response):
    response = ext.SHORTCUT.onHTTPRequestWebServer(webServerDAT, request, response)
    return response

def onWebSocketReceiveText(webServerDAT, client, data):
    ext.SHORTCUT.onWebSocketReceiveTextWebServer(webServerDAT, client, data)
```

**Extension methods added:** `onHTTPRequestWebServer`, `onWebSocketOpenWebServer`, `onWebSocketCloseWebServer`, `onWebSocketReceiveTextWebServer`, `onWebSocketReceiveBinaryWebServer`, `onWebSocketReceivePingWebServer`, `onWebSocketReceivePongWebServer`, `onServerStartWebServer`, `onServerStopWebServer`

---

### WebSocket

**Operator:** `websocketDAT` named `websocket`

| Parameter | Type | Description |
|-----------|------|-------------|
| `Websocketactive` | `toggle` | Enable/disable the WebSocket connection |
| `Websocketnetaddress` | `str` | Server network address |
| `Websocketport` | `str` | Server port |

**Callbacks template:** `WebsocketCallbacksTemplate.py.j2` -- delegates all WebSocket events to the extension:

```python
def onConnect(dat):
    ext.SHORTCUT.onConnect(dat)

def onReceiveText(dat, rowIndex, message):
    ext.SHORTCUT.onReceiveText(dat, rowIndex, message)

def onReceiveBinary(dat, contents):
    ext.SHORTCUT.onReceiveBinary(dat, contents)
```

**Extension methods added:** `onConnectWebsocket`, `onDisconnectWebsocket`, `onReceiveTextWebsocket`, `onReceiveBinaryWebsocket`, `onReceivePingWebsocket`, `onReceivePongWebsocket`, `onMonitorMessageWebsocket`, `sendTextWebsocket`, `sendPongWebsocket`, `sendPingWebsocket`, `sendBinaryWebsocket`

---

## Callback Templates

The AcroComponentCreator uses 15 Jinja2 templates stored in `scripts/CallbacksTemplates/`. Each template receives context variables (such as `class_name`, `shortcut`, `docstring`, and feature flags) and produces Python source code.

| # | Template | Purpose |
|---|----------|---------|
| 1 | `ComponentTemplate.py.j2` | Main extension class with `CallbacksExt` inheritance, `StorageManager` setup, and connection-specific methods. This is the primary code file for the component. |
| 2 | `ComponentCallbacksTemplate.py.j2` | External callbacks DAT with `onInit` and optional `onStart`/`onDone` stubs (when examples are enabled). |
| 3 | `PulseParExecuteTemplate.py.j2` | Parameter execute DAT that routes `onPulse` and `onValueChange` events to extension methods using `getattr` naming conventions. |
| 4 | `DatExecuteDatCallbacksTemplate.py.j2` | DAT execute callbacks that sync the callbacks DAT content to the backup DAT on table change. |
| 5 | `ExecuteDatCallbacksTemplate.py.j2` | Execute DAT with `onCreate` logic that auto-creates the external callbacks DAT from the backup when the component is instantiated. |
| 6 | `OpExecCallbacksTemplate.py.j2` | OP execute DAT that monitors component rename events and updates the callbacks DAT name to stay in sync. |
| 7 | `MacroCallbacksTemplate.py.j2` | Macro callbacks with `onInit` (subscribes to all macro events) and `onTrigger` stubs. |
| 8 | `MQTTCallbacksTemplate.py.j2` | MQTT client callbacks that delegate `onConnect`, `onMessage`, `onPublish`, and other MQTT events to the extension via `ext.{shortcut}`. |
| 9 | `OSCCallbacksTemplate.py.j2` | OSC receiver callbacks that delegate `onReceiveOSC` to the extension. |
| 10 | `TCPIPClientCallbacksTemplate.py.j2` | TCP/IP client callbacks that delegate `onConnect`, `onReceive`, and `onClose` to the extension via `onConnectTCP`, `onReceiveTCPMsg`, `onCloseTCP`. |
| 11 | `TCPIPServerCallbacksTemplate.py.j2` | TCP/IP server callbacks that delegate `onConnect`, `onReceive`, and `onClose` to the extension via `onConnectTCPServer`, `onReceiveTCPServerMsg`, `onCloseTCPServer`. |
| 12 | `UDPCallbacksTemplate.py.j2` | UDP receiver callbacks that delegate `onReceive` to the extension via `onReceiveUDPMsg`. |
| 13 | `WebclientCallbacksTemplate.py.j2` | Web client callbacks that delegate `onConnect`, `onDisconnect`, and `onResponse` to the extension. |
| 14 | `WebserverCallbacksTemplate.py.j2` | Web server callbacks that delegate HTTP requests and WebSocket events to the extension. Notably, `onHTTPRequest` returns the response dictionary. |
| 15 | `WebsocketCallbacksTemplate.py.j2` | WebSocket callbacks that delegate connect, disconnect, text, binary, ping, pong, and monitor events to the extension. |

### Template Variables

All templates receive their context through Jinja2 rendering. The key variables are:

| Variable | Type | Description |
|----------|------|-------------|
| `class_name` | `str` | The extension class name from the `Classname` parameter |
| `shortcut` | `str` | The parent shortcut name from the `Shortcut` parameter |
| `docstring` | `str` | The class docstring from the `Docstring` parameter |
| `include_examples` | `bool` | Whether to include example code |
| `include_mqtt` | `bool` | Whether MQTT was selected |
| `include_oscin` | `bool` | Whether OSC In was selected |
| `include_oscout` | `bool` | Whether OSC Out was selected |
| `include_tcpclient` | `bool` | Whether TCP Client was selected |
| `include_tcpserver` | `bool` | Whether TCP Server was selected |
| `include_udpin` | `bool` | Whether UDP In was selected |
| `include_udpout` | `bool` | Whether UDP Out was selected |
| `include_webclient` | `bool` | Whether Web Client was selected |
| `include_webserver` | `bool` | Whether Web Server was selected |
| `include_websocket` | `bool` | Whether WebSocket was selected |
| `include_toxext` | `bool` | Whether AcroToxExt or AcroVersionExt mixin was selected |
| `include_versionext` | `bool` | Whether AcroVersionExt mixin was selected |

---

## Extension Template

The main extension is generated from `ComponentTemplate.py.j2`. The resulting class always includes:

1. **Imports** -- `json.loads`, `json.dumps`, `traceback`, `CallbacksExt`, `StorageManager`, `TDFunctions`, and optionally `AcroToxExt` or `AcroVersionExt`
2. **Class declaration** -- inherits from `CallbacksExt`, and optionally `AcroToxExt` or `AcroVersionExt`
3. **`__init__`** -- initializes callbacks with error handling, runs the `onInit` callback, optionally calls mixin `__init__`, sets up `StorageManager`
4. **Connection references** -- `self.mqttDat`, `self.oscInDat`, `self.oscOutDat`, `self.tcpClientDat`, `self.tcpServerDat`, `self.udpInDat`, `self.udpOutDat`, etc. based on selected connection types
5. **Connection methods** -- protocol-specific send/receive methods injected based on feature flags
6. **`pulse_Editextension`** -- opens the extension DAT for editing

When `Examples` is enabled, the template additionally includes:

- A `Start()` method that demonstrates `run()` with a delayed callback and `DoCallback`
- A `done()` private method showing callback invocation
- A `pulse_Start()` method wired to the Start pulse parameter on the Controls page

The generated extension uses `getattr`-based parameter routing, so adding new pulse parameters only requires defining a method named `pulse_{ParameterName}` on the extension class. Value change handlers follow the same pattern with `par_{ParameterName}`.
