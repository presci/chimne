

def percentencode(val):
    str0 = ""
    for i in val:
        val0 = ord(i)
        if 48 <= val0 <= 57:
            str0 += i
        elif 65 <= val0 <= 90:
            str0 +=i
        elif 97 <= val0 <= 122:
            str0 += i
        elif val0 == 45 or val0 == 95 or val0 == 46 or val0 == 126:
            str0 += i
        elif val0 == 10:
            str0 += "%0d%0a"
        else:
            str0 += "%" + ((str(hex(val0)))[-2:]).upper()
    return str0

