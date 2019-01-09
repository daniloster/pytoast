class Scenario(object):

    def __init__(self, name, tags):
        self.name = name
        self.tags = tags or []
        self.steps = []
        self.stats = {}
