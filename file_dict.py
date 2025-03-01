from collections import UserDict
import pickle

class FileDict(UserDict):
    def __init__(self, filename):
        super().__init__()
        self._filename = filename
        try:
            self._downsync()
        except IOError:
            self._upsync()

    def _upsync(self):
        with open(self._filename, 'wb') as fp:
            pickle.dump(self.data, fp)

    def _downsync(self):
        with open(self._filename, 'rb') as fp:
            self.data = pickle.load(fp)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._upsync()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._upsync()

    def get(self, key, default=None):
        return self.data.get(key, default)
