from lense._data_load.loader import load_document , load_folder


class lense:
    def __init__(self):
        pass
    def load_data(self, filename):
        return (load_document(filename))
    
    def load_folder(self,foldername):
        return (load_folder(foldername))

