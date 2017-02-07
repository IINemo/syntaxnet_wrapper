class Span(object):
    def __init__(self, begin = -1, end = -1):
        self.begin = begin
        self.end = end
    
    def left_overlap(self, other):
        return (self.begin <= other.begin and self.end <= other.end and self.end > other.begin
                or
                self.begin >= other.begin and self.end <= other.end)
    
    def overlap(self, other):
        return self.left_overlap(other) or other.left_overlap(self)
    
    def __str__(self):
        return "{} {}".format(self.begin, self.end)
    
    def equal(self, other):
        return self.begin == other.begin and self.end == other.end
        