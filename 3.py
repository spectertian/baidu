import  hashlib

def md5Value(value):
    m = hashlib.md5()
    m.update(value)
    sign = m.hexdigest()

a = md5Value('22')