# the code for analysis of input string
# the basic format should be:
#   a single word should not have a space in it
#   Functional operation, i.e. func(xxx), should be input like:
#                           "func(xxx)"
#   operations except these: ["<", ">", ">=", "<=", "=", "+", "-", "*", "/", ".", "(", ")"]
#       should be separated by a space
#   all functional operation are stored in bracket.json

import json
import unicodedata
from stack import Stack

with open("./priority.json", 'r', encoding='UTF-8') as f:
# with open("./priority.json", 'r', encoding='UTF-8') as f:
    priority = json.load(f)
    f.close()

with open("./bracket.json", 'r', encoding='UTF-8') as f:
# with open("./bracket.json", 'r', encoding='UTF-8') as f:
    bracket = json.load(f)
    methods = bracket.copy()
    methods.remove("(")
    f.close()

algebra_operations = ["<", ">", ">=", "<=", "=", "+", "-", "*", "/", ".", "(", ")"]
list_symbols = ["[", "]", ","]
def pre_processing(string):
    for i in algebra_operations+list_symbols:
        string = string.replace(i, " " + i + " ")
    return string


# determine whether a string s is a string of a number
def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def detect_input_lists(request):
    # eg. ["a", "in", "[", "a", "b", "]"]
    start = 0
    end_index = len(request)-1
    while start <= end_index:
        if request[start] != "[":
            start += 1
        else:
            break
    if start >= end_index:
        return request
    # detect a list?
    stop = start+1
    while stop <= end_index:
        if request[stop] != "]":
            stop += 1
        else:
            break
    if stop > end_index:
        return request
    temp = ''
    for i in range(start, stop+1):
        temp += request[i]
    temp = eval(temp)
    request = request[0:start] + request[stop+1:len(request)]
    request.insert(start, temp)
    return request

def segment(query):
    # get the request from terminal, split it and put parts into a list
    flag = 0
    query = pre_processing(query)
    # print(query)
    request = query.split()
    # result of semantic: a operation sequence
    request = detect_input_lists(request)
    seq = []
    # stack used to analysis
    stk = Stack()
    for w in request:
        # print(w)
        # operator in bracket would be pushed until meet a ")"
        if w in bracket:
            if w in methods:
                flag = 1
                stk.push(w)
            else:
                if stk.peek() in methods and w == "(" and flag == 1:
                    flag = 0
                    continue
                stk.push(w)
        # if w is a number (could be int or float)
        else:
            flag = 0
            if is_number(w):
                seq.append(float(w))
            # compare the priority of w and operator on the top of the stack
            elif type(w) is list:
                seq.append(w)
            elif w in priority:
                top = stk.peek()
                # if the priority of w is not bigger than the top
                # pop the top into result until priority of w is bigger than top
                while top is not None and priority[w] <= priority[top]:
                    seq.append(stk.pop())
                    top = stk.peek()
                stk.push(w)
            # meet a ")", continue popping until meet operator in bracket
            elif w == ")":
                top = stk.peek()
                while top is not None and top not in bracket:
                    # print(top)
                    seq.append(stk.pop())
                    top = stk.peek()
                # assert(stk.peek() != "(")
                # ignore "("
                if top != "(":
                    seq.append(stk.pop())
            # append the external name
            else:
                seq.append(w)
        # request end
        # append remain operator
    while stk.peek() is not None:
        # ignore "("
        if stk.peek() != "(":
            seq.append(stk.pop())
        else:
            stk.pop()
    # print(seq)
    return seq


if __name__ == "__main__":
    a = "PERFORMANCE where(&cinema = Flora)"
    # this is one query which should result in few id numbers in stack
    print(segment(a))
    a = "deref(deref(PERFORMANCE where(&cinema = Flora)))"
    print(segment(a))
    a = "(PERFORMANCE x THEATRE) where(&cinema = &title)"
    print(segment(a))
    a = "PERFORMANCE where(&cinema = Flora) In [9,10]"
    print(segment(a))
    a = "PLACE where(PERFORMANCE where (&cinema = Flora) In [9,10])"
    print(segment(a))
