## primjer_2
## pozivi funkcija, složeniji graf
## provjera lokalnosti varijabli i prijenosa kopiranjem


primjer_3 = '''
void main(){
    node A = (2,2)
    node B = (4,8)
    node C = (100, 20)
    node D = (23 , 2)
    node E = (34 ,18)
    node F = (12, 12)
    node H = (69 ,1)

    // graf je tip podatka proizvoljno velike duljine
    graph G = A(B[2], C[1], D[3]), B(A[2], C[5]), C(A[1], D[2], F[7], H[8]), D(A[6]), E(B[1], C[9], D[6]), F(C[4], H[7]), H(D[3]),;
    PRINT (G)

    // pronalazak najkraćeg puta Bellman-Fordom
    PATH G(A, H)

    // pronalazak susjeda
    MATCH G(B)

    for (int i = 1 ; 7 ; i +=1){
        PRINT (i)
    }

}
''' 

from projekt import * 

lekser(primjer_3)
prikaz( kod := P(primjer_3))
izvrši(kod)