from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

# customized from NanoAODTools/python/postprocessing/tools.py to perform unique matching sorted by deltaR
def matchObjectCollectionUnique(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {[(x,None) for x in objs]}

    combs = sorted([ (deltaR(obj,mobj), (obj,mobj)) for obj in objs for mobj in collection if presel(obj,mobj) ])
    freeobj = {[(x,True) for x in objs]}
    freemobj = {[(x,True) for x in collection]}

    for dR, (obj,mobj) in combs:
        if dR<dRmax:
            if freeobj[obj] and freemobj[mobj]:
                pairs[obj] = mobj
                freeobj[obj] = False
                freemobj[mobj] = False
        else:
            break

    return pairs

