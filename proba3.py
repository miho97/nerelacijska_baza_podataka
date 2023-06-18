## lekser nerelacijske baze podataka


from vepar import *
#from backend import *


class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL = 'MATCH','WITH','WHERE','CALL'
    RETURN,AS = 'RETURN','AS'

    FOR, IF, PRINT = 'for','if', 'print'
    VOID,NODE, INT = 'void', 'node','int'   

    ULEFT ,URIGHT ='[]'

    DVOTOČKA = ':'
    ARROW = '->'
    LINE = '-'
    OPEN, CLOSED, COLON, SEMICOLON, EQUAL, LESS = '(),;=<'
    CCLOSED, COPEN = '}{'
    PLUS, PUTA, = '+*'
    EEQUAL = '=='
    PLUSJ = '+='

    # node A = f( B )
    # cuvanje koordinata vrhova grafa
    class PAIR(Token):
        def vrijednost(a,b):
            return zip(rt.mem[a], rt.mem[b])
        
    class IME(Token):
        def vrijednost(t): return t.sadržaj
        #def izvrši(ime,lokalni): return rt.mem[ime]
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
                    lex * str.isdecimal      # A,B,C,D1,E23
                yield lex.token(T.IME)
            else: yield lex.token(T.IME)

        # ključne riječi oznančene isključivo malim slovima i imena varijabli, zasad neku su varijable a,b,c,x,y,z,...
            
        elif znak.isalpha and znak.islower():
            if lex > str.isalpha:
                lex * str.isalpha
                if lex.sadržaj == 'for':
                    yield lex.token(T.FOR)
                elif lex.sadržaj == 'if':
                    yield lex.token(T.IF)
                elif lex.sadržaj == 'void':
                    yield lex.token(T.VOID)
                elif lex.sadržaj == 'int':
                    yield lex.token(T.INT)
                elif lex.sadržaj == 'node':
                    yield lex.token(T.NODE)
                else:
                    yield lex.token(T.IME)
            else:
                yield lex.token(T.IME)
#  (1,2) DA TREBA VRATITI node A = (5,6)
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
## program -> funkcija  | funkcija program
## funkcija -> ime OPEN parametri CLOSED COPEN naredbe CCLOSED
## parametri -> ime | parametri COLON ime
## naredbe -> naredba |  naredbe naredba
## naredba -> ispis | unos |  petlja

## to zelimo prosiriti na nacin da zelimo omoguciti dodavanje funkcija

class P(Parser):
    def program(p):
        rt.mem = Memorija()  # GLOBALNA MEMORIJA AKO CE NAM TREBATI
        p.funkcije = Memorija( redefinicija=False)
        while not p > KRAJ:
            funkcija = p.funkcija()
            p.funkcije[funkcija.ime] = funkcija
        return p.funkcije
    
    def ime(p) -> 'IME': return p >> T.IME

    # pozivamo ju u dohvacanju parametara funkcije, vraca samo listu tipova
    def parametri(p) -> 'lista value tip':
        p >= T.OPEN
        if p >= T.CLOSED: return {}
        trenutni_tip = p.tip_parametra()

        params = {}
        trenutni_parametar = p >> { T.NODE, T.IME }
        params[trenutni_parametar] = trenutni_tip

        while p >= T.COLON:
            trenutni_tip = p.tip_parametra()
            trenutni_parametar = p >> { T.NODE, T.IME }
            params[trenutni_parametar] = trenutni_tip

        p >> T.CLOSED
        return params
    
    def tip_parametra(p) -> 'INT|NODE':
        return p >> {T.INT, T.NODE}
    
    def tip_funkcije(p) -> 'INT|NODE|VOID':
        return p >> {T.INT, T.NODE, T.VOID}


    def funkcija(p) -> 'Funkcija':
        #atributi = p.imef, p.parametrif = p.ime(), p.parametri()
        atributi = p.tipf, p.imef, p.parametrif = p.tip_funkcije(), p.ime(), p.parametri()

        p >> T.COPEN
        lokalna_memorija_funkcije = Memorija()
        for ime in p.parametrif:
            # za funkciju int f(int x) u lokalnoj memoriji će biti 
            tip_vrijednost = {'tip':p.parametrif[ime],'vrijednost':nenavedeno}
            lokalna_memorija_funkcije[ime] = tip_vrijednost

       
        return Funkcija(*atributi, lokalna_memorija_funkcije,  p.sve_naredbe(p.tipf, p.parametrif, lokalna_memorija_funkcije))
        #p >> T.CCLOSED
        #return nesto
    #def tipa(p,ime) :
    #    if ime ^ T.IME: return p.aritm()
    #    #elif ime ^ T.GIME: return p.gime()
    #    else: assert False, f'Nepoznat tip od {ime}'
    
    #def aritm(p):

  

    def možda_poziv(p,ime, mem) -> 'Poziv|ime':
        p >> T.OPEN
        lista_param = []
        
        while not p >= T.CLOSED:
            varijabla = p >> T.IME
            lista_param.append(varijabla)
            p >= T.COLON
        if ime in p.funkcije:
        # if p.funkcije[ime] != nenavedeno:
            funkcija = p.funkcije[ime]
            return Poziv(funkcija, ime, lista_param, mem)
        else: 
            raise SemantičkaGreška('Koristite nepostojeću funkciju')
     
    # sve_naredbe kao parametar primaju tip fje i parametar fje i vraca AST tijela te funkcije
    def sve_naredbe(p, tip, param, mem):
        naredbe = []
        while not p >= T.CCLOSED:
            naredbe.append(p.naredba(tip, param, mem))
        return Blok(naredbe)

    def naredba(p, tip, param, mem):
        if p > T.PRINT:
            return p.ispis(param, mem)
   
        elif p > T.FOR:
            return p.petlja(tip, param, mem)
        elif p > {T.INT, T.NODE}: 
            #p > T.IME
            return p.unos(param, mem)
        elif p > T.CALL:
            p >> T.CALL
            if name := p >> T.IME: print("procitali smo ime funkcije")
            return p.možda_poziv(name, mem)
        
        elif p > T.IME:
            return p.azuriraj(param,mem)
        
        else:
            p >> T.RETURN
            if name := p >= T.IME:
                print( "vratit cemo ime")
            return Vrati(name, param, mem, tip)
            
    ## ova funkcija služi za update pojedine varijable
    ## obzirom da ne možemo u ovoj fazi zaključiti koji je tip varijable kojoj nešto pridružujemo jer se ne čuva u globalnoj već u lokalnoj 
    ## memoriji, a ime ne nosi informaciju u tipu varijable pojedine funkcije greška u pridruživanju bit će ona u runtimeu
    def azuriraj(p,param,mem): 
        ime = p >> T.IME
        p >> T.EQUAL
        if p > T.CALL:
            p >> T.CALL
            name = p >> T.IME
            # vrijednost =  p.možda_poziv(name, mem)
            vrijednost =  p.unos_iz_funkcije(name, mem)
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)
        elif vrijednost := p >= T.BROJ:
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)
        elif drugo_ime := p >= T.IME:
            return Ažuriraj(ime, drugo_ime, mem, pregledaj = True)
        elif p >= T.OPEN:
            ## tu treba prihvatiti i (1,2) i (x,y) i kombinacije
            prva = p >> T.BROJ
            p >> T.COLON
            druga = p >> T.BROJ
            p >> T.CLOSED
            vrijednost = (prva, druga)
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)
        return nenavedeno

    def unos_iz_funkcije(p, name, mem):  
        if name in p.funkcije:
            pozvana = p.funkcije[name]
            if(pozvana.tip ^ T.VOID ):
                raise SemantičkaGreška('pozvana funkcije ne vraća povratnu vrijednost')
            else:
                return p.možda_poziv(name, mem)
        else:
            raise SemantičkaGreška('Ne postoji funkcija deklarirana tim imenom')  

    def unos(p,param,mem):
        tip_var = p >> {T.INT, T.NODE}
        ime = p >> T.IME
        p >> T.EQUAL
        if tip_var ^ T.INT:
            if p > T.CALL:
                p >> T.CALL
                name = p >> T.IME
                vrijednost = p.unos_iz_funkcije(name, mem)
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)
            elif vrijednost := p >= T.BROJ:
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)
            elif drugo_ime := p >= T.IME:
                return Unos(tip_var, ime, drugo_ime, mem, pregledaj = True)
        elif tip_var ^ T.NODE:
            if p > T.CALL:
                p >> T.CALL
                vrijednost = p.unos_iz_funkcije(mem)
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)

            elif p >= T.OPEN:
                ## tu treba prihvatiti i (1,2) i (x,y) i kombinacije
                prva = p >> T.BROJ
                p >> T.COLON
                druga = p >> T.BROJ
                p >> T.CLOSED
                vrijednost = (prva, druga)
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)
            elif drugo_ime := p >= T.IME:
                return Unos(tip_var, ime, drugo_ime, mem, pregledaj = True)
        return nenavedeno

    def ispis(p, param, mem):
        p >= T.PRINT
        varijable = []
        p >= T.OPEN
        if varijabla := p >= T.IME:
            varijable.append(varijabla)
        while p >= T.COLON:
            varijabla = p >> T.IME
            varijable.append(varijabla)
        
        p >= T.CLOSED

        return Ispis(varijable, mem)

    def petlja(p, tip, param, mem):
        krivo = SemantičkaGreška('greška u inicijalizaciji for petlje')
        p >= T.FOR
        p >= T.OPEN
        if ime_iteratora := p >= T.IME:
            print("okej")
        p >= T.EQUAL
        if donja_ograda := p>= T.BROJ:
            print("Broj")
        p >= T.SEMICOLON
        if gornja_ograda := p >= T.BROJ: print("Okej")
        p >= T.SEMICOLON
        if (p >> T.IME) != ime_iteratora: raise krivo
        elif p >= T.PLUSJ: inkrement = p >> T.BROJ
        p >> T.CLOSED

        if p >= T.COPEN:
            blok = []
            while not p >= T.CCLOSED:
                blok.append(p.naredba(tip, param, mem))
        else:
            blok = [p.naredba(tip, param, mem)]
        
        return Petlja(ime_iteratora, donja_ograda, gornja_ograda, inkrement, blok, mem)

class Petlja(AST):
    ime_iteratora: 'IME'
    donja_ograda: 'BROJ'
    gornja_ograda: 'BROJ'
    inkrement: 'BROJ'
    blok: 'naredba*'
    mem: 'lokalna memorija'
    def izvrši(petlja):
        iter = petlja.ime
        petlja.mem[iter]['vrijednost'] = petlja.donja_ograda.vrijednost()
        inc = petlja.inkrement.vrijednost(); 

        while( petlja.mem[iter]['vrijednost'] < petlja.gornja_ograda.vrijednost()):

            for naredba in petlja.blok: 
                naredba.izvrši()
            petlja.mem[iter]['vrijednost'] += inc
        

class Funkcija(AST):
    tip: 'TIP'
    ime: 'IME'
    parametri: 'ULAZNI PARAM'
    memorija: 'lokalna mem'
    tijelo: 'naredba'

    def pozovi( funkcija):
        return (funkcija.tijelo.izvrši())

def izvrši(funkcije, *argv):
    print('Program je vratio:', funkcije['main'].pozovi())

class Poziv(AST):
    funkcija: 'Funkcija'
    ime: 'IME'
    param: 'PARAMTERI'
    mem: 'LOKALNA MEMORIJA majcinske funkcije'

    def izvrši(poziv):
        pozvana = poziv.funkcija
        if ( len(pozvana.parametri) != len(poziv.param) ):
            raise SintaksnaGreška('Broj parametra funkcije nije odgovarajuć')
        i = 0
        for iter in poziv.param:
            if poziv.mem[iter]['tip'] != list(pozvana.parametri.items())[i][1]:
                raise SemantičkaGreška('Tip parametra ne odgovara')
            else:
                pozvana.memorija[list(pozvana.parametri.items())[i][0]] = {}
                pozvana.memorija[list(pozvana.parametri.items())[i][0]]['tip'] = list(pozvana.parametri.items())[i][1]
                pozvana.memorija[list(pozvana.parametri.items())[i][0]]['vrijednost'] = poziv.mem[iter]['vrijednost']
            i += 1
        #argumenti = []
        #for key, value in poziv.param.items():
        #    par = (key, value)
        #    argumenti.append(par)
        return pozvana.pozovi()

        
class Vrati(AST):
   
    ime: 'IME varijable koju vracamo'
    param: 'PARAMETRI'
    mem: 'LOKALNA MEMORIJA'
    tip: 'TIP'

    def izvrši(vrati):
        if(vrati.ime not in vrati.mem):
            raise SemantičkaGreška("pokušavaš vratiti neinstanciranu varijablu")
        elif(vrati.tip != vrati.mem[vrati.ime]['tip']):
            raise SemantičkaGreška("povratna vrijednost varijable ne odgovara povratnom tipu funkcije")
        else:
            return vrati.mem[vrati.ime]['vrijednost']

class Blok(AST):
    naredbe: 'naredba*'

    def izvrši(program):
        ret_val = None
        for naredba in program.naredbe:
            ret_val = naredba.izvrši()
            if(ret_val): 
                return ret_val

class Ažuriraj(AST):
    ime : 'ime varijable'
    drugo_ime : 'varijabla ili vrijednost koja se pridružuje'
    mem : 'lokalna_memorija'
    pregledaj : 'bool'

    def izvrši(azuriraj):
        if(azuriraj.ime.vrijednost() not in azuriraj.mem):
            raise SemantičkaGreška('nije dozvoljena implicitna inicijalizacija varijable')
        trenutacni_tip = azuriraj.mem[azuriraj.ime.vrijednost()]['tip']
        if azuriraj.pregledaj: # znači da pokušavamo pridružiti varijablu
            if azuriraj.drugo_ime in azuriraj.mem:
                drugi_tip = azuriraj.mem[ azuriraj.drugo_ime]['tip']
                if drugi_tip == trenutacni_tip:
                    azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.mem[azuriraj.drugo_ime]['vrijednost']
                else:
                    raise SemantičkaGreška('varijable nisu istog tipa i ne postoji implicitni cast')
            else:
                raise SemantičkaGreška('varijabla koju pridružuješ nije instancirana')
        else: ## pridruzujem novu varijablu
            if(azuriraj.drugo_ime ^ Poziv):
                azuriraj.drugo_ime = azuriraj.drugo_ime.izvrši()
            if isinstance(azuriraj.drugo_ime, tuple ) and trenutacni_tip ^ T.NODE:
                azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.drugo_ime
            elif azuriraj.drugo_ime ^ T.BROJ and trenutacni_tip ^ T.INT:
                azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.drugo_ime
            else:
                raise SemantičkaGreška('varijabla i vrijednost nisu istog tipa')

class Unos(AST):
    tip_var: 'TIP'
    ime: 'IME'
    drugo_ime: 'IME ili vrijednost'
    mem: 'lokalna mem'
    pregledaj: 'bool'

    def izvrši(unos):
        if(unos.ime.vrijednost() in unos.mem):
            raise SemantičkaGreška('nije dozvoljena redeklaracija varijable')
        unos.mem[unos.ime.vrijednost()] = {}
        unos.mem[unos.ime.vrijednost()]['tip'] = unos.tip_var
        if unos.pregledaj:
            if unos.drugo_ime in unos.mem:
                drugi_tip = unos.mem[ unos.drugo_ime]['tip']
                if drugi_tip == unos.tip_var:
                    unos.mem[unos.ime]['vrijednost'] = unos.mem[unos.drugo_ime]['vrijednost']
                else:
                    raise SemantičkaGreška('varijable nisu istog tipa i ne postoji implicitni cast')
            else:
                raise SemantičkaGreška('varijabla koju pridružuješ nije instancirana')
        else:
            if(unos.drugo_ime ^ Poziv):
                unos.drugo_ime = unos.drugo_ime.izvrši()
            if isinstance(unos.drugo_ime, tuple ) and unos.tip_var ^ T.NODE:
                unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime
            elif unos.drugo_ime ^ T.BROJ and unos.tip_var ^ T.INT:
                unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime
            
            else:
                raise SemantičkaGreška()


class Ispis(AST):
    varijable: 'IME*'
    mem: 'lokalna memorija'
    def izvrši(ispis):
        for varijabla in ispis.varijable:
            if varijabla in ispis.mem:
                print(ispis.mem[varijabla]['vrijednost'], end='')
            else:
                raise SemantičkaGreška('varijabla ne postoji') 
        print()

ulaz=('''
int f(int x){
    x = 8
    RETURN x
}
int g( int x, int y ){
    CALL f(x, y)
    PRINT(x)
}
void h(int x){
    PRINT(x)
}
void main(){
    int y = 1
    int z = CALL f(y)
    PRINT (z)
}
''')
def test():
    lekser(ulaz)
    prikaz( kod := P(ulaz))
    izvrši(kod)

if __name__ == '__main__':
    print('Želiš li raditi interaktivno (I) ili samo istestirati (T)')
    intp = input()
    if intp == 'I':
        while(1):
            print("upiši novu naredbu")
            inpt = input()
            if(inpt == 'exit') : break
            lekser(inpt)
    else:
        test()