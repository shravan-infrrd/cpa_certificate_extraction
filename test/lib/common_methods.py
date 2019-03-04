
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def remove_extra_spaces( line ):
    words = line.split('  ')
    valid_words = list( filter( None, words ) )
    print("RemoveExtraSpaces---->", valid_words)
    return valid_words

def validate_line(content, keyword):
    words = content.split(keyword)
    #print(f"CommonMEthod2---->{words}--->{keyword}")
    if len(words) == 1:
        return None
    valid_words = remove_extra_spaces( words[1].strip() )
    if len(valid_words) == 0:
        return None
    return valid_words
