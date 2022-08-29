import re
import sys
import itertools

sig_dict = ['+', '-']
num_list = []
sig_list = []

formula_raw = sys.argv[1]
formula = formula_raw.strip()
form = re.sub(r'(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', formula)


numbers = re.findall(r'[0-9]+', form)
sigs = re.findall(r'[+-]+', form)
num_sig  = re.split(r'(\D)', form)
if '' in num_sig:
    num_sig.remove('')
if ' ' in num_sig:
    num_sig.remove(' ')


def check_first(list):
    if list[0] in sig_dict:
        raise Exception("Primeiro valor tem sinal")
    else:
        num_list = list[::2]
        sig_list = list[1::2]
        return sig_list, num_list

def check_syntax(num_list, sig_list):
    if len(num_list) != len(sig_list) + 1:
        raise Exception("Existem elementos faltando")
    if len(sig_list) == 0:
        raise Exception("A formula nao contem sinais")
    if len(num_list) == 0:
        raise Exception("A formula nao contem numeros")

sig_list, num_list = check_first(num_sig)

if '' in num_list:
    num_list.remove('')
if ' ' in num_list:
    num_list.remove(' ')

if '' in sig_list:
    sig_list.remove('')
if ' ' in sig_list:
    sig_list.remove(' ')


check_syntax(num_list, sig_list)
res = 0
minus = False

#print(sig, num)

for num, sig in itertools.zip_longest(num_list, sig_list):
    #print(num_list)
    #print(sig_list)
    if num == ' ' or num == '':
        pass
    #print(f"num: {num}")
    num = int(num)
    if minus == True:
        res -= num
    elif minus == False: 
        res += num
    if sig == '-':
        minus = True
    if sig == '+':
        minus = False
    if sig is None:
        minus = False

print(res)

