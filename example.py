from reftracker import ObjTracker

class LargeObject(object):
    def __init__(self):
        self.data = [0] * 1000000

# define a function that should be called repeatedly but contains a memory 
# leak.
leaks = []

def do_work():
    global leaks
    
    # create a large object
    data = LargeObject()
    
    # accidentally leak the reference
    leaks.append(data)
    
    return data


# Create a base snapshot of all "benign" objects known to the python garbage 
# collector
ot = ObjTracker()

# now start generating objects
x = do_work()

# ..and take a new snapshot. The output of this method shows the new list that
# was created (which we still expect to be alive, because of our reference 'x')
ot.diff()

# Generate objects again; this overwrites 'x' and hopefully the previous list
# has been freed from memory.
x = do_work()

# ..but when we take the next snapshot, we can see our old list still appears
# under the "persistent" objects.
ot.diff()

# Can we find out who still has a reference?
ot.findPersistent('LargeObject').describe(0)
# This should print "__main__.leaks[0]" as one of the descriptions.
