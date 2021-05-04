# major 2ASM machine

import semanticAnalysis as semantic
from database import DataBase
from stack import Stack
# import pysnooper

class ASMachine:
    def __init__(self, dataFile, queryFile):
        self.database = DataBase(ASMachine.read(dataFile))
        self.queryList = self.read(queryFile)
        self.RES = Stack()
        self.ENV = Stack()
        self.Lists = list(self.database.roots[0].keys())
        self.properties = list(self.database.roots[1].keys())
        self.deref_properties = self.properties.copy()
        for i in range(len(self.deref_properties)):
            self.deref_properties[i] = "&" + self.deref_properties[i]
        print(self.deref_properties)
        self.init_env()
        self.functions = self.function_init()
        self.function_names = list(self.functions.keys())
        print("Initialized\n")

    def init_env(self):
        tmp = self.database.find_roots("all")
        print("the initial ENV contains: ", tmp)
        self.ENV.push(tmp)

    def function_init(self):
        return {
            "<": self.smaller,
            ">": self.greater,
            "<=": self.smaller_equal,
            ">=": self.greater_equal,
            "=": self.eq,
            "neq": self.neq,
            "+": self.add,
            "-": self.minus,
            "*": self.multiply,
            "/": self.division,
            ".": self.projection,
            "x": self.cartesian,
            "count": self.count,
            "min": self.min,
            "max": self.max,
            "deref": self.deref,
            "In": self.In,
            "distinct": self.distinct,
            "eqjoin": self.equijoin
        }

    # database or queryList init
    @staticmethod
    def read(file):
        content = []
        print("Reading data...")
        with open(file, "r") as f:
            for i in f.readlines():
                content.append(eval(i.strip()))
            f.close()
        return content

    # do the evaluation
    # call semanticAnalysis.segment(query) at the beginning
    # @pysnooper.snoop()
    def evaluate(self, query):
        # @pysnooper.snoop()
        def __execute(self, commands):
            print("\n########")
            self.RES.show()
            print("########\n")
            global return_commands
            # check the command list
            try:
                command = commands.pop(0)
            except IndexError:
                return None
            if command in self.Lists:
                # push id numbers into RES
                self.find_lists(command)
                return __execute(self, commands.copy())
            elif command in self.deref_properties:
                command = command[1:]
                assert (self.RES.isempty() is False)
                result_ids = []
                # loop over the id numbers of list headers
                for cur in self.RES.pop():
                    if type(cur) is list:
                        raise Exception("Invalid Syntax")
                    succeed = 0
                    self.search_in_lists(cur)
                    assert (self.ENV.isempty() is False)
                    attributes = self.ENV.pop()
                    for attribute in attributes:
                        search_ans = self.database.search(attribute)
                        if search_ans[0] == command:
                            # match the attribute
                            self.RES.push([attribute])
                            self.deref()
                            succeed = 1
                            break
                    if not succeed:
                        continue
                    # then recursively use the __execute
                    parameters = __execute(self, commands.copy())
                    bool_val = parameters[0]
                    return_commands = parameters[1]
                    assert(type(bool_val) is bool)
                    if bool_val:
                        # if True
                        result_ids.append(cur)
                self.RES.push(result_ids)
                # update command list
                commands = return_commands
                # recursion
                return __execute(self, commands)
            elif command in self.function_names:
                # detect build in functions
                self.functions[command]()
                return __execute(self, commands)
            elif type(command) is list:
                # special input like lists
                self.RES.push(command)
                return __execute(self, commands)
            elif semantic.is_number(command):
                # special input like digits
                self.RES.push([command])
                return __execute(self, commands)
            elif command == "where":
                assert(self.RES.isempty() is False)
                bool_val = self.RES.pop()[0]
                return [bool_val, commands]
            else:
                # plain text input
                assert(type(command) is str)
                self.RES.push([command])
                return __execute(self, commands)

        commands = semantic.segment(query)
        # print(commands)
        __execute(self, commands)
        assert(self.RES.isempty() is False)
        final_result = self.RES.pop()
        self.clear_res()
        return final_result

    # output
    def output(self):
        result = []
        for query in self.queryList:
            # iterate through all the results
            result.append(self.evaluate(query))
        for i in result:
            print(i)
        return

    def control(self):
        cmd = input("please input commands: ").strip()
        while True:
            if cmd == ':h':
                msg = '''
                :o -- output the results
                :q -- quit the program
                :i -- read a new query from terminal, which will be evaluated as the next query
                :h -- help
                '''
                print(msg)
            elif cmd == ':o':
                self.output()
                break
            elif cmd == ':i':
                self.queryList.insert(0, input("please enter the next query: "))
            elif cmd == ':q':
                print("End of program")
                break
            else:
                print("Unknown commands")
            cmd = input("Please input commands: ").strip()
        return

    def clear_res(self):
        while self.RES.isempty() is False:
            self.RES.pop()

    def find_lists(self, name):
        # given the name of a list head
        # push into the corresponding values which are id values
        self.RES.push(self.database.find_roots(name))

    def search_in_lists(self, one_list_head):
        # few headers of a list are contained in the list heads
        # print(one_list_head)
        temp = self.database.search(one_list_head)
        if type(temp[1]) is not list:
            raise Exception("the top of ENV should now be ids of list headers")
        self.ENV.push(temp[1])

    # get the value corresponding to the name of a id-list, i.e. [1, 2, 6, 10]
    # constraint: the ids should directly give out the values instead of the lists
    # @pysnooper.snoop()
    def get_val_by_name(self):
        assert (self.RES.isempty() == False)
        name = self.RES.pop()
        assert (self.RES.isempty() == False)
        idlist = self.RES.pop()
        # print(idlist)
        l = self.database.search(idlist)
        for i in l:
            if i[0] == name:
                val = i[1]
                assert (type(val) is not list)
                assert (val is not None)
                self.RES.push([val])
                return
        self.RES.push([None])
        return

    def add(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([a + b])

    def minus(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([a - b])

    def multiply(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([a * b])

    def division(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b / a])

    def greater(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b > a])

    # @pysnooper.snoop()
    def smaller(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b < a])

    def greater_equal(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b >= a])

    def smaller_equal(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
            if not semantic.is_number(a):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
            if not semantic.is_number(b):
                raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b <= a])

    def neq(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b != a])
    
    def max(self):
        if self.RES.top is not None:
            a = self.RES.pop()
            for elem in a:
                if not semantic.is_number(elem):
                    raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([max(a)])

    def min(self):
        if self.RES.top is not None:
            a = self.RES.pop()
            for elem in a:
                if not semantic.is_number(elem):
                    raise TypeError("not digit!")
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([min(a)])

    def eq(self):
        if self.RES.top is not None:
            a = self.RES.pop()[0]
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            b = self.RES.pop()[0]
        else:
            raise Exception("The Stack is empty!")
        self.RES.push([b == a])
    
    def In(self):
        # a in b, first pop b, then pop a
        if self.RES.top is not None:
            b = self.RES.pop()
            if type(b) != list:
                raise TypeError("not a list!")
        else:
            raise Exception("The Stack is empty!")
        if self.RES.top is not None:
            a = self.RES.pop()
            if type(a) != list:
                raise TypeError("not a list!")
        else:
            raise Exception("The Stack is empty!")
        for elem in a:
            if elem not in b:
                self.RES.push(["False"])
                return
        self.RES.push(["True"])
    
    def count(self):
        # only count the leaves here
        if self.RES.top is not None:
            self.RES.push([len(self.RES.pop())])

    # @pysnooper.snoop()
    def distinct(self):
        # make the leave values distinct
        # suppose all the values read from the stack are id numbers
        assert(self.RES.isempty() is False)
        distinct_values = set(self.RES.pop())
        self.RES.push(list(distinct_values))

    # @pysnooper.snoop()
    def projection(self):
        def __find(database, id_list, name):
            return_val = []
            for i in id_list:
                entry = database.search(i)
                if entry[0] == name:
                    return_val.append(entry[1])
                else:
                    # different names
                    if type(entry[1]) is list:
                        temp = __find(database, entry[1], name)
                        return_val.extend(temp)
            return return_val

        assert (self.RES.top is not None)
        name = self.RES.pop()[0]
        id_list = self.RES.pop()
        # the id in the list should point to the roots
        result_id = __find(self.database, id_list, name)
        self.RES.push(result_id)

    # @pysnooper.snoop()
    def cartesian(self):
        # suppose all the values read from the stack are id numbers
        if self.RES.top is not None:
            tmp = []
            a = self.RES.pop()
            b = self.RES.pop()
            for i in b:
                for j in a:
                    tmp.append([j] + [i])
            self.RES.push(tmp)

    # equijoin of 2 lists corresponding to their column
    # after processing the top of RES, there should be 2 nested list
    # consists of tuples, i.e. [(i_21,i_22),(i_24,i_25)]
    # it would join the records in l1 and l2 with the same value corresponding to the external names respectively
    # it would return a list with joined records
    # three parameters, Q1, Q2 and the name
    # @pysnooper.snoop()
    def equijoin(self):
        assert(self.RES.isempty() == False)
        name2 = self.RES.pop()[0]
        assert(self.RES.isempty() == False)
        id2 = self.RES.pop()
        assert(self.RES.isempty() == False)
        name1 = self.RES.pop()[0]
        assert(self.RES.isempty() == False)
        id1 = self.RES.pop()
        id_list2 = [i[1] for i in self.database.search(id2)]
        id_list1 = [i[1] for i in self.database.search(id1)]
        l1 = self.merge_sort(id_list1, name1)
        l2 = self.merge_sort(id_list2, name2)
        reslist = []
        m = n = 0
        while m < len(l1) and n < len(l2):
            val1 = l1[m][-1]
            val2 = l2[n][-1]
            while val2 <= val1 and n < len(l2):
                val2 = l2[n][-1]
                if val2 == val1:
                    # merge 2 records
                    reslist.append(l1[m][:-1] + l2[n][:-1])
                n += 1
            n -= 1
            m += 1
        self.RES.push(reslist)
        return

    # merge-sort the nestlist, i.e. [[id1,id2,id3],[id4,id5,id6],[id7,id8,id9]]
    # corresponding to the given external name
    # return a list consists of pairs of value and the nested tuple
    # i.e. [[id1,id2,id3,val1],[id4,id5,id6,val2]]
    # tuples which lack the value corresponding to the external name are discarded
    # two parameters: nestedlist and name
    def merge_sort(self, nestlist, name):
        if len(nestlist) <= 1:
            self.RES.push(nestlist[0])
            self.RES.push(name)
            self.get_val_by_name()
            assert (self.RES.isempty() == False)
            val = self.RES.pop()
            if val[0] is None:
                return []
            else:
                return [nestlist[0] + val]
        mid = len(nestlist) // 2
        left = self.merge_sort(nestlist[:mid], name)
        right = self.merge_sort(nestlist[mid:], name)
        return self.merge(left, right)

    def merge(self, l1, l2):
        reslist = []
        m = n = 0
        while m < len(l1) and n < len(l2):
            e1 = l1[m][-1]
            e2 = l2[n][-1]
            if e1 < e2:
                reslist.append(l1[m])
                m += 1
            else:
                reslist.append(l2[n])
                n += 1
        if m == len(l1):
            reslist.extend(l2[n:])
        else:
            reslist.extend(l1[m:])
        return reslist

    def deref(self):
        if self.RES.peek() is not None:
            assert (type(self.RES.peek()) is list)
            reslist = self.__deref(self.RES.pop())
            self.RES.push(reslist)

    def __deref(self, l):
        reslist = []
        for i in l:
            if type(i) == list:
                reslist.append(self.__deref(i))
            else:
                val = self.database.search([i])[0][1]
                # print(val)
                if type(val) == list:
                    reslist.append(self.__deref(val))
                else:
                    reslist.append(val)
        return reslist


if __name__ == "__main__":
    asm = ASMachine("./data.txt", "./queries.txt")
    asm.control()

    # print(asm.database.search([1, 4]))
    # print(asm.database.search([7, 9]))
    # asm.RES.push([[1, 4], [7, 9]])
    # print(asm.deref())
    #
    # print(asm.database.search([23, 24]))
    # print(asm.database.search([26, 27]))
    # asm.RES.push([[23, 24], [26, 27]])
    # print(asm.deref())
    #
    # print(asm.database.search(5))
    # asm.RES.push([5])
    # print(asm.deref())