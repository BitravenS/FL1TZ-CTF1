ch = "67144453486F004E036F70010343756F505C63"  
e=" 0"
j=0
ch2=""
for i in range(0,len(ch)-1,2):
    if(j>=3):
        j=0
    ch2=ch2+chr(int(ch[i:i+2],16)^ord(e[j-1]))
    j=j+1

print("FL1TZ{"+ch2+"}")
