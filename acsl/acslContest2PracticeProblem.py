common_string_result = []
result = ""
def common_string(string1, string2):
    common_string = ""
    string1 = list(string1)
    string2 = list(string2)
    for char in string1:
        if char in string2:
            common_string = common_string + char
            index = string2.index(char)
            string2 = string2[index + 1:]
    return common_string


common_string_result.append(common_string("friends", "afraid"))
common_string_result.append(common_string("afraid", "friends"))
common_string_result.append(common_string("sdneirf", "diarfa"))
common_string_result.append(common_string("diarfa", "sdneirf"))
shortest_string = min(common_string_result, key=len)
for char in shortest_string:
    for string in common_string_result:
        if char not in string:
            break
        else:
            result = result + char

result = set(list(result))
result = list(result)
result.sort()
if len(result) != 0:
    print("".join(result))
else:
    print("NONE")

