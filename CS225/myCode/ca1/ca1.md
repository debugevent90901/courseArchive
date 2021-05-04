# CA1

the first computing assignment of CS225, data structure. The implementation of a two-stack abstract machine (2SAM) for processing query requests on a
list-based object store.

## Getting Started

This abstract machine consists mainly four parts: the database.py to store the list-based object. the semanticAnalysis.py to analysis the input queries, spliting and translating them for evaluate. stack.py, the ADT stack used in implementation. machine.py, the machine itself that processes the query requests

### Prerequisites

To run the assignment, the following environment is required

```
python 3.7.6
```
### Usage

```
$ python3 machine.py
```
when executing in python consolo
```
:o -- output the results
:q -- quit the program
:i -- read a new query from terminal, which will be evaluated as the next query
:h -- help
```
the list-based data is stored in ./data.txt  
the queries is stored in ./queries.txt

## Anaconda (Windows) Notes
If you are using Anaconda in Windows, using 'python3' might not work. Use 'python' instead.

## Running the tests

The program is expected to execute as follows:

### The  list-based data used for tests

```
["THEATRE", [["cinema", "Abaton"], ["address", "Grindle_Alley"]]]
["THEATRE", [["cinema", "Flora"], ["address", "Old_Village"]]]
["THEATRE", [["cinema", "Holi"]]]
["PERFORMANCE", [["cinema", "Flora"], ["title", "The_Piano"], ["date", "May_7"]]]
["PERFORMANCE", [["cinema", "Holi"], ["title", "Manhattan"]]]
["PLAY", [["title", "The_Piano"], ["director", "Campio"], ["price", 10]]]
["PLAY", [["title", "Manhattan"], ["director", "Allen"], ["price", 15]]]
["NATIONALITY", [["director", "Campio"], ["country", "USA"]]]
["NATIONALITY", [["director", "Allen"], ["country", "USA"]]]
```

### The operations supported

our abstract machine supports the following operators

```
aggregation operators: count, sum, min, max, average
arithmetic operators: +, −, ∗, /
comparison operators: <, >, ≤, ≥, ==, !=
Boolean operators: AND, OR, NOT
other operators: In, distinct, deref, selection, projection, cartesian, equaljoin
```

### detailed tests
```
query = "PERFORMANCE where(&cinema = Flora)"
output: [9]
```
```
query = "deref(PERFORMANCE where(&cinema = Flora))"
output: ['Flora', 'The_Piano', 'May_7']]
```
```
query = "deref(eqjoin(PERFORMANCE cinema THEATRE cinema))"
output: [['Flora', 'The_Piano', 'May_7', 'Flora', 'Old_Village'], ['Holi', 'Manhattan', 'Holi']]
```
```
query = "(NATIONALITY where(&director = Campio)).country"
output: ['USA']
```
```
query = "PERFORMANCE where(&cinema = GZM)"
output: []
```
```
query = "(PERFORMANCE where(&cinema = Flora)) In [9,10,11]"
output: ['True']
``` 
```
query = "distinct([2,3,4,4,5,5,6,77,77,88])"
output: [2, 3, 4, 5, 6, 77, 88]
```
```
query = "distinct(NATIONALITY.country)"
output: ['USA']
```
```
query = "deref(THEATRE)"
output: [['Abaton', 'Grindle_Alley'], ['Flora', 'Old_Village'], ['Holi']]
```
```
query = "NATIONALITY x PLAY"
output: [[16, 24], [20, 24], [16, 27], [20, 27]]
```
```
query = "deref(NATIONALITY) x deref(NATIONALITY)"
output: [[['Campio', 'USA'], ['Campio', 'USA']], [['Allen', 'USA'], ['Campio', 'USA']], [['Campio', 'USA'], ['Allen', 'USA']], [['Allen', 'USA'], ['Allen', 'USA']]]
```
```
query = "(PLAY where (&director = Campio)).price > (PLAY where(&director = Allen)).price"
output: [False]
```
```
query = "(PLAY where (&director = Campio)).price < (PLAY where(&director = Allen)).price"
output: [True]
```
```
query = "deref(PERFORMANCE where(&cinema = ((THEATRE where(&address = Old_Village)).cinema)))"
output: [['Flora', 'The_Piano', 'May_7']]
```
```
query = "deref(PLAY where (&price < 12))"
output: [['The_Piano', 'Campio', 10]]
```
```
query = "deref(PLAY where (&price < 20))"
output: [['The_Piano', 'Campio', 10], ['Manhattan', 'Allen', 15]]
```

## Time Complexity Analysis
leave out
```
you have to say something
```

## Authors
### Group 7

* **Zhu Zhongbo** - *3180111635* 

* **Guan Zimu** - *3180111630*
  
* **Xie Tian** - *3180111631* 
  
*  **Yang Zhaohua** - *3180111374*



## Donate us
### your contribution really makes a difference
* Zimu_8028 (Wechat)
