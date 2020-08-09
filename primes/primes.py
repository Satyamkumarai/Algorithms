#Few util functions revolving a round primes.. 



from ast import literal_eval
import time
import pickle
import os 
import json
primesDict = {2: 1, 3: 2}
primesPickleFile = os.path.join(os.path.abspath(os.path.dirname(__file__)),"PRIMES10000000.bin.pkl")
def getLastPrime(primesDict = primesDict):
    """Get the Last prime Number in the $primesDict
        format of primesDict ->  "prime":"ordinal of the prime"
    """
    popped = primesDict.popitem()
    primesDict[popped[0]] = popped[1]
    return popped[0]
def importPrimesDict()->None:
    global primesDict
    print("Importing Pickle file")
    with open(primesPickleFile , "rb") as file:
        primesDict = pickle.load(file)
    print("Dicitonary Loaded!")

def parsePrimesFromTxt(filename :str, keySep:str ,itemSep:str) -> dict:
    """
    returns a dictionary With the primes..
    keySep: The seperator used to sepearate the key from the  value  
    itemSep: The sepearator used to seperate the items..
        eg: in python dict {"key1":"value1","key2":"Value2"}  -> itemSep =  "," keySep = ':'
    """
    try:
        with open(filename,"r") as file:
            data = file.read()
        if itemSep !=  "," :
            data = data.replace(itemSep,",")
        if keySep != ":":
            data = data.replace(keySep,":")
        data = data.lstrip("{").rstrip("}")
        return literal_eval("{"+data+"}")
    except Exception as e:
        print("Exception Occurred",e)

def isPrime(m:int,primesDict = primesDict)->bool:
    """Check if  a number is a prime"""
    lastPrime = 0
    if len(primesDict) > 0:
        lastPrime = getLastPrime(primesDict)
    if lastPrime >= m:                                  ##If the last prime no in the dict is larger than  the no..
        return m in primesDict
    if (m % 2 == 0)and(m > 2):
        return False
    elif int(m**0.5) == (m**0.5):       ##is a sq no?
        return False    
    else:
        r2t = m**0.5
        for i in range(3, int(r2t)):
            if(m % i == 0)or(m % (int(r2t)+i) == 0):
                return False
        return True

# So Here instead of checking for numbers divisible by the *numbers* in range [2,sqrt(n)]  (2,3,4,5,6,7,8,9) for n = 81 vs
# here we check if the number is divisible by *prime numbers* in  range[2,sqrt(n)]          (2,3,5,7)  for n = 81 (only primes..)
    #i.e we use the same dict to already available primes and use those primes to check if this new number is prime or not..
#This is sufficient cuz if a number P is not divisible py primes < P then it is also a prime..
#In fact if this number is not divisible by primes up to sqrt(P)  then it is  a  prime..  (same as how you have to check up to sqrt(P) to check if P is prime )

def prma(u:int, l:int=2,primesDict:dict = primesDict)->None:
    """fills the primesDict dict with prime numbers <=u\n
        l: (optional) Starting value \n
        primesDict: (optional) Dictionary containing primes and  ordinal of the prime as Key Value pair.\n
    """
    if len(primesDict) <= 1:
        primesDict[2] = 1
        primesDict[3] = 2
    
    psrt = 2
    while l <= u:                               # while the number (l) is less than(or equal to ) the given
    
        if l > psrt**2:                         # if l exceeds the previous val of psrt

            psrt = (l**0.5)                     # psrt = sqrt(l)

        for i in primesDict:                          #for the primes currently in primesDict

            if i > psrt:                        # You need to only check till the sqrt(l) to see if it is a prime..
                primesDict[l] = len(primesDict)+1                 #if it exceeds the value then it must be prime..
                break

            if l % i == 0:                      # if it is divisible.. it jumps to the next number for l i.e: l++
                break
        l += 1



def primeIterator(no = 0,lessThan = None ):
    """A prime numbers iterator \n
        no: int  -> Returns $no number of  primes  (if 0 => inf)
        lessThan : int -> returns all primes lessthan $lessThan
        if ($n == 0 and $lessThan is valid ) => limited by $lessThan
        """
    
    prmd  = {2:1,3:2}
    sqrtn = 2
    l = 1
    count = 0
    #or (no==-1 and not lessThan) l < no or:
    print("no", no)
    while ((no!=0 and count < no) or ( (no==0) and (lessThan and l<lessThan ) or (not lessThan ) ))and (l<4) :
        if l in prmd:
            count += 1
            yield l
        l+=1
    l=5
    add = 2
    
    while (no!=0 and count < no) or ( (no==0) and ( (lessThan and l<lessThan ) or (not lessThan )) ) :  #check only 6n-1 and 6n+1
        if l > sqrtn**2:
            sqrtn = l**0.5
        for i in prmd:
            if i > sqrtn:
                prmd[l] = len(prmd)
                add = 2 if add==4 else 2
                count +=1
                yield l
                break
            if l%i ==0 :  
                break
        l+=add
def prmn(n, l=2,primesDict = primesDict):
    """fills up primesDict dict with n primes..(starting from 2)"""
    if len(primesDict) <= 1:
        primesDict[2] = 1
        primesDict[3] = 2
    u = n
    psrt = 2
    while len(primesDict) <= u:
        if l > psrt**2:
            psrt = (l**0.5)

        for i in primesDict:
            if i > psrt:

                # store the last_value_in_dict:current_prime_no
                primesDict[l] = len(primesDict)+1
                break
            if l % i == 0:
                break
        l += 1
    primesDict[3] = 2

def factorize(n:int,primesDict:dict = primesDict):
    """
    (incomplete)
    Factorizes $n using the primes in dict $primesDict\n
    \nIt first calculates the primes upto n So If the primes in the primesDict is precalculated It would Make it a lot faster..

    """

    
    if isPrime(n,primesDict):
        return {n:1}

    factors = {}

    lastPrime = getLastPrime(primesDict)
    print (lastPrime,"Lastprimes")
    if lastPrime < n:
        print ("Creating DictS")

        prma(n,lastPrime,primesDict)

    for i in primesDict:
        if n%i == 0 :
            count = 0
            while n % i**(count+1) == 0 :
                count+=1 
            factors[i]= count

    return factors

from itertools import islice

def n_th_prime(n:int, primesDict:dict = primesDict):
    """returns the nth prime number.."""
    if n > len(primesDict):
        prmn(n,primesDict)
    count = 0
    for i in primesDict:
        count+=1
        if count == n:
            return i




def getDivisors(n):
    """returns a list of divisors of the given no.."""

#       By       SatyamRai





# if __name__ == "__main__":
#     print("importing dict..")
#     print(parsePrimesFromTxt(primesTxtFile,primes_keySep,primes_itemSep))

"""000000
st=time.time()
a=1000000
q=[]
prma(a)
print(time.time()-st)
    """

'''for i in range(1,32436851,2):
    if(prime(i)):
        k.append(i)

'''
