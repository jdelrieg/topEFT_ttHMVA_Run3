_cmgToolsProdGlobalOptions = {}

def getCMGOption(optname,default=None):
    global _cmgToolsProdGlobalOptions
    return _cmgToolsProdGlobalOptions.get(optname,default)
def setCMGOption(optname,value):
    global _cmgToolsProdGlobalOptions
    _cmgToolsProdGlobalOptions[optname] = value
