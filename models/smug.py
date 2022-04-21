#!/usr/bin/env python3
import yaml

class pane:
  def __init__(self, pwd, splitType, commands):
    self.pwd = pwd
    self.splitType = splitType
    self.commands = commands or []
  
  def toDict(self):
    data = {'root': self.pwd, 'type': self.splitType, 'commands': self.commands}
    for k in ['root', 'type']:
      if not data[k]:
        data.pop(k)
    return data
  
  def toYAML(self):
    return yaml.dump(self.toDict())

class window:
  """
  # define windows and panes here
  windows:
    # define window name
    - name: window-1
      root: downloads # can be relative directory
      layout: tiled # set current window layout
      commands: [] # send tmux raw inputs here, omit if necessary
      panes:
      - root: even-deeper # relative directory again
        type: horizontal # split type
        commands: [] # send tmux raw input for specific pane
  """
  def __init__(self, name, pwd, layout):
    self.name = name
    self.pwd = pwd
    self.layout = layout or 'even-horizontal'
    self.commands = []
    self.panes = []
  
  def addPane(self, pwd, splitType, commands):
    self.panes.append(pane(pwd, splitType, commands))
  
  def toDict(self):
    data = {
      'name': self.name,
      'root': self.pwd,
      'layout': self.layout,
      'commands': self.commands,
      'panes': [p.toDict() for p in self.panes]
    }
    for k in ['name', 'root', 'commands']:
      if not data[k]:
        data.pop(k)
    return data
  
  def toYAML(self):
    return yaml.dump(self.toDict())

class config:
  """
  smug-session.yml
  ```yml
  # define tmux session name here
  session: session-name
  # define session specific environment variables
  env:
    ENV_NAME_1: ENV_VALUE_1
    ENV_NAME_2: ENV_VALUE_2
  # define starting directory of a session
  root: ~
  # define a pre-initializer commands here
  before_start:
    - echo 1
    - echo 2
    - echo SUCCESS
  # define post-finalzier commands here
  stop:
    - echo 'FINISHED (not showed)'
  # enforce layout to tiled after N panes created inside a window
  # this option is to readjust pane before window layout is applied.
  rebalance_panes_after: 5
  ```
  """
  def __init__(self, name, pwd):
    self.name = name
    self.env = {}
    self.pwd = pwd
    self.initializer = []
    self.finisher = []
    self.retile_after = 5
    self.windows = []
  
  def addWindow(self, name, pwd, layout):
    newWindow = window(name, pwd, layout)
    self.windows.append(newWindow)
    return newWindow
  
  def toDict(self):
    data = {
      'session': self.name,
      'env': self.env,
      'root': self.pwd,
      'before_start': self.initializer,
      'stop': self.finisher,
      'rebalance_panes_after': self.retile_after,
      'windows': [w.toDict() for w in self.windows]
    }
    for k in ['env', 'root', 'before_start', 'stop', 'rebalance_panes_after']:
      if not data[k]:
        data.pop(k)
    return data
  
  def toYAML(self):
    return yaml.dump(self.toDict())
