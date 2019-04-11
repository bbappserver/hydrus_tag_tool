
def search_tag(tag):
    raise NotImplementedError()

def get_tag_incidence(tag):
    return len(search_tag(tag))

def top_creators(exclude=[]):
    raise NotImplementedError()

def tags_for_file(f):
    raise NotImplementedError()

def list_tags(namespace=None):
    raise NotImplementedError()

def list_creators():
    return list_tags(namespace="creator")

def trim_namespace(tag):
    return tag.replace(r"^[^:]+:","")

def replace_tag(fid,old,new):
    #If hydrus can't do this transactionally
    #always add then remove tag just in case
    #add_tag(fid,new)
    #remove_tag(fid,old)
    raise NotImplementedError()

    

class BumpDict:
    def __init__(self, *args, **kwargs):
        self.d={}
    def bump(self,k):
        if k not in self.d:
            self.d[k]=0
        else:
            self.d[k] +=1
    def extract(self):
        return self.d


def coincident_creators(creator_tag):
    d=BumpDict()
    if not creator_tag.starts_with("creator:"):
        raise ValueError("Provided tag did not start with creator: namespace")
    for f in search_tag(creator_tag):
        for t in tags_for_file(f,namespace="creator"):
            d.bump(t)

def upgradable_creators():
    for c in list_creators():
        bare=trim_namespace(c)
        for f in search_tag(c):
            yield (f,c,bare)

def interactive_upgrade_creators():
    for c in list_creators():
        bare=trim_namespace(c)
        l=[]
        for f in search_tag(c):
            l.append(f)
        if len(l) >0:
            ask=True
            upgrade=False
            print("Found %s => %s in %d files")
            print("yes for [a]ll - [s]kip all -  [y]es - [n]o")
            for e in l:
                if ask:
                    action = input("Upgrade %s?" %(l,))
                    if action == 'n':
                        upgrade=False
                    elif action =="y":
                        upgrade=True
                    elif action =="s":
                        upgrade=False
                        break
                    elif action == "a":
                        upgrade =True
                        ask = False
                if upgrade:
                    replace_tag(e,bare,c)






        
