// ==================== SUBJECTIVE QUESTIONS DATABASE ====================
// This file contains all Python and SQL subjective/coding questions
// To be merged with questions-database.js

const PYTHON_SUBJECTIVE = [
    {
        id: 'PY_SUB_001',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find All Prime Numbers in a Range\n\nInput:\n10 30\n\nOutput:\n11 13 17 19 23 29',
        starterCode: `def primes_in_range(a, b):
    # Write your code here to find prime numbers in range [a, b]
    pass

a, b = map(int, input().split())
primes_in_range(a, b)`,
        explanation: 'Check each number for primality using trial division up to square root.'
    },
    {
        id: 'PY_SUB_002',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Check if a String is Pangram\n\nA pangram contains every letter of the alphabet at least once.\n\nInput:\nThe quick brown fox jumps over the lazy dog\n\nOutput:\nPangram',
        starterCode: `import string
# Write your code here to check if the input string is a pangram
s = input().lower()
pass`,
        explanation: 'Check if all 26 letters are present in the input string.'
    },
    {
        id: 'PY_SUB_003',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Frequency of Each Word in a Sentence\n\nInput:\nhello world hello python\n\nOutput:\nhello:2 world:1 python:1',
        starterCode: `from collections import Counter
# Write your code here to find frequency of each word
words = input().split()
pass`,
        explanation: 'Use Counter to count word frequencies.'
    },
    {
        id: 'PY_SUB_004',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find Intersection of Two Lists\n\nInput:\n1 2 3 4\n3 4 5 6\n\nOutput:\n3 4',
        starterCode: `# Write your code here to find intersection of two lists
a = list(map(int, input().split()))
b = list(map(int, input().split()))
pass`,
        explanation: 'Use set intersection to find common elements.'
    },
    {
        id: 'PY_SUB_005',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find All Pairs with Given Sum\n\nInput:\n6\n1 2 3 4 5 6\n7\n\nOutput:\n(1,6) (2,5) (3,4)',
        starterCode: `# Write your code here to find all pairs with given sum
n = int(input())
arr = list(map(int, input().split()))
target = int(input())
pass`,
        explanation: 'Nested loop to find all pairs that sum to target.'
    },
    {
        id: 'PY_SUB_006',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Longest Word in a Sentence\n\nInput:\nPython makes coding interesting\n\nOutput:\ninteresting',
        starterCode: `# Write your code here to find the longest word
s = input().split()
pass`,
        explanation: 'Use max with key=len to find longest word.'
    },
    {
        id: 'PY_SUB_007',
        type: 'coding',
        category: 'python',
        points: 10,
        question: "Print Pascal's Triangle\n\nInput:\n5\n\nOutput:\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1",
        starterCode: `def pascal(n):
    # Write your code here to print Pascal's triangle
    pass

n = int(input())
pascal(n)`,
        explanation: 'Calculate Pascal triangle using binomial coefficients.'
    },
    {
        id: 'PY_SUB_008',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find GCD of Two Numbers\n\nInput:\n24 36\n\nOutput:\n12',
        starterCode: `import math
# Write your code here to find GCD of two numbers
a, b = map(int, input().split())
pass`,
        explanation: 'Use built-in GCD function from math module.'
    },
    {
        id: 'PY_SUB_009',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Count the Number of Words and Characters\n\nInput:\nI love programming\n\nOutput:\nWords: 3 Characters: 18',
        starterCode: `# Write your code here to count words and characters
s = input()
pass`,
        explanation: 'Split for word count, len for character count.'
    },
    {
        id: 'PY_SUB_010',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Sort Dictionary by Values\n\nInput:\na 3 b 1 c 2\n\nOutput:\n{\'b\': 1, \'c\': 2, \'a\': 3}',
        starterCode: `# Write your code here to sort dictionary by values
data = input().split()
pass`,
        explanation: 'Sort dictionary by values using sorted with lambda.'
    },
    {
        id: 'PY_SUB_011',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Count Unique Words in a Sentence\n\nInput:\nPython is easy and Python is powerful\n\nOutput:\n5',
        starterCode: `# Write your code here to count unique words
s = input().lower().split()
pass`,
        explanation: 'Convert to set to get unique words.'
    },
    {
        id: 'PY_SUB_012',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Convert a List into a Dictionary\n\nInput:\na b c\n1 2 3\n\nOutput:\n{\'a\': 1, \'b\': 2, \'c\': 3}',
        starterCode: `# Write your code here to convert list into dictionary
keys = input().split()
values = list(map(int, input().split()))
pass`,
        explanation: 'Zip keys and values together.'
    },
    {
        id: 'PY_SUB_013',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Missing Number in Sequence\n\nInput:\n1 2 4 5 6\n\nOutput:\n3',
        starterCode: `# Write your code here to find missing number in sequence
arr = list(map(int, input().split()))
pass`,
        explanation: 'Check all numbers in range to find missing one.'
    },
    {
        id: 'PY_SUB_014',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find All Duplicates in a List\n\nInput:\n1 2 3 2 4 1 5\n\nOutput:\n1 2',
        starterCode: `# Write your code here to find all duplicates
arr = list(map(int, input().split()))
pass`,
        explanation: 'Find elements that appear more than once.'
    },
    {
        id: 'PY_SUB_015',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Check if a String is Anagram\n\nInput:\nlisten\nsilent\n\nOutput:\nAnagram',
        starterCode: `# Write your code here to check if strings are anagrams
s1 = input()
s2 = input()
pass`,
        explanation: 'Sort both strings and compare.'
    },
    {
        id: 'PY_SUB_016',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Sum of Diagonals of a Square Matrix\n\nInput:\n3\n1 2 3\n4 5 6\n7 8 9\n\nOutput:\nSum: 30',
        starterCode: `# Write your code here to find sum of diagonals
n = int(input())
mat = [list(map(int, input().split())) for _ in range(n)]
pass`,
        explanation: 'Sum both diagonals, subtract center if odd dimension.'
    },
    {
        id: 'PY_SUB_017',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Count Capital Letters in String\n\nInput:\nHelloWorld\n\nOutput:\n2',
        starterCode: `# Write your code here to count capital letters
s = input()
pass`,
        explanation: 'Count uppercase letters using isupper().'
    },
    {
        id: 'PY_SUB_018',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find All Armstrong Numbers in a Range\n\nInput:\n1 500\n\nOutput:\n1 153 370 371 407',
        starterCode: `# Write your code here to find Armstrong numbers in range
a, b = map(int, input().split())
pass`,
        explanation: 'Armstrong number equals sum of digits raised to power of digit count.'
    },
    {
        id: 'PY_SUB_019',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Rotate Array by K Positions\n\nInput:\n5\n1 2 3 4 5\n2\n\nOutput:\n4 5 1 2 3',
        starterCode: `# Write your code here to rotate array by K positions
n = int(input())
arr = list(map(int, input().split()))
k = int(input())
pass`,
        explanation: 'Use slicing to rotate array.'
    },
    {
        id: 'PY_SUB_020',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Most Frequent Character\n\nInput:\nmississippi\n\nOutput:\ni',
        starterCode: `from collections import Counter
# Write your code here to find most frequent character
s = input()
pass`,
        explanation: 'Use Counter.most_common() to find most frequent.'
    },
    {
        id: 'PY_SUB_021',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find Sum of Elements Above Main Diagonal\n\nInput:\n3\n1 2 3\n4 5 6\n7 8 9\n\nOutput:\n11',
        starterCode: `# Write your code here to find sum above main diagonal
n = int(input())
mat = [list(map(int, input().split())) for _ in range(n)]
pass`,
        explanation: 'Sum elements where column > row.'
    },
    {
        id: 'PY_SUB_022',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Merge and Sort Two Lists\n\nInput:\n1 3 5\n2 4 6\n\nOutput:\n1 2 3 4 5 6',
        starterCode: `# Write your code here to merge and sort two lists
a = list(map(int, input().split()))
b = list(map(int, input().split()))
pass`,
        explanation: 'Concatenate and sort lists.'
    },
    {
        id: 'PY_SUB_023',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Remove All Punctuation from String\n\nInput:\nHello, world! Welcome.\n\nOutput:\nHello world Welcome',
        starterCode: `import string
# Write your code here to remove all punctuation
s = input()
pass`,
        explanation: 'Filter out punctuation characters.'
    },
    {
        id: 'PY_SUB_024',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find the Sum of Numbers in a String\n\nInput:\nabc12xyz5\n\nOutput:\n17',
        starterCode: `import re
# Write your code here to find sum of numbers in string
s = input()
pass`,
        explanation: 'Extract numbers using regex and sum them.'
    },
    {
        id: 'PY_SUB_025',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Convert Decimal to Binary Without Built-in\n\nInput:\n10\n\nOutput:\n1010',
        starterCode: `# Write your code here to convert decimal to binary
n = int(input())
pass`,
        explanation: 'Repeatedly divide by 2 and collect remainders.'
    },
    {
        id: 'PY_SUB_026',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Sort Words Alphabetically\n\nInput:\nbanana apple orange\n\nOutput:\napple banana orange',
        starterCode: `# Write your code here to sort words alphabetically
s = input().split()
pass`,
        explanation: 'Sort words lexicographically.'
    },
    {
        id: 'PY_SUB_027',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Remove Duplicate Characters from a String\n\nInput:\nprogramming\n\nOutput:\nprogamin',
        starterCode: `# Write your code here to remove duplicate characters
s = input()
pass`,
        explanation: 'Maintain order while removing duplicates.'
    },
    {
        id: 'PY_SUB_028',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Check Substring Occurrence Count\n\nInput:\nabababa\naba\n\nOutput:\n3',
        starterCode: `# Write your code here to count substring occurrences
s = input()
sub = input()
pass`,
        explanation: 'Check each position for substring match.'
    },
    {
        id: 'PY_SUB_029',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Print All Substrings of a String\n\nInput:\nabc\n\nOutput:\na ab abc b bc c',
        starterCode: `# Write your code here to print all substrings
s = input()
pass`,
        explanation: 'Generate all possible substrings.'
    },
    {
        id: 'PY_SUB_030',
        type: 'coding',
        category: 'python',
        points: 10,
        question: 'Find All Unique Permutations of a String\n\nInput:\nabc\n\nOutput:\nabc acb bac bca cab cba',
        starterCode: `from itertools import permutations
# Write your code here to find all unique permutations
s = input()
pass`,
        explanation: 'Generate permutations and remove duplicates.'
    }
];

const SQL_SUBJECTIVE = [
    {
        id: 'SQL_SUB_001',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Second Highest Salary\n\nTable: Employee(emp_id, name, salary)',
        starterCode: `-- Write your SQL query here to find second highest salary
SELECT `,
        explanation: 'Find maximum salary less than the absolute maximum.'
    },
    {
        id: 'SQL_SUB_002',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Employees Who Earn More Than Their Manager\n\nTable: Employee(emp_id, name, manager_id, salary)',
        starterCode: `-- Write your SQL query here to find employees earning more than their manager
SELECT `,
        explanation: 'Self-join to compare employee salary with manager salary.'
    },
    {
        id: 'SQL_SUB_003',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Duplicate Email IDs\n\nTable: Users(id, email)',
        starterCode: `-- Write your SQL query here to find duplicate email IDs
SELECT `,
        explanation: 'Group by email and find those appearing more than once.'
    },
    {
        id: 'SQL_SUB_004',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Display the nth Highest Salary (e.g., 3rd highest)\n\nTable: Employee(emp_id, name, salary)',
        starterCode: `-- Write your SQL query here to find nth highest salary
SELECT `,
        explanation: 'Count distinct salaries greater than or equal to current.'
    },
    {
        id: 'SQL_SUB_005',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Departments with Average Salary > 50000\n\nTable: Employee(emp_id, name, dept_id, salary)',
        starterCode: `-- Write your SQL query here to find departments with average salary > 50000
SELECT `,
        explanation: 'Group by department and filter with HAVING.'
    },
    {
        id: 'SQL_SUB_006',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve Employees Who Joined in the Last 6 Months\n\nTable: Employee(emp_id, name, join_date)',
        starterCode: `-- Write your SQL query here to find employees joined in last 6 months
SELECT `,
        explanation: 'Use DATE_SUB to find recent joiners.'
    },
    {
        id: 'SQL_SUB_007',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Get Total Salary Paid per Department\n\nTable: Employee(emp_id, name, dept_id, salary)',
        starterCode: `-- Write your SQL query here to get total salary per department
SELECT `,
        explanation: 'Aggregate salary by department.'
    },
    {
        id: 'SQL_SUB_008',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find All Employees Without a Manager\n\nTable: Employee(emp_id, name, manager_id)',
        starterCode: `-- Write your SQL query here to find employees without manager
SELECT `,
        explanation: 'Check for NULL manager_id.'
    },
    {
        id: 'SQL_SUB_009',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Customers Who Have Never Placed an Order\n\nTables: Customers(cust_id, cust_name), Orders(order_id, cust_id)',
        starterCode: `-- Write your SQL query here to find customers with no orders
SELECT `,
        explanation: 'Left join and filter for NULL orders.'
    },
    {
        id: 'SQL_SUB_010',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Top 3 Highest Paid Employees per Department\n\nTable: Employee(emp_id, name, dept_id, salary)',
        starterCode: `-- Write your SQL query here to find top 3 paid employees per department
SELECT `,
        explanation: 'Use window function RANK() to rank within department.'
    },
    {
        id: 'SQL_SUB_011',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Departments Having More Than 5 Employees',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Group and filter with HAVING clause.'
    },
    {
        id: 'SQL_SUB_012',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Employees Who Have the Same Salary',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Group by salary and find duplicates.'
    },
    {
        id: 'SQL_SUB_013',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Employee with the Longest Name',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Sort by name length in descending order.'
    },
    {
        id: 'SQL_SUB_014',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve the 3 Most Recent Orders\n\nTable: Orders(order_id, order_date)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Sort by date descending and limit to 3.'
    },
    {
        id: 'SQL_SUB_015',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Average Salary of Employees per Manager',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Group by manager and calculate average.'
    },
    {
        id: 'SQL_SUB_016',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Get the Name of Employees Whose Salary Is Above the Company Average',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Compare with subquery calculating average.'
    },
    {
        id: 'SQL_SUB_017',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Departments with No Employees\n\nTables: Department(dept_id, dept_name), Employee(emp_id, dept_id)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Left join and find NULL employee references.'
    },
    {
        id: 'SQL_SUB_018',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Total Number of Orders per Customer\n\nTables: Orders(order_id, cust_id)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Count orders grouped by customer.'
    },
    {
        id: 'SQL_SUB_019',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Get the Product with the Highest Price per Category\n\nTables: Products(prod_id, category, price)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Rank products within each category by price.'
    },
    {
        id: 'SQL_SUB_020',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve Employees Hired in the Same Year',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Extract year and group by it.'
    },
    {
        id: 'SQL_SUB_021',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Get Customer Who Spent the Most Money\n\nTables: Orders(order_id, cust_id, amount)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Sum amounts per customer and sort descending.'
    },
    {
        id: 'SQL_SUB_022',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Difference Between Highest and Lowest Salary in Each Department',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Calculate difference between max and min.'
    },
    {
        id: 'SQL_SUB_023',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve Employees Who Share the Same Department and Salary',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Group by both department and salary.'
    },
    {
        id: 'SQL_SUB_024',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Customers Who Ordered All Products\n\nTables: Orders(order_id, cust_id, prod_id), Products(prod_id)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Count distinct products ordered equals total products.'
    },
    {
        id: 'SQL_SUB_025',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve the Longest Tenured Employee per Department',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Rank by earliest join date within department.'
    },
    {
        id: 'SQL_SUB_026',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find Products Never Ordered\n\nTables: Products(prod_id), Orders(order_id, prod_id)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Left join and find products with no orders.'
    },
    {
        id: 'SQL_SUB_027',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Retrieve Departments with the Highest Average Salary',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Calculate average per department and get maximum.'
    },
    {
        id: 'SQL_SUB_028',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Get Employees Working Under More Than One Manager',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Count distinct managers per employee.'
    },
    {
        id: 'SQL_SUB_029',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Cumulative Sum of Salaries by Department',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Use window function for running total.'
    },
    {
        id: 'SQL_SUB_030',
        type: 'coding',
        category: 'sql',
        points: 10,
        question: 'Find the Month with Maximum Sales\n\nTables: Sales(sale_id, sale_date, amount)',
        starterCode: `-- Write your SQL query here
SELECT `,
        explanation: 'Group by month and find maximum total.'
    }
];

// Merge with main database
if (typeof QUESTION_DATABASE !== 'undefined') {
    QUESTION_DATABASE.pythonSubjective = PYTHON_SUBJECTIVE;
    QUESTION_DATABASE.sqlSubjective = SQL_SUBJECTIVE;
}

// Export for standalone use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PYTHON_SUBJECTIVE,
        SQL_SUBJECTIVE
    };
}
