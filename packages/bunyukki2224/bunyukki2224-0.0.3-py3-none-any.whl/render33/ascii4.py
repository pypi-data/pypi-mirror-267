import pandas as pd

def kdh(inar):
    if len(inar) != 1:
        return pd.DataFrame({"Message": ["하나의 문자를 입력해주세요.", "문자열의 번역을 원하시면 2를 선택해주세요."]})
    else:
        ascii_code = ord(inar)
        return pd.DataFrame({"문자": [inar], "아스키코드": [ascii_code]})

def qwer(input_string):
    ascii_list = [ord(char) for char in input_string]
    if (1):
        pass
    else:
        return pd.DataFrame({"Message": ["잘못된 입력입니다. 다시 입력해주세요."]})
    
    return pd.DataFrame({"문자": list(input_string), "아스키코드": ascii_list})
