class Model(object):

    id = -1
    name = ""
    apiId = -1
    selected = 0

    def __init__(self, name=name, apiId=apiId, selected=selected):
        self.name = name
        self.apiId = apiId
        self.selected = selected

    def id_construct(self, id=id):
        self.id = id
