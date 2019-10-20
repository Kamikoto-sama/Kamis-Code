try:
    alpha="abcdefghijklmnopqrstuvwxyz"
    mod=0
    
#Convert input
    def convIn(val):
        f = alpha.find(val,0,26)
        if f != -1: return f+10
        else:   return int(val)
#Convert output
    def convOut(val):
        if val >= 10: return alpha[val-10]
        else:   return val

#Convert module
    def Convert(val,basein,baseout):
        val  = val.lower()
        output=[]
#Convert to 10
        pow = len(val)-1
        val10 = 0
        for i in range(len(val)):
            val10 += convIn(val[i])*(basein**pow)
            pow -=1
#Convert from 10
        while val10 >= baseout:
            output.append(convOut(val10%baseout))
            val10//=baseout
            pow+=1
        output.append(convOut(val10%baseout))
#Output
        output.reverse()
        file=open("out.txt","a")

        if mod == 1 or mod == 3:
            file.write(''.join(map(str,output)))
            file.write(" ")
        elif mod == 2:
            file.write(''.join(map(str,output)))
            file.write("{} ".format(convOut(baseout)))
        file.close()

# Start
    file=open("out.txt","w")
    file.close()
    f=open("in.txt")
    mod=int(f.readline().strip())

    r = f.readline()
    while r != "":
        if mod == 1 or mod == 2:
            basein=int(r.strip())
            baseout=int(f.readline().strip())
            val= f.readline().strip()
            Convert(val,basein,baseout)
            r = f.readline()
        elif mod == 3:
            r = r.strip()
            basein=convIn(r[-1])
            baseout=36
            val= r[:-1]
            Convert(val,basein,baseout)
            r = f.readline()
    f.close()

except Exception as e:
        file=open("out.txt","w")
        file.write("[Syntax error!]\n")
        file.write(str(e))
        file.close()