class Default(dict):
    def __missing__(self, key):
        return ''
