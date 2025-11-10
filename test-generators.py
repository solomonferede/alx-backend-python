def infinite_counter(start=0):
    """A generator counting infinitly from the given start"""
    for i in range(start, float('inf')):
        yield i

counter = infinite_counter(5)
for i in range(10):
    print(next(counter))