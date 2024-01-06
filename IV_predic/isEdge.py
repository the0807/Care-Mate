import os

def get(Lb):
    h,w = Lb.shape
    LbEdge = Lb.copy()

    for hei in range(h-1):
        for wid in range(w-1):
            if hei<1 and wid<1 : continue
            if hei==h or wid==w : continue
            else :
                edgecnt = 0;
                if Lb[hei-1, wid]==0 : edgecnt = edgecnt+1
                if Lb[hei+1, wid]==0 : edgecnt = edgecnt+1
                if Lb[hei, wid-1]==0 : edgecnt = edgecnt+1
                if Lb[hei, wid+1]==0 : edgecnt = edgecnt+1
                
                if edgecnt == 0 :
                    LbEdge[hei, wid] = 0

    return LbEdge
