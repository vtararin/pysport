from boltons.fileutils import atomic_rename

from . import binary, json
from ..configs.configs import Config


class File:
    BINARY = 'binary'
    JSON = 'json'

    def __init__(self, file_name, logger, ft='binary'):
        self._file_name = file_name
        self._logger = logger
        self._format = ft
        self._factory = {
            self.BINARY: binary,
            self.JSON: json,
        }
        self._factory_mode = {
            self.BINARY: 'wb',
            self.JSON: 'w',
        }
        self._factory_mode_read = {
            self.BINARY: 'rb',
            self.JSON: 'r',
        }

    @staticmethod
    def backup(file_name, func, mode='wb'):
        use_utf8 = Config().configuration.get('save_in_utf8', False)
        # if user set UTF-8 usage, first try to open file in UTF-8, then in system locale (1251 for RU Windows)
        try:
            def_encoding = None
            if use_utf8:
                def_encoding = 'utf-8'

            with open(file_name, mode, encoding=def_encoding) as f:
                func(f)

        except UnicodeDecodeError:
            f.close()

            alt_encoding = 'utf-8'
            if use_utf8:
                alt_encoding = None

            with open(file_name, mode, encoding=alt_encoding) as f:
                func(f)

    def create(self):
        self._logger.info('Create ' + self._file_name)
        self.backup(
            self._file_name + '.tmp',
            self._factory[self._format].dump,
            self._factory_mode[self._format],
        )
        atomic_rename(self._file_name + '.tmp', self._file_name, overwrite=True)

    def save(self):
        self._logger.info('Save ' + self._file_name)
        self.backup(
            self._file_name + '.tmp',
            self._factory[self._format].dump,
            self._factory_mode[self._format],
        )
        atomic_rename(self._file_name + '.tmp', self._file_name, overwrite=True)

    def open(self):
        self._logger.info('Open ' + self._file_name)
        self.backup(
            self._file_name,
            self._factory[self._format].load,
            self._factory_mode_read[self._format],
        )
