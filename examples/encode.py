def decode_me(text):
  key='a b c d e f g h i j k l m n o p q r s t u v w x y z'
  value='n o p q r s t u v w x y z a b c d e f g h i j k l m'
  decoder = dict(zip(key.split(), value.split()))
  encoded_text = ''
  for c in text:
    if c.lower() in decoder:
        encoded_char = decoder[c.lower()]
        if c.islower():
            encoded_text += encoded_char
        else:
            encoded_text += encoded_char.upper()
    else:
        encoded_text += c

  print (encoded_text)


text="I am cool 123"
decode_me(text)
