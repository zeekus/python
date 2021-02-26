#python one lines
#create a SHA512 password from clear text
#source: https://serverfault.com/questions/330069/how-to-create-an-sha-512-hashed-password-for-shadow
python3 -c "import crypt;print(crypt.crypt(input('clear-text pw: '), crypt.mksalt(crypt.METHOD_SHA512)))"

