def any_is_empty(*strings:str):
    for i in strings:
        if len(i) < 2:
            return True
    return False