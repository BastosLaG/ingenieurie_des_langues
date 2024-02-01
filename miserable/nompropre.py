import string

a1 = list(string.ascii_lowercase) + list(string.ascii_uppercase)
print( a1 )

liste_bruit_debu = []
liste_bruit_mili = []
liste_res = {}

current = ''
count = 0

for i in range(1, 4):
    with open("miserable_vol"+str(i), 'r') as reader:
        txt = reader.read()
        liste_bruit_debu = txt.split(". ")
        liste_bruit_mili = txt.split()

# for elem in liste_bruit_debu:
#     if elem.istitle():
#         for letter in elem:
#             if letter in a1:
#                 current += letter
        
#         if current in liste_res:
#             liste_res[current] += 1
#             current = ''
#         else:
#             liste_res[current] = 1
#             current = ''

# for elem in liste_bruit_mili:
#     if elem.istitle():
#         for letter in elem:
#             if letter in a1:
#                 current += letter
#         if current in liste_res:
#             liste_res[current] += 1
#             current = ''
#         else:
#             liste_res[current] = 1
#             current = ''

for elem in liste_bruit_debu:
    if elem.istitle():
        if elem in liste_res:
            liste_res[elem] += 1
        else:
            liste_res[elem] = 1

for elem in liste_bruit_mili:
    if elem.istitle():
        if elem in liste_res:
            liste_res[elem] += 1
            elem = ''
        else:
            liste_res[elem] = 1
            elem = ''


for elem in liste_res:
    print(elem + " " + str(liste_res[elem]))
    count += 1

print("count: " + str(count))

