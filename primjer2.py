## primjer_2
## pozivi funkcija, složeniji graf
## provjera lokalnosti varijabli i prijenosa kopiranjem


primjer_2 = '''
void f(){
    int x = 5
    PRINT (x)
}
void g(int x){
    x = 8
    PRINT (x)
    int y = 2
    node A = (2,1)
    node B = A
    DISTANCE (A, B)
}
node h(node A, node B){
    int z = 8
    node C = (4,4)
    RETURN C
}
void main(){
    int x = 2
    int y = 11
    CALL g(x)
    PRINT (x) // trebalo bi printati 2, a ne 8
    CALL f()
    PRINT (x) // trebalo bi printati 2, a ne 5

    node A = (2,2)
    node B = (4,8)
    node H = CALL h(A, B)

    graph G = A(B[2], H[3]),B(H[4]),H(A[1]),;
    PRINT (G)
}
''' 

from projekt import * 

lekser(primjer_2)
prikaz( kod := P(primjer_2))
izvrši(kod)