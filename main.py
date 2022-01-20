'''Componenta echipei:
    Ene Marius-Andrei
    Doncea Batrice-Anamaria
'''


import sys

def Load_Section(Nume, vector):  #sursa, laboratorul 1.
    section_list = [] #variabila auxiliara
    check = False
    for line in vector:
        if line == (Nume + ":"):    #verificam fiecare sectiune in parte Tapes, Transitions etc
            check = True
            continue

        if line == "End":           #Daca intalnim end inseamna ca sectiunea s-a terminat
            check = False

        if check == True:           #Adaugam in lista auxiliara linia curenta, daca s-au indeplinit conditiile de mai sus
            section_list.append(line)
    return section_list             #returnam lista

def load_tm_from_file(file_name):
    throw = 0
    try:
        f = open(file_name) # citim din fisier, daca numele fisierului este introdus gresit "aruncam" o eroare
    except IOError:
        throw = 1
        return [], [], [], [], [], [], throw
    read_line = []      # lista in care "prelucram" ce se afla in fisier
    for line in f:      # pentru fiecare linie din fisier scapam de spatiile albe
        line = line.strip()
        if line and '#' not in line: # aici verificam ca linia sa nu fie nula sau sa aiba # in ea (asa am facut noi fisierul)
            read_line.append(line)

     #aici se apeleaza functia load_Section pentru fiecare sectiune in parte
    states_list = Load_Section("States", read_line)
    transitions_list = Load_Section("Transitions", read_line)
    tape_list = Load_Section("Tape", read_line)
    start = Load_Section("Start state", read_line)
    accept = Load_Section("Accept state", read_line)
    reject = Load_Section("Reject state", read_line)

    start = start[0]
    accept = accept[0]
    reject = reject[0]


    # verificam daca listele create anterior sunt nule
    if not states_list or not transitions_list or not tape_list or not start or not accept or not reject:
        throw = 2
        return [], [], [], [], [], [], throw

    # verificam daca starea de start, accept si reject se afla in lista de stari
    if start not in states_list or accept not in states_list or reject not in states_list:
        throw = 3
        return [], [], [], [], [], [], throw

    transitions_list_aux = []


    for i in range(len(transitions_list)):
        aux = transitions_list[i].split(" ")
        # verificam daca o tranzitie a fost scrisa gresit (trebuie sa aiba lungimea 8)
        # caracterul _ reprezinta blank
        if len(aux) != 8:
            throw = 7
            return [], [], [], [], [], [], throw

        # verificam daca starea in care ne aflam si starea in care vom merge se afla in lista de stari
        if aux[0] not in states_list or aux[1] not in states_list:
            throw = 4
            return [], [], [], [], [], [], throw

        # verificam daca caracterul de pe pozitia 2, 3, 5, 6 (adica cele care se rescriu) se afla in lista de simboluri
        if (aux[2] not in tape_list or (aux[3] not in tape_list and 'e' not in aux[3])) and (aux[5] not in tape_list or (aux[6] not in tape_list and aux[6] != 'e')):
            throw = 5
            return [], [], [], [], [], [], throw

        # verificam daca s-a introdus o directie
        if (aux[4] != 'R' and aux[4] != 'L') and (aux[7] != 'R' and aux[7] != 'L'):
            throw = 6
            return [], [], [], [], [], [], throw

        transitions_list_aux.append(transitions_list[i])

    return states_list, transitions_list_aux, tape_list, start, accept, reject, throw


states_list, transitions_list, tape_list, start, accept, reject, throw = load_tm_from_file(sys.argv[1])

def catch(throw): # aici am facut o mica functie bazata pe exceptiile din c++ (am zis sa fie frumos pastrand oarecum)
                  # sintaxa de try, throw, catch
                  # si practic daca fisierul de input nu este scris corect se afiseaza o eroare cu codul ei
    print("Status check: ")
    if throw==0:
        print("Program is working")
    elif throw == 1:
        print("Cannot load from this file")
    elif throw == 2:
        print("Lists are empty(Check your input file)")
    elif throw == 3:
        print("Start/Accept/Reject invalid")
    elif throw == 4:
        print("The first 2 values cannot be found")
    elif throw == 5:
        print("The third values is incorrect")
    elif throw == 7:
        print("Check transitions length")
    elif throw == 6:
        print("The forth and the seventh values must be R or L (left - right)")

catch(throw)


for i in range(len(transitions_list)):
    transitions_list[i] = transitions_list[i].split()

def crate_text(transitions_list, start, accept, reject, input_string):
    tape_aux = input_string
    #_aab_aab_   # caracterul _ este blank
    current_state = start

    tape_aux = '_' + tape_aux + '_'     #stringul v-a fi de forma _aa_aa_ pentru a fi mai usor de verificat capetele
    head_begin = 1  #capatul 1
    head_middle = tape_aux.find('_', 1) + 1   #capatul 2

    #am fixat acpatul 1 la inceputul primei jumatati si pe cel de-al doilea la inceputul celei de-a 2 jumatati

    if (len(tape_aux[:head_middle - 1]) != len(tape_aux[head_middle:])): #daca cele 2 jumatati nu au lungimi =, respingem
        current_state = reject

    contor = 0

    while current_state != accept and current_state != reject:

        for transition in transitions_list: #parcurgem tranzitiile
            contor = contor + 1

            if current_state == transition[0]: # caut o noua stare, primul venit primul servit
                current_state = transition[1]

                if tape_aux[head_begin] == transition[2] and transition[3] != 'e':
                    tape_aux[head_begin] = transition[3]
                    if transition[4] == 'R' and tape_aux[head_begin+1] != '_':
                        head_begin = head_begin + 1
                    elif transition[4] == 'L' and tape_aux[head_begin-1] != '_':
                        head_begin = head_begin - 1

                if tape_aux[head_middle] == transition[5] and transition[6] != 'e':
                    tape_aux[head_middle] = transition[6]
                    if transition[7] == 'R' and tape_aux[head_middle+1] != '_':
                        head_middle = head_middle+1
                    elif transition[7] == 'R' and tape_aux[head_middle-1] != '_':
                        head_middle = head_middle-1

        if contor > 10000: #inseamna ca a intrat in loop infinit -> tranzitiile nu sunt bune
            return 'Rejected'

    if 'accept' in current_state:
        return 'Accepted'
    elif 'reject' in current_state:
        return 'Rejected'

print(crate_text(transitions_list, start, accept, reject, sys.argv[2]))

#am incercat inca o versiune, primim acelasi raspuns pentru acest file (nu am facut tranzitiile bine)

'''
def check_s(input_list, transitions_list, start, accept, reject):
    current_state = start                       # facem ca starea curenta sa fie chiar starea de start, deoarece suntem la inceputul cuvantului 
    contor = 0                                  # vom contoriza cu contor numarul de tranzitii pe care il face
    tape = [x for x in input_list]
    # initializam 2 indecsi, unul pentru primul cap care pleaca din stanga
    # cel de-al doilea pentru al doilea cap care pleaca din dreapta(de la finalul inputului)
    index1 = 0
    index2 = len(tape) - 1
    while current_state != accept and current_state != reject:  # punem conditia ca starea curenta sa nu fie una finala, pentru a putea parcurge tranzitiile
        contor = contor + 1
        for transition in transitions_list: # extragem fiecare lista din lista mare 
            if transition[0] == current_state:  #verificam ca prima stare a primei tranzitii sa fie cea curenta, in cazul acesta,
                 current_state = transition[1]   # aici urmatoarea stare se face stare curenta 
                if transition[5] != 'e':        # verificam ca, caracterul cu care trebuie inlocuit cel curent sa nu fie el insusi
                    tape[index1] = transition[5]
                if transition[4] == 'L' and index1 > 0: #daca ne pozitionam cu primul cap pe prima pozitie a inputului, acesta va ramane acolo, chiar daca primeste comanda L
                    index1 = index1 - 1
                elif transition[5] == 'R' and index1 < len(tape) -1 :
                    index1 = index1 + 1
                if transition[6] != 'e':    # si aici se verifica cu ce trebuie inlocuit caracterul
                    tape[index2] = transition[6]    
                if transition[7] == 'R' and index2 < len(tape)-1:   # daca ne pozitionam cu al doilea cap pe ultima pozitie a inputului, acesta va ramane acolo, chiar daca primeste comanda R
                    index2 = index2 + 1
                elif transition[7] == 'L' and index2 > 0:
                    index2 = index2 - 1
        if contor > 1000:       # am contorizat de cate ori masina Turing intra si reface algoritmul, pentru a-i putea da un break 
            break               # in cazul in care acesta intra in loop(nu ajunge nici in starea de accept, nici in cea de reject)

    if current_state == accept:
        return 'Acceptat'
    if current_state == reject:
        return 'Respins'
    else:
        return 'Necunoscut'

print(check_s(sys.argv[2], transitions_list, start, accept, reject))
'''





