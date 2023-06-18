## jednostavan primjer korištenja jezika GraphiC
# samo main funkcija i jednostavni pozivi


primjer_1 = '''
void main(){
    int x = 5
    int y = 17
    int z = y
    PRINT (z)

    // jednolinijski komentar

    node A = (1,1)
    node B = (2,1)
    node C = B
    PRINT (A)

    graph G = A(B[2]),B(C[4]),;
    PRINT (G)

    // računanje euklidske udaljenosti
    DISTANCE (A, C)

    // ispisuje nodove s kojima je A povezan u grafu G
    MATCH G(A)

    // ispis grafa u datoteku
    ISPISDAT (G , "dat.txt")
}
''' 

from projekt import * 

lekser(primjer_1)
prikaz( kod := P(primjer_1))
izvrši(kod)