from re import fullmatch
 
def is_valid_mail(email):
    return fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)
 