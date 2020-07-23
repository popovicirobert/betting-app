
def reduce_string(bad_string):
    """Aici trebuie facut ceva mai destept"""
    good_string = bad_string.strip(' \n\r')
    good_string = good_string.replace('.', '')

    lower_string = good_string.lower()
    string_list = lower_string.split(' ')

    answer = ''
    for string in string_list:
        if len(string) > 2:
            answer += string
    
    return answer

if __name__ == '__main__':
    print(reduce_string('E. Sdf'))
