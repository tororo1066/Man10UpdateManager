from abc import ABCMeta, abstractmethod

class AbstractCUI(metaclass=ABCMeta):

    @abstractmethod
    def get_command(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def run(self):
        pass

