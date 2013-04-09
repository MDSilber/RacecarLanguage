class SymbolLookupTable:
    '''A class implementing a Symbol Lookup Table that records each
    identifier's name, type, and scope.'''

    def __init__(self):
        '''Create a new empty table with the given name'''
        self.table = {}

    def addEntry(self, entry):
        '''Add the given entry to the table.  Throws an error if
        there is already an entry with the given name and scope, regardless
        of the type.'''

        # check if the id is already in the table (error)
        if entry.id in self.table and self.table[entry.id].scope == entry.scope:
            raise Exception()

        # if not, add the entry to the table
        self.table[entry.id] = entry

    def verifyEntry(self, entry):
        '''Verify that a given entry is in the table with the appropriate
        type and scope. Checks entry.validateWithTableEntry() on each
        entry in the table that has the same id as entry'''

        potentialEntries = [y for (x, y) in self.table.iteritems() if y.id == entry.id]

        for existingEntry in potentialEntries:
            if entry.validateWithTableEntry(existingEntry):
                return True

        # if none validate
        return False


class SymbolTableEntry:
    '''A class representing a SymbolLookupTable entry. Each entry has
    an id (name), type, and scope.'''

    def __init__(self):
        '''Default constructor, initializes everything to
        empty strings'''
        self.id = ""
        self.type = ""
        self.scope = ""

    def __init__(self, inId, inType, inScope):
        '''Sets the entry's id, type, and scope'''
        self.id = inId
        self.type = inType
        self.scope = inScope

    def validateWithTableEntry(self, tableEntry):
        '''Returns true if all fields of self are the same as those
        in tableEntry'''
        idEq = (self.id == tableEntry.id)
        typeEq = (self.type == tableEntry.type)
        scopeEq = (self.scope == tableEntry.scope)
        if idEq and typeEq and scopeEq:
            return True
        else:
            return False
