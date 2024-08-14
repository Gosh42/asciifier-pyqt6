class Resizeable:
    """Yeah, so here's the thing:
    when you try to maintain ratio between two int values, it may not always work
    because the math will result in a float that gets rounded down into the same
    number as before. This isn't an issue with floats since they don't get rounded
    down like that, so here I'm making a fake int that's actually a float, but
    it gives you an int when you access it. Maybe a silly solution but whatever"""
    def __init__(self, w, h):
        self.width: float = w
        self.height: float = h

    def __str__(self):
        return "(%s, %s)" % (self.width, self.height)

    def get_int_width(self) -> int:
        return int(round(self.width))

    def get_int_height(self) -> int:
        return int(round(self.height))

    def get_int_size(self) -> (int, int):
        return self.get_int_width(), self.get_int_height()

    def resize_by_height(self, new_height):
        ratio = self.width / self.height
        self.width = ratio * new_height
        self.height = new_height

    def resize_by_width(self, new_width):
        ratio = self.width / self.height
        self.height = new_width / ratio
        self.width = new_width