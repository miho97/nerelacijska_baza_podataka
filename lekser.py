## lekser nerelacijske baze podataka


from vepar import *
#from backend import *


class T(TipoviTokena):

    MATCH, WITH, WHERE, CALL = 'match','with','where','call'
    RETURN,AS = 'return','as'

    OPEN, CLOSED, COLON, SEMICOLON = '(),;'
    COPEN, CCLOSED = '}{'
    PLUS, PUTA, = '+*'

    class NODE(Token):... 
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
         
       
        elif znak == '(':
            yield lex.token(T.OPEN)
        elif znak == ',':
            yield lex.token(T.COLON)
        elif znak == ')':
            yield lex.token(T.CLOSED)
        elif znak == ';':
            yield lex.token(T.SEMICOLON)
        elif znak == '/':   ## jednolinijski komentari neka budu oznaceni sa //
            lex >> '/'
            lex - '\n'
            lex.zanemari()

        
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

#ulaz = 'A12(B,C,E),B(),C(F)//par nodeova grafa su dodani\n  F(G,A,H,I)'
#ulaz = 'A1B2'
#ulaz = 'ABCDEF'
#ulaz = 'MATCH A RETURN A'
ulaz = '''

MATCH A RETURN A
B(C,D,E),D(E),G(H,A,I,J);

'''
lekser( ulaz )

##ulaz2 = 'A23sd'
##program(ulaz2)


