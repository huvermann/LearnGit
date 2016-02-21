
a = {}
b = 1
c = [1,2,3]

a["xb"]= b
a["xc"]=c
print ("b ist: {0} und a[xb] ist: {1}, a[xc] ist {2}".format(b, a["xb"], a["xc"]))
b = 2
c.append(99)
print ("b ist: {0} und a[xb] ist: {1}, a[xc] ist {2}".format(b, a["xb"], a["xc"]))
# c eine neue Liste zuweisen
c = [47,11]
print("c ist jetzt :{0}".format(c))
# Nochmal die Augabe wie oben:
print ("b ist: {0} und a[xb] ist: {1}, a[xc] ist {2}".format(b, a["xb"], a["xc"]))




