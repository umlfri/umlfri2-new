from umlfri2.datalayer import AddOnLoader


class AddOnManager:
    def __init__(self, storage):
        self.__addons = []
        for dir in storage.list():
            addon_storage = storage.create_substorage(dir)
            if addon_storage.exists('addon.xml'):
                self.__addons.append(AddOnLoader(addon_storage).load())
    
    def get_addon(self, identifier):
        for addon in self.__addons:
            if addon.identifier == identifier:
                return addon
