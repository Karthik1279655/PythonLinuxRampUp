def validate_email(email):
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.compile(pattern)
    return re.match(match, email) is not None


print(validate_email('karthikem832@gmail.com'))
