import os 
from tqdm import tqdm
g = os.walk("/home/lxy/chemistry/pubChem/descriptor/compound")  

source = []
for path,dir_list,file_list in g:  
    for file_name in file_list:
        source.append(os.path.join(path, file_name))
    
    for dir_name in dir_list:
        dir = os.path.join(path, dir_name)
        temp = os.walk(dir)
        for p, d_list, f_list in temp:  
            for file_name in f_list:
                source.append(os.path.join(p, file_name))
source.sort()
print(source[0])
temp = set()
for s in tqdm(source):
    if s not in temp:
        temp.add(s)
    else:
        continue
    if s.find(".ttl.gz") != -1:
        os.system('gzip -dk {}'.format(s)) 
