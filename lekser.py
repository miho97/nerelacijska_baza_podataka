## lekser nerelacijske baze podataka


from vepar import *
#from backend import *


class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL = 'match','with','where','call'
    RETURN,AS = 'return','as'
    OPEN, CLOSED, COLON, SEMICOLON = '(),;'
    PLUS, PUTA, = '+*'

    #class GRAF(Token):...
    class NODE(Token):... 
    #class NEIGHBOURS(Token):...

    #class TIP(Token):...





# kao oznake cvorova ideja bi bila imati A,B,C,... A1,D2,...   
# ali ne AB jer bi dolazilo do miješanja sa AS, MATCH itd..
# graf bi se ucitavao oblika:
##  A(B,C,D,E), B(B), C(), D(A,B);
# mozemo se dogovorit u svezi prelaska u druge redove
##  B(B)
##  C()
##  D(A,B);

@lexer
def program(lex):
    for znak in lex:
        ## mala slova sacuvati za for petlju itd
        if znak.isspace(): 
            lex.zanemari()
        if znak.isalpha and znak.isupper():   
            if lex > str.isalpha: 
                yield lex.token(T.NODE)
            elif lex > str.isdecimal:
                prvo = next(lex)
                if prvo != '0': 
                    lex * str.isdecimal
                yield lex.token(T.NODE)
            else: yield lex.token(T.NODE)
       
        elif znak == '(':
            yield lex.token(T.OPEN)
        elif znak == ',':
            yield lex.token(T.COLON)
        elif znak == ')':
            yield lex.token(T.CLOSED)
        elif znak == ';':
            yield lex.token(T.SEMICOLON)
        elif znak == '[':   ## jednolinijski komentari neka budu oznaceni sa [[, ako ko smisli bolji znak koji zaseban nema znacenje minjamo
            lex >> '['
            lex - '\n'
            lex.zanemari()
        else:
            yield lex.literal(T)
        
        """
        elif znak == '(':
            drugo = next(lex)
            if drugo == ')': yield lex.token(T.NEIGHBOURS)
            elif drugo.isalpha:
                if not drugo.isupper(): raise lex.greška('NODE nije označen sukladno pravilima')
                prvo = next(lex)
                if prvo != '0':
                    lex * str.isdecimal
                yield lex.token()
        """

ulaz = 'A12(B,C,E),B(),C(F)[[\nF(G,A,H,I)'
#ulaz = 'A1B2'
#ulaz = 'ABCDEF'
program( ulaz )

##ulaz2 = 'A23sd'
##program(ulaz2)


