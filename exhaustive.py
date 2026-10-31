"""Exhaustive equivalence of two blifs on all 2^n inputs, bit-parallel with big ints, matched by port name."""
import re,sys
def parse(p):
    t=re.sub(r"\\\n"," ",open(p).read()); ins=[];outs=[];nodes={};cur=None
    for l in t.splitlines():
        l=l.strip()
        if not l or l[0]=='#': continue
        if l.startswith('.inputs'): ins+=l.split()[1:]
        elif l.startswith('.outputs'): outs+=l.split()[1:]
        elif l.startswith('.names'):
            s=l.split()[1:]; cur=(s[:-1],[]); nodes[s[-1]]=cur
        elif l[0]=='.': cur=None
        elif cur is not None:
            q=l.split(); cur[1].append((q[0],q[1]) if len(q)==2 else ('',q[0]))
    return ins,outs,nodes
def run(p,n,order):
    ins,outs,nodes=parse(p); assert sorted(ins)==sorted(order)
    size=1<<n; mask=(1<<size)-1; val={}
    for i,name in enumerate(order):
        w=1<<i; b=((1<<w)-1)<<w; x=b; cur=2*w
        while cur<size: x|=x<<cur; cur*=2
        val[name]=x
    seq=[];seen=set(ins)
    for o in outs:
        st=[(o,0)]
        while st:
            s,_=st.pop()
            if s in seen: continue
            fan=nodes[s][0]; miss=[f for f in fan if f not in seen]
            if miss: st.append((s,0)); st+=[(f,0) for f in miss]
            else: seen.add(s); seq.append(s)
    refs={}
    for s in seq:
        for f in nodes[s][0]: refs[f]=refs.get(f,0)+1
    for o in outs: refs[o]=refs.get(o,0)+1
    for s in seq:
        fan,cubes=nodes[s]; r=0; onset=True
        for c,v in cubes:
            onset=(v=='1'); a=mask
            for ch,f in zip(c,fan):
                if ch=='1': a&=val[f]
                elif ch=='0': a&=~val[f]&mask
            r|=a
        val[s]=r if onset else r^mask
        for f in fan:
            refs[f]-=1
            if refs[f]==0: del val[f]
    return {o:val[o] for o in outs},ins
a,b=sys.argv[1],sys.argv[2]
ins,_,_=parse(b); n=len(ins); print('inputs',n,flush=True)
A,_=run(a,n,ins); print('a done',flush=True)
B,_=run(b,n,ins); print('b done',flush=True)
assert set(A)==set(B),'outputs differ'
bad=[o for o in A if A[o]!=B[o]]
print('outputs',len(A),'different',len(bad),bad[:5]); print('EQUIVALENT' if not bad else 'NOT EQUIVALENT')
