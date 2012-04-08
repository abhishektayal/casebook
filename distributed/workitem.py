class Workitem(object):
    def __init__(self, start, total):
        print("Created workitem %s" % start, total)
        self.start=start
        self.total=total
        self.result=None
        self.processedBy=None
    def __str__(self):
        return "<Workitem id=%s>" % str(self.itemId)
