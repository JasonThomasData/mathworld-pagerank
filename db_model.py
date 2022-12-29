class DB_MODEL:
    def __init__(self, url, type, visited, links_out):
        self.url = url
        self.type = type
        self.visited = visited
        self.links_out = links_out

    def values(self):
        return [self.url, self.type, self.visited, self.links_out]
