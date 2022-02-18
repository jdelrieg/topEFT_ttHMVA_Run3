_cmgToolsProdGlobalOptions = {}

def getCmgToolsProdOption(optname,default=None):
    global _cmgToolsProdGlobalOptions
    return _cmgToolsProdGlobalOptions.get(optname,default)
def setCmgToolsProdOption(optname,value):
    global _cmgToolsProdGlobalOptions
    _cmgToolsProdGlobalOptions[optname] = value
