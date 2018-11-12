import os


class ConfigTest:
    resource_path = None

    @classmethod
    def build_path(cls):
        cur_path = os.path.realpath(__file__)
        path_to_root = os.path.abspath(os.path.join(cur_path, os.pardir, os.pardir, os.pardir))
        cls.resource_path = os.path.join(path_to_root, 'data')


a = ConfigTest()
a.build_path()
