import bcrypt

preach = "ihateyou"
preach = preach.encode('utf-8')
print(isinstance(preach, bytes))
print("Hello world")

new = "Whatis893happeing"
password = bcrypt.hashpw(new.encode('utf-8'), bcrypt.gensalt())
print(password)
print(password.decode('utf-8'))
password = str(password)
print(password.encode('utf-8'))