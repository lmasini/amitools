import ConfigParser
import os
import os.path

from Log import log_main

class VamosConfig(ConfigParser.SafeConfigParser):
  def __init__(self, extra_file=None, args=None):
    ConfigParser.SafeConfigParser.__init__(self)
    self.files = []
    
    # prepend extra file
    if extra_file != None:
      self.files.append(extra_file)    
    # add config in current working dir
    self.files.append(os.path.join(os.getcwd(),".vamosrc"))
    # add config in home directory
    self.files.append(os.path.expanduser("~/.vamosrc"))
    
    # read configs
    self.found_files = self.read(self.files)

    # setup config
    self._reset()
    self._parse_config()
    self._parse_args(args)

  def log(self):
    if len(self.found_files) == 0:
      log_main.info("no config file found: %s" % ",".join(self.files))
    else:
      log_main.info("read config file: %s" % ",".join(self.found_files))

  def _reset(self):
    self.lib_versions = {
        'dos' : 39,
        'exec' : 39
      }
    # define keys that can be set
    self._keys = {
      'logging' : str, 
      'verbose' : int, 
      'quiet' : bool, 
      'log_file' : str,
      'instr_trace' : bool, 
      'memory_trace' : bool, 
      'internal_memory_trace' : bool,
      'cycles_per_block' : int, 
      'max_cycles' : int,
      'ram_size' : int, 
      'stack_size' : int
    }
    for key in self._keys:
      setattr(self, key, None)
  
  def _parse_config(self):
    sect = 'vamos'
    for key in self._keys:
      if self.has_option(sect, key) and getattr(self, key) == None:
        f = self._keys[key]
        setattr(self, key, f(self.get(sect, key)))
    
  def _parse_args(self, args):
    # parse lib version
    if hasattr(args, 'lib_versions') and args.lib_versions != None:
      for p in args.lib_version.split(','):
        n,v = p.split(':')
        if self.lib_versions.has_key(n):
          self.lib_versions[n] = int(v)
        
    # get paramters from args
    for key in self._keys:
      if hasattr(args, key) and getattr(self, key) == None:
        setattr(self, key, getattr(args, key))
