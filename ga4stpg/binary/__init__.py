from random import choices

def random_binary(length):
    return ''.join(choices(['0', '1'], k=length))
