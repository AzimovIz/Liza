
def add(s, k):
    s.append(k)
    s.pop(0)
    return(s)

def analys(s):
    s_ = 0

    for i in s:
        if i > 1:
            s_= s_+1
        if i < 1:
            s_= s_-1
    if s_ > 2:
        return(1)
    if s_ < -2:
        return(2)
    return(False)