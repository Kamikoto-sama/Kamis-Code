h = int(input("Hours:"))
m = int(input("Minutes:"))

angle = abs(h * 30 + (1/60*m) - m * 6)
if  angle > 180:angle = 360 - angle

print(angle)