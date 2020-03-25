# Updated version of heapq from standard library
# Updated to be used on variables from cdcl

__all__ = ['heapify', 'decreaseKey']

def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos].heapVal > heap[rightpos].heapVal:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        # Update position in both
        heap[pos].heapPos = pos
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    newitem.heapPos = pos
    decreaseKey(heap, pos, startpos)

def decreaseKey(heap, pos, startpos=0):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos-1) // 2
        parent = heap[parentpos]
        if newitem.heapVal > parent.heapVal:
            heap[pos] = parent
            parent.heapPos = pos
            pos = parentpos
            continue
        break
    heap[pos] = newitem
    newitem.heapPos = pos

def heapify(x):
    n = len(x)
    for i in range(n//2-1, -1, -1):
        _siftup(x, i)