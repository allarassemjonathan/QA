import pandas as pd
df = pd.read_csv('csvData.csv')
abrs = df.Code.values.tolist()
f = open('dirtytxt.txt', encoding='utf-8')
out = open('cleantxt.txt','x', encoding='utf-8')
classes = {'FF', 'SO', 'JR', 'SR', 'UN'}
s = ''
second = False
third = False
fourth = False
fifth = False
sixth = False
seventh = False
u = 0
for line in f.readlines():
    arr = line.split()
    i = 0
    while i < len(arr):
        if arr[i] in classes:
            s = s + '\t\t' + arr[i]
            second = True
        elif second ==True:
            s = s + '\t\t' + arr[i] + arr[i+1]
            i = i+1
            third = True
            second = False
        elif third == True:
            s = s + '\t\t' + arr[i]
            third = False
            fourth = True
        elif fourth == True:
            s = s + '\t\t' + arr[i]
            fourth = False
            fifth = True
        elif fifth == True:
            s = s + '\t\t' + arr[i]
            fifth = False
            sixth = True
        elif sixth ==True:
            s = s + '\t\t' + arr[i]
            sixth = False
            seventh = True
        elif seventh ==True:
            s = s + '\t\t' + arr[i]
            seventh =False
            #print(s)
        else:
            s = s + ' ' + arr[i]
        i = i + 1

    out.write(s + '\n')
    s = ''

out.close()

