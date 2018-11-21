with open("out.txt", "w") as ofile:
    with open("testCatSites.csv", "r") as ifile:
        for line in ifile:
            link = line.split(",")[0]
            link = link.replace(r'"', "")
            ofile.write(link+" ")