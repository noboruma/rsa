#Transforme une chaine de caractere en paquets d'entiers de N bits
def numerise(mess,N):
        N = int(ln(N)/ln(10) + 1)
        monoide = BinaryStrings()
        mess = monoide.encoding(mess)
        mess = str(mess)
        # On ajoute les '0' manquants pour avoir des paquets de tailles fixes et identiques
        if N > len(mess):
                N = len(mess)
        res = []
        #On decoupe la chaine en paquets de taille N
        while mess:
                #On recupere une partie de la chaine
                res.append(mess[:N])
                #On passe au reste de la chaine
                mess = mess[N:]
        return res

#Transforme des paquets d'entiers de N bits en une chaine de caractere
def alphabetise(lis,N):
        for i in range(0,len(lis)-1):
                lis[i] = lis[i].zfill(int((ln(N)/ln(10))+1))
        monoide = BinaryStrings()
        res = '';
        for i in range(0,len(lis)-1):
                res += lis[i]

        #comblons les trous du dernier paquet pour retrouver la des octets (suites de 8 bits)
        tmp = lis[len(lis)-1]
        while (len(res) + len(tmp)) %8 <> 0:
                tmp = '0'+tmp
        res += tmp
        return monoide(res).decoding()

#Genere un N, un e et un d pour le RSA
def clefRSA(m):
        sup = 10**(floor(m/2))
        p = next_prime(randint(sup,sup*10-1))
        q = next_prime(randint(sup,sup*10-1))
        n = p*q
        #Phi
        f = (p-1)*(q-1)

        e =0
        while gcd(e,f) <> 1:
                e = randint(2,1000)
        #Bezout
        d = xgcd(e,f)[1]

        return n,e,d

#Crypt/Decrypt ne liste d'entier
def chiff(l,e,n):
        return [Integer(power_mod(int(x,2),e,n)).binary() for x in l]

#Premier test
def protocole1():
        Bob = clefRSA(20)
        Alice = clefRSA(20)
        publicBob = [Bob[1],Bob[0]]
        privateBob = [Bob[2],Bob[0]]
        publicAlice = [Alice[1],Alice[0]]
        privateAlice = [Alice[2],Alice[0]]

        print 'Alice prepare un message :\n'
        #Ici on a publicBob et privateAlice

        m1 = 'coucou je suis alice'
        s1 = 'Alice'
        #On donne le N de Bob pour le decoupage en paquet
        m1c = numerise(m1,publicBob[1])
        #On donne le N d'Alice pour le decoupage en paquet
        s1c = numerise(s1,privateAlice[1])

        m2c = chiff(m1c,publicBob[0],publicBob[1])
        s2c = chiff(s1c,privateAlice[0],privateAlice[1])

        print 'Alice envoie le message a Bob :\n'
        print 'Bob decrypte :\n'
        #Ici on a privateBob et publicAlice

        mc2 = chiff(m2c,privateBob[0],privateBob[1])
        sc2 = chiff(s2c,publicAlice[0],publicAlice[1])

        m1f = alphabetise(mc2,privateBob[1])
        s1f = alphabetise(sc2,publicAlice[1])
        print 'Bob a : '+m1f 
        print s1f


def protocole2():
        Bob = clefRSA(20)
        Alice = clefRSA(20)
        print Bob[0]
        print Alice[0]
        publicBob = [Bob[1],Bob[0]]
        privateBob = [Bob[2],Bob[0]]
        publicAlice = [Alice[1],Alice[0]]
        privateAlice = [Alice[2],Alice[0]]

        print 'Alice part :'

        m1 = 'coucou c\'est alice'
        s1 = 'Alice'
        m1c = []

        if publicBob[1] > privateAlice[1]:
                print 'cas1' 
                m1c = numerise(m1,publicBob[1])
                m2c = chiff(m1c,privateAlice[0],privateAlice[1])
                m3c = chiff(m2c,publicBob[0],publicBob[1])
                
                print 'Bob part'
                m2c = chiff(m3c,privateBob[0],privateBob[1])
                m1c = chiff(m2c,publicAlice[0],publicAlice[1])

                m1 = alphabetise(m1c,privateBob[1])
                print 'Bob a :'+m1
        elif publicBob[1] < privateAlice[1]:
                print 'cas2' 
                m1c = numerise(m1,privateAlice[1])
                m2c = chiff(m1c,publicBob[0],publicBob[1])
                m3c = chiff(m2c,privateAlice[0],privateAlice[1])
                
                print 'Bob part'
                m2c = chiff(m3c,publicAlice[0],publicAlice[1])
                m1c = chiff(m2c,privateBob[0],privateBob[1])
                m1 = alphabetise(m1c,publicAlice[1])
                print 'Bob a :'+m1
        return 1
