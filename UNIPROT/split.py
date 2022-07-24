def split():
    file = open("uniprot_sprot.dat", "r")
    line = file.readline().replace("\n", "")
    i = 1
    j = 0
    f = open("proteins.txt", "w")
    while line:
        if line[0:2] == "AC":
            j += 1
            interactor = line[5:len(line) - 1].split(";")[0]
            f.write(interactor + "\n")
        line = file.readline().replace("\n", "")
    print(j)

split()
            
        