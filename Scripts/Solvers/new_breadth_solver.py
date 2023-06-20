class Queue:

    # Initialiase empty queue
    def __init__(self):
        self._data = []

    # Add element to back of queue
    def enqueue(self, element):
        self._data.append(element) 

    # Remove and return element from front of queue
    def dequeue(self):
        assert self.size() > 0
        return self._data.pop(0)

    # find and return size of the queue
    def size(self):
        return len(self._data)