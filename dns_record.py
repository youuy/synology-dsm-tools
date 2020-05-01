class DnsRecord(object):

    def __init__(self, id, type, name, content, ttl):
        self.id = id
        self.type = type
        self.name = name
        self.content = content
        self.ttl = ttl
