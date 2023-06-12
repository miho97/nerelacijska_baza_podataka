## lekser nerelacijske baze podataka


from vepar import *
#from backend import *


class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL = 'MATCH','WITH','WHERE','CALL'
    RETURN,AS = 'RETURN','AS'

    FOR, IF, MAIN, PRINT = 'for','if','main', 'print'

    OPEN, CLOSED, COLON, SEMICOLON, EQUAL, LESS = '(),;=<'
    CCLOSED, COPEN = '}{'
    PLUS, PUTA, = '+*'
    EEQUAL = '=='
    PLUSJ = '+='

    class NODE(Token):... 
    class IME(Token):
        def vrijednost(t): return rt.symtab[t]
    class BROJ(Token):
        def vrijednost(t): return int(t.sadržaj)
    #class KEYWORD(Token):pass






# kao oznake cvorova ideja bi bila imati A,B,C,... A1,D2,...   
# ali ne AB jer bi dolazilo do miješanja sa AS, MATCH itd..
# graf bi se ucitavao oblika:
##  A(B,C,D,E), B(B), C(), D(A,B);
# mozemo se dogovorit u svezi prelaska u druge redove
##  B(B)
##  C()
##  D(A,B);

@lexer
def lekser(lex):
    for znak in lex:
        ## mala slova sacuvati za for petlju itd
        if znak.isspace(): 
            lex.zanemari()
        if znak.isalpha and znak.isupper():   
            if lex > str.isalpha:
                lex * str.isalpha 
                if lex.sadržaj == 'MATCH':
                    yield lex.token(T.MATCH)
                elif lex.sadržaj == 'WITH':
                    yield lex.token(T.WITH)
                elif lex.sadržaj == 'WHERE':
                    yield lex.token(T.WHERE)
                elif lex.sadržaj == 'CALL':
                    yield lex.token(T.CALL)
                elif lex.sadržaj == 'RETURN':
                    yield lex.token(T.RETURN)
                elif lex.sadržaj == 'AS':
                    yield lex.token(T.AS)
                else:
                    raise lex.greška('Naredba nije leksički podržana')

            elif lex > str.isdecimal:
                prvo = next(lex)
                if prvo != '0': 
                    lex * str.isdecimal
                yield lex.token(T.NODE)
            else: yield lex.token(T.NODE)

        # ključne riječi oznančene isključivo malim slovima i imena varijabli, zasad neku su varijable a,b,c,x,y,z,...
            
        elif znak.isalpha and znak.islower():
            if lex > str.isalpha:
                lex * str.isalpha
                if lex.sadržaj == 'main':
                    lex >> '('
                    lex >> ')'
                    yield lex.token(T.MAIN)
                elif lex.sadržaj == 'for':
                    yield lex.token(T.FOR)
                elif lex.sadržaj == 'if':
                    yield lex.token(T.IF)
                #else:
                #    yield lex.literal(T)
            else:
                yield lex.token(T.IME)

        elif znak == '+':
            if lex >= '=':
                yield lex.token(T.PLUSJ)
        elif znak == '(':
            yield lex.token(T.OPEN)
        elif znak == ',':
            yield lex.token(T.COLON)
        elif znak == ')':
            yield lex.token(T.CLOSED)
        elif znak == '{':
            yield lex.token(T.COPEN)
        elif znak == '}':
            yield lex.token(T.CCLOSED)
        elif znak == ';':
            yield lex.token(T.SEMICOLON)
        elif znak == '/':   ## jednolinijski komentari neka budu oznaceni sa //
            lex >> '/'
            lex - '\n'
            lex.zanemari()
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
     

# pogledati sto cemo sa TIJELO i NAREDBA
        
### pocetna BKG
##  program -> main |  funkcija program         # tu mozemo dodat proizvoljno mnogo funkcija prije ulaska u main
##  funkcija -> ime OPEN parametri CLOSED  COPEN TIJELO CCLOSED         # klasicna definicija funkcije
##  parametri -> ime  |  parametri COLON ime
##  TIJELO   ->  deklaracija TIJELO | NAREDBA
##  main  -> deklaracija main | NAREDBA main | NAREDBA
##  NAREDBA  ->  petlja  |  grananje   |  ispis
##  petlja   ->  for COPEN  NAREDBA CCLOSED
##  for   ->  FOR OPEN IME# EQUAL BROJ SEMICOLON IME# LESS BROJ SEMICOLON inkrement CLOSED
##  inkrement -> PLUSJ BROJ
##  ispis ->  PRINT  OPEN varijabla CLOSED



## ISPROBAVANJE LEKSERA

#ulaz = 'A12(B,C,E),B(),C(F)//par nodeova grafa su dodani\n  F(G,A,H,I)'
#ulaz = 'A1B2'
#ulaz = 'ABCDEF'
#ulaz = 'MATCH A RETURN A'
ulaz = '''

main(){
    MATCH A RETURN A
    for(i = 0; i < 10; i += 1)

}
'''
lekser( ulaz )

ulaz2 = '''

funkcija()

main(){

    print(x)


}


'''

class P(Parser):
    def program(p) -> 'Memorija':
        p.funkcije = Memorija()  # redefinicija = False?
        while not p >= T.MAIN:
            funkcija = p.funkcija()
            p.funkcije[funkcija.ime] = funkcija
        p.main()
        return p.funkcije
    def main(p) :
        p.naredba()

    def naredba(p):
        p >= T.PRINT
        return p.ispis()
    def ispis(p):
        p >= T.PRINT
        p >= T.OPEN
        p >= T.PRINT
        p >= T.CLOSED
        return T.IME.vrijednost()
    def funkcija(p)-> 'Funkcija':
        atributi = p.imef, p.parametrif = p.ime(), p.parametri()
        p >= T.COPEN
        nesto = Funkcija(*atributi, p.naredba())
        p >= T.CLOSED
        return nesto
    #def parametri(p):...

prikaz( P(ulaz2))

class Funkcija(AST):
    ime: 'IME'
    parametri: 'IME*'
    tijelo: 'naredba'
    def pozovi(funkcija, argumenti):

class Parametri(AST):...
print( help(Memorija))