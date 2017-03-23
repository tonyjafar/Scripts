import random


def generate_passwords():
    x = []
    charsetlower = 'abcdefghijklmnopqrstuvwxyz'
    charsetupper = 'ABCDEFGHIJKLMNOPQRSTUWXYZ'
    digitset = '1234567890'
    minlength = 4
    diglength = 2
    pass1 = ''.join(map(lambda unused: random.choice(charsetlower),
                        range(minlength)))
    pass2 = ''.join(map(lambda unused: random.choice(charsetupper),
                        range(minlength)))
    pass3 = ''.join(map(lambda unused: random.choice(digitset),
                        range(diglength)))
    full_pass = pass1 + pass2 + pass3

    for i in full_pass:
        x.append(i)
    new = random.sample(x, 10)
    new_pass = ''.join(new)

    return new_pass

psw = generate_passwords()

print(psw)
