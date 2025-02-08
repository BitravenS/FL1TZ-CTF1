try:
    key=input("pass ? ")
except :
    print("error !! visit again")
    exit(0)
else:
    if key=="d408d48448d8":
        a=open("flag.txt","r")
        print(a.read())
    else :
        print("really ...")
    exit(1)