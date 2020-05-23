import random

var_list = ['a','b']
exp_list = ['a+b','b-a', 'b//a']
sign = ['+','-','/','*','//']
sign2 = ['>','<','==','>=','<=','!=']
a = 3
b = 2
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

def or_and(det1,det2):
    det1,det2,sol = make_solution(det1,det2)
    if sol==-1:
        return('and')
    elif sol==1:
        return('or')
    else:
        return('')

def if_sub(exp_list, var_list, sign):
    sub_str = ''
    sol = 9
    det1 = 0.5
    det2 = 0.5
    choice_list = [exp_list, var_list]
    flag = 0
    while sol!=0:
        det1,det2,sol = make_solution(det1,det2)
        sub_str+='(('+rand(rand(choice_list))+')'+rand(sign2)+'('+rand(rand(choice_list))+'))'
        if flag == 1 and sol==1:
            sub_str+=')'
            flag=0
        or_and_exp = or_and(det1,det2)
        if len(or_and_exp):
            sub_str+=or_and_exp
        else:
            break
        det1,det2,sol2 = make_solution(det1,det2)
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

def action_str_gen(choice_list, offset_koeff):
    det1 = 0.5
    det2 = 0.5
    sol = 9
    curr_offset = ' '*offset_koeff
    act_str = ''
    while sol!=0:
        act_str+= curr_offset+rand(rand(choice_list[1]))+'='+rand(rand(choice_list))+'\n'
        det1,det2,sol = make_solution(det1,det2)
    return(act_str)

def elif_else(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag):
    det1=0.5
    det2 = 0.5
    ee_str = ''
    if ee_string=='else':
        ee_str += ' '*offset_koeff+ee_string + ':\n'
    elif ee_string=='elif':
        ee_str += ' '*offset_koeff+ee_string+' '+if_sub(exp_list, var_list, sign) + ':\n'
    det1,det2,sol = make_solution(det1,det2)
    if sol!=0:
        det1,det2,sol2=make_solution(det1,det2)
        if sol2!=0:
            ee_str+=action_str_gen(choice_list,offset_koeff+3)
        else:
            ee_str+=' '*(offset_koeff+3)+'None\n'
        return(ee_str, offset_koeff,  else_flag, fin_else_flag)
    else:
        
        if_str, offset_koeff, else_flag, fin_else_flag = if_gen(exp_list, var_list, if_str, offset_koeff+3, else_flag, fin_else_flag)                 # рекурсия
        
        ee_str+=if_str
        return(ee_str, offset_koeff,  else_flag, fin_else_flag)


def elif_else_block(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag):
    det1 = 0.5
    det2 = 0.5
    if ee_string=='elif':
        sol3 = 9
        wall_offset = offset_koeff
        while sol3!=0 and fin_else_flag!=1:
            temp_str, offset_koeff, else_flag, fin_else_flag=elif_else('elif', wall_offset, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag)
            if_str+=temp_str
            det1,det2,sol3 = make_solution(det1,det2)
        
        det1,det2,sol=make_solution(det1,det2)
        if sol!=0:
            fin_else_flag=1
            temp_str,offset_koeff, else_flag, fin_else_flag=elif_else('else', wall_offset, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag)
            if_str+=temp_str
        return(if_str,offset_koeff, else_flag, fin_else_flag)
    
    elif ee_string=='else':
          
          temp_str,offset_koeff, else_flag, fin_else_flag=elif_else('else', offset_koeff, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag)
          if_str+=temp_str
          return(if_str, offset_koeff, else_flag, fin_else_flag)
    else:
           action_str = action_str_gen(choice_list, offset_koeff+3)
           return(if_str+action_str, offset_koeff, else_flag,fin_else_flag)

def if_gen(exp_list, var_list, if_str, offset_koeff, else_flag, fin_else_flag):
    det1 = 0.5
    det2 = 0.5
    choice_list = [exp_list, var_list]
    det1,det2,sol = make_solution(det1,det2)
    action_str = ''
    base_offset = ' '
    if sol == 0:                                                                        # if + блок действия
        action_str = action_str_gen(choice_list, offset_koeff+3)                        # генерим блок действия со смещением+3
        return(base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign) +':\n' + action_str, offset_koeff, else_flag, fin_else_flag)                          # законченное ветвление

    elif sol == -1:                                                                     # if + elif/else
        if_str= base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign) +':\n' + action_str_gen(choice_list, offset_koeff+3)
        if fin_else_flag==0:
            det1,det2,sol2=make_solution(det1,det2)
            if sol2!=0:
                ee_string='elif'
            else:
                ee_string='else'
            if_str, offset_koeff, else_flag, fin_else_flag = elif_else_block(ee_string, offset_koeff, exp_list, var_list, sign, if_str, choice_list, else_flag, fin_else_flag)
        return(if_str, offset_koeff, else_flag, fin_else_flag)
    
    else:
            
            if_str= base_offset*offset_koeff+'if '+ if_sub(exp_list,var_list, sign) +':\n'
            det1,det2,sol = make_solution(det1,det2)
            if sol==0:
                if_str+=action_str_gen(choice_list, offset_koeff+3)
            wall_offset = offset_koeff
            if_rek, offset_koeff, else_flag, fin_else_flag = if_gen(exp_list, var_list, if_str, offset_koeff+3, else_flag, fin_else_flag)
            if_str+=if_rek
           
            
            det1,det2,sol2=make_solution(det1,det2)
            if sol2!=0:
                det1,det2,sol3=make_solution(det1,det2)
                if sol3!=0:
                    ee_string='elif'
                else:
                    ee_string='else'
                if_str, offset_koeff, else_flag, fin_else_flag = elif_else_block(ee_string, wall_offset, exp_list, var_list, sign, if_str, choice_list, 0, fin_else_flag)  
            else:
                if_str+=action_str_gen(choice_list, offset_koeff+3)
            return(if_str, offset_koeff, else_flag,fin_else_flag)
          
          
        
while True:
     if_str = ''
     if_str, offset_koeff, else_flag,fin_else_flag = if_gen(exp_list, var_list, if_str, 0,0,0)
     try:
         exec(compile(if_str,'fuck','exec'))
         print(if_str)
         input()
         
     except ZeroDivisionError:
         None
     except:
         print('error')
         print(if_str)
         input()
     
