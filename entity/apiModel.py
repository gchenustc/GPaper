class Api(object):

    id = -1
    platform = ""
    key = ""
    host = ""
    selected = 0

    def __init__(self, platform=platform, key=key, host=host, selected=selected):
        self.platform = platform
        self.key = key
        self.host = host
        self.selected = selected

    def id_construct(self, id=id):
        self.id = id
