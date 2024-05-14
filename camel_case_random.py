import random
import string

def generate_camel_case_string(length):
    # Generate a random string of lowercase letters
    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
    
    # Capitalize the first letter
    camel_case_string = random_string[0].upper() + random_string[1:]
    
    # Randomly capitalize some letters
    for i in range(1, len(camel_case_string)):
        if random.randint(0, 3) == 0:  # 25% chance of capitalizing a letter
            camel_case_string = camel_case_string[:i] + camel_case_string[i].upper() + camel_case_string[i+1:]
    
    return camel_case_string

mypass=generate_camel_case_string(10)
print(mypass)
