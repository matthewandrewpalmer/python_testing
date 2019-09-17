from pip._vendor.distlib.compat import raw_input

input = raw_input("Why are you here?\n")
print(" %s , Is an odd reason" % input)

if input == "?":
    print("Also a ? is not even text")

i = 0
while i <= 10:
    print(i)
    i += 1
