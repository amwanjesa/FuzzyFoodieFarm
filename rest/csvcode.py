import csv

def readfile():
    data = []
    with open('world-food-facts\FoodFacts.csv') as file:
        for row in csv.reader(file):
            data.append(row)
    return data

def fatNsug():
    r = readfile()
#    print(r[8].index('Root bier'))
    proInd = r[0].index('product_name')
    catInd = r[0].index('categories')
#    print(proInd)
#    print(r[0][14])
    fatInd = r[0].index('fat_100g')
    satInd = r[0].index('saturated_fat_100g')
    sugInd = r[0].index('sugars_100g')
    for i in range(1,20):
        j = i
        prod = r[j][proInd]
        cat = r[j][catInd]
        fat = r[j][fatInd]
        sat = r[j][satInd]
        sug = r[j][sugInd]
        print(sat)
        if fat == '' and sat == '':
            fat = 0
            sat = 0
            fatPerc = 0
        else:
            fat = float(fat)
            # om de een of andere reden ziet hij 0.0 als een string waar hij geen float van kan maken
            # en ik heb geen idee waarom.
            if sat == '0.0':
                print('hoi')
                sat = 0
                sat = float(0)
            print(sat)
            sat = float(sat)
            sug = float(sug)
            if fat != 0:
                fatPerc = sat/fat
        if sug == '':
            sug = 0

            print(prod, cat, fatPerc, sug)
if __name__ == '__main__':
    fatNsug()
