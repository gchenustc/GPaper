class Prompt:

    id = -1
    name = ""
    text = ""
    selected = 0

    def __init__(self, name=name, text=text, selected=selected):
        self.name = name
        self.text = text
        self.selected = selected

    def id_construct(self, id):
        self.id = id