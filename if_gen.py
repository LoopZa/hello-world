import random


def make_solution(p_random, p_deter):                       # функция принятия решения на развилке
    deter_flag = 0
    random_flag = 0
    if p_random >= random.random():
            p_random-=0.01                                  # изменение приоритета
            p_deter+=0.01
            random_flag = 1
    if p_deter >= random.random():
            p_deter-=0.01                                   # баланс приоритета
            p_random+=0.01
            deter_flag = 1
    if random_flag == 1 and deter_flag == 0:
        return(p_random, p_deter, 1)
    elif deter_flag == 1 and random_flag == 0:
        return(p_random, p_deter, -1)
    else:
        return (p_random, p_deter,0)

def rand(t_list):
    return(t_list[random.randint(0,len(t_list)-1)])

def or_and(prob_list):
    prob_list[8],prob_list[9],sol = make_solution(prob_list[8],prob_list[9])
    if sol==-1:
        return('and')
    elif sol==1:
        return('or')
    else:
        return('')

def if_sub(exp_list, var_list, sign, prob_list):
    sub_str = ''
    sol = 9
    choice_list = [exp_list, var_list]
    flag = 0
    while sol!=0:
        prob_list[6],prob_list[7],sol = make_solution(prob_list[6],prob_list[7])
        sub_str+='(('+rand(rand(choice_list))+')'+rand(sign2)+'('+rand(rand(choice_list))+'))'
        if flag == 1 and sol==1:
            sub_str+=')'
            flag=0
        or_and_exp = or_and(prob_list)
        if len(or_and_exp):
            sub_str+=or_and_exp
        else:
            break
        prob_list[6],prob_list[7],sol2 = make_solution(prob_list[6],prob_list[7])
        if sol2 == 1 and (sub_str[-1]=='D' or sub_str[-1]=='R') and flag == 0:
            sub_str+='('
            flag = 1
    
    if sub_str[-1] == '(':
        if sub_str[-2]=='d':
           sub_str=sub_str[0:-4]
        elif sub_str[-2]=='r':
             sub_str=sub_str[0:-3]
        else:
            sub_str=sub_str[0:-1]
    elif sub_str[-1]=='d':
         sub_str=sub_str[0:-3]
    elif sub_str[-1]=='r':
         sub_str=sub_str[0:-2]
    else:
         None
    if flag == 1:
        sub_str+=')'
        return(sub_str)
    else:
        return(sub_str)

def action_str_gen(choice_list, offset_koeff, prob_list):
    sol = 9
    curr_offset = ' '*offset_koeff
    act_str = ''
    while sol!=0:
        act_str+= curr_offset+rand(rand(choice_list[1]))+'='+rand(rand(choice_list))+'\n'
        prob_list[6],prob_list[7],sol = make_solution(prob_list[6],prob_list[7])
    return(act_str)

def elif_else(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list):
    ee_str = ''
    if ee_string=='else':
        ee_str += ' '*offset_koeff+ee_string + ':\n'
    elif ee_string=='elif':
        ee_str += ' '*offset_koeff+ee_string+' '+if_sub(exp_list, var_list, sign, prob_list) + ':\n'
    prob_list[2],prob_list[3],sol = make_solution(prob_list[2],prob_list[3])
    if sol!=0:
        prob_list[6],prob_list[7],sol2 = make_solution(prob_list[6],prob_list[7])
        if sol2!=0:
            ee_str+=action_str_gen(choice_list,offset_koeff+3, prob_list)
        else:
            ee_str+=' '*(offset_koeff+3)+'None\n'
        return(ee_str, offset_koeff, fin_else_flag, prob_list)
    else:
        prob_list[6],prob_list[7],sol2 = make_solution(prob_list[6],prob_list[7])
        if sol2==0:
            ee_str+=action_str_gen(choice_list,offset_koeff+3, prob_list)
        if_str, offset_koeff,  fin_else_flag, prob_list = if_gen(exp_list, var_list, if_str, offset_koeff+3, fin_else_flag, prob_list)                 # рекурсия
        
        ee_str+=if_str
        return(ee_str, offset_koeff, fin_else_flag, prob_list)


def elif_else_block(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list,  fin_else_flag, prob_list):
    if ee_string=='elif':
        sol3 = 9
        wall_offset = offset_koeff
        while sol3!=0 and fin_else_flag!=1:
            temp_str, offset_koeff, fin_else_flag, prob_list=elif_else('elif', wall_offset, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list)
            if_str+=temp_str
            prob_list[6],prob_list[7],sol3 = make_solution(prob_list[6],prob_list[7])
        
        prob_list[2],prob_list[3],sol = make_solution(prob_list[2],prob_list[3])
        if sol!=0:
            fin_else_flag=1
            temp_str,offset_koeff, fin_else_flag, prob_list=elif_else('else', wall_offset, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list)
            if_str+=temp_str
        return(if_str,offset_koeff, fin_else_flag, prob_list)
    
    else: 
          temp_str,offset_koeff, fin_else_flag, prob_list=elif_else('else', offset_koeff, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list)
          if_str+=temp_str
          return(if_str, offset_koeff, fin_else_flag, prob_list)
    

def if_gen(exp_list, var_list, if_str, offset_koeff, fin_else_flag, prob_list):             # главная функция генерации 
    choice_list = [exp_list, var_list]
    base_offset = ' '
    prob_list[0],prob_list[1],sol = make_solution(prob_list[0],prob_list[1])                # основная структурная развилка
    if sol == 0:                                                                            # if + блок действия (1 вариант в схеме)
        action_str = action_str_gen(choice_list, offset_koeff+3, prob_list)                 # генерим блок действия со смещением+3
        return(base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign, prob_list) +':\n' + action_str, offset_koeff, fin_else_flag, prob_list)            
    elif sol == -1:                                                                         # if + elif/else (2 вариант в схеме)
        if_str= base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign, prob_list) +':\n' + action_str_gen(choice_list, offset_koeff+3, prob_list) # if [..]:
        prob_list[2],prob_list[3],sol2=make_solution(prob_list[2],prob_list[3])             # развилка elif/else
        if sol2!=0:
            ee_string='elif'
        else:
             ee_string='else'
        if_str, offset_koeff, fin_else_flag, prob_list = elif_else_block(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list) # генерация блока elif/else
        return(if_str, offset_koeff, fin_else_flag, prob_list)
    
    else:                                                                                   # if + if(рекурсия) (3 вариант в схеме)
            if_str= base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign, prob_list) +':\n' # if [..]:
            prob_list[4],prob_list[5],sol = make_solution(prob_list[4],prob_list[5])        # развилка if/if+блок действия
            if sol==0:
                if_str+=action_str_gen(choice_list, offset_koeff+3, prob_list)              # генерим блок действия со смещением+3
            wall_offset = offset_koeff                                                      # сохраняем смещение
            if_rek, offset_koeff, fin_else_flag, prob_list = if_gen(exp_list, var_list, if_str, offset_koeff+3, fin_else_flag, prob_list) # рекурсия if+if
            if_str+=if_rek                                                                  # прицепляем сгенерированный рекурсивный кусок
            prob_list[4],prob_list[5],sol2=make_solution(prob_list[4],prob_list[5])         # развилка блок elif-else/блок действия
            if sol2!=0:
                prob_list[2],prob_list[3],sol3=make_solution(prob_list[2],prob_list[3])
                if sol3!=0:
                    ee_string='elif'
                else:
                    ee_string='else'
                if_str, offset_koeff, fin_else_flag, prob_list = elif_else_block(ee_string, wall_offset, exp_list, var_list, sign, if_str, choice_list, fin_else_flag, prob_list)  
            else:
                if_str+=action_str_gen(choice_list, offset_koeff+3, prob_list)              # генерим блок действия со смещением+3
            return(if_str, offset_koeff,fin_else_flag, prob_list)
          
var_list = ['a','b']
exp_list = ['a+b','b-a', 'b//a']
sign = ['+','-','/','*','//']
sign2 = ['>','<','==','>=','<=','!=']
a = 3
b = 2       
prob_list = [0.5 for y in range(0,10)]      
while True:
     if_str = ''
     if_str, offset_koeff, fin_else_flag, prob_list = if_gen(exp_list, var_list, if_str, 0,0, prob_list)
     try:
         exec(compile(if_str,'gen','exec'))
         print(if_str)
         input()
         
     except ZeroDivisionError:
         None
     except:
         print('error')
         print(if_str)
         input()
     
