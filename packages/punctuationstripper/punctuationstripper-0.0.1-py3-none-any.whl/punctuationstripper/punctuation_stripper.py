import string

def stripper(text: str, punct: str = None):
    '''
    @param file_name: File to strip
    @param punct: OPTIONAL: Punctuation you DONT want stripped
    @returns: Text
    If calling via package use this function, returns new text
    '''
    # Get the punctuation to be stripped
    if not punct:
        punct = ''
    punctuation = ''.join([x for x in string.punctuation if x not in punct])

    return text.translate(str.maketrans('', '', punctuation))

def strip_and_save(file_name: str, punct: str = None, new_file_name: str = None) -> str:
    '''
    @param file_name: File to strip
    @param punct: OPTIONAL: Punctuation you DONT want stripped
    @new_file_name: OPTIONAL: New file name to be saved as

    @returns: Text
    Returns new text: strips a file of pucntuation and then saves the new file as new_file_name
    '''
    # Read in file and strip punctuation
    with open(file_name, 'r') as f:
        s = stripper(f.read(), punct)

    # Save file without specified punctuation to new file
    newfilename = new_file_name or f'{file_name}_new.txt'
    with open(newfilename, 'w') as f:
        f.write(s)
    return s

def main(file_name: str, punct: str = None, new_file_name: str = None) -> None:
    '''
    @param filename: File to strip
    @param punct: OPTIONAL: Punctuation you DONT want stripped

    @returns: None
    Called via CLI; See stripper for detailed description
    '''
    strip_and_save(file_name, punct, new_file_name)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Strip a file of punctuation.")

    # Required positional argument
    parser.add_argument('-f', '--filename', type=str,
                        help='File to strip. Useage: punctuation_stripper.py -f <filename> [-n <newfilename>] [-p <punct>]')

    # Optional arguments
    parser.add_argument('-n', '--newfilename', type=str,
                        help='New file to save to; will be created, make sure another file doesn\'t exist with the same name. If NONE is supplied new file x_new.txt')
    
    parser.add_argument('-p', '--punct', type=str,
                        help="OPTIONAL: Punctuation you DONT want stripped. Should be string with no spaces e.g. '.,-'")
    
    args = parser.parse_args()
    main(args.filename, args.punct)

