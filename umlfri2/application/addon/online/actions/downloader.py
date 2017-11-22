from concurrent.futures import ThreadPoolExecutor

from umlfri2.datalayer.storages import ZipStorage


class OnlineAddonVersionDownloader:
    __download_executor = ThreadPoolExecutor(max_workers=4)
    
    def __init__(self, version):
        location = version.valid_location
        
        if location is None:
            raise Exception("There is no valid add-on location for current platform")
        
        self.__feature = self.__download_executor.submit(location.download)
    
    @property
    def downloaded(self):
        return self.__feature.done()
    
    @property
    def storage(self):
        if not self.downloaded:
            raise Exception("Not downloaded yet")
        
        return ZipStorage.read_from_memory(self.__future.result(0))
