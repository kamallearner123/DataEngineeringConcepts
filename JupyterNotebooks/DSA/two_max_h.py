a = [10,20,30,30,40,15,17]
max_val = 0
res_i,res_j = 0,0

for i in range(len(a)-1):
    for j in range(i+1,len(a)):
        if max_val < min(a[i], a[j])*(j-i):
            max_val = min(a[i], a[j])*(j-i)
            res_i, res_j = i,j
            print(i,j,max_val)
print(res_i,res_j,max_val)
