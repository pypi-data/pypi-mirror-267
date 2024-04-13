def kdh(inar):  # 문자
    
    if len(inar) != 1:
        print("\n하나의 문자를 입력해주세요.\n문자열의 번역을 원하시면 2를 선택해주세요.")
    else:
        ascii_code = ord(inar)
       
        return inar, ascii_code

def qwer(input_string):
 
    ascii_list = [ord(char) for char in input_string]
   
    if (1):
        pass
    else: print("잘못된 입력입니다. 다시 입력해주세요.")

    return input_string, ascii_list
