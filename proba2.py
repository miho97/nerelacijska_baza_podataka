## lekser nerelacijske baze podataka


from vepar import *
#from backend import *


class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL = 'MATCH','WITH','WHERE','CALL'
    RETURN,AS = 'RETURN','AS'

    FOR, IF, MAIN, PRINT = 'for','if','main', 'print'

    ULEFT ,URIGHT ='[]'
    DVOTOČKA = ':'
    ARROW = '->'
    LINE = '-'
    OPEN, CLOSED, COLON, SEMICOLON, EQUAL, LESS = '(),;=<'
    CCLOSED, COPEN = '}{'
    PLUS, PUTA, = '+*'
    EEQUAL = '=='
    PLUSJ = '+='

    class NODE(Token):
        def vrijednost(a,b):
            return zip(rt.mem[a], rt.mem[b])
    class IME(Token):
        def vrijednost(t): return rt.mem[t]
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
                elif lex.sadržaj == 'PRINT':
                    yield lex.token(T.PRINT)
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
                else:
                    yield lex.token(T.IME)
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
        elif znak == '=':
            yield lex.token(T.EQUAL)
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



## simple cfg:
## program -> start  | funkcija program
## funkcija -> ime OPEN parametri CLOSED COPEN naredbe CCLOSED
## parametri -> ime | parametri COLON ime
## start -> naredbe naredba
## naredbe -> '' |  naredbe naredba
## naredba -> ispis | unos |  petlja

## to zelimo prosiriti na nacin da zelimo omoguciti dodavanje funkcija

class P(Parser):
    def program(p):
        p.funkcije = Memorija( redefinicija=False)
        provjera = True
        while not p >= T.MAIN and provjera == True:
            funkcija = p.funkcija()
            p.funkcije[funkcija.ime] = funkcija
            provjera = False
        if provjera == True: return p.main()
        return p.main()
    
    def ime(p) -> 'IME': return p >> T.IME

    def parametri(p) -> 'IME*':
        p >= T.OPEN
        if p >= T.CLOSED: return []
        params = [p.ime()]
        while p >= T.COLON:
            if varijabla := p >= T.IME:
                params.append( varijabla)
        p >= T.CLOSED
        return params
    
    def funkcija(p) -> 'Funkcija':
        atributi = p.imef, p.parametrif = p.ime(), p.parametri()
        p >> T.COPEN
        nesto = Funkcija(*atributi, p.naredba())
        p >> T.CCLOSED
        return nesto
    
    def main(p):
        naredbe = []
        while not p > KRAJ:
            naredbe.append(p.naredba())
        return Start(naredbe)
    
    def naredba(p):
        if p > T.PRINT:
            return p.ispis()
   
        elif p > T.FOR:
            return p.petlja()
        else: 
            #p > T.IME
            return p.unos()
        
    def unos(p):
        if ime := p >= T.IME:
            print( "Unijeli smo ime")
        p >= T.EQUAL
        if broj := p >= T.BROJ:
            print( "Unesen je broj")
        return Unos(ime,broj)

    def ispis(p):
        p >= T.PRINT
        varijable = []
        p >= T.OPEN
        if varijabla := p >= T.IME:
            varijable.append(varijabla)
        p >= T.CLOSED
        return Ispis(varijable)

    def petlja(p):
        krivo = SemantičkaGreška('greška u inicijalizaciji for petlje')
        p >= T.FOR
        p >= T.OPEN
        if ime := p >= T.IME:
            print("okej")
        p >= T.EQUAL
        if donja_ograda := p>= T.BROJ:
            print("Broj")
        p >= T.SEMICOLON
        if gornja_ograda := p >= T.BROJ: print("Okej")
        p >= T.SEMICOLON
        if (p >> T.IME) != ime: raise krivo
        if p >= T.PLUSJ: inkrement = p >> T.BROJ
        p >> T.CLOSED

        if p >= T.COPEN:
            blok = []
            while not p >= T.CCLOSED:
                blok.append(p.naredba())
        else:
            blok = [p.naredba()]
        
        return Petlja(ime, donja_ograda, gornja_ograda, inkrement, blok)

class Petlja(AST):
    ime: 'IME'
    donja_ograda: 'BROJ'
    gornja_ograda: 'BROJ'
    inkrement: 'BROJ'
    blok: 'naredba*'

    def izvrši(petlja):
        iter = petlja.ime
        rt.mem[iter] = petlja.donja_ograda.vrijednost()
        inc = petlja.inkrement.vrijednost(); 

        while( rt.mem[iter] < petlja.gornja_ograda.vrijednost()):

            for naredba in petlja.blok: 
                naredba.izvrši()
            rt.mem[petlja.ime] += inc
        

class Funkcija(AST):
    ime: 'IME'
    parametri: 'IME*'
    tijelo: 'naredba'
    def pozovi( funkcija, argumenti):
        lokalni = Memorija(zip(funkcija.parametri, argumenti))
        funkcija.tijelo.izvrši(mem = lokalni, unutar = funkcija)

#def izvrši(funkcije, *argv):
#    print('Program je vratio:', funkcije['program'].pozovi(argv))



class Start(AST):
    naredbe: 'naredba*'

    def izvrši(program):
        rt.mem = Memorija()
        for naredba in program.naredbe:
            naredba.izvrši()

class Unos(AST):
    ime: 'IME'
    broj: 'BROJ'

    def izvrši(unos):
        name = unos.ime
        rt.mem[name] = unos.broj.vrijednost()

class Ispis(AST):
    varijable: 'IME*'
    
    def izvrši(ispis):
        for varijabla in ispis.varijable:
            print(varijabla.vrijednost(), end='')
        print()


ulaz=('''

succ(x){
    x = 2
}

main()
    x = 5
    PRINT(x)

''')
lekser(ulaz)
prikaz( kod := P(ulaz))
kod.izvrši()