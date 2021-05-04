# this is the data base for the object store


class DataBase:
    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    class __Record:
        def __init__(self, identity, name, value):
            # the record will be uniquely determined by the id
            self.id = identity
            self.name = name
            self.leaf = False if type(value) is list else True
            self.value = value

    def __init__(self, contents=[]):
        self.items = [None] * 10
        self.numItems = 0
        self.roots = {}
        # suppose the largest depth of the tree won't exceed 3 (0 1 2)
        for i in range(3):
            self.roots[i] = {}
        self.get_id = DataBase.get_id()
        for e in contents:
            # the e should be a list: [name, [values]]
            self.add(e[0], e[1], 0)

    @staticmethod
    def get_id():
        val = 1
        while True:
            yield val
            val += 1

    def add(self, name, value, recursion_depth):
        identity = next(self.get_id)
        if type(value) is list:
            id_list = []
            for obj in value:
                # the obj[0] should be name the obj[1] should be value
                sub_identity = self.add(obj[0], obj[1], recursion_depth + 1)
                id_list.append(sub_identity)
            value = id_list
        # at the end of the recursion, the item should be [name, value: eg. a string]
        if name in self.roots[recursion_depth].keys():
            self.roots[recursion_depth][name] += [identity]
        else:
            self.roots[recursion_depth][name] = [identity]
        record = DataBase.__Record(identity, name, value)
        if DataBase.__add(record, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                new_length = len(self.items * 2)
                self.items = DataBase.__rehash(self.items, [None] * new_length)
            return identity

    @staticmethod
    def __add(record, items):
        # insert the record to the corresponding hash value index
        index = hash(record.id) % len(items)
        location = -1
        while items[index] is not None:
            if items[index].value == record.value:
                return False
            if location < 0 and type(items[index]) == DataBase.__Placeholder:
                location = index
                break
            index = (index + 1) % len(items)
        if location < 0:
            location = index
        items[location] = record
        return True

    @staticmethod
    def __rehash(old_items, new_items):
        for e in old_items:
            if e is not None and type(e) != DataBase.__Placeholder:
                DataBase.__add(e, new_items)
        return new_items

    def __contains__(self, item):
        # the item should be like (name, value)
        index = hash(item[0]) % len(self.items)
        while self.items[index] is not None:
            if (self.items[index]) != DataBase.__Placeholder:
                record = self.items[index]
                name = record.name
                value = record.value
                assert (type(value) is not list)
                if name == item[0] and value == item[1]:
                    return True
            index = (index + 1) % len(self.items)
        return False

    def get_address(self, identity):
        return hash(identity) % len(self.items)

    def search(self, id_list):
        result = []
        flag = 0
        if type(id_list) is int:
            # print(id_list)
            id_list = [id_list]
            flag = 1
        for i in id_list:
            index = hash(i) % len(self.items)
            while self.items[index] is not None:
                if type(self.items[index]) != DataBase.__Placeholder:
                    temp = self.items[index]
                    if temp.id == i:
                        result.append([temp.name, temp.value])
                        break
        if flag:
            return result[0]
        return result

    def find_roots(self, name, depth=0):
        # eg. the input can be depth = 0, name = PERFORMANCE
        # then the return value will be all the id numbers of PERFORMANCE within depth 1 of the tree
        if depth >= 3:
            return None
        if name == "all":
            result = []
            for i in self.roots[depth].values():
                result += list(i)
            return result
        if name not in self.roots[depth].keys():
            return None
        return self.roots[depth][name]

    def show(self):
        for item in self.items:
            if item is not None and type(item) != self.__Placeholder:
                print("id: %d" % item.id, end="    ")
                print("name: %s" % item.name, end="    ")
                print("value: ", item.value)

    # def delete(self):


if __name__ == "__main__":
    record1 = ["THEATRE", [["cinema", "Abaton"], ["address", "Grindle_Alley"]]]
    record2 = ["THEATRE", [["cinema", "Flora"], ["address", "Old_Village"]]]
    record3 = ["THEATRE", [["cinema", "Holi"]]]
    record4 = [
        "PERFORMANCE",
        [["cinema", "Flora"], ["title", "The_Piano"], ["date", "May_7"]]
    ]
    record5 = ["PERFORMANCE", [["cinema", "Holi"], ["title", "Manhattan"]]]
    record6 = ["PLAY", [["title", "The_Piano"], ["director", "Campio"], ["price", 10]]]
    record7 = ["PLAY", [["title", "Manhattan"], ["director", "Allen"], ["price", 15]]]
    record8 = ["NATIONALITY", [["director", "Campio"], ["country", "USA"]]]
    record9 = ["NATIONALITY", [["director", "Allen"], ["country", "USA"]]]
    content = [
        record1, record2, record3, record4, record5, record6, record7, record8,
        record9
    ]
    database = DataBase(content)
    database.show()
    ans = database.search([8, 9])
    print(ans)
    print(database.roots)
    a = database.find_roots("PERFORMANCE")
    print(a)
    test_search_result = database.search(a)
    print(test_search_result)
    all_roots = database.find_roots("all")
    print(all_roots)
    print(database.search([10]))
    temp = database.search(19)[1]
    print(type(temp))

