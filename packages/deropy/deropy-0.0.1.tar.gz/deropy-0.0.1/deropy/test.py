short_string = 'hello world!'
long_string = '''Function Initialize(metadataFormat String, metadata String, freezeMetadata Uint64) Uint64
1 IF EXISTS("owner") == 1 THEN GOTO 11
2 STORE("owner", SIGNER())
3 STORE("originalOwner", SIGNER())
4 STORE("type", "G45-C")
5 STORE("frozenAssets", 0)
6 STORE("frozenMetadata", freezeMetadata)
7 STORE("metadataFormat", metadataFormat)
8 STORE("metadata", metadata)
9 STORE("timestamp", BLOCK_TIMESTAMP())
10 RETURN 0
11 RETURN 1
End Function

Function Freeze(assets Uint64, metadata Uint64) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 7
2 IF assets == 0 THEN GOTO 4
3 STORE("frozenAssets", 1)
4 IF metadata == 0 THEN GOTO 6
5 STORE("frozenMetadata", 1)
6 RETURN 0
7 RETURN 1
End Function

Function SetAssets(index Uint64, assets String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 5
2 IF LOAD("frozenAssets") >= 1 THEN GOTO 5
3 STORE("assets_" + index, assets)
4 RETURN 0
5 RETURN 1
End Function

Function DelAssets(index Uint64) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 5
2 IF LOAD("frozenAssets") >= 1 THEN GOTO 5
3 DELETE("assets_" + index)
4 RETURN 0
5 RETURN 1
End Function

Function SetMetadata(format String, metadata String) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 6
2 IF LOAD("frozenMetadata") >= 1 THEN GOTO 6
3 STORE("metadataFormat", format)
4 STORE("metadata", metadata)
5 RETURN 0
6 RETURN 1
End Function

Function TransferOwnership(newOwner string) Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 4
2 STORE("tempOwner", ADDRESS_RAW(newOwner))
3 RETURN 0
4 RETURN 1
End Function

Function CancelTransferOwnership() Uint64
1 IF LOAD("owner") != SIGNER() THEN GOTO 4
2 DELETE("tempOwner")
3 RETURN 0
4 RETURN 1
End Function

Function ClaimOwnership() Uint64
1 IF LOAD("tempOwner") != SIGNER() THEN GOTO 5
2 STORE("owner", SIGNER())
3 DELETE("tempOwner")
4 RETURN 0
5 RETURN 1
End Function
'''

def base64_vocabulary(s: str):
    keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    next_key = 0
    second_key = 0
    d = dict()

    # loop through all the word of the string s
    for word in s.split():
        # if the word is not in the dictionary, add it
        if word not in d:
            d[word] = keys[next_key]
            next_key += 1

            if next_key == len(keys):
                next_key = 0
                second_key += 1

                if second_key == len(keys):
                    raise ValueError('The vocabulary is too small')
    
    # Create a new string with the encoded words
    encoded = ''
    for word in s.split():
        encoded += d[word]

    return d, encoded

def convert_dict_to_base64(d: dict):
    str_output=''
    for k, v in d.items():
        str_output += f'{k}:{v},'
    return str_output

def print_stats(s: str):
    vocabulary, encoded = base64_vocabulary(s)
    print('------------------------')
    print(f'Original string length: {len(s)}')
    print(f'Encoded string length: {len(encoded)}')
    print('Vocabulary string length:', len(convert_dict_to_base64(vocabulary)))
    print(f'{convert_dict_to_base64(vocabulary)[:40]} ...')

    print(f'new total length: {len(encoded) + len(convert_dict_to_base64(vocabulary))}')
    
print_stats(short_string)
print_stats(long_string)