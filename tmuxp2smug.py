#!/usr/bin/env python3
import sys
import models.smug
import models.tmuxp

if __name__ == '__main__':
  if len(sys.argv) < 1:
    sys.exit(1)
  for tmuxpFile, smugFile in zip(*[iter(sys.argv[1:])]*2):
    print(tmuxpFile, smugFile)
    tmuxp = models.tmuxp.parse(tmuxpFile)
    smug  = models.smug.config(tmuxp.name, tmuxp.pwd)
    smug.initializer = tmuxp.initializer
    for twin in tmuxp.windows:
      swin = models.smug.window(None, None, None)
      swin.__dict__.update(twin.__dict__)
      swin.panes = []
      for tpane in twin.panes:
        spane = models.smug.pane(None, None, None)
        spane.pwd = tpane.pwd
        spane.commands = [c for c in tpane.commands if not (' ' not in c and 'sh' == c[-2:])]
        swin.panes.append(spane)
      firstPane = swin.panes.pop(0)
      swin.pwd = swin.pwd or firstPane.pwd
      swin.commands = firstPane.commands
      smug.windows.append(swin)
    with open(smugFile, 'w') as smugIO:
      smugIO.write(smug.toYAML())
