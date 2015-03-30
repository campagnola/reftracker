Reftracker - Memory leak analysis for Python
============================================

Luke Campagnola 2015
Adapted from PyQtGraph


Overview
--------

Although Python automates memory management with garbage collection, it is up
to the user to ensure that objects are deleted by removing all references to
them. In practice, reference leaks are common and can be difficult to track
because a typical Python program creates and destroys many objects over time.

This module simplifies the process of identifying leaked references. It works
by taking snapshots of all objects tracked by the python garbage collection 
system at multiple timepoints and displaying the differences between these
timepoints. This allows you to see the number and estimated size of objects
that are created and deleted, as well as those that persist longer than their
intended lifetime.


Usage
-----

This module provides the `ObjTracker` class for finding leaked objects, and
the `describe_obj()` function for determining the sources of leaked 
references.

Identifying leaked references works in a few stages: 

1. After the program has initialized, create an `ObjTracker` instance. This
   will immediately build a catalog of all known objects to be ignored in
   subsequent analyses.
2. Allow the program to operate and create new objects, then call
   `ObjTracker.diff()`. This will update the catalog of objects and generate
   a report of everything that was created and deleted since the `ObjTracker`
   was instantiated. (Sometimes this provides enough information to find a
   leak.)
3. Allow the program to operate again (ideally long enough that objects 
   created before the first `diff()` _should_ have been deleted), then call 
   `ObjTracker.diff()` a second time. This will generate a similar report 
   that includes a third category of "persistent" objects--those that were 
   created before the first call to `diff()` but that have not yet been 
   collected. This set often contains obvious leaked objects. 
4. Determine the source of leaked references using `describeObj()`. This
   will attempt to generate a description of each reference that is keeping
   a persistent object alive.

See the docstrings for more information and examples.


Features
--------

* Captures a baseline catalog of objects to ignore
* At each snapshot, displays objects that are created and deleted since the
  last snapshot
* Also identifies objects that were created after the first snapshot but
  have not yet been deleted (potentially leaked references)
* Operates without creating any new references to tracked objects
* Recursively searches leaked object referrers to generate a description
  that aids in determining the source of leaked references.


