from collections import Counter
pA = 0.0
pNotA = 0.0
noSpam = {}
yesSpam = {}
spam_main_yes = {}
spam_main_no = {}
yesSpam['Kol-vo vhozh']=0
noSpam['Kol-vo vhozhdenii']=0

train_data = [  
    ['Купите новое чистящее средство', 'SPAM'],   
    ['Купи мою новую книгу', 'SPAM'],  
    ['Подари себе новый телефон', 'SPAM'],
    ['Добро пожаловать и купите новый телевизор', 'SPAM'],
    ['Привет давно не виделись', 'NOT_SPAM'], 
    ['Довезем до аэропорта из пригорода всего за 399 рублей', 'SPAM'], 
    ['Добро пожаловать в Мой Круг', 'NOT_SPAM'],  
    ['Я все еще жду документы', 'NOT_SPAM'],  
    ['Приглашаем на конференцию Data Science', 'NOT_SPAM'],
    ['Потерял твой телефон напомни', 'NOT_SPAM'],
    ['Порадуй своего питомца новым костюмом', 'SPAM']
]  

def calculate_word_frequencies(body, label):
    if label=='SPAM':
        body = body.lower().split(' ')
        c = Counter(body)
        for x,y in c.items():
            if x not in yesSpam.keys():
                yesSpam[x]=y
            else:
                yesSpam[x]+=1
        yesSpam['Kol-vo vhozh']+=1
        return(yesSpam)
    else:
        body = body.lower().split(' ')
        c = Counter(body)
        for x,y in c.items():
            if x not in noSpam.keys():
                noSpam[x]=y
            else:
                noSpam[x]+=1
    noSpam['Kol-vo vhozhdenii']+=1
    return(noSpam)

def train():
    for test_str in train_data:
        calculate_word_frequencies(test_str[0],test_str[1])
    for x,y in yesSpam.items():
         if x != 'Kol-vo vhozh':
                if (y/yesSpam['Kol-vo vhozh']) <=1:
                    spam_main_yes[x]=round(y/yesSpam['Kol-vo vhozh'],2)
                else:
                    spam_main_yes[x]=1
    for x,y in noSpam.items():
        if x != 'Kol-vo vhozhdenii':
            if (y/noSpam['Kol-vo vhozhdenii']) <=1:
                spam_main_no[x]=round(y/noSpam['Kol-vo vhozhdenii'],2)
            else:
                spam_main_no[x]=1

train()
pA = round(yesSpam['Kol-vo vhozh'] / (yesSpam['Kol-vo vhozh'] + noSpam['Kol-vo vhozhdenii']),2)
pNotA = round(noSpam['Kol-vo vhozhdenii'] / (noSpam['Kol-vo vhozhdenii'] + yesSpam['Kol-vo vhozh']),2)

def classify(text):
    text = text.lower().split(' ')
    pYES=1
    pNO=1
    for each_word in text:
        if each_word in spam_main_yes.keys():
            pYES *=spam_main_yes[each_word]
        else:
            pYES *=1/yesSpam['Kol-vo vhozh']       #если слова нет в словаре
    for each_word in text:
        if each_word in spam_main_no.keys():
            pNO *=spam_main_no[each_word]
        else:
            pNO *=1/noSpam['Kol-vo vhozhdenii']   #если слова нет в словаре
    pYES *=pA                                      #формула Байеса
    pNO *=pNotA                                    #формула Байеса
    print(pYES)
    print(pNO)
    if pYES > pNO:
        return('spam')
    else:
        return('nospam')

rez = classify('Порадуй своего питомца новым костюмом')
print(rez)
print(noSpam)
print(yesSpam)
