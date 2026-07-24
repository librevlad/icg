from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def initialize(self):
        pass

class PluginManager:
    def __init__(self):
        self.plugins = []
        
    def load(self, plugin: Plugin):
        plugin.initialize()
        self.plugins.append(plugin)
