p = 11 #prime
g = 2  #generator, selected based on AI recomendation, forgot it's significance

a = 5  #alice private number
b = 7  #bob private number

A = pow(g, a, p) #alice public key
B = pow(g, b, p) #bob public key
print ("alice pubKey: ", A, " Bob pubKey: ", B)

#shared secrect computation on both side
Ax = pow(B, a, p) #alice 
Bx = pow(A, b, p) #bob 
print ("alice computed secret: ", Ax, " Bob computed secret: ", Bx)

print ("result of both sepearately computed secrets:  ")
print (Ax == Bx)
