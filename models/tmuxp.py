import yaml

class pane:
  def __init__(self, pwd, commands):
    self.pwd = pwd
    self.commands = commands or []
    self.focus = False
  
  def toYAML(self):
    data = {
      'start_directory': self.pwd,
      'shell_command': self.commands
    }
    for k in ['shell_command', 'start_directory']:
      if not data[k]:
        data.pop(k)
    if self.focus:
      data['focus'] = 'true'
    return yaml.dump(data)

class window:
  def __init__(self, name, pwd, layout):
    self.name = name
    self.pwd = pwd
    self.layout = layout or 'even-horizontal'
    self.commands = []
    self.panes = []
    self.focus = False
  
  def addPane(self, pwd, commands):
    self.panes.append(pane(pwd, commands))
  
  def toYAML(self):
    data = {
      'window_name': self.name,
      'start_directory': self.pwd,
      'layout': self.layout,
      'shell_command_before': self.commands,
      'panes': [p.toYAML() for p in self.panes],
    }
    for k in ['window_name', 'start_directory', 'shell_command_before']:
      if not data[k]:
        data.pop(k)
    if self.focus:
      data['focus'] = 'true'
    return yaml.dump(data)

class config:
  def __init__(self, name, pwd):
    self.name = name
    self.pwd = pwd
    self.initializer = []
    self.windows = []
  
  def addWindow(self, name, pwd, layout):
    newWindow = window(name, pwd, layout)
    self.windows.append(newWindow)
    return newWindow
  
  def toYAML(self):
    data = {
      'session_name': self.name,
      'start_directory': self.pwd,
      'shell_command_before': self.initializer,
      'windows': [w.toYAML() for w in self.windows]
    }
    for k in ['start_directory', 'shell_command_before']:
      if not data[k]:
        data.pop(k)
    return yaml.dump(data)

def parse(filename):
  rawConfig = yaml.load(open(filename).read())
  cfg = config(rawConfig['session_name'], rawConfig.get('start_directory', None))
  for shellLine in rawConfig.get('shell_command_before', []):
    cfg.initializer.append(shellLine)
  for tmuxWin in rawConfig['windows']:
    win = cfg.addWindow(
      tmuxWin['window_name'],
      tmuxWin.get('start_directory', None),
      tmuxWin['layout']
    )
    win.focus = tmuxWin.get('focus', None) == 'true'
    for tmuxPane in tmuxWin['panes']:
      if isinstance(tmuxPane, str):
        tpane = pane(None, [tmuxPane])
      else:
        commands = tmuxPane.get('shell_command', [])
        if isinstance(commands, str):
          commands = [commands]
        tpane = pane(tmuxPane.get('start_directory', None), commands)
        tpane.focus = tmuxPane.get('focus', None) == 'true'
      win.panes.append(tpane)
  return cfg
