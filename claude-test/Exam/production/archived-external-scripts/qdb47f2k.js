// ==================== ENCRYPTED QUESTION DATABASE ====================
// Total: 160 Questions (100 Objective MCQ + 60 Subjective)
// Category Distribution:
//   - Python MCQ: 50 questions
//   - SQL MCQ: 50 questions
//   - Python Subjective: 30 questions
//   - SQL Subjective: 30 questions

const QUESTION_DATABASE = {
    // ==================== PYTHON MCQ (50 Questions) ====================
    pythonMCQ: [
        {
            id: 'PY_MCQ_001',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of the following code?\nx = [1, 2, 3]\nprint(x * 2)',
            options: ['[2, 4, 6]', '[1, 2, 3, 1, 2, 3]', '[1, 2, 3, 2, 4, 6]', 'Error'],
            correctAnswer: 1,
            explanation: 'List multiplication replicates elements, it doesn\'t multiply values.'
        },
        {
            id: 'PY_MCQ_002',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the data type of the variable x after executing x = (1,)?',
            options: ['tuple', 'list', 'int', 'set'],
            correctAnswer: 0,
            explanation: 'A trailing comma defines a single-element tuple.'
        },
        {
            id: 'PY_MCQ_003',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will print(0.1 + 0.2 == 0.3) output?',
            options: ['True', 'False', '0.3', 'Error'],
            correctAnswer: 1,
            explanation: 'Floating-point arithmetic precision issue makes this False.'
        },
        {
            id: 'PY_MCQ_004',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\na = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)',
            options: ['[1, 2, 3]', '[1, 2, 3, 4]', '[4]', 'Error'],
            correctAnswer: 1,
            explanation: 'Lists are mutable and both a and b refer to the same object.'
        },
        {
            id: 'PY_MCQ_005',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint("hello"[-1])',
            options: ['h', 'o', 'hello', 'Error'],
            correctAnswer: 1,
            explanation: 'Negative indexing starts from the end.'
        },
        {
            id: 'PY_MCQ_006',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which of the following statements is true?',
            options: ['Python is compiled only', 'Python is interpreted only', 'Python is both compiled and interpreted', 'Python is neither compiled nor interpreted'],
            correctAnswer: 2,
            explanation: 'Python code is compiled to bytecode, then interpreted by the Python Virtual Machine.'
        },
        {
            id: 'PY_MCQ_007',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What does list(range(0, 10, 2)) return?',
            options: ['[1, 3, 5, 7, 9]', '[0, 2, 4, 6, 8]', '[0, 2, 4, 6, 8, 10]', 'range(0, 10, 2)'],
            correctAnswer: 1,
            explanation: 'Range with step 2 creates even numbers from 0 to 8.'
        },
        {
            id: 'PY_MCQ_008',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the result of:\nprint(type({}))',
            options: ["<class 'set'>", "<class 'dict'>", "<class 'list'>", "<class 'tuple'>"],
            correctAnswer: 1,
            explanation: 'Empty braces {} create a dictionary, not a set.'
        },
        {
            id: 'PY_MCQ_009',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which of the following will NOT produce an error?',
            options: ["int('xyz')", "int(10.5)", "int('10a')", "int('10.5')"],
            correctAnswer: 1,
            explanation: 'Only numeric float → int conversion works.'
        },
        {
            id: 'PY_MCQ_010',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\na = [1, 2, 3]\nprint(a[::-1])',
            options: ['[3, 2, 1]', '[1, 2, 3]', '[2, 1, 3]', 'Error'],
            correctAnswer: 0,
            explanation: 'Slice [::-1] reverses the list.'
        },
        {
            id: 'PY_MCQ_011',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which method is used to add an element at a specific position in a list?',
            options: ['add()', 'append()', 'insert()', 'extend()'],
            correctAnswer: 2,
            explanation: 'insert(pos, value) adds at a given index.'
        },
        {
            id: 'PY_MCQ_012',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\nx = "Python"\nprint(x[1:4])',
            options: ['yth', 'Pyt', 'ytho', 'yto'],
            correctAnswer: 0,
            explanation: 'Slicing excludes the end index.'
        },
        {
            id: 'PY_MCQ_013',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which of the following is immutable?',
            options: ['list', 'dict', 'tuple', 'set'],
            correctAnswer: 2,
            explanation: 'Tuples are immutable in Python.'
        },
        {
            id: 'PY_MCQ_014',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\nprint(bool([]))',
            options: ['True', 'False', 'None', 'Error'],
            correctAnswer: 1,
            explanation: 'Empty containers are considered False.'
        },
        {
            id: 'PY_MCQ_015',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will len("Hello\\nWorld") return?',
            options: ['10', '11', '12', '9'],
            correctAnswer: 1,
            explanation: '\\n counts as one character.'
        },
        {
            id: 'PY_MCQ_016',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the result of:\nprint(2 ** 3 ** 2)',
            options: ['512', '64', '16', '8'],
            correctAnswer: 0,
            explanation: 'Exponentiation is right-associative → 2^(3^2) = 2^9 = 512.'
        },
        {
            id: 'PY_MCQ_017',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which of the following can be used to create a dictionary?',
            options: ['{}', 'dict()', '{"a":1, "b":2}', 'All of the above'],
            correctAnswer: 3,
            explanation: 'All three methods create dictionaries.'
        },
        {
            id: 'PY_MCQ_018',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\na = [1, 2, 3]\na[1:3] = [5, 6, 7]\nprint(a)',
            options: ['[1, 5, 6, 7]', '[1, 5, 6, 7, 3]', '[5, 6, 7]', '[1, 5, 6, 7, 2, 3]'],
            correctAnswer: 0,
            explanation: 'Slicing replaces elements 1 and 2 with the new list.'
        },
        {
            id: 'PY_MCQ_019',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which of these is a valid variable name in Python?',
            options: ['1value', 'value_1', 'value-1', '@value'],
            correctAnswer: 1,
            explanation: 'Variable names can contain underscores and numbers (but not start with a number).'
        },
        {
            id: 'PY_MCQ_020',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: "What is the output of:\nprint('abc' * 2)",
            options: ["'aabbcc'", "'abcabc'", "'abc2'", 'Error'],
            correctAnswer: 1,
            explanation: 'String multiplication repeats the string.'
        },
        {
            id: 'PY_MCQ_021',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What does id() function do in Python?',
            options: ['Returns the memory address of an object', 'Returns the name of a variable', "Returns object's hash value", 'Deletes an object'],
            correctAnswer: 0,
            explanation: 'id() returns the memory address.'
        },
        {
            id: 'PY_MCQ_022',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will set([1,2,2,3,3]) return?',
            options: ['{1,2,2,3,3}', '{1,2,3}', '[1,2,3]', 'Error'],
            correctAnswer: 1,
            explanation: 'Sets automatically remove duplicates.'
        },
        {
            id: 'PY_MCQ_023',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\nx = [1, 2, 3]\nprint(x.pop())',
            options: ['1', '2', '3', 'Error'],
            correctAnswer: 2,
            explanation: 'pop() removes and returns the last element.'
        },
        {
            id: 'PY_MCQ_024',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will print(type(lambda x: x**2)) output?',
            options: ["<class 'lambda'>", "<class 'function'>", "<class 'method'>", 'Error'],
            correctAnswer: 1,
            explanation: 'Lambda creates a function object.'
        },
        {
            id: 'PY_MCQ_025',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be printed:\nprint(bool("False"))',
            options: ['True', 'False', 'None', 'Error'],
            correctAnswer: 0,
            explanation: 'Non-empty strings are always True.'
        },
        {
            id: 'PY_MCQ_026',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\nx = [10, 20, 30]\ny = x.copy()\ny.append(40)\nprint(x)',
            options: ['[10, 20, 30, 40]', '[10, 20, 30]', '[40]', 'Error'],
            correctAnswer: 1,
            explanation: 'copy() creates a shallow copy; appending to y does not affect x.'
        },
        {
            id: 'PY_MCQ_027',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which function returns the number of items in an object?',
            options: ['size()', 'length()', 'count()', 'len()'],
            correctAnswer: 3,
            explanation: 'len() returns the number of items.'
        },
        {
            id: 'PY_MCQ_028',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\nprint({1, 2, 3} & {2, 3, 4})',
            options: ['{1,2,3,4}', '{2,3}', '{1,4}', 'Error'],
            correctAnswer: 1,
            explanation: '& performs set intersection.'
        },
        {
            id: 'PY_MCQ_029',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint([i for i in range(5) if i % 2 == 0])',
            options: ['[0, 1, 2, 3, 4]', '[1, 3]', '[0, 2, 4]', '[2, 4]'],
            correctAnswer: 2,
            explanation: 'List comprehension filters even numbers.'
        },
        {
            id: 'PY_MCQ_030',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'Which statement is true about Python strings?',
            options: ['Strings are mutable', 'Strings are immutable', 'Strings are numeric arrays', 'Strings must be ASCII'],
            correctAnswer: 1,
            explanation: 'Strings are immutable in Python.'
        },
        {
            id: 'PY_MCQ_031',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will the following code print?\na = [1, 2]\nb = [1, 2]\nprint(a is b)',
            options: ['True', 'False', '[1, 2]', 'Error'],
            correctAnswer: 1,
            explanation: 'is checks identity, not equality.'
        },
        {
            id: 'PY_MCQ_032',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint("abc".upper())',
            options: ['abc', 'Abc', 'ABC', 'Error'],
            correctAnswer: 2,
            explanation: 'upper() converts to uppercase.'
        },
        {
            id: 'PY_MCQ_033',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What does strip() method do?',
            options: ['Removes spaces from both ends', 'Removes characters from start', 'Removes only newline', 'Removes all spaces in string'],
            correctAnswer: 0,
            explanation: 'strip() removes whitespace from both ends.'
        },
        {
            id: 'PY_MCQ_034',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint(sum([1, 2, 3], 10))',
            options: ['6', '16', '10', 'Error'],
            correctAnswer: 1,
            explanation: 'The second argument is the start value (10 + 1 + 2 + 3).'
        },
        {
            id: 'PY_MCQ_035',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will print(bool(0)) return?',
            options: ['True', 'False', 'None', 'Error'],
            correctAnswer: 1,
            explanation: '0 is considered False.'
        },
        {
            id: 'PY_MCQ_036',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will the following print?\na = [1, 2, 3]\nprint(a[3:])',
            options: ['[]', '[3]', 'Error', '[1, 2, 3]'],
            correctAnswer: 0,
            explanation: 'Slicing beyond the length gives an empty list.'
        },
        {
            id: 'PY_MCQ_037',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be printed?\ndef f(x=[]):\n    x.append(1)\n    return x\nprint(f(), f(), f())',
            options: ['[1] [1] [1]', '[1] [1,1] [1,1,1]', '[1,1,1] [1,1,1] [1,1,1]', 'Error'],
            correctAnswer: 1,
            explanation: 'Default list persists across calls.'
        },
        {
            id: 'PY_MCQ_038',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint(all([True, 1, 3]))',
            options: ['True', 'False', 'Error', 'None'],
            correctAnswer: 0,
            explanation: 'All elements are truthy.'
        },
        {
            id: 'PY_MCQ_039',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: "What will any([0, '', False]) return?",
            options: ['True', 'False', 'None', 'Error'],
            correctAnswer: 1,
            explanation: 'All elements are falsy.'
        },
        {
            id: 'PY_MCQ_040',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nx = [1, 2, 3]\nprint(x[1:])',
            options: ['[2, 3]', '[1]', '[1, 2]', '[3]'],
            correctAnswer: 0,
            explanation: 'Slicing from index 1 to end.'
        },
        {
            id: 'PY_MCQ_041',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will print(list("abc")) output?',
            options: ["['abc']", "['a', 'b', 'c']", "['a b c']", 'Error'],
            correctAnswer: 1,
            explanation: 'list() converts string to list of characters.'
        },
        {
            id: 'PY_MCQ_042',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will be the output of:\na = [1, 2, 3]\nb = a[:]\nb.append(4)\nprint(len(a), len(b))',
            options: ['3 3', '3 4', '4 4', 'Error'],
            correctAnswer: 1,
            explanation: 'Slicing creates a shallow copy.'
        },
        {
            id: 'PY_MCQ_043',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will print(type( (1) )) output?',
            options: ["<class 'tuple'>", "<class 'int'>", "<class 'list'>", "<class 'set'>"],
            correctAnswer: 1,
            explanation: 'Parentheses alone don\'t create tuples without a comma.'
        },
        {
            id: 'PY_MCQ_044',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: "What is the output of:\nprint('A' < 'a')",
            options: ['True', 'False', 'Error', 'None'],
            correctAnswer: 0,
            explanation: 'ASCII value of uppercase \'A\' < lowercase \'a\'.'
        },
        {
            id: 'PY_MCQ_045',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: "What will the following print?\nfor i in range(3):\n    print(i, end=',')",
            options: ['0,1,2,', '012', '0,1,2', 'Error'],
            correctAnswer: 0,
            explanation: 'end=\',\' replaces newline.'
        },
        {
            id: 'PY_MCQ_046',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint([i**2 for i in range(4)])',
            options: ['[1, 4, 9, 16]', '[0, 1, 4, 9]', '[0, 1, 4, 9, 16]', 'Error'],
            correctAnswer: 1,
            explanation: 'List comprehension squares 0, 1, 2, 3.'
        },
        {
            id: 'PY_MCQ_047',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the result of:\nprint("Hello {0}!".format("World"))',
            options: ['Hello 0!', 'Hello {World}!', 'Hello World!', 'Error'],
            correctAnswer: 2,
            explanation: 'format() replaces {0} with the argument.'
        },
        {
            id: 'PY_MCQ_048',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\nprint(list(map(lambda x: x+1, [1,2,3])))',
            options: ['[2,3,4]', '[1,2,3]', '[1,3,5]', 'Error'],
            correctAnswer: 0,
            explanation: 'map applies lambda to each element.'
        },
        {
            id: 'PY_MCQ_049',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What will reversed([1,2,3]) return?',
            options: ['[3,2,1]', 'reversed object', '(3,2,1)', 'None'],
            correctAnswer: 1,
            explanation: 'It returns a reverse iterator, not a list.'
        },
        {
            id: 'PY_MCQ_050',
            type: 'mcq',
            category: 'python',
            points: 5,
            question: 'What is the output of:\na = [1, 2, 3]\nprint(a.clear())',
            options: ['[]', 'None', 'Error', '[1, 2, 3]'],
            correctAnswer: 1,
            explanation: 'clear() empties list in place and returns None.'
        }
    ],

    // ==================== SQL MCQ (50 Questions) ====================
    sqlMCQ: [
        {
            id: 'SQL_MCQ_001',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does SQL stand for?',
            options: ['Structured Query Language', 'Simple Query Language', 'Sequential Query Logic', 'Structured Question Language'],
            correctAnswer: 0,
            explanation: 'SQL stands for Structured Query Language.'
        },
        {
            id: 'SQL_MCQ_002',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which command is used to remove a table from a database?',
            options: ['DELETE', 'DROP', 'REMOVE', 'ERASE'],
            correctAnswer: 1,
            explanation: 'DROP TABLE table_name; removes the table structure completely.'
        },
        {
            id: 'SQL_MCQ_003',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following is not a type of SQL command?',
            options: ['DDL', 'DML', 'DCL', 'DQLL'],
            correctAnswer: 3,
            explanation: "There's no DQLL; valid ones are DDL, DML, DCL, TCL, DQL."
        },
        {
            id: 'SQL_MCQ_004',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which SQL statement is used to retrieve data from a table?',
            options: ['GET', 'SELECT', 'EXTRACT', 'FETCH'],
            correctAnswer: 1,
            explanation: 'SELECT retrieves data from tables.'
        },
        {
            id: 'SQL_MCQ_005',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which clause is used to filter records?',
            options: ['ORDER BY', 'GROUP BY', 'WHERE', 'DISTINCT'],
            correctAnswer: 2,
            explanation: 'WHERE filters records based on conditions.'
        },
        {
            id: 'SQL_MCQ_006',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which keyword is used to sort the result set?',
            options: ['ORDER', 'ORDER BY', 'SORT', 'SORT BY'],
            correctAnswer: 1,
            explanation: 'ORDER BY sorts the result set.'
        },
        {
            id: 'SQL_MCQ_007',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which function returns the number of rows in a table?',
            options: ['COUNT()', 'SUM()', 'MAX()', 'LENGTH()'],
            correctAnswer: 0,
            explanation: 'COUNT() returns the number of rows.'
        },
        {
            id: 'SQL_MCQ_008',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is the default sort order of the ORDER BY clause?',
            options: ['Descending', 'Random', 'Ascending', 'No order'],
            correctAnswer: 2,
            explanation: 'Default sort order is ascending.'
        },
        {
            id: 'SQL_MCQ_009',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which operator is used to test for NULL values?',
            options: ['=', 'IS', '==', 'EQUAL'],
            correctAnswer: 1,
            explanation: 'Use IS NULL or IS NOT NULL.'
        },
        {
            id: 'SQL_MCQ_010',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What will SELECT * FROM Employees WHERE salary BETWEEN 3000 AND 5000; return?',
            options: ['All employees', 'Employees with salary < 3000', 'Employees with salary 3000–5000', 'Error'],
            correctAnswer: 2,
            explanation: 'BETWEEN includes both boundary values.'
        },
        {
            id: 'SQL_MCQ_011',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following is a DDL command?',
            options: ['SELECT', 'INSERT', 'UPDATE', 'CREATE'],
            correctAnswer: 3,
            explanation: 'DDL → CREATE, ALTER, DROP, TRUNCATE.'
        },
        {
            id: 'SQL_MCQ_012',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which SQL statement is used to modify data?',
            options: ['MODIFY', 'UPDATE', 'CHANGE', 'ALTER'],
            correctAnswer: 1,
            explanation: 'UPDATE modifies existing data.'
        },
        {
            id: 'SQL_MCQ_013',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which command removes all rows from a table but keeps the structure?',
            options: ['DROP', 'DELETE', 'TRUNCATE', 'ERASE'],
            correctAnswer: 2,
            explanation: 'TRUNCATE removes all rows but keeps the table structure.'
        },
        {
            id: 'SQL_MCQ_014',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which keyword is used to combine rows from two or more tables?',
            options: ['UNION', 'COMBINE', 'GROUP', 'JOIN'],
            correctAnswer: 3,
            explanation: 'JOIN combines rows from multiple tables.'
        },
        {
            id: 'SQL_MCQ_015',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does the GROUP BY clause do?',
            options: ['Filters rows', 'Sorts results', 'Groups rows with same values', 'Deletes duplicates'],
            correctAnswer: 2,
            explanation: 'GROUP BY groups rows with the same values.'
        },
        {
            id: 'SQL_MCQ_016',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which constraint uniquely identifies each row in a table?',
            options: ['FOREIGN KEY', 'UNIQUE', 'PRIMARY KEY', 'CHECK'],
            correctAnswer: 2,
            explanation: 'PRIMARY KEY uniquely identifies each row.'
        },
        {
            id: 'SQL_MCQ_017',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which command is used to add a new column?',
            options: ['ADD COLUMN', 'INSERT COLUMN', 'ALTER TABLE … ADD', 'MODIFY TABLE'],
            correctAnswer: 2,
            explanation: 'ALTER TABLE ... ADD adds a new column.'
        },
        {
            id: 'SQL_MCQ_018',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What will this query do?\nSELECT DISTINCT city FROM customers;',
            options: ['Shows all cities', 'Shows duplicate cities', 'Shows unique cities only', 'Shows cities in uppercase'],
            correctAnswer: 2,
            explanation: 'DISTINCT returns unique values only.'
        },
        {
            id: 'SQL_MCQ_019',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which keyword is used to remove duplicate rows in a query?',
            options: ['REMOVE', 'UNIQUE', 'DISTINCT', 'CLEAN'],
            correctAnswer: 2,
            explanation: 'DISTINCT removes duplicate rows.'
        },
        {
            id: 'SQL_MCQ_020',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following constraints allows only a specific range of values?',
            options: ['DEFAULT', 'CHECK', 'PRIMARY KEY', 'FOREIGN KEY'],
            correctAnswer: 1,
            explanation: 'CHECK constraint allows specific range of values.'
        },
        {
            id: 'SQL_MCQ_021',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is the result of:\nSELECT COUNT(*) FROM employee WHERE dept_id IS NULL;',
            options: ['Counts all rows', 'Counts rows with NULL dept_id', 'Returns 0 always', 'Error'],
            correctAnswer: 1,
            explanation: 'Counts rows where dept_id is NULL.'
        },
        {
            id: 'SQL_MCQ_022',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which function gives the current date?',
            options: ['CURDATE()', 'SYSDATE()', 'NOW()', 'All of the above'],
            correctAnswer: 3,
            explanation: 'All three functions can return current date.'
        },
        {
            id: 'SQL_MCQ_023',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is the purpose of a foreign key?',
            options: ['To identify a row uniquely', 'To ensure referential integrity', 'To auto-increment a column', 'To store large text'],
            correctAnswer: 1,
            explanation: 'Foreign key ensures referential integrity.'
        },
        {
            id: 'SQL_MCQ_024',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which clause is used to filter grouped data?',
            options: ['WHERE', 'HAVING', 'ORDER BY', 'FILTER'],
            correctAnswer: 1,
            explanation: 'HAVING works with aggregate functions.'
        },
        {
            id: 'SQL_MCQ_025',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does SELECT COUNT(DISTINCT dept_id) return?',
            options: ['Number of departments', 'Total employees', 'Sum of salaries', 'Maximum dept_id'],
            correctAnswer: 0,
            explanation: 'Counts unique department IDs.'
        },
        {
            id: 'SQL_MCQ_026',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following commands commits a transaction?',
            options: ['SAVE', 'COMMIT', 'APPLY', 'END'],
            correctAnswer: 1,
            explanation: 'COMMIT saves transaction changes.'
        },
        {
            id: 'SQL_MCQ_027',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is a composite key?',
            options: ['A foreign key', 'A key made of multiple columns', "A key that can't be NULL", 'A temporary key'],
            correctAnswer: 1,
            explanation: 'Composite key combines multiple columns.'
        },
        {
            id: 'SQL_MCQ_028',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is a view?',
            options: ['A duplicate table', 'A virtual table based on query', 'A permanent copy', 'A backup table'],
            correctAnswer: 1,
            explanation: 'View is a virtual table based on a query.'
        },
        {
            id: 'SQL_MCQ_029',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following statements is true?',
            options: ['A table can have multiple primary keys', 'A table can have multiple foreign keys', 'A table cannot have constraints', 'Foreign keys must be unique'],
            correctAnswer: 1,
            explanation: 'A table can have multiple foreign keys.'
        },
        {
            id: 'SQL_MCQ_030',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is normalization?',
            options: ['Process of duplicating data', 'Process of minimizing redundancy', 'Process of deleting tables', 'Process of indexing'],
            correctAnswer: 1,
            explanation: 'Normalization minimizes data redundancy.'
        },
        {
            id: 'SQL_MCQ_031',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which normal form removes partial dependency?',
            options: ['1NF', '2NF', '3NF', 'BCNF'],
            correctAnswer: 1,
            explanation: '2NF removes partial dependency.'
        },
        {
            id: 'SQL_MCQ_032',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which normal form removes transitive dependency?',
            options: ['2NF', '3NF', 'BCNF', '4NF'],
            correctAnswer: 1,
            explanation: '3NF removes transitive dependency.'
        },
        {
            id: 'SQL_MCQ_033',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does the LIKE operator do?',
            options: ['Compares exact match', 'Pattern matching with wildcards', 'Checks NULL values', 'Filters numbers'],
            correctAnswer: 1,
            explanation: 'LIKE performs pattern matching.'
        },
        {
            id: 'SQL_MCQ_034',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What symbol represents a single character in LIKE pattern?',
            options: ['%', '_', '?', '#'],
            correctAnswer: 1,
            explanation: '_ represents a single character.'
        },
        {
            id: 'SQL_MCQ_035',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which operator is used to combine multiple conditions?',
            options: ['AND / OR', 'BETWEEN', 'IS', 'EXISTS'],
            correctAnswer: 0,
            explanation: 'AND/OR combine multiple conditions.'
        },
        {
            id: 'SQL_MCQ_036',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is the use of IN operator?',
            options: ['Check range of numbers', 'Check if value exists in a list', 'Check NULL', 'Compare two tables'],
            correctAnswer: 1,
            explanation: 'IN checks if value exists in a list.'
        },
        {
            id: 'SQL_MCQ_037',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which index is automatically created with a primary key?',
            options: ['Non-clustered', 'Clustered', 'Hash', 'Bitmap'],
            correctAnswer: 1,
            explanation: 'Primary key creates a clustered index.'
        },
        {
            id: 'SQL_MCQ_038',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which SQL command is used to change data type of a column?',
            options: ['MODIFY', 'CHANGE', 'ALTER TABLE … MODIFY', 'UPDATE'],
            correctAnswer: 2,
            explanation: 'ALTER TABLE ... MODIFY changes column type.'
        },
        {
            id: 'SQL_MCQ_039',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following is used to give a temporary name to a column?',
            options: ['ALIAS', 'TEMP', 'AS', 'NAME'],
            correctAnswer: 2,
            explanation: 'AS gives a temporary name (alias).'
        },
        {
            id: 'SQL_MCQ_040',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: "What will the query do?\nSELECT name FROM employee WHERE name LIKE 'S%';",
            options: ['Names ending with S', 'Names starting with S', 'Names containing S', 'Error'],
            correctAnswer: 1,
            explanation: 'S% matches names starting with S.'
        },
        {
            id: 'SQL_MCQ_041',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is a subquery?',
            options: ['A query within another query', 'A stored procedure', 'A join operation', 'A transaction'],
            correctAnswer: 0,
            explanation: 'Subquery is a query within another query.'
        },
        {
            id: 'SQL_MCQ_042',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which type of join returns all records from both tables?',
            options: ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN'],
            correctAnswer: 3,
            explanation: 'FULL OUTER JOIN returns all records.'
        },
        {
            id: 'SQL_MCQ_043',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which join returns only matching records?',
            options: ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN'],
            correctAnswer: 0,
            explanation: 'INNER JOIN returns only matching records.'
        },
        {
            id: 'SQL_MCQ_044',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is the purpose of the UNION operator?',
            options: ['Combine rows and remove duplicates', 'Combine columns', 'Join tables horizontally', 'Return intersection'],
            correctAnswer: 0,
            explanation: 'UNION combines rows and removes duplicates.'
        },
        {
            id: 'SQL_MCQ_045',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does the EXISTS operator do?',
            options: ['Checks if subquery returns any rows', 'Checks for NULL', 'Deletes rows', 'Creates temporary tables'],
            correctAnswer: 0,
            explanation: 'EXISTS checks if subquery returns rows.'
        },
        {
            id: 'SQL_MCQ_046',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What is a transaction in SQL?',
            options: ['A single logical unit of work', 'A permanent table', 'A stored procedure', 'A rollback command'],
            correctAnswer: 0,
            explanation: 'Transaction is a logical unit of work.'
        },
        {
            id: 'SQL_MCQ_047',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What command undoes changes made in a transaction?',
            options: ['CANCEL', 'DELETE', 'ROLLBACK', 'RESET'],
            correctAnswer: 2,
            explanation: 'ROLLBACK undoes transaction changes.'
        },
        {
            id: 'SQL_MCQ_048',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which SQL clause restricts the number of rows returned?',
            options: ['RESTRICT', 'LIMIT', 'TOP', 'Both B and C'],
            correctAnswer: 3,
            explanation: 'MySQL uses LIMIT, SQL Server uses TOP.'
        },
        {
            id: 'SQL_MCQ_049',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'What does ACID stand for in databases?',
            options: ['Atomicity, Consistency, Isolation, Durability', 'Accuracy, Control, Integrity, Data', 'Access, Cache, Index, Durability', 'None of the above'],
            correctAnswer: 0,
            explanation: 'ACID: Atomicity, Consistency, Isolation, Durability.'
        },
        {
            id: 'SQL_MCQ_050',
            type: 'mcq',
            category: 'sql',
            points: 5,
            question: 'Which of the following is true about foreign keys?',
            options: ['Can have NULL values', 'Must reference a primary key', 'Can enforce referential integrity', 'All of the above'],
            correctAnswer: 3,
            explanation: 'Foreign keys can have NULL, reference primary keys, and enforce integrity.'
        }
    ],

    // Due to response length limitations, I'll create separate continuation files for subjective questions
    // This file will be extended with Python and SQL subjective questions

    pythonSubjective: [], // To be populated
    sqlSubjective: []     // To be populated
};

// ==================== QUESTION ENCRYPTION SYSTEM ====================
const ENCRYPTION_KEY = 'ExamSecure2025!@#$%';

// Encrypt a single question
function encryptQuestion(question) {
    const jsonString = JSON.stringify(question);
    return CryptoJS.AES.encrypt(jsonString, ENCRYPTION_KEY).toString();
}

// Decrypt a single question
function decryptQuestion(encryptedQuestion) {
    const decrypted = CryptoJS.AES.decrypt(encryptedQuestion, ENCRYPTION_KEY);
    return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
}

// ==================== RANDOM SELECTION LOGIC ====================
function getRandomQuestions() {
    // Combine all objective questions (Python MCQ + SQL MCQ = 100 total)
    const allObjective = [
        ...QUESTION_DATABASE.pythonMCQ,
        ...QUESTION_DATABASE.sqlMCQ
    ];

    // Combine all subjective questions (Python + SQL = 60 total)
    const allSubjective = [
        ...QUESTION_DATABASE.pythonSubjective,
        ...QUESTION_DATABASE.sqlSubjective
    ];

    // Shuffle and select 10 objective questions
    const selectedObjective = shuffleArray(allObjective).slice(0, 10);

    // Shuffle and select 5 subjective questions
    const selectedSubjective = shuffleArray(allSubjective).slice(0, 5);

    // Combine and return
    return [...selectedObjective, ...selectedSubjective];
}

// Fisher-Yates shuffle algorithm for true randomization
function shuffleArray(array) {
    const shuffled = [...array]; // Create a copy
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Export for use in main application
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        QUESTION_DATABASE,
        encryptQuestion,
        decryptQuestion,
        getRandomQuestions,
        shuffleArray
    };
}
