## Autori : Ivka Ćaćić, Mihovil Stručić, Matej Crnković
## lipanj 2023.
## PMF - MO Zagreb, kolegij Interpretacija Programa

# Ova datoteka predstavlja jezik namijenjen upravljanju grafovima i grafovskim strukturama.
# Ideja jezika je samostalno korištenje ili kao jezik korišten za postavljenjem upita na grafovske baze podataka.
# Jezik je razvijen u python modulu vepar.

## U sklopu jezika se onim deklaracije brojeva tipa int mogu i deklarirati varijable NODES koje predstavljaju čvorove grafa u 2D prostoru,
## varijable GRAPH koje predstavljaju povezane grafove sačinjene od više grafova i težine (bridova) među njima

## Jezik je napravljen po uzoru na one funkcijske i svaka naredba mora biti deklarirana unutar neke funkcije.
## Program mora imati minimalno main funkciju, a može imati i više funkcija definiranih prije 'maina' koje se mogu pozivati u 'main' funkciji.

## Omogućeno je pokretanje statičkog koda jezika zapisanog u obliku python stringa ili interaktivno pokretanje pojedinih naredbi. Interaktivno izvršavanje ima stanje 
## osnosno slično kao u python konzoli 'pamte' se prethodno definirane varijable.

## U jeziku nije moguće samo deklarirati varijable već svaka varijabla mora biti inicijalizirana vrijednostima ili drugom varijablom istog tipa.
## Varijablama je moguće mijenjati vrijednosti, ali ne i deklaraciju.

## Sve korištene varijable imaju lokalni scope unutar funkcije. Prijenos varijabli među funkcijama vrši se kopiranjem. Funkcije mogu, ali ne moraju, imati povratnu vrijednost
## te se takve funkcije mogu koristiti za inicijalizaciju ili pridruživanje.

## Na dva noda možemo pozvati funkciju DISTANCE koja će nam ispisati euklidsku udaljenost ta dva noda, na grafu i nodu možemo pozvati funkciju MATCH koja će nam vratiti
## parove svih nodova u grafu povezanih s tim nodom i težinu brida.

## Na grafu i 2 noda možemo pozvati funkciju PATH koja će nam vratiti najkraći put između ta dva čvora u obratnom poretku.
## Moguće je neki graf ispisati u datoteku na lokalnom disku kroz funkciju ISPISDAT


from vepar import *

## ugly global variables
## globalne varijable korištene za interaktivni rad
interaktivan_rad = False
rt.mem = Memorija() 

## tokeni 
class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL, DISTANCE = 'MATCH','WITH','WHERE','CALL', 'DISTANCE'
    RETURN,AS = 'RETURN','AS'
    UNOSDAT, ISPISDAT = 'UNOSDAT', 'ISPISDAT'
    PATH = 'path'
    FOR, IF, PRINT = 'for','if', 'print'
    VOID, NODE, INT, GRAPH= 'void', 'node','int', 'graph'   
    ULEFT ,URIGHT ='[',']'
    DVOTOČKA = ':'
    ARROW = '->'
    LINE = '-'
    OPEN, CLOSED, COLON, SEMICOLON, EQUAL, LESS = '(),;=<'
    CCLOSED, COPEN = '}{'
    PLUS, PUTA, = '+*'
    EEQUAL = '=='
    PLUSJ = '+='
    QUOTES = '"'

    # node A = f( B )
    # cuvanje koordinata vrhova grafa
    class PAIR(Token):
        def vrijednost(a,b):
            return zip(rt.mem[a], rt.mem[b])
        
    class IME(Token):
        def vrijednost(t): return str(t.sadržaj)

    class BROJ(Token):
        def vrijednost(t): return int(t.sadržaj)
    
    class FILEPATH(Token):
        def vrijednost(t): return str(t.sadržaj)

@lexer
def lekser(lex):
    for znak in lex:
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
                elif lex.sadržaj == 'DISTANCE':
                    yield lex.token(T.DISTANCE)
                elif lex.sadržaj == 'CALL':
                    yield lex.token(T.CALL)
                elif lex.sadržaj == 'RETURN':
                    yield lex.token(T.RETURN)
                elif lex.sadržaj == 'UNOSDAT':
                    yield lex.token(T.UNOSDAT)
                elif lex.sadržaj == 'ISPISDAT':
                    yield lex.token(T.ISPISDAT)
                elif lex.sadržaj == 'AS':
                    yield lex.token(T.AS)
                elif lex.sadržaj == 'PRINT':
                    yield lex.token(T.PRINT)
                elif lex.sadržaj == 'PATH':
                    yield lex.token(T.PATH)
                else:
                    raise lex.greška('Naredba nije leksički podržana')

            elif lex > str.isdecimal:
                prvo = next(lex)
                if prvo != '0': 
                    lex * str.isdecimal      # A,B,C,D1,E23
                yield lex.token(T.IME)
            else: yield lex.token(T.IME)            
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
                elif lex.sadržaj == 'graph':
                    yield lex.token(T.GRAPH)
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
        elif znak == '[':
            yield lex.token(T.ULEFT)
        elif znak == ']':
            yield lex.token(T.URIGHT)
        elif znak == ';':
            yield lex.token(T.SEMICOLON)
        elif znak == '/':   ## jednolinijski komentari neka budu oznaceni sa //
            lex >> '/'
            lex - '\n'
            lex.zanemari()
        elif znak == '"':
            lex - '"'
            yield lex.token(T.FILEPATH)
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
     
        
### pocetna BKG
##  program -> main |  funkcija program         # tu mozemo dodat proizvoljno mnogo funkcija prije ulaska u main
##  funkcija -> ime OPEN parametri CLOSED  COPEN blok CCLOSED         # klasicna definicija funkcije
##  parametri -> tip ime  |  parametri COLON tip ime
##  blok   ->  deklaracija blok | NAREDBA
##  NAREDBA  ->  unos | mozda_poziv | azuriraj | match | path | ispis_u_datoteku | vrati | petlja  |  ispis
##  petlja   ->  for  COPEN  NAREDBA CCLOSED
##  for   ->  FOR OPEN IME# EQUAL BROJ SEMICOLON IME# LESS BROJ SEMICOLON inkrement CLOSED
##  inkrement -> PLUSJ BROJ
##  ispis ->  PRINT  OPEN varijabla CLOSED
##  match -> ime OPEN ime CLOSED
##  path -> ime OPEN ime COLON ime CLOSED
##  ispis_u_datoteku -> GRAPH put_do_datoteke

## glavni parser
class P(Parser):

    ## startna funkcija parsera
    def program(p):
        if interaktivan_rad == False:
            p.funkcije = Memorija( redefinicija=False)
            while not p > KRAJ:
                funkcija = p.funkcija()
                p.funkcije[funkcija.ime] = funkcija
            return p.funkcije
        else: 
            return p.interaktivna_funkcija(T.VOID, nenavedeno, rt.mem) 
    
    def ime(p) -> 'IME': return p >> T.IME

    # pozivamo ju u dohvacanju parametara funkcije, vraca samo riječnik tipova
    def parametri(p) -> 'lista value tip':
        p >= T.OPEN
        if p >= T.CLOSED: return {}
        trenutni_tip = p.tip_parametra()

        params = {}
        trenutni_parametar = p >> { T.NODE, T.IME , T.GRAPH}
        params[trenutni_parametar] = trenutni_tip

        while p >= T.COLON:
            trenutni_tip = p.tip_parametra()
            trenutni_parametar = p >> { T.NODE, T.IME, T.GRAPH }
            params[trenutni_parametar] = trenutni_tip

        p >> T.CLOSED
        return params
    
    def tip_parametra(p) -> 'INT|NODE|GRAPH':
        return p >> {T.INT, T.NODE, T.GRAPH}
    
    def tip_funkcije(p) -> 'INT|NODE|VOID|GRAPH':
        return p >> {T.INT, T.NODE, T.VOID, T.GRAPH}


    ## glavna funkcija Parsera za kreiranje Funkcijskih ASTova. Budući da je GraphiC funkcijski jezik 'sve' prolazi ovdje
    def funkcija(p) -> 'Funkcija':
        atributi = p.tipf, p.imef, p.parametrif = p.tip_funkcije(), p.ime(), p.parametri()
        p >> T.COPEN

        ## definiramo lokalnu memoriju za svaku funkciju kako bi čuvali scope varijabli
        lokalna_memorija_funkcije = Memorija()
        for ime in p.parametrif:
            tip_vrijednost = {'tip':p.parametrif[ime],'vrijednost':nenavedeno}
            lokalna_memorija_funkcije[ime] = tip_vrijednost
        return Funkcija(*atributi, lokalna_memorija_funkcije,  p.sve_naredbe(p.tipf, p.parametrif, lokalna_memorija_funkcije))
  

    ## slično kao na predavanjima 
    def možda_poziv(p,ime, mem) -> 'Poziv|ime':
        p >> T.OPEN
        lista_param = []
        
        while not p >= T.CLOSED:
            varijabla = p >> T.IME
            lista_param.append(varijabla)
            p >= T.COLON
        if ime in p.funkcije:
            funkcija = p.funkcije[ime]
            return Poziv(funkcija, ime, lista_param, mem)
        else: 
            raise SemantičkaGreška('Koristite nepostojeću funkciju')
        return nenavedeno
     
    ## sve_naredbe kao parametar primaju tip funkcije i parametre funkcije i vraca AST tijela te funkcije
    ## koristimo za 'izgradnju' tijela funkcije 
    def sve_naredbe(p, tip, param, mem):
        naredbe = []
        while not p >= T.CCLOSED:
            naredbe.append(p.naredba(tip, param, mem))
        return Blok(naredbe)

    def interaktivna_funkcija(p, tip, param, mem):
        return Funkcija(tip, nenavedeno, param, mem,  Blok(p.naredba(tip, param, mem)))
    
    ## glavna funkcija za persiranje to jest odlučivanje o kreaciji AST-ova
    def naredba(p, tip, param, mem):
        if p > T.PRINT:
            return p.ispis(param, mem)
   
        elif p > T.FOR:
            return p.petlja(tip, param, mem)

        elif p > {T.INT, T.NODE, T.GRAPH}: 
            return p.unos(param, mem)

        elif p > T.CALL:
            p >> T.CALL
            if name := p >> T.IME: print("procitali smo ime funkcije")
            return p.možda_poziv(name, mem)

        elif p > T.MATCH:
            p >> T.MATCH
            ime_grafa = p >> T.IME
            p >> T.OPEN
            ime_vrha = p >> T.IME
            nesto =  Match(param,ime_grafa, ime_vrha, mem)
            p >> T.CLOSED   
            return nesto

        elif p > T.DISTANCE:
            return p.distance(tip,param,mem)

        elif p > T.PATH:
            p >> T.PATH
            ime_grafa = p >> T.IME
            p >> T.OPEN
            pocetni_vrh = p >> T.IME
            p >> T.COLON
            krajnji_vrh = p >> T.IME
            p >> T.CLOSED
            return Path(param, ime_grafa, pocetni_vrh, krajnji_vrh, mem)
        
        elif p > T.IME:
            return p.azuriraj(param,mem)

        elif p > T.ISPISDAT:
            return p.ispisi_u_dat(param,mem)
        
        elif p > T.UNOSDAT:
            raise SintaksnaGreška("Unos iz datoteke u trenutačnoj verziji nije podržan")
            return nenavedeno

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
            vrijednost =  p.unos_iz_funkcije(name, mem)
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)

        elif vrijednost := p >= T.BROJ:
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)

        elif drugo_ime := p >= T.IME:
            return Ažuriraj(ime, drugo_ime, mem, pregledaj = True)

        elif p >= T.OPEN:
            prva = p >> T.BROJ
            p >> T.COLON
            druga = p >> T.BROJ
            p >> T.CLOSED
            vrijednost = (prva, druga)
            return Ažuriraj(ime, vrijednost, mem, pregledaj = False)

        return nenavedeno

    ## koristimo za ispis grafa u datoteku
    def ispisi_u_dat(p, param, mem):
        p >> T.ISPISDAT
        p >> T.OPEN
        ime = p >> T.IME
        p >> T.COLON
        path = p >> T.FILEPATH
        p >> T.CLOSED
        return ISPISDAT(ime, path, mem)

    ## funkcija koja nam služi da pridruživanje povratnih vrijednosti funkcija varijablama
    def unos_iz_funkcije(p, name, mem):  
        if name in p.funkcije:
            pozvana = p.funkcije[name]
            if(pozvana.tip ^ T.VOID ):
                raise SemantičkaGreška('pozvana funkcije ne vraća povratnu vrijednost')
            else:
                return p.možda_poziv(name, mem)
        else:
            raise SemantičkaGreška('Ne postoji funkcija deklarirana tim imenom')  

    ## obrada inicijalizacije varijabli
    def unos(p,param,mem):
        tip_var = p >> {T.INT, T.NODE, T.GRAPH}
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
                name = p >> T.IME
                vrijednost = p.unos_iz_funkcije(name, mem)
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)

            elif p >= T.OPEN:
                prva = p >> T.BROJ
                p >> T.COLON
                druga = p >> T.BROJ
                p >> T.CLOSED
                vrijednost = (prva, druga)
                return Unos(tip_var, ime, vrijednost, mem, pregledaj = False)

            elif drugo_ime := p >= T.IME:
                return Unos(tip_var, ime, drugo_ime, mem, pregledaj = True)

        elif tip_var ^ T.GRAPH:

            if p > T.IME:
                graf_dict = {}
                while ime_nodea := p >= T.IME:
                    trenutni_dict = {}
                    p >= T.OPEN
                    novi_susjed = p >> T.IME
                    p >> T.ULEFT
                    trenutna_tezina = p >> T.BROJ
                    p >> T.URIGHT
                    trenutni_dict[novi_susjed] = trenutna_tezina

                    while  p > T.COLON:
                        p >> T.COLON
                        novi_susjed = p >> T.IME
                        p >> T.ULEFT
                        trenutna_tezina = p >> T.BROJ
                        p >> T.URIGHT
                        trenutni_dict[novi_susjed] = trenutna_tezina

                    graf_dict[ime_nodea] = trenutni_dict
                    p >> T.CLOSED
                    p >> T.COLON
                p >> T.SEMICOLON

            else:
                raise SemantičkaGreška('Prvo unosimo ime nodea za unos grafa')
           
            return UnosGrafa(tip_var, ime, graf_dict, mem, pregledaj = True)
        return nenavedeno

    ## obrada ispisa u konzolu
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

    ## for petlja
    def petlja(p, tip, param, mem):
        krivo = SemantičkaGreška('greška u inicijalizaciji for petlje')
        p >= T.FOR
        p >= T.OPEN

        tip_var = p >= T.INT
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
        
        return Petlja(ime_iteratora, donja_ograda, gornja_ograda, inkrement, blok, mem, tip_var)

    ## računanje euklidske udaljenosti među nodovima
    def distance(p, tip, param, mem):
        p >> T.DISTANCE
        p >> T.OPEN
        varijable = []
        if node1 := p >> T.IME:
            varijable.append(node1)
        p >> T.COLON
        if node2 := p >> T.IME:
            varijable.append(node2)
        p >> T.CLOSED
        return Distance(varijable,mem)

class Distance(AST): 
    varijable: 'varijable'
    mem: 'mem'

    def izvrši(self):
        if (not self.varijable[0] in self.mem):
            raise SemantičkaGreška("Proslijeđeni node na mjestu 1 ne postoji")
        if (not self.varijable[1] in self.mem):
            raise SemantičkaGreška("Proslijeđeni node na mjestu 2 ne postoji")
        node1 = self.mem[self.varijable[0]]
        node2 = self.mem[self.varijable[1]]
        if(not node1['tip'] ^ T.NODE or not node1['tip'] ^ T.NODE):
            raise SemantičkaGreška("Varijable prosljeđene operatoru DISTANCE moraju biti tipa T.NODE")
        x1, y1 = node1['vrijednost']
        x1 = x1.vrijednost()
        y1 = y1.vrijednost()
        x2, y2 = node2['vrijednost']
        x2 = x2.vrijednost()
        y2 = y2.vrijednost()
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        print(f"euklidska vrijednost izmedu {self.varijable[0]} i {self.varijable[1]} je {distance}")

class Petlja(AST):
    ime_iteratora: 'IME'
    donja_ograda: 'BROJ'
    gornja_ograda: 'BROJ'
    inkrement: 'BROJ'
    blok: 'naredba*'
    mem: 'lokalna memorija'
    tip_var : 'tip iteratora.'
    def izvrši(petlja):
        iter = petlja.ime_iteratora.vrijednost()
        petlja.mem[iter] = {}
        petlja.mem[iter]['vrijednost'] = petlja.donja_ograda.vrijednost()
        petlja.mem[iter]['tip'] = petlja.tip_var
        inc = petlja.inkrement.vrijednost(); 

        while( petlja.mem[iter]['vrijednost'] < petlja.gornja_ograda.vrijednost()):

            for naredba in petlja.blok: 
                naredba.izvrši()
            petlja.mem[iter]['vrijednost'] += inc

## AST koji koristimo za traženje najkraćeg puta Bellman-Fordovim algoritmom
class Path(AST):
    param: 'Parametri'
    ime_grafa: 'IME'
    pocetni_vrh: 'IME'
    krajnji_vrh: 'IME'
    mem: 'LOKALNA MEMORIJA'

    def izvrši(path):
        if path.ime_grafa not in path.mem:
            raise SemantičkaGreška('Ne postoji graf s tim imenom')
        elif path.pocetni_vrh not in path.mem[ path.ime_grafa]['nodovi']:
            raise SemantičkaGreška('Ne postoji vrh s tim imenom u danom grafu')    
        elif path.krajnji_vrh not in path.mem[ path.ime_grafa ]['nodovi']:
            raise SemantičkaGreška('Ne postoji vrh s tim imenom u danom grafu')
        else:
            distance = {}
            predecessor = {}
            temp_nodes = {}
            broj_vrhova = 0
            # spremimo graf jednostavnosti radi
            for key, value in path.mem[path.ime_grafa]['nodovi'].items():
                broj_vrhova +=1
                temp_neighbours = {}
                distance[ key.vrijednost()] = 1000
                predecessor[key.vrijednost()] = ''
                for neigh, weight in value.items():
                    temp_neighbours[neigh.vrijednost()] = weight.vrijednost()
                temp_nodes[key.vrijednost()] = temp_neighbours

            distance[path.pocetni_vrh.vrijednost()] = 0
            while( broj_vrhova > 1):
                for key, value in path.mem[path.ime_grafa]['nodovi'].items():
                    for neigh, weight in value.items():
                        if distance[key.vrijednost()] + weight.vrijednost() < distance[neigh.vrijednost()]:
                            distance[neigh.vrijednost()] = distance[key.vrijednost()] + weight.vrijednost()
                            predecessor[neigh.vrijednost()] = key.vrijednost()
                broj_vrhova = broj_vrhova-1
            kreni = path.krajnji_vrh.vrijednost()
            if( path.pocetni_vrh.vrijednost() == path.krajnji_vrh.vrijednost() ):
                print( "Najkraci put je duzine 0")
            else:
                print("Najkraci put (obrnuti redoslijed) = ", kreni, "<- ", end="")
                while(kreni != path.pocetni_vrh.vrijednost()):
                    if predecessor[kreni] == path.pocetni_vrh.vrijednost():
                        print( predecessor[kreni], end="")
                    else:
                        print( predecessor[kreni], "<- ", end="" )
                    kreni = predecessor[kreni]
                print()

class Match(AST):
    param: 'PARAMETRI'
    ime_grafa: 'IME GRAFA'
    ime_vrha: 'IME VRHA'
    mem: 'LOKALNA MEMORIJA'

    def izvrši(match):
        if match.ime_grafa not in match.mem:
            raise SemantičkaGreška('Ne postoji graf s tim imenom')
        elif match.ime_vrha not in match.mem[ match.ime_grafa]['nodovi']:
            raise SemantičkaGreška('Ne postoji vrh s tim imenom u danom grafu')
        else: 
            for neighbours, weights in match.mem[match.ime_grafa]['nodovi'][match.ime_vrha].items():
                print("(", match.ime_vrha.vrijednost(),"," ,neighbours.vrijednost(),")= ", weights.vrijednost())
               

## 'glavni' AST
class Funkcija(AST):
    tip: 'TIP'
    ime: 'IME'
    parametri: 'ULAZNI PARAM'
    memorija: 'lokalna mem'
    tijelo: 'naredba'

    def pozovi( funkcija):
        return (funkcija.tijelo.izvrši())

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
        return pozvana.pozovi()

## za RETURN      
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
            return vrati.mem[vrati.ime]

## tijelo funkcije
class Blok(AST):
    naredbe: 'naredba*'

    def izvrši(program):
        ret_val = None
        if(interaktivan_rad == False):
            for naredba in program.naredbe:
                ret_val = naredba.izvrši()
                if(ret_val): 
                    return ret_val
        else:
            ret_val = program.naredbe.izvrši()
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
            if(isinstance(azuriraj.drugo_ime, Poziv)):
                azuriraj.drugo_ime = azuriraj.drugo_ime.izvrši()
                if(azuriraj.drugo_ime['tip'] ^ T.BROJ and trenutacni_tip ^ T.INT):
                    azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.drugo_ime['vrijednost']
                elif(azuriraj.drugo_ime['tip'] ^ T.NODE and trenutacni_tip ^ T.NODE):
                    azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.drugo_ime['vrijednost']
                else:
                    raise SemantičkaGreška('tipovi varijable i argumenta ne odgovaraju')
            elif isinstance(azuriraj.drugo_ime, tuple ) and type(azuriraj.drugo_ime) != T.BROJ \
                and trenutacni_tip ^ T.NODE:
                azuriraj.mem[azuriraj.ime]['vrijednost'] = azuriraj.drugo_ime
            elif azuriraj.drugo_ime ^T.BROJ and trenutacni_tip ^ T.INT:
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
            if(isinstance(unos.drugo_ime, Poziv)):
                unos.drugo_ime = unos.drugo_ime.izvrši()
                if(unos.drugo_ime['tip']  ^ T.BROJ and unos.tip_var ^ T.INT):
                    unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime['vrijednost']
                elif(unos.drugo_ime['tip'] ^ T.NODE and unos.tip_var ^ T.NODE):
                    unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime['vrijednost']
                else:
                    raise SemantičkaGreška('tipovi varijable i argumenta ne odgovaraju')
            elif isinstance(unos.drugo_ime, tuple ) and type(unos.drugo_ime) != T.BROJ and\
                unos.tip_var ^ T.NODE:
                unos.mem[unos.ime]['vrijednost'] = (unos.drugo_ime[0],unos.drugo_ime[1])
            elif isinstance(unos.drugo_ime, tuple ) and type(unos.drugo_ime) != T.BROJ and\
                unos.tip_var ^ T.GRAPH:
                unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime
            elif unos.drugo_ime ^ T.BROJ and unos.tip_var ^ T.INT:
                unos.mem[unos.ime]['vrijednost'] = unos.drugo_ime
            else:
                raise SemantičkaGreška('tipovi varijable i argumenta ne odgovaraju')

class UnosGrafa(AST):
    tip_var: 'TIP'   # u nasem slucaju mora biti tip graf
    ime: 'IME grafa'  
    graf_dict: 'RJECNIK GRAFA'
    mem: 'lokalna mem'
    pregledaj: 'bool'
    # graf_dict[a][b] = 10

    def izvrši(unos):
        if ( unos.ime.vrijednost() in unos.mem):
            raise SemantičkaGreška('nije dozvoljena redeklaracija varijable')
        unos.mem[unos.ime.vrijednost()] = {}
        unos.mem[unos.ime.vrijednost()]['tip']= unos.tip_var
        if unos.pregledaj:
            neighbours_dict = {}

            for key, values in unos.graf_dict.items():
                if key not in unos.mem:
                    raise SemantičkaGreška('varijabla koju pridružuješ nije istancirana')
                temp_dict = {}

                #neighbours_dict = {}
                for neighbours_key, neigh_values in values.items():
                   
                    if neighbours_key not in unos.mem:
                        raise SemantičkaGreška('varijabla koju pridružuješ nije istancirana')
                    elif not unos.mem[neighbours_key]['tip'] ^ T.NODE:
                        raise SemantičkaGreška('grafu se smiju pridruživati samo već instancirani NODOVI')
                    else:
                        temp_dict[neighbours_key] = neigh_values
                        print("susjedi= ",neighbours_key, neigh_values)

                neighbours_dict[key] = temp_dict
                unos.mem[unos.ime.vrijednost()]['nodovi'] = neighbours_dict
        else:
            raise SemantičkaGreška("Semantic Error")

## print na konzolu
class Ispis(AST):
    varijable: 'IME*'
    mem: 'lokalna memorija'
    def izvrši(ispis):
        for varijabla in ispis.varijable:
            if varijabla in ispis.mem:
                if ispis.mem[varijabla.vrijednost()]['tip'] ^ T.GRAPH:
                    print(ispis.mem[varijabla.vrijednost()]['nodovi'], end='')
                else:
                    print(ispis.mem[varijabla]['vrijednost'], end='')
            else:
                raise SemantičkaGreška('varijabla ne postoji') 
        print()

## ispis grafa u datoteku
class ISPISDAT(AST):
    ime : 'ime grafa'
    path : 'put do datoteke'
    mem : 'lokalna memorija'

    def izvrši(ispis):
        if (ispis.ime not in ispis.mem):
            raise SemantičkaGreška('dani graf ne postoji u memoriji')
        if (not ispis.mem[ispis.ime.vrijednost()]['tip'] ^ T.GRAPH) :
            raise SemantičkaGreška('dani argument nije graf')
        path_datoteka = ispis.path.vrijednost().replace('"', '')
        ispis.ispiši(path_datoteka)
    
    def ispiši(ispis, path):
        try:
            with open(path, 'w') as file:
                # Ovdje možete pisati u datoteku
                file.write("ISPISAN JE GRAF : " + ispis.ime.vrijednost() + "\n")
                file.write("NJEGOVI NODOVI SU : \n")
                for nod, value in ispis.mem[ispis.ime.vrijednost()]['nodovi'].items():
                    file.write("\n" + nod.vrijednost() + "  ")
                    file.write(" KOJI JE POVEZAN S : ")
                    for susjed, vrijednost in value.items():
                        file.write(susjed.vrijednost() + ":")
                        file.write(str(vrijednost.vrijednost()) + " ")
            file.close()
        except IOError:
            raise SemantičkaGreška("dan je neispravan put do datoteke")

## funkcija za izvršavanje 'programa'
def izvrši(funkcije, *argv):
    print('Program je vratio:', funkcije['main'].pozovi())

## funkcija za izvršavanje interaktivnih naredbi
def izvrši_interaktivno(funkcija, *argv):
    print('Program je vratio:', funkcija.pozovi())
        

## jednostavni primjer
ulaz=('''
void main(){
    node a = (1,2)
    node b = (2,3)
    node c = (2,3)
    node d = (2,3)
    node e = (9,9)
    for (int i = 1 ; 7 ; i += 1){
        PRINT(e)
    }
    // print euklidske udaljenost među čvorovima
    DISTANCE (a, e)
    graph G = a(b[2],c[5],e[11]),b(d[4]),c(b[2]),d(a[1]),e(c[3]),;
    ISPISDAT (G , "dat.txt")
    MATCH G(a)
    PATH G(b,e)
}
''')

## pokretanje jednostavnog primjera
def test():
    lekser(ulaz)
    prikaz( kod := P(ulaz))
    izvrši(kod)

## help text korišten u interaktivnom načinu
help_me = '''HELP : 
Dobrodošli u help jezika GraphiC, jezik namijenjen obradi grafova i grafovskih baza podataka.
Kroz ovu interaktivnu konzolu možete unositi pojedinačne naredbe koje podržava jezik.
Primjeri poziva su inicijalizacija verijabli, pridruživanje vrijednosti varijablama, printanje varijabli,
ispis grafa u datoteku i tako dalje.

Neki od primjera atomarnih poziva kroz konzolu su :
>>> int a = 5
>>> int y = a
>>> PRINT (a)
>>> node z = (2,1)
>>> node c = z
'''

## poziv filea
if __name__ == '__main__':
    print('Želiš li raditi interaktivno (I) ili samo istestirati (T)')
    intp = input()
    if intp == 'I':
        print("Dobrodošli u konzolu:")
        print("Za pomoć u bilo kojem trenutku upišite help_me(), za izlaz iz konzole upišite exit")
        interaktivan_rad = True
        while(1):
            print(">>>")
            inpt = input()
            if(inpt == 'exit') : exit()
            elif (inpt == 'help_me()') : 
                print(help_me)
                continue
            ## ovdje je namjerno izostavljen prikaz leksiranja i parsiranja kako
            ## bi se izbjegla gužva u konzolu
            kod = P(inpt)
            izvrši_interaktivno(kod)
    else:
        test()
