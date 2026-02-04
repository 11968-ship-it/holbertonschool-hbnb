import bcrypt

# Hash the password 'admin1234'
password = "admin1234"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print("Hashed password for admin:")
print(hashed.decode('utf-8'))
