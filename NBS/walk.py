import os 

g = os.walk("/home/lxy/NBS")  

source = []
for path,dir_list,file_list in g:  
    for file_name in file_list:
        source.append(os.path.join(path, file_name))
    
    for dir_name in dir_list:
        dir = os.path.join(path, dir_name)
        temp = os.walk(dir)
        for p, d_list, f_list in temp:  
            # print(p)
            # print(d_list)
            # print(f_list)
            for file_name in f_list:
                source.append(os.path.join(p, file_name))
print(source)
ls =set()
for s in source:
    if s.find(".py") == -1:
        # s = s.replace('(', '\\(').replace(')', '\\)')
        if s.find("(") != -1 or s.find(")") != -1:
            ls.append(s)
            continue
        target = "/home/lxy/NBS/data/" + s.replace("/home/lxy/NBS/", "").replace("/", "_").replace("(", "\\(").replace(")", "\\)")
        print(target)
        os.system('cp {} {}'.format(s, target))
        # break
file = open("含括号文件.txt", "w", encoding="utf-8")
for item in ls:
    file.write(item + "\n")   
file.close()

    

            
          
    