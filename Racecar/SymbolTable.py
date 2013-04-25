class SymbolLookupTable:
    '''A class implementing a Symbol Lookup Table that records each
    identifier's name, type, and scope.'''

    def __init__(self):
        '''Create a new empty table with the given name'''
        self.table = {}

    def addEntry(self, entry):
        '''Add the given entry to the table.  Throws an error if
        there is already an entry with the given name and scope, regardless
        of the type. Also throws an error if entry does not have a type.'''

        if self.verifyEntry(entry):
            raise Exception()

        # if not, add the entry to the table
        self.table[entry.id] = entry

    def verifyEntry(self, entry):
        '''Verify that a given entry is in the table with the appropriate
        scope. Checks entry.validateWithTableEntry() on each
        entry in the table that has the same id as entry
        
        Returns true if entry exists in the table, regardless of type,
        meaning that addEntry should not work'''

        for x, existingEntry in self.table.iteritems():
            if entry.validateWithTableEntry(existingEntry):
                return True

        # if none validate
        return False

    def getEntry(self, entryQuery):
        '''Returns the entry corresponding to the specified id and scope.
        This is really only useful to find out the type of a particular id.'''

        matches = [y for (x, y) in self.table.iteritems()
                   if self.verifyEntry(entryQuery)]
        if len(matches) == 1:
            return matches[0]
        else:
            raise Exception()


class SymbolTableEntry:
    '''A class representing a SymbolLookupTable entry. Each entry has
    an id (name), maybe a type, and scope list.'''

    def __init__(self):
        '''Default constructor, initializes everything to
        empty strings'''
        self.id = ""
        self.type = ""
        self.scopeList = ""

    def __init__(self, inId, inType, inScopeList):
        '''Sets the entry's id, type, and scope list'''
        self.id = inId
        self.type = inType
        self.scopeList = inScopeList

    def validateWithTableEntry(self, tableEntry):
        '''Returns true if the existence of tableEntry means that
        self cannot be added to the table (same ID and overlapping scopes)
        Ignore type since we don't want to allow different types'''
        idEq = (self.id == tableEntry.id)
        topScopeCountTableEntry = tableEntry.scopeList.pop()
        tableEntry.scopeList.append(topScopeCountTableEntry
        selfScopeAcceptable = topScopeCountTableEntry in self.scopeList
        if idEq and selfScopeAcceptable:
            return True
        else:
            return False
