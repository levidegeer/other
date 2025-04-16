# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import random
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Add Jinja2 filter to properly format code
@app.template_filter('code_format')
def code_format(text):
    return text.replace('\n', '<br>')

# All questions from the original code
all_questions = [
    {
        "id": 1,
        "questionText": "Which software development methodology follows a linear and sequential approach, often with clearly defined stages?",
        "options": ["Agile", "Waterfall", "Spiral", "Scrum"],
        "correctAnswer": "Waterfall"
    },
    {
        "id": 2,
        "questionText": "What type of error occurs when the code is grammatically correct and running smoothly, but does not convey the intended meaning of the program?",
        "options": ["Logic Error", "Runtime Error", "Semantic Error", "Syntax Error"],
        "correctAnswer": "Logic Error"
    },
    {
        "id": 3,
        "questionText": "Which of the following is the correct hexadecimal representation for the binary number 110011?",
        "options": ["66", "CC", "33", "99"],
        "correctAnswer": "33"
    },
    {
        "id": 4,
        "questionText": "What is the main benefit of cloud computing?",
        "options": ["Cost-efficiency", "Local infrastructure management", "Physical presence requirement", "Scalability and flexibility"],
        "correctAnswer": "Scalability and flexibility"
    },
    {
        "id": 5,
        "questionText": "What is SQL injection?",
        "options": [
            "A security vulnerability caused by inserting malicious SQL code through user input",
            "A technique for securely executing SQL queries with user input",
            "A process of cleaning and validating user input against SQL syntax",
            "A method for preventing unauthorized access to databases"],
        "correctAnswer": "A security vulnerability caused by inserting malicious SQL code through user input"
    },
    {
        "id": 6,
        "questionText": """x = 7
        if (x % 2 == 0):
          print("Even")
        elif (x % 3 == 0):
          print("Multiple of 3")
        else:
          print("Neither")

        What is the output to the above code?""",
        "options": ["Even", "Neither", "Error: Invalid operator", "Multiple of 3"],
        "correctAnswer": "Neither"
    },
    {
        "id": 7,
        "questionText": "Why is it essential to understand the requirements for constructing new objects?",
        "options": [
            "To complicate code readability",
            "To reduce the risk of errors and unexpected behavior",
            "To minimize documentation usage",
            "To introduce inconsistencies in code"],
        "correctAnswer": "To reduce the risk of errors and unexpected behavior"
    },
    {
        "id": 8,
        "questionText": "What is the term for delivering media content in real-time without downloading it?",
        "options": ["Content Delivery Networks (CDNs)", "Relational databases", "Streaming services", "File hosting"],
        "correctAnswer": "Streaming services"
    },
    {
        "id": 9,
        "questionText": "What is the purpose of order of operation in software programming?",
        "options": [
            "how many mathematical operations are required",
            "which mathematical operation to perform first",
            "which mathematical operations are valid",
            "which mathematical operation are NOT valid"],
        "correctAnswer": "which mathematical operation to perform first"
    },
    {
        "id": 10,
        "questionText": "Which of the following are an example of multi-factor authentication?",
        "options": [
            "Asking for a code sent to a phone number",
            "Answering a security question",
            "Solving a Captcha puzzle",
            "Asking for the password to be entered twice"],
        "correctAnswer": "Asking for a code sent to a phone number"
    },
    {
        "id": 11,
        "questionText": "What is the purpose of error recovery in handling runtime errors?",
        "options": [
            "To teach the program to automatically fix runtime errors",
            "To prevent the occurrence of runtime errors",
            "To provide alternative paths or fallback actions when runtime errors occur",
            "To display error messages to the user"],
        "correctAnswer": "To provide alternative paths or fallback actions when runtime errors occur"
    },
    {
        "id": 12,
        "questionText": "How can software defects contribute to security vulnerabilities?",
        "options": [
            "By ensuring the confidentiality, integrity, and availability of software systems",
            "By improving the performance and usability of software systems",
            "By facilitating easier integration with other software components",
            "By introducing coding errors or design flaws that can be exploited by attackers"],
        "correctAnswer": "By introducing coding errors or design flaws that can be exploited by attackers"
    },
    {
        "id": 13,
        "questionText": "How can version control systems be useful in documentation?",
        "options": [
            "They track changes and provide a revision history",
            "They eliminate the need for documentation",
            "They can automatically generate documentation",
            "They restrict access to documentation files"],
        "correctAnswer": "They track changes and provide a revision history"
    },
    {
        "id": 14,
        "questionText": "The phase in the SDLC (system design life cycle) where the system is monitored, maintained, and updated is called:",
        "options": ["Testing", "Implementation", "Maintenance", "Planning"],
        "correctAnswer": "Maintenance"
    },
    {
        "id": 15,
        "questionText": "Which strategy involves utilizing online resources and collaborating with colleagues to find solutions?",
        "options": ["Test assumptions", "Debugging techniques", "Research and collaborate", "Divide and conquer"],
        "correctAnswer": "Research and collaborate"
    },
    {
        "id": 16,
        "questionText": "What is the purpose of recognizing patterns in loop variables within nested loops?",
        "options": ["To create infinite loops", "To simplify the code", "To introduce random variables", "To make the code more complex"],
        "correctAnswer": "To simplify the code"
    },
    {
        "id": 17,
        "questionText": "The documentation for a class states that the constructor requires two parameters: name and age. Which of the following statements is true?",
        "options": ["The documentation is incomplete because it does not specify the data types of the parameters.", 
                   "The documentation does not provide any information about the parameter requirements.", 
                   "The parameters name and age are optional.", 
                   "The parameters name and age are required."],
        "correctAnswer": "The parameters name and age are required."
    },
    {
        "id": 18,
        "questionText": "What is the purpose of default parameters in functions?",
        "options": ["To provide values if no explicit argument is provided", 
                   "To prevent any changes to parameter values", 
                   "To ensure that parameters are of a specific data type", 
                   "To force all parameters to be mandatory"],
        "correctAnswer": "To provide values if no explicit argument is provided"
    },
    {
        "id": 19,
        "questionText": "What does image transformation involve in graphics development?",
        "options": ["Creating image animations", 
                   "Adjusting image positions, scaling, or rotation", 
                   "Manipulating image colors", 
                   "Changing image file formats"],
        "correctAnswer": "Adjusting image positions, scaling, or rotation"
    },
    {
        "id": 20,
        "questionText": "What is the primary advantage of binary search over linear search?",
        "options": ["Binary search works with unsorted data.", 
                   "Binary search uses less memory.", 
                   "Binary search is faster for large datasets.", 
                   "Binary search is simpler to implement."],
        "correctAnswer": "Binary search is faster for large datasets."
    },
    {
        "id": 21,
        "questionText": "Which of the following statements is true about interfaces?",
        "options": ["An interface can have private methods.", 
                   "An interface can define constants.", 
                   "An interface can have constructors.", 
                   "An interface can have instance variables."],
        "correctAnswer": "An interface can define constants."
    },
    {
        "id": 22,
        "questionText": "What are language standards and style guides?",
        "options": ["Best practices recommended by the programming community", 
                   "Guidelines enforced by code editors", 
                   "Guidelines set by individual developers", 
                   "Standards enforced by government regulatory bodies"],
        "correctAnswer": "Best practices recommended by the programming community"
    },
    {
        "id": 23,
        "questionText": "Which sorting algorithm is known for its divide-and-conquer approach, splitting the array into smaller subarrays?",
        "options": ["Bubble sort", "Selection sort", "Linear search", "Merge sort"],
        "correctAnswer": "Merge sort"
    },
    {
        "id": 24,
        "questionText": "Which data type should be used to store a person's email address?",
        "options": ["string", "float", "boolean", "integer"],
        "correctAnswer": "string"
    },
    {
        "id": 25,
        "questionText": "Which phase of the SDLC (system design life cycle) involves gathering information about the current system and its problems?",
        "options": ["Development", "Design", "Maintenance", "Analysis"],
        "correctAnswer": "Analysis"
    },
    {
        "id": 26,
        "questionText": "What is the purpose of the checkout/switch command in Git?",
        "options": ["To navigate between different branches or commit states", 
                   "To submit pull requests for contributions", 
                   "To revert the code to a previous state", 
                   "To create a personal copy of a repository"],
        "correctAnswer": "To navigate between different branches or commit states"
    },
    {
        "id": 27,
        "questionText": "How would you represent the number 15 using only zeroes and ones?",
        "options": ["1111", "0011", "1100", "0110"],
        "correctAnswer": "1111"
    },
    {
        "id": 28,
        "questionText": "What is the primary factor contributing to platform independence in interpreted code?",
        "options": ["The presence of a compiler", 
                   "Real-time code translation", 
                   "The use of standalone executables", 
                   "The interpreter handling platform-specific details"],
        "correctAnswer": "The interpreter handling platform-specific details"
    },
    {
        "id": 29,
        "questionText": "What is the primary reason to avoid writing your own function when a standard library function exists for the task?",
        "options": ["To ensure that your code is faster", 
                   "To avoid errors", 
                   "To avoid reinventing the wheel and use well-tested solutions", 
                   "To improve the aesthetics of your code"],
        "correctAnswer": "To avoid reinventing the wheel and use well-tested solutions"
    },
    {
        "id": 30,
        "questionText": "What is the purpose of FERPA?",
        "options": ["To protect sensitive patient health information", 
                   "To regulate the sharing of cyber threat information", 
                   "To ensure the privacy of student education records", 
                   "To protect the online privacy of children"],
        "correctAnswer": "To ensure the privacy of student education records"
    },
    {
        "id": 31,
        "questionText": "If a = 5 and b = 3, what is the value of the expression 'a % b'",
        "options": ["0", "1", "3", "2"],
        "correctAnswer": "2"
    },
    {
        "id": 32,
        "questionText": "Which of the following best describes the concept of space complexity?",
        "options": ["It calculates the efficiency of data compression techniques.", 
                   "It measures the physical size of the data stored.", 
                   "It determines the number of operations needed to manipulate data", 
                   "It quantifies the time complexity of an algorithm."],
        "correctAnswer": "It determines the number of operations needed to manipulate data"
    },
    {
        "id": 33,
        "questionText": "What are the 5 Project Management phases in order?",
        "options": ["Initiation,Planning,Execution,Monitoring and Controlling,Closing", 
                   "Execution,Initiation,Monitoring and Controlling,Closing,Planning", 
                   "Closing,Execution,Initiation,Monitoring and Controlling,Planning", 
                   "Monitoring and Controlling,Planning,Closing,Execution,Initiation"],
        "correctAnswer": "Initiation,Planning,Execution,Monitoring and Controlling,Closing"
    },
    {
        "id": 34,
        "questionText": "Which of the following correctly arranges the units of storage in increasing order of size?",
        "options": ["Bit, Byte, Kilobyte, Megabyte, Terabyte, Gigabyte", 
                   "Bit, Byte, Kilobyte, Megabyte, Gigabyte, Terabyte", 
                   "Kilobyte, Byte, Bit, Megabyte, Terabyte, Gigabyte", 
                   "Byte, Bit, Terabyte, Kilobyte, Megabyte, Gigabyte"],
        "correctAnswer": "Bit, Byte, Kilobyte, Megabyte, Gigabyte, Terabyte"
    },
    {
        "id": 35,
        "questionText": "What is the appropriate data type for storing a person's address?",
        "options": ["integer", "boolean", "string", "character"],
        "correctAnswer": "string"
    },
    {
        "id": 36,
        "questionText": "x = \"false\" declares what data type?",
        "options": ["boolean", "integer", "string", "double"],
        "correctAnswer": "string"
    },
    {
        "id": 37,
        "questionText": "If you are writing a program to determine if a number is even, which of the following data types would allow a true response to be reported when the number is even?",
        "options": ["string", "boolean", "double", "numeric"],
        "correctAnswer": "boolean"
    },
    {
        "id": 38,
        "questionText": "Which accessibility feature is important for users with visual disabilities to navigate and understand web content?",
        "options": ["Captions for multimedia content", 
                   "Logical tab order", 
                   "Consistent navigation structure across all pages", 
                   "Audio descriptions for multimedia content"],
        "correctAnswer": "Audio descriptions for multimedia content"
    },
    {
        "id": 39,
        "questionText": "To ensure that your text appears exactly as intended when executing your program, in what container should it be encapsulated?",
        "options": ["Angle braces", "Curly braces", "Quotation marks", "Square brackets"],
        "correctAnswer": "Quotation marks"
    },
    {
        "id": 40,
        "questionText": "What does input validation involve in software development?",
        "options": ["Generating unique hash values for data integrity checks", 
                   "Verifying and validating user input to prevent malicious input", 
                   "Encrypting sensitive data during transmission", 
                   "Ensuring software has the latest updates and patches"],
        "correctAnswer": "Verifying and validating user input to prevent malicious input"
    },
    {
        "id": 41,
        "questionText": "int product = 1;\nfor (int i = 1; i <= 3; i++) {\n    for (int j = 1; j <= i; j++) {\n        product *= i * j;\n    }\n}\nSystem.out.println(product);\nWhat will be the output of the above code?",
        "options": ["25", "4320", "1296", "144"],
        "correctAnswer": "1296"
    },
    {
        "id": 42,
        "questionText": "What is the primary purpose of self-documenting code?",
        "options": ["To make the code shorter", 
                   "To eliminate the need for documentation", 
                   "To generate user-level documentation", 
                   "To improve code readability and understanding"],
        "correctAnswer": "To improve code readability and understanding"
    },
    {
        "id": 43,
        "questionText": "Which of the following is NOT a valid data type?",
        "options": ["Float", "Variable", "String", "Boolean"],
        "correctAnswer": "Variable"
    },
    {
        "id": 44,
        "questionText": "Which regulation aims to enhance cybersecurity by allowing the sharing of cyber threat information between private companies and the government?",
        "options": ["FERPA", "COPPA", "HIPAA", "CISPA"],
        "correctAnswer": "CISPA"
    },
    {
        "id": 45,
        "questionText": "What is the primary purpose of a class in object-oriented programming?",
        "options": ["To control the flow of a program.", 
                   "To encapsulate unrelated functions.", 
                   "To define the data and behavior of an object.", 
                   "To store variables and perform calculations."],
        "correctAnswer": "To define the data and behavior of an object."
    },
    {
        "id": 46,
        "questionText": "public class Circle {\n    private double radius;\n\n    public Circle(double radius) {\n        this.radius = radius;\n    }\n    \n    public double calculateArea() {\n        return Math.PI * radius * radius;\n    }\n}\nWhat is the access modifier used for the radius variable in the code snippet?",
        "options": ["return", "private", "this", "public"],
        "correctAnswer": "private"
    },
    {
        "id": 47,
        "questionText": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n    \n    def calculate_area(self):\n        return self.width * self.height\nWhat is the purpose of the code snippet?",
        "options": ["Accessing the width and height attributes of a rectangle object", 
                   "Defining a user-defined class named Rectangle with an area calculation method", 
                   "Defining a function to calculate the area of a rectangle", 
                   "Initializing the width and height of a rectangle object"],
        "correctAnswer": "Defining a user-defined class named Rectangle with an area calculation method"
    },
    {
        "id": 48,
        "questionText": "What is the main difference between interpreted and compiled code?",
        "options": ["Interpreted code is platform-specific, while compiled code is portable.", 
                   "Interpreted code requires compilation before execution, while compiled code does not.", 
                   "Interpreted code is executed line by line, while compiled code is executed as a whole.", 
                   "Interpreted code runs faster than compiled code."],
        "correctAnswer": "Interpreted code is executed line by line, while compiled code is executed as a whole."
    },
    {
        "id": 49,
        "questionText": "Which statement accurately defines instance variables in object-oriented programming?",
        "options": ["Instance variables are accessed using the class name.", 
                   "Instance variables are shared among all instances of a class.", 
                   "Instance variables are initialized at the class level.", 
                   "Instance variables are unique to each instance of a class and store specific data."],
        "correctAnswer": "Instance variables are unique to each instance of a class and store specific data."
    },
    {
        "id": 50,
        "questionText": "What does O(n^2) complexity indicate in the context of data manipulation?",
        "options": ["Linear time complexity.", "Quadratic time complexity.", "Constant time complexity.", "Exponential time complexity."],
        "correctAnswer": "Quadratic time complexity."
    },
    {
        "id": 51,
        "questionText": "What is the value of the expression (4 + 2) * 3 % 2?",
        "options": ["7.5", "4", "6", "0"],
        "correctAnswer": "0"
    },
    {
        "id": 52,
        "questionText": "If x = 5 and y = 2, what is the value of the expression 'x ** y'?",
        "options": ["25", "8", "10", "7"],
        "correctAnswer": "25"
    },
    {
        "id": 53,
        "questionText": "sum = 0\nfor i in range(1, 4):\n    for j in range(i, 4):\n        sum += i + j\nprint(sum)\n\nWhat will be the output of the above code?",
        "options": ["16", "24", "10", "15"],
        "correctAnswer": "24"
    },
    {
        "id": 54,
        "questionText": "What does the == symbol in programming mean?",
        "options": ["division", "assignment", "equal", "subtraction"],
        "correctAnswer": "equal"
    },
    {
        "id": 55,
        "questionText": "In Big-O notation, what does O(n^2) represent?",
        "options": ["Quadratic time complexity.", "Constant time complexity.", "Linear time complexity.", "Logarithmic time complexity."],
        "correctAnswer": "Quadratic time complexity."
    },
    {
        "id": 56,
        "questionText": "What is the recommended approach to identify errors in code by breaking it down into smaller parts and testing each part individually?",
        "options": ["Use a debugger", "Print statements", "Code review", "Divide and conquer"],
        "correctAnswer": "Divide and conquer"
    },
    {
        "id": 57,
        "questionText": "Which process involves systematically executing test cases using automated tools to detect errors?",
        "options": ["Collaborative Debugging", "Code Review", "Profiling", "Automated Testing"],
        "correctAnswer": "Automated Testing"
    },
    {
        "id": 58,
        "questionText": "What is the purpose of method overriding in inheritance?",
        "options": ["Hiding methods from the superclass", 
                   "Creating new methods in the subclass", 
                   "Preventing inheritance from the superclass", 
                   "Providing a specific implementation in the subclass"],
        "correctAnswer": "Providing a specific implementation in the subclass"
    },
    {
        "id": 59,
        "questionText": "Which term describes the operations involved in reading data from and writing data to files in a program?",
        "options": ["File Input/output (I/O)", "Data formatting", "Input validation", "Error handling"],
        "correctAnswer": "File Input/output (I/O)"
    },
    {
        "id": 60,
        "questionText": "What does the \"Fair Use\" doctrine in copyright law allow?",
        "options": ["Unlimited use of copyrighted material", 
                   "Limited use of copyrighted material without permission for specific purposes", 
                   "Public domain distribution of copyrighted material", 
                   "Complete ownership of copyrighted material"],
        "correctAnswer": "Limited use of copyrighted material without permission for specific purposes"
    },
    {
        "id": 61,
        "questionText": "What is the purpose of alternative text for images in web accessibility?",
        "options": ["To enhance search engine optimization", 
                   "To prevent image theft", 
                   "To improve website performance", 
                   "To provide a description for screen reader users"],
        "correctAnswer": "To provide a description for screen reader users"
    },
    {
        "id": 62,
        "questionText": "Which of the following Boolean expressions are equivalent to the expression num <=15",
        "options": ["NOT num=15", "NOT num<15", "num<15 AND num=15", "num<15 OR num=15"],
        "correctAnswer": "num<15 OR num=15"
    },
    {
        "id": 63,
        "questionText": "What is one key difference between an abstract class and an interface?",
        "options": ["Abstract classes cannot be instantiated on their own.", 
                   "Abstract classes can have concrete methods.", 
                   "Abstract classes cannot have abstract methods.", 
                   "Interfaces can have instance variables"],
        "correctAnswer": "Abstract classes can have concrete methods."
    },
    {
        "id": 64,
        "questionText": "Which of the following is a potential issue when using floating-point numbers in arithmetic operations?",
        "options": ["Loss of precision due to rounding errors", 
                   "Difficulty in representing fractional numbers", 
                   "Inability to perform arithmetic operations", 
                   "Limited range of representable values"],
        "correctAnswer": "Loss of precision due to rounding errors"
    },
    {
        "id": 65,
        "questionText": "What is a constructor in object-oriented programming languages responsible for?",
        "options": ["Destroying objects", 
                   "Controlling object inheritance", 
                   "Managing object lifecycles", 
                   "Initializing newly created objects"],
        "correctAnswer": "Initializing newly created objects"
    },
    {
        "id": 66,
        "questionText": "Regular updates and bug fixes contribute to an app's success by:",
        "options": ["Increasing the app's download size", 
                   "Reducing user engagement and feedback", 
                   "Building user trust and maintaining functionality over time", 
                   "Releasing a completely new app version"],
        "correctAnswer": "Building user trust and maintaining functionality over time"
    },
    {
        "id": 67,
        "questionText": "How can you protect yourself from phishing attacks?",
        "options": ["Disabling security features on your devices", 
                   "Verifying the legitimacy of emails and websites", 
                   "Sharing personal information through email", 
                   "Clicking on links without verifying their source"],
        "correctAnswer": "Verifying the legitimacy of emails and websites"
    },
    {
        "id": 68,
        "questionText": "Which of the following best describes the relationship between a class and an object?",
        "options": ["A class is an instance of an object.", 
                   "An object is an implementation of a class.", 
                   "An object is a blueprint for creating a class.", 
                   "A class is a subset of an object."],
        "correctAnswer": "An object is an implementation of a class."
    },
    {
        "id": 69,
        "questionText": "Given the following lines of code:\n\nx = 10\ny = 3\nresult = x // y + 2\n\nWhat is the value of 'result'",
        "options": ["4", "5.33333", "5", "3.0"],
        "correctAnswer": "5"
    },
    {
        "id": 70,
        "questionText": "Which of the following expressions is evaluated first in this expression, 4 + 8 / 2 * 3 - 5, according to the precedence of operations?",
        "options": ["Subtraction", "Multiplication", "Division", "Addition"],
        "correctAnswer": "Division"
    },
    {
        "id": 71,
        "questionText": "What is the purpose of hashing in software development?",
        "options": ["To authenticate users during the login process", 
                   "To encrypt sensitive data during transmission", 
                   "To convert data into a fixed-length string of characters", 
                   "To ensure secure communication between software components"],
        "correctAnswer": "To convert data into a fixed-length string of characters"
    },
    {
        "id": 72,
        "questionText": "Which regulation protects the privacy and personal data of European Union residents?",
        "options": ["PCI DSS", "COPPA", "GDPR", "HIPAA"],
        "correctAnswer": "GDPR"
    },
    {
        "id": 73,
        "questionText": "Which one of these units are larger than a gigabyte?",
        "options": ["Kilobyte", "Terabyte", "Nibble", "Megabyte"],
        "correctAnswer": "Terabyte"
    },
    {
        "id": 74,
        "questionText": "What is a \"paywall\" in app monetization?",
        "options": ["A type of ad format used in apps.", 
                   "A strategy to remove ads from free apps.", 
                   "A tool for managing app subscriptions.", 
                   "A feature that blocks access to certain content unless payment is made."],
        "correctAnswer": "A feature that blocks access to certain content unless payment is made."
    },
    {
        "id": 75,
        "questionText": "What role does a build system play in continuous integration and deployment?",
        "options": ["Ensuring code quality through automated testing and code analysis", 
                   "Enforcing version control policies and branching strategies", 
                   "Monitoring server performance and optimizing resource utilization", 
                   "Managing project documentation and generating API references"],
        "correctAnswer": "Ensuring code quality through automated testing and code analysis"
    },
    {
        "id": 76,
        "questionText": "In the context of web APIs, what does REST stand for?",
        "options": ["Remote Execution and Service Transfer", 
                   "Rapid Elastic Service Transfer", 
                   "Representational State Transfer", 
                   "Responsive State Transfer"],
        "correctAnswer": "Representational State Transfer"
    },
    {
        "id": 77,
        "questionText": "Which of the following best describes data sanitization?",
        "options": ["Converting user input to a different data type", 
                   "Ensuring user input is free from malicious code or special characters", 
                   "Removing leading or trailing whitespaces from user input", 
                   "Encrypting user input for secure storage"],
        "correctAnswer": "Ensuring user input is free from malicious code or special characters"
    },
    {
        "id": 78,
        "questionText": "What is the primary purpose of a two-dimensional array?",
        "options": ["To store multiple elements of different types", 
                   "To perform mathematical operations on numeric data", 
                   "To represent a matrix-like structure with rows and columns", 
                   "To iterate over a single-dimensional array"],
        "correctAnswer": "To represent a matrix-like structure with rows and columns"
    },
    {
        "id": 79,
        "questionText": "What is a good approach to a message that looks like phishing?",
        "options": ["Do not reply or press any links.", 
                   "Reply to the message", 
                   "Press the link they sent", 
                   "Fill out all the info they ask for"],
        "correctAnswer": "Do not reply or press any links."
    },
    {
        "id": 80,
        "questionText": "In programming, a constant is a variable that remains unchanged throughout the program or its execution.\nHow can you identify that a variable is designated as a constant?",
        "options": ["There variable will be declared using snake_case notation.", 
                   "The variable will be declared using camelCase notation.", 
                   "The variable will be declared using all capital letters.", 
                   "There will be a comment to the right side of the variable declartion."],
        "correctAnswer": "The variable will be declared using all capital letters."
    },
    {
        "id": 81,
        "questionText": "What is the objective of \"phishing\"?",
        "options": ["To allow only open-source code to be taken", 
                   "To hack into a users personal account", 
                   "To trick someone into divulging secure and/or personal information", 
                   "To allow network users to openly exchange information"],
        "correctAnswer": "To trick someone into divulging secure and/or personal information"
    },
    {
        "id": 82,
        "questionText": "What is the value of the expression \"x += 5\" if x is initially 10?",
        "options": ["10", "5", "15", "20"],
        "correctAnswer": "15"
    },
    {
        "id": 83,
        "questionText": "While x is not equal to 1\n    Do some tasks\nEnd While\nWhen do you get OUT of this loop?",
        "options": [
            "When x is larger than 1",
            "When x is assigned -1",
            "When x is assigned 1",
            "When x is larger than 0"],
        "correctAnswer": "When x is assigned 1"
    },
    {
        "id": 84,
        "questionText": "What role does a build system play in managing project dependencies?",
        "options": [
            "Resolving conflicts between different versions of software libraries",
            "Analyzing runtime behavior and memory usage of software applications",
            "Enforcing coding conventions and style guidelines",
            "Ensuring secure communication between client and server components"],
        "correctAnswer": "Resolving conflicts between different versions of software libraries"
    },
    {
        "id": 85,
        "questionText": "What is the purpose of a reference variable in object-oriented programming?",
        "options": [
            "To execute methods in a class",
            "To store the memory address of an object",
            "To define a class",
            "To access static members in a class"],
        "correctAnswer": "To store the memory address of an object"
    },
    {
        "id": 86,
        "questionText": "How is object instantiation different from class declaration?",
        "options": [
            "Object instantiation creates instances of a class, while class declaration defines the structure and behavior of the class.",
            "Object instantiation combines multiple classes into one, while class declaration creates instances of the class.",
            "Object instantiation and class declaration are the same concepts.",
            "Object instantiation is the process of creating a new class, while class declaration defines the properties and methods."],
        "correctAnswer": "Object instantiation creates instances of a class, while class declaration defines the structure and behavior of the class."
    },
    {
        "id": 87,
        "questionText": "What is one reason encapsulation is important in object-oriented programming?",
        "options": [
            "Exposes all internal details of an object.",
            "Protects an object's internal state (data)",
            "Deletes objects from memory",
            "Creates instances of a class"],
        "correctAnswer": "Protects an object's internal state (data)"
    },
    {
        "id": 88,
        "questionText": "Which of the following is a common interpreted programming language?",
        "options": ["Rust", "Python", "C", "C++"],
        "correctAnswer": "Python"
    },
    {
        "id": 89,
        "questionText": "What is the purpose of test-driven development (TDD)?",
        "options": [
            "To ensure the program meets all the specified requirements",
            "To provide a detailed user manual for the program",
            "To automate the testing process for the program",
            "To focus on writing tests before writing the actual code"],
        "correctAnswer": "To focus on writing tests before writing the actual code"
    },
    {
        "id": 90,
        "questionText": "What is the primary purpose of shader programming in graphics development?",
        "options": [
            "Creating responsive graphics",
            "Optimizing graphics performance",
            "Manipulating graphics at a pixel level for advanced visual effects",
            "Manipulating image colors"],
        "correctAnswer": "Manipulating graphics at a pixel level for advanced visual effects"
    },
    {
        "id": 91,
        "questionText": "Why is visualizing important before writing code?",
        "options": [
            "It aids in understanding the problem and planning the solution.",
            "It helps improve typing speed and accuracy.",
            "It allows programmers to skip the planning phase.",
            "It speeds up the code execution process."],
        "correctAnswer": "It aids in understanding the problem and planning the solution."
    },
    {
        "id": 92,
        "questionText": "What is the role of try-catch blocks in error handling?",
        "options": [
          "They have no impact on error handling",
          "They ensure error-free code execution",
          "They handle exceptions in a controlled manner",
          "They provide a user-friendly display of error messages"],
        "correctAnswer": "They handle exceptions in a controlled manner"
    },
    {
        "id": 93,
        "questionText": "Which of the following is NOT a benefit of Encapsulation:",
        "options": [
          "Security via controlling access to an object's attributes",
          "The ability to change the internal implementation without affecting the external code",
          "Code reusability through method overloading and overriding",
          "Modularity that makes the code easier to manage and maintain"],
        "correctAnswer": "Code reusability through method overloading and overriding"
    },
    {
        "id": 94,
        "questionText": "Which of the following is not an internet connection type?",
        "options": ["Smartphone", "Bluetooth", "DSL", "Fiber-optic"],
        "correctAnswer": "Bluetooth"
    },
    {
        "id": 95,
        "questionText": "Which naming convention is commonly used for Python variables and functions?",
        "options": ["snake_case", "PascalCase", "camelCase", "kebab-case"],
        "correctAnswer": "snake_case"
    },
    {
        "id": 96,
        "questionText": "What potential challenges may arise when decomposing a large programming problem?",
        "options": [
          "Eliminating the need for documentation and testing",
          "Ensuring that different components work well together and communicate properly.",
          "Determining the optimal programming language to be used",
          "Managing the project budget effectively"],
        "correctAnswer": "Ensuring that different components work well together and communicate properly."
    },
    {
        "id": 97,
        "questionText": "Match the decimal number on the LEFT to the equivalent hexadecimal representation on the RIGHT.\n\n29\n58\n128\n255",
        "options": [
          "1B, 38, 80, FF",
          "1C, 3A, 81, FE",
          "2D, 39, 82, FA",
          "1A, 36, 79, EE"],
        "correctAnswer": "1B, 38, 80, FF"
    },
    {
        "id": 98,
        "questionText": "Which of the following is a recommended practice for using whitespace in code?",
        "options": [
          "Use excessive whitespace to make the code look longer",
          "Utilize whitespace effectively to enhance code readability",
          "Avoid using whitespace as it adds unnecessary characters",
          "Randomly add whitespace for aesthetic purposes"],
        "correctAnswer": "Utilize whitespace effectively to enhance code readability"
    },
    {
        "id": 99,
        "questionText": "In which data structure can keys be of any data type?",
        "options": ["Queue", "Array", "Linked list", "Hash map"],
        "correctAnswer": "Hash map"
    },
    {
        "id": 100,
        "questionText": "Determine the highest precedence of operations in this example: 10 + 12 * 5 % 3 - 2.",
        "options": ["Addition", "Subtraction", "Multiplication", "Modulo"],
        "correctAnswer": "Multiplication"
    },
    {
        "id": 101,
        "questionText": "How can input filtering and sanitization libraries assist in input sanitization?",
        "options": [
          "By encrypting user input before processing",
          "By automating the process of validating and cleaning user input",
          "By generating secure encryption keys for user input",
          "By removing all user input to prevent security issues"],
        "correctAnswer": "By automating the process of validating and cleaning user input"
    },
    {
        "id": 102,
        "questionText": "What is the purpose of the catch block in exception handling?",
        "options": [
          "To exit the program abruptly",
          "To throw an exception",
          "To handle and process a caught exception",
          "To ignore the caught exception"],
        "correctAnswer": "To handle and process a caught exception"
    },
    {
        "id": 103,
        "questionText": "What is the primary use of Remote Desktop Services (RDS)?",
        "options": [
          "Access and control of remote desktops",
          "Secure remote access to networks",
          "Virtualized computing resources",
          "Delivery of software applications"],
        "correctAnswer": "Access and control of remote desktops"
    },
    {
        "id": 104,
        "questionText": "The phase in the SDLC (System Design Life Cycle) where requirements are gathered and analyzed is called:",
        "options": ["Design", "Analysis", "Development", "Testing"],
        "correctAnswer": "Analysis"
    },
    {
        "id": 105,
        "questionText": "What is a user-defined class?",
        "options": [
          "A class used for unit testing purposes",
          "A class provided by the programming language's standard library",
          "A class created by the user or developer",
          "A class with restricted access permissions"],
        "correctAnswer": "A class created by the user or developer"
    },
    {
        "id": 106,
        "questionText": "Which of the following is the best description of keylogging?",
        "options": [
          "A software that can track every key typed in a keyboard",
          "A computer hardware part that holds the key based input",
          "Expanding the memory space on a computer",
          "The process of saving more passwords"],
        "correctAnswer": "A software that can track every key typed in a keyboard"
    },
    {
        "id": 107,
        "questionText": "Using simple symbols to represent more complicated information is a definition for what idea?",
        "options": ["Polymorphism", "Encapsulation", "Abstraction", "Inheritance"],
        "correctAnswer": "Abstraction"
    },
    {
        "id": 108,
        "questionText": "When performing arithmetic operations on integers, what is the potential issue to be aware of?",
        "options": ["Rounding errors", "Overflow or underflow", "Precision loss", "Type conversion errors"],
        "correctAnswer": "Overflow or underflow"
    },
    {
        "id": 109,
        "questionText": "What does the 'Extract Method' refactoring technique involve?",
        "options": [
          "Adding comments to the code",
          "Replacing methods with inline code",
          "Breaking down long, complex methods into smaller pieces",
          "Combining multiple methods into one"],
        "correctAnswer": "Breaking down long, complex methods into smaller pieces"
    },
    {
        "id": 110,
        "questionText": "Which of the following is an example of O(log n) time complexity?",
        "options": [
          "Bubble sort algorithm",
          "Linear search algorithm",
          "Binary search algorithm",
          "Insertion sort algorithm"],
        "correctAnswer": "Binary search algorithm"
    },
    {
        "id": 111,
        "questionText": "for (int i = 0; i <= 10; i += 2) {\n    System.out.print(i + ' ');\n}\n\nWhat will be the output of the above code snippet?",
        "options": [
          "0 2 4 6 8",
          "0 2 4 6 8 10",
          "0 1 2 3 4 5 6 7 8 9 10",
          "1 3 5 7 9"],
        "correctAnswer": "0 2 4 6 8 10"
    },
    {
        "id": 112,
        "questionText": "What kind of inputs should be considered when designing integration tests?",
        "options": [
          "Only valid and expected inputs",
          "Both valid and invalid inputs, including edge cases and unexpected inputs",
          "Only invalid inputs to stress-test the system",
          "Randomly chosen inputs"],
        "correctAnswer": "Both valid and invalid inputs, including edge cases and unexpected inputs"
    },
    {
        "id": 113,
        "questionText": "What is the purpose of a constructor in a class?",
        "options": [
          "To provide custom methods for objects.",
          "To initialize objects when they are created.",
          "To access private members of a class.",
          "To destroy objects when they are no longer needed."],
        "correctAnswer": "To initialize objects when they are created."
    },
    {
        "id": 114,
        "questionText": "What is the best way to increase password security?",
        "options": [
          "Include symbols such as $, *, !",
          "Use the same password across multiple accounts",
          "Make the password longer and more complex",
          "Shorter passwords for easy memorization"],
        "correctAnswer": "Make the password longer and more complex"
    },
    {
        "id": 115,
        "questionText": "What is the main purpose of inheritance in object-oriented programming?",
        "options": [
          "Method abstraction",
          "Code reuse and extensibility",
          "Data encapsulation",
          "Polymorphism"],
        "correctAnswer": "Code reuse and extensibility"
    },
    {
        "id": 116,
        "questionText": "How many bytes are in a kilobyte?",
        "options": ["1024", "1000", "1 000 000", "1 048 576"],
        "correctAnswer": "1024"
    },
    {
        "id": 117,
        "questionText": "What does the acronym API stand for in software development?",
        "options": [
          "Application Program Interface",
          "Automated Programming Interface",
          "Application Programming Intranet",
          "Advanced Program Interaction"],
        "correctAnswer": "Application Program Interface"
    },
    {
        "id": 118,
        "questionText": "What is the purpose of merging in version control?",
        "options": [
          "Integrating changes from one branch into another",
          "Keeping changes isolated from the main codebase",
          "Reviewing code changes made by others",
          "Creating independent copies of repositories"],
        "correctAnswer": "Integrating changes from one branch into another"
    },
    {
        "id": 119,
        "questionText": "Imagine a guest at a restaurant. The waiter comes and takes the guest's order and takes it to the chef to cook the food. Then, the waiter brings the food to the guest's table. In this example, which of the following is like an API?",
        "options": ["The chef", "The restaurant", "The guest", "The waiter"],
        "correctAnswer": "The waiter"
    },
    {
        "id": 120,
        "questionText": "Which security standard is established to protect cardholder data for payment card transactions?",
        "options": ["CISPA", "FERPA", "PCI DSS", "COPPA"],
        "correctAnswer": "PCI DSS"
    },
    {
        "id": 121,
        "questionText": "What is the primary goal of a search operation in an array?",
        "options": [
          "To sort the array in ascending order",
          "To determine if the array is sorted.",
          "To locate a specific element within the array.",
          "To rearrange the elements in descending order."],
        "correctAnswer": "To locate a specific element within the array."
    },
    {
        "id": 122,
        "questionText": "In which scenario is a hybrid search algorithm likely to be beneficial?",
        "options": [
          "When the data is consistently distributed",
          "When the data is well-sorted",
          "When the data distribution varies",
          "When the data is small"],
        "correctAnswer": "When the data distribution varies"
    },
    {
        "id": 123,
        "questionText": "Which communication interface allows devices to establish a connection by bringing them close together?",
        "options": [
          "Bluetooth",
          "NFC",
          "LTE",
          "Wi-Fi"],
        "correctAnswer": "NFC"
    },
    {
        "id": 124,
        "questionText": "What happens if the condition of an iterative loop is never met?",
        "options": [
          "The loop will run 10 times and stop.",
          "It throws an error.",
          "It won't run in the first place.",
          "The loop continues forever."],
        "correctAnswer": "The loop continues forever."
    },
    {
        "id": 125,
        "questionText": "What is the term used for the process of assigning initial values to an array?",
        "options": [
          "Initialization",
          "Creation",
          "Allocation",
          "Assignment"],
        "correctAnswer": "Assignment"
    },
    {
        "id": 126,
        "questionText": "What is a key benefit of using version control systems like Git and Mercurial?",
        "options": [
          "Increased server storage space",
          "Reversion and Rollback",
          "Faster internet connection speeds",
          "Enhanced network security"],
        "correctAnswer": "Reversion and Rollback"
    },
    {
        "id": 127,
        "questionText": "x = 6\ny = 3\nresult = x > 5 and y < 2\nWhat is the value of \"result\" in the above code?",
        "options": [
          "Error: Invalid operation",
          "True",
          "False",
          "Error: Undefined variable"],
        "correctAnswer": "False"
    },
    {
        "id": 128,
        "questionText": "Which technique allows us to embed variable values directly into a string for output formatting?",
        "options": [
          "Date and time formatting",
          "String interpolation",
          "Numeric formatting",
          "HTML escaping"],
        "correctAnswer": "String interpolation"
    },
    {
        "id": 129,
        "questionText": "What are graphics methods in the context of software development?",
        "options": [
          "File formats for saving images",
          "Data structures for storing images",
          "Programming functions for drawing and manipulating graphical elements",
          "Communication protocols for graphics rendering"],
        "correctAnswer": "Programming functions for drawing and manipulating graphical elements"
    },
    {
        "id": 130,
        "questionText": "In a two-dimensional array, how are elements typically accessed?",
        "options": [
          "Using a single index",
          "Using a single index, and a column identifier.",
          "Using two indices, representing row and column positions.",
          "Using the length of the array."],
        "correctAnswer": "Using two indices, representing row and column positions."
    },
    {
        "id": 131,
        "questionText": "What does i-- do to the value of i?",
        "options": [
          "multiplies the current value of i by 1",
          "adds 1 to the current value of i",
          "multiplies current value of i by 2",
          "subtracts 1 to the current value of i"],
        "correctAnswer": "subtracts 1 to the current value of i"
    },
    {
        "id": 132,
        "questionText": "All of the following are types of data at risk in a \"Sensitive Data Exposure\" vulnerability EXCEPT ONE.\nWhich one of the following is data types are NOT at risk in a 'Sensitive Data Exposure' vulnerability?",
        "options": [
          "Session tokens",
          "Publicly available information",
          "Internal files",
          "Personal details"],
        "correctAnswer": "Publicly available information"
    },
    {
        "id": 133,
        "questionText": "Which strategy is useful for dealing with a complex problem that is difficult to solve as a whole?",
        "options": [
          "Regression Testing",
          "Decomposition",
          "Integration",
          "Abstraction"],
        "correctAnswer": "Decomposition"
    },
    {
        "id": 134,
        "questionText": "What programming statement is used to exit a loop prematurely?",
        "options": [
          "Break statement",
          "Halt statement",
          "Stop statement",
          "Terminate statement"],
        "correctAnswer": "Break statement"
    },
    {
        "id": 135,
        "questionText": "Which expression is evaluated first in this example, 2 + 3 * 4 ** 2 % 5, according to the precedence of operations?",
        "options": [
          "Modulo, %",
          "Exponentiation, **",
          "Addition, +",
          "Multiplication, *"],
        "correctAnswer": "Exponentiation, **"
    },
    {
        "id": 136,
        "questionText": "Which of the following best describes interpreted code?",
        "options": [
          "Code that is executed line by line by an interpreter in real-time.",
          "Code that does not require debugging.",
          "Code that is platform-independent and executed faster.",
          "Code that is translated into machine code before execution"],
        "correctAnswer": "Code that is executed line by line by an interpreter in real-time."
    },
    {
        "id": 137,
        "questionText": "Which of the following statements is true about abstract classes?",
        "options": [
          "An abstract class can provide default method implementations.",
          "An abstract class can be directly implemented by a class.",
          "An abstract class can be instantiated.",
          "An abstract class cannot have any abstract methods."],
        "correctAnswer": "An abstract class can provide default method implementations."
    },
    {
        "id": 138,
        "questionText": "What does the substring method typically do when applied to a string?",
        "options": [
          "Reverses the characters in the string",
          "Splits the string into multiple substrings based on a specified delimiter",
          "Extracts a portion of the string based on a specified starting index and length",
          "Capitalizes the first letter of the string"],
        "correctAnswer": "Extracts a portion of the string based on a specified starting index and length"
    },
    {
        "id": 139,
        "questionText": "What does the term \"sprint\" refers to:",
        "options": [
          "A meeting to discuss progress on the project",
          "A phase in the Waterfall methodology",
          "The final stage of project development",
          "A time-boxed iteration for completing tasks"],
        "correctAnswer": "A time-boxed iteration for completing tasks"
    },
    {
        "id": 140,
        "questionText": "What does LTE stand for in the context of IoT communication?",
        "options": [
          "Low-Transmission Energy",
          "Localized Technology Environment",
          "Long-Term Evolution",
          "Light-Thin Encryption"],
        "correctAnswer": "Long-Term Evolution"
    },
    {
        "id": 141,
        "questionText": "Which logic gate is represented by the Boolean expression A or B?",
        "options": [
          "AND gate",
          "NOT gate",
          "OR gate",
          "XOR gate"],
        "correctAnswer": "OR gate"
    },
    {
        "id": 142,
        "questionText": "In the expression x >= 5, what does the >= operator signify?",
        "options": [
          "x is greater than or equal to 5",
          "x is less than 5",
          "x is greater than 5",
          "x is equal to 5"],
        "correctAnswer": "x is greater than or equal to 5"
    },
    {
        "id": 143,
        "questionText": "What does decomposing a problem into smaller procedures allow developers to do?",
        "options": [
          "Leave the problem-solving to someone else.",
          "Avoid understanding the problem as a whole.",
          "Solve each part independently and then combine the solutions to solve the entire problem.",
          "Ignore the problem's complexities."],
        "correctAnswer": "Solve each part independently and then combine the solutions to solve the entire problem."
    },
    {
        "id": 144,
        "questionText": "Which U.S. federal law facilitates information sharing and cooperation between private companies and the government concerning cybersecurity threats?",
        "options": [
          "COPPA",
          "FERPA",
          "CISPA",
          "HIPAA"],
        "correctAnswer": "CISPA"
    },
    {
        "id": 145,
        "questionText": "What are media queries used for in responsive design?",
        "options": [
            "Controlling image size and resolution",
            "Enhancing website accessibility for individuals with disabilities",
            "Implementing interactive animations on web pages",
            "Applying different styles and layout rules based on device characteristics"],
        "correctAnswer": "Applying different styles and layout rules based on device characteristics"
    },
    {
        "id": 146,
        "questionText": "Which remote computing service allows users to access and control a remote desktop environment?",
        "options": [
            "Infrastructure as a Service (IaaS)",
            "Remote Desktop Services (RDS)",
            "Virtual Private Network (VPN)",
            "Software as a Service (SaaS)"],
        "correctAnswer": "Remote Desktop Services (RDS)"
    },
    {
        "id": 147,
        "questionText": "Which learning resources are helpful for improving visualization skills in problem-solving?",
        "options": [
            "Journals and magazines",
            "Social media platforms",
            "Music videos",
            "Books, online tutorials, and YouTube videos"],
        "correctAnswer": "Books, online tutorials, and YouTube videos"
    },
    {
        "id": 148,
        "questionText": "Which of the following best explains ownership and use of digital download copies?",
        "options": [
            "The copy can be used according to the license agreement with ownership being transferred only with permission to a second license holder.",
            "The copy can be used, according to the license agreement, but the originator retains ownership so the license can not be copied, transferred or sold",
            "The copy can be used, according to the license agreement, sold or copied as long as original receipt and use agreement is also transferred",
            "The copy can be used, according to the license agreement and the user can make up to 4 additional copies for their own use only"],
        "correctAnswer": "The copy can be used, according to the license agreement, but the originator retains ownership so the license can not be copied, transferred or sold"
    },
    {
        "id": 149,
        "questionText": "What is the main purpose of an API in software development?",
        "options": [
            "To simplify the development process by providing pre-built code modules.",
            "To ensure data security and encryption in software applications.",
            "To provide a graphical user interface for the end-users.",
            "To enable integration and interaction between different software systems."],
        "correctAnswer": "To enable integration and interaction between different software systems."
    },
    {
        "id": 150,
        "questionText": "Which of the following would undermine data integrity and security?",
        "options": [
            "Using symmetrical encryption",
            "Using a caesar cypher",
            "Using unapproved software",
            "Using internet explorer"],
        "correctAnswer": "Using unapproved software"
    },
    {
        "id":151,
        "questionText": """What will be the value of array[2] after executing the following code?
        array = [10, 20, 30, 40, 50]
        array[2] = array[0] + array[-1]""",
        "options": ["9", "30", "60", "29"],
        "correctAnswer": "60"
    },
    {
        "id": 152,
        "questionText": "Which of the following HTTP status codes indicates a successful response from an API request?",
        "options": ["302 Found", "404 Not Found", "200 OK", "500 Internal Server Error"],
        "correctAnswer": "200 OK"
    },
    {
        "id": 153,
        "questionText": "When should merging typically take place in version control systems?",
        "options": [
            "After completing a feature or bug fix in a branch",
            "Only when conflicts arise between branches",
            "Before creating a new branch",
            "Whenever a developer wants to experiment with new ideas"],
        "correctAnswer": "After completing a feature or bug fix in a branch"
    },
    {
        "id": 154,
        "questionText": "Which data type would be most suitable to store a person's age?",
        "options": ["integer", "boolean", "string", "character"],
        "correctAnswer": "integer"
    },
    {
        "id": 155,
        "questionText": "What is object instantiation in programming?",
        "options": [
            "Executing a method in a class.",
            "Creating a specific instance of a class.",
            "Defining attributes in a class.",
            "Creating a blueprint for a class."],
        "correctAnswer": "Creating a specific instance of a class."
    },
    {
        "id": 156,
        "questionText": "Which type of exception is commonly associated with division by zero?",
        "options": [
            "ArrayIndexOutOfBoundsException",
            "ClassCastException",
            "ArithmeticException",
            "NullPointerException"],
        "correctAnswer": "ArithmeticException"
    },
    {
        "id": 157,
        "questionText": "In which kind of language does the code needs to be translated into something the computer can understand?",
        "options": [
            "Foreign language",
            "Compiled language",
            "Interpreted language",
            "Encrypted language"],
        "correctAnswer": "Compiled language"
    },
    {
        "id": 158,
        "questionText": "In the flowcharts, which shape is for the start/stop?",
        "options": ["oval", "star", "square", "diamond"],
        "correctAnswer": "oval"
    },
    {
        "id": 159,
        "questionText": "Which factor should be considered when decomposing a large programming problem?",
        "options": [
            "The company's overall mission statement",
            "The logical relationships between procedures",
            "The budget allocated for each step",
            "The physical location of the programmers"],
        "correctAnswer": "The logical relationships between procedures"
    },
    {
        "id": 160,
        "questionText": "Which of the following is NOT a common type of in-app purchase (IAP)?",
        "options": [
            "Non-consumable features",
            "User-generated content",
            "Subscriptions",
            "Consumable items"],
        "correctAnswer": "User-generated content"
    },
    {
        "id": 161,
        "questionText": "Which sorting algorithm is based on the divide-and-conquer strategy?",
        "options": [
            "Selection sort",
            "Merge sort",
            "Bubble sort",
            "Insertion sort"],
        "correctAnswer": "Merge sort"
    },
    {
        "id": 162,
        "questionText": "Which type of malware is a piece of code designed to repeat a task over and over again, overwhelming a system?",
        "options": ["Adwares", "Bad bots", "Trojans", "Ransomewares"],
        "correctAnswer": "Bad bots"
    },
    {
        "id": 163,
        "questionText": "What is NOT a type of inheritance?",
        "options": [
            "Multiple inheritance",
            "Single inheritance",
            "Double inheritance",
            "Multilevel inheritance"],
        "correctAnswer": "Double inheritance"
    },
    {
        "id": 164,
        "questionText": "class Student {\n    constructor(name, age) {\n        this.name = name;\n        this.age = age;\n    }\n    setName(newName) {\n        this.name = newName;\n    }\n    getName() {\n        return this.name;\n    }\n    setAge(newAge) {\n        this.age = newAge;\n    }\n    getAge() {\n        return this.age;\n    }\n}\nconst student1 = new Student(\"John\", 20);\nstudent1.setName(\"Alice\");\nlet name = student1.getName();\n\nWhich one of the modifier methods in the Student class is being used?",
        "options": ["setAge()", "setName()", "getAge()", "getName()"],
        "correctAnswer": "setName()"
    },
    {
        "id": 165,
        "questionText": "In a linear search, the number of elements to be searched increases linearly with the size of the array. What is the worst-case time complexity of a linear search?",
        "options": ["O(1)", "O(n)", "O(n^2)", "O(log n)"],
        "correctAnswer": "O(n)"
    },
    {
        "id": 166,
        "questionText": "Which keyword is used to declare a variable that holds text?",
        "options": ["boolean", "float", "string", "integer"],
        "correctAnswer": "string"
    },
    {
        "id": 167,
        "questionText": "Which type of error might occur when attempting to divide a number by zero during runtime?",
        "options": [
            "Null Pointer Exception",
            "Syntax Error",
            "Type Error",
            "Divide-by-Zero Error"],
        "correctAnswer": "Divide-by-Zero Error"
    },
    {
        "id": 168,
        "questionText": "What is the output of the following code?\n\nlet fruits = [\"apple\", \"mango\", \"grape\"];\nconsole.log(fruits.length);",
        "options": ["grape", "3", "[\"apple\", \"mango\", \"grape\"]", "5"],
        "correctAnswer": "3"
    },
    {
        "id": 169,
        "questionText": "What does a hash map use to locate the corresponding value for a given key?",
        "options": ["Linear search", "Collisions", "Hash function", "Binary search"],
        "correctAnswer": "Hash function"
    },
    {
        "id": 170,
        "questionText": "What is the purpose of input validation in data sanitization?",
        "options": [
            "Converting user input to the correct data type",
            "Removing leading or trailing whitespaces from user input",
            "Ensuring user input is free from malicious code",
            "Checking user input against expected formats or patterns"],
        "correctAnswer": "Checking user input against expected formats or patterns"
    },
    {
        "id": 171,
        "questionText": "Which sorting algorithm has the worst space efficiency?",
        "options": ["Insertion Sort", "Quick Sort", "Merge Sort", "Selection Sort"],
        "correctAnswer": "Merge Sort"
    },
    {
        "id": 172,
        "questionText": "What is the advantage of using established libraries and frameworks for output formatting and escaping?",
        "options": [
            "They allow embedding variable values into a string",
            "They ensure data sanitization and security",
            "They have built-in methods for output formatting and escaping",
            "They provide control over the display of numbers"],
        "correctAnswer": "They have built-in methods for output formatting and escaping"
    },
    {
        "id": 173,
        "questionText": "All of the following are key ethical concerns related to data handling EXCEPT ONE. What one of the following is NOT considered a key ethical concern related to data handling, regardless of software type?",
        "options": [
            "Visual presentation of data",
            "Data Ownership",
            "Data Monetization",
            "Transparency and Accountability"],
        "correctAnswer": "Visual presentation of data"
    },
    {
        "id": 174,
        "questionText": "Which operation involves arranging the elements of an array in a specific order based on their values?",
        "options": ["Sorting", "Bound checking", "Indexing", "Initialization"],
        "correctAnswer": "Sorting"
    },
    {
        "id": 175,
        "questionText": "Which of the following refers to how an algorithm repeats?",
        "options": ["variety", "iteration", "selection", "sequencing"],
        "correctAnswer": "iteration"
    },
    {
        "id": 176,
        "questionText": "What are digital signatures used for in software development?",
        "options": [
            "To authenticate users during the login process",
            "To encrypt data at rest",
            "To securely store passwords in databases",
            "To ensure the integrity and authenticity of digital documents"],
        "correctAnswer": "To ensure the integrity and authenticity of digital documents"
    },
    {
        "id": 177,
        "questionText": "p = false\nk = true\nresult = !(p NOR k)\nWhat is the value of \"result\" in the above code?",
        "options": ["Error", "Undefined", "False", "True"],
        "correctAnswer": "True"
    },
    {
        "id": 178,
        "questionText": "Which of the following statements best describes encapsulation in object-oriented programming?",
        "options": [
            "Restricting access to certain members of a class",
            "Combining data and behavior in a single entity",
            "Inheriting properties and methods from a base class",
            "Treating objects of different classes as interchangeable"],
        "correctAnswer": "Combining data and behavior in a single entity"
    },
    {
        "id": 179,
        "questionText": "UML (Unified Modeling Language) is commonly used for:",
        "options": [
            "Testing the functionality of a program",
            "Planning the structure and relationships of objects in an object-oriented program",
            "Defining the hardware and software requirements for a program",
            "Writing pseudocode for program development"],
        "correctAnswer": "Planning the structure and relationships of objects in an object-oriented program"
    },
    {
        "id": 180,
        "questionText": "Which style convention focuses on error handling and testing practices?",
        "options": [
            "Commenting",
            "Error Handling and Testing",
            "Indentation and Formatting",
            "Naming Conventions"],
        "correctAnswer": "Error Handling and Testing"
    },
    {
        "id": 181,
        "questionText": "Which approach is generally preferred for input sanitization: whitelisting or blacklisting?",
        "options": [
            "Blacklisting",
            "validating user input against predefined SQL query patterns",
            "Removing all special characters from user input",
            "Whitelisting"],
        "correctAnswer": "Whitelisting"
    },
    {
        "id": 182,
        "questionText": "What does the term \"Composition Over Inheritance\" emphasize?",
        "options": [
            "Prioritizing code reusability through inheritance",
            "Avoiding all forms of relationships between classes",
            "Favoring composition for code reuse and flexibility",
            "Ignoring the diamond problem in multiple inheritance"],
        "correctAnswer": "Favoring composition for code reuse and flexibility"
    },
    {
        "id": 183,
        "questionText": "In a hash map, what are collisions, and how are they typically addressed?",
        "options": [
            "Collisions are the same as heterogeneous elements, and they are addressed by using chaining.",
            "Collisions are errors in the hash function, and they are fixed by rehashing.",
            "Collisions are not an issue in hash maps.",
            "Collisions occur when two keys produce the same hash value, and they are addressed using collision resolution strategies like chaining or open addressing."],
        "correctAnswer": "Collisions occur when two keys produce the same hash value, and they are addressed using collision resolution strategies like chaining or open addressing."
    },
    {
        "id": 184,
        "questionText": "What does dropping a database mean?",
        "options": [
            "Erasing the entire database and its associated tables and data",
            "Removing all data from a database table",
            "Disconnecting from the database",
            "Deleting a specific row from a table"],
        "correctAnswer": "Erasing the entire database and its associated tables and data"
    },
    {
        "id": 185,
        "questionText": "Which type of attack uses someone else's identity or credentials to give them access to information?",
        "options": ["Brute Force", "Identity Theft", "Phishing", "Malaware"],
        "correctAnswer": "Identity Theft"
    },
    {
        "id": 186,
        "questionText": "In which data structure are elements accessed using an index, and the order of elements is guaranteed?",
        "options": ["Set", "Array", "Hash map", "Linked list"],
        "correctAnswer": "Array"
    },
    {
        "id": 187,
        "questionText": "What is the potential issue with comparing floating-point numbers for equality? For example:\n\na <- 0.1 + 0.2\nb <- 0.3\ndisplay to console: a == b   # This might not necessarily print True",
        "options": [
            "Integer overflow during floating-point operations",
            "Floating-point numbers can not be divided",
            "Floating-point numbers cannot handle irrational numbers",
            "Inexact binary representations can cause rounding errors"],
        "correctAnswer": "Inexact binary representations can cause rounding errors"
    },
    {
        "id": 188,
        "questionText": "What is the primary purpose of using nested loops?",
        "options": [
            "To improve code efficiency",
            "To increase code readability",
            "To perform input validation",
            "To handle exceptions"],
        "correctAnswer": "To improve code efficiency"
    },
    {
        "id": 189,
        "questionText": "A program is intended to calculate the average of a list of numbers, but instead it calculates the sum of the numbers without dividing by the count. What type of error occurred?",
        "options": ["Runtime Error", "Syntax Error", "Semantic Error", "Logic Error"],
        "correctAnswer": "Logic Error"
    },
    {
        "id": 190,
        "questionText": "Which of the following is NOT an access modifier used for encapsulation in many programming languages?",
        "options": ["Static", "Protected", "Private", "Public"],
        "correctAnswer": "Static"
    },
    {
        "id": 191,
        "questionText": "What do graphics methods offer for manipulating images?",
        "options": [
            "Methods for embedding images into web pages",
            "Encryption algorithms for image security",
            "Compression techniques for reducing file size",
            "Transformations, such as rotation and scaling"],
        "correctAnswer": "Transformations, such as rotation and scaling"
    },
    {
        "id": 192,
        "questionText": "What is the role of a testing plan in program development?",
        "options": [
            "To outline the development process and milestones", 
            "To define the hardware requirements for the program", 
            "To identify potential risks and issues in the program", 
            "To document the approach and scope of testing"],
        "correctAnswer": "To document the approach and scope of testing"
    },
    {
        "id": 193,
        "questionText": "What is the primary role of a whitelist when sanitizing user input?",
        "options": [
            "Identifying malicious user", 
            "Accepting only predefined inputs", 
            "Blocking specific IP addresses", 
            "Logging user activities"],
        "correctAnswer": "Accepting only predefined inputs"
    },
    {
        "id": 194,
        "questionText": "What is monetization in the context of app development?",
        "options": [
            "Techniques for improving app visibility", 
            "Strategies for generating revenue from the app", 
            "The process of reducing development costs", 
            "The creation of app interfaces"],
        "correctAnswer": "Strategies for generating revenue from the app"
    },
    {
        "id": 195,
        "questionText": "What constitutes the membership of the Internet Engineering Task Force (IETF)?",
        "options": [
            "A group of political leaders and heads of state", 
            "A loosely organized collection of citizens and engineers", 
            "A collection of the leaders of the top internet providers", 
            "An international coalition of goernment agencies"],
        "correctAnswer": "A loosely organized collection of citizens and engineers"
    },
    {
        "id": 196,
        "questionText": "Which statement is used to specify an alternative code block to be executed when the condition is false?",
        "options": [
            "switch case statement", 
            "if/else statement", 
            "while loop statement", 
            "for loop statement"],
        "correctAnswer": "if/else statement"
    },
    {
        "id": 197,
        "questionText": "class Book:\n    def __init__(self, title, author):\n        self.title = title\n        self.author = author\n    def setTitle(self, newTitle):\n        self.title = newTitle\n    def setAuthor(self, newAuthor):\n        self.author = newAuthor\nbook1 = Book(\"The Great Gatsby\", \"F. Scott Fitzgerald\")\nbook1.setTitle(\"To Kill a Mockingbird\")\n\nWhich method in the Book class is the modifier method?",
        "options": [
            "self.title = newTitle", 
            "self.title = title", 
            "book1.setTitle(\"To Kill a Mockingbird\")", 
            "setTitle()"],
        "correctAnswer": "setTitle()"
    },
    {
        "id": 198,
        "questionText": "x = 5\nif x > 3:\n    print(\"Hello\")\nelse:\n    print(\"Hi\")\n\nWhat is the output of the above code?",
        "options": [
            "No output; this block of code will not execute.", 
            "Hello Hi", 
            "Hi", 
            "Hello"],
        "correctAnswer": "Hello"
    },
    {
        "id": 199,
        "questionText": "Which of the following statements is true about object instantiation?",
        "options": [
            "Instantiating an object automatically creates a new class.", 
            "Objects can only be instantiated from abstract classes.", 
            "Each instance of an object has its own set of properties and methods.", 
            "Instantiating an object modifies the behavior of the class."],
        "correctAnswer": "Each instance of an object has its own set of properties and methods."
    },
    {
        "id": 200,
        "questionText": "Which of the following is the best definition for 'royalty fees'?",
        "options": [
            "A one time fee paid for the use of a licensed asset for the duration of use whether it is profit or nonprofit", 
            "A fee based on the income earned because of the use of the licensed asset", 
            "An ongoing fee paid for the use of a licensed asset each time the asset is used, normally a percentage of the sales", 
            "An ongoing fee that changes based on the value of the licenses asset at the time it is being used"],
        "correctAnswer": "An ongoing fee paid for the use of a licensed asset each time the asset is used, normally a percentage of the sales"
    },
    {
        "id": 201,
        "questionText": "What is the value of 17 % 5?",
        "options": [
            "3", 
            "2", 
            "0.4", 
            "3.4"],
        "correctAnswer": "2"
    },
    {
        "id": 202,
        "questionText": "What are the common types of integration testing?",
        "options": [
            "Black-box testing and white-box testing", 
            "Functional testing and performance testing", 
            "Top-down and bottom-up testing", 
            "Unit testing and system testing"],
        "correctAnswer": "Top-down and bottom-up testing"
    },
    {
        "id": 203,
        "questionText": "In Python, which naming convention is typically used for constant variables?",
        "options": [
            "PascalCase", 
            "UPPER-CASE-WITH-HYPHENS", 
            "kebab-case", 
            "UPPER_CASE_WITH_UNDER_SCORES"],
        "correctAnswer": "UPPER_CASE_WITH_UNDER_SCORES"
    },
    {
        "id": 204,
        "questionText": "Which type of code is more likely to create apps or programs that can run on their own as standalone executables?",
        "options": [
            "Compiled code", 
            "Virtual machine code", 
            "Hybrid code", 
            "Interpreted code"],
        "correctAnswer": "Compiled code"
    },
    {
        "id": 205,
        "questionText": "What is the first step to creating a new repository on GitHub?",
        "options": [
            "Creating a new repository on the GitHub website", 
            "Initializing a local repository using \"git init\"", 
            "Forking a repository", 
            "Cloning an existing repository"],
        "correctAnswer": "Creating a new repository on the GitHub website"
    },
    {
        "id": 206,
        "questionText": "What is the purpose of the CIA triad in information security?",
        "options": [
            "To focus solely on data confidentiality", 
            "To enforce strict access controls for data protection", 
            "To prevent all potential security breaches", 
            "To provide a balanced approach to information security"],
        "correctAnswer": "To provide a balanced approach to information security"
    },
    {
        "id": 207,
        "questionText": "Which term refers to the process of managing and responding to unexpected or erroneous input in a program?",
        "options": [
            "Input validation", 
            "Output generation", 
            "Error handling", 
            "Data formatting"],
        "correctAnswer": "Error handling"
    },
    {
        "id": 208,
        "questionText": "class Car:\n    def __init__(self, make, model):\n        self.make = make\n        self.model = model\nmy_car = Car(\"Toyota\", \"Camry\")\n\nWhat is happening in the the last line of code?",
        "options": [
            "A new instance of the Car class is created.", 
            "The make and model attributes of the Car class are being defined.", 
            "The Car class is being defined.", 
            "The Car class is being modified."],
        "correctAnswer": "A new instance of the Car class is created."
    },
    {
        "id": 209,
        "questionText": "What is the unique number for each computing device called?",
        "options": [
            "IP Address", 
            "Device Location Address", 
            "Domain Name System", 
            "Device Number System"],
        "correctAnswer": "IP Address"
    },
    {
        "id": 210,
        "questionText": "In zero-based indexing, which index is used to access the first element of an array?",
        "options": [
            "0", 
            "2", 
            "1", 
            "-1"],
        "correctAnswer": "0"
    },
    {
        "id": 211,
        "questionText": "larr ← [5, 2, 8, 4, 9]\narr.sortDescending()\noutput(arr)\n\nWhat will be the output of the code snippet above?",
        "options": [
            "[9, 8, 5, 4, 2]", 
            "[2, 4, 5, 8, 9]", 
            "[4, 8, 2, 5, 9]", 
            "[5, 2, 8, 4, 9]"],
        "correctAnswer": "[9, 8, 5, 4, 2]"
    },
    {
        "id": 212,
        "questionText": "What are NoSQL databases primarily used for?",
        "options": [
            "Relational data modeling", 
            "Structured data storage", 
            "Transaction management", 
            "Non-relational data storage with specific data modeling requirements"],
        "correctAnswer": "Non-relational data storage with specific data modeling requirements"
    },
    {
        "id": 213,
        "questionText": "What is the primary benefit of encapsulation?",
        "options": [
            "Code reuse and extensibility", 
            "Method overriding and polymorphism", 
            "Data hiding and security", 
            "Code organization and modularity"],
        "correctAnswer": "Data hiding and security"
    },
    {
        "id": 214,
        "questionText": "All of the following are benefits of automated testing except for ONE.\nWhich of the following is NOT a benefit of automated testing?",
        "options": [
            "Increases test coverage and accuracy", 
            "Reduces the need for manual testing", 
            "Assess the overall user experience", 
            "Provides faster feedback on code changes"],
        "correctAnswer": "Assess the overall user experience"
    },
    {
        "id": 215,
        "questionText": "What is one benefit of using return values in programming?",
        "options": [
            "It eliminates the need for writing comments and documentation", 
            "It allows for faster program execution", 
            "It improves code maintainability and flexibility", 
            "It enhances code security and prevents data leakage"],
        "correctAnswer": "It improves code maintainability and flexibility"
    },
    {
        "id": 216,
        "questionText": "If A is true and B is false, what is the result of the expression A OR B?",
        "options": [
            "False", 
            "True", 
            "XOR", 
            "AND"],
        "correctAnswer": "True"
    },
    {
        "id": 217,
        "questionText": "Which of the following statements is true about the relationship between a class and an object?",
        "options": [
            "An object is a collection of classes.", 
            "A class is a subset of an object", 
            "A class can exist without any objects.", 
            "An object can exist without any classes."],
        "correctAnswer": "A class can exist without any objects."
    },
    {
        "id": 218,
        "questionText": "Which of the following is a benefit of using a version control system in a collaborative software development environment?",
        "options": [
            "Simplified code compilation and deployment", 
            "Improved code quality through automated testing", 
            "Enhanced code documentation and commenting", 
            "Facilitated coordination and conflict resolution among team members"],
        "correctAnswer": "Facilitated coordination and conflict resolution among team members"
    },
    {
        "id": 219,
        "questionText": "Why is providing user-friendly error messages important in runtime error handling?",
        "options": [
            "To avoid handling errors altogether", 
            "To provide clear information about the error to end-users", 
            "To introduce intentional errors", 
            "To confuse users"],
        "correctAnswer": "To provide clear information about the error to end-users"
    },
    {
        "id": 220,
        "questionText": "The phase in the SDLC (system design life cycle) where the system is tested to ensure it meets the specified requirements is called:",
        "options": [
            "Testing", 
            "Development", 
            "Design", 
            "Implementation"],
        "correctAnswer": "Testing"
    },
    {
        "id": 221,
        "questionText": "What type of error will be thrown?\n\nfunction divideByZero() {\n    result = 10 / 0;  \n    return result;\n}\ndivideByZero();",
        "options": [
            "Runtime error", 
            "Semantic error", 
            "Syntax error", 
            "Logic error"],
        "correctAnswer": "Runtime error"
    },
    {
        "id": 222,
        "questionText": "Convert the decimal number 70 to hexadecimal.",
        "options": [
            "3A", 
            "2E", 
            "46", 
            "5C"],
        "correctAnswer": "46"
    },
    {
        "id": 223,
        "questionText": "What is the outcome of the Boolean expression (A OR B) AND (NOT A) if A is True?",
        "options": [
            "False", 
            "XOR", 
            "True", 
            "AND"],
        "correctAnswer": "False"
    },
    {
        "id": 224,
        "questionText": "Which term refers to the system that defines the positions of elements and is used by Graphic methods?",
        "options": [
            "Rendering Context", 
            "Image Transformation", 
            "Vector Graphics", 
            "Coordinate System"],
        "correctAnswer": "Coordinate System"
    },
    {
        "id": 225,
        "questionText": "What does the term \"stability\" refer to in the context of sorting algorithms?",
        "options": [
            "The ability to rearrange elements in ascending order.", 
            "The time it takes to sort an array.", 
            "The preservation of the relative order of equal elements in the sorted array.", 
            "The number of comparisons made during sorting."],
        "correctAnswer": "The preservation of the relative order of equal elements in the sorted array."
    },
    {
        "id": 226,
        "questionText": "count = 0\nfor i in range(1, 4):\n    for j in range(i):\n        count += j + 1\nprint(count)\n\nWhat will be the output of the above code?",
        "options": [
            "6", 
            "10", 
            "40", 
            "9"],
        "correctAnswer": "10"
    },
    {
        "id": 227,
        "questionText": "What are nested loops in programming?",
        "options": [
            "Loops that are never executed", 
            "Loops that contain subroutines", 
            "A loop that is located inside another loop", 
            "Loops that are executed one after another"],
        "correctAnswer": "A loop that is located inside another loop"
    },
    {
        "id": 228,
        "questionText": "What term describes the ability to work on documents, code, or content simultaneously with others with real-time changes?",
        "options": [
            "Real-time collaboration", 
            "Version control", 
            "File synchronization", 
            "Code hosting"],
        "correctAnswer": "Real-time collaboration"
    },
    {
        "id": 229,
        "questionText": "The level of security a person or organization has for their computer presence is referred to as their security ________.",
        "options": [
            "Posture", 
            "Profile", 
            "Holes", 
            "Position"],
        "correctAnswer": "Posture"
    },
    {
        "id": 230,
        "questionText": "Which of these methodologies is often associated with risk analysis and/or management?",
        "options": [
            "Scrum", 
            "Top-Down", 
            "Waterfall", 
            "Spiral"],
        "correctAnswer": "Spiral"
    },
    {
        "id": 231,
        "questionText": "In programming, what is the assignment operator used for?",
        "options": [
            "To assign values to variables", 
            "To create mathematical inequalities", 
            "To check for equality", 
            "To compare values"],
        "correctAnswer": "To assign values to variables"
    },
    {
        "id": 232,
        "questionText": "Set i to 0\nWhile i is less than 5\n    If i equals 3\n        Exit the loop\n    End If\n    Print the value of i\n    Increment i by 1\nEnd While\n\nWhat will be the output of the above code?",
        "options": [
            "0 1 2", 
            "0 1 2 3", 
            "0 1 2 4 5", 
            "0 1 2 4"],
        "correctAnswer": "0 1 2"
    },
    {
        "id": 233,
        "questionText": "string str1 ← \"Hello\"\nstring str2 ← \"world!\"\nstring result ← str1 + \" \" + str2\noutput(result)\n\nWhat will be the output of the above pseudocode?",
        "options": [
            "Hello + world!", 
            "Hello World!", 
            "\"Hello\" \"World!\"", 
            "\"Hello\" + \"World!\""],
        "correctAnswer": "Hello World!"
    },
    {
        "id": 234,
        "questionText": "What is the hexadeciaml number CE converted to decimal notation?",
        "options": [
            "105",
            "206",
            "205",
            "236"],
        "correctAnswer": "206"
    },
    {
        "id": 235,
        "questionText": "When is the use of open web standards like HTML and CSS most relevant?",
        "options": [
            "When generating random numbers",
            "When formatting data for a printed report",
            "When displaying data in a user interface",
            "When encrypting sensitive data"],
        "correctAnswer": "When displaying data in a user interface"
    },
    {
        "id": 236,
        "questionText": "What is one recommended procedure to maintain data integrity and security on your computer?",
        "options": [
            "Keep the screen unlocked for easy access",
            "Lock the screen when not in use",
            "Use any thumb drive available",
            "Delete all emails, even if they seem familiar"],
        "correctAnswer": "Lock the screen when not in use"
    },
    {
        "id": 237,
        "questionText": "What is the purpose of a coordinate system in graphics?",
        "options": [
            "To define the position and orientation of objects",
            "To encrypt and secure images",
            "To specify the size and dimensions of an image",
            "To compress image file sizes"],
        "correctAnswer": "To define the position and orientation of objects"
    },
    {
        "id": 238,
        "questionText": "What is the approximate size of a typical high-resolution photo?",
        "options": [
            "Megabytes",
            "Terabytes",
            "Gigabytes",
            "Kilobytes"],
        "correctAnswer": "Megabytes"
    },
    {
        "id": 239,
        "questionText": "In the maintenance phase of a software application, how would you address user-identified issues and additional feature requests in a systematic manner?",
        "options": [
            "Request user feedback on new features",
            "Proceed to the deployment phase",
            "Prioritize and fix identified issues",
            "Implement additional features directly"],
        "correctAnswer": "Prioritize and fix identified issues"
    },
    {
        "id": 240,
        "questionText": "What is the purpose of a destructor in a class?",
        "options": [
            "To initialize object attributes",
            "To clean up resources when an object is destroyed",
            "To set default values for attributes",
            "To create new instances of a class"],
        "correctAnswer": "To clean up resources when an object is destroyed"
    },
    {
        "id": 241,
        "questionText": "What is the primary purpose of a Virtual Private Network (VPN)?",
        "options": [
            "Secure remote desktop access",
            "Encrypt internet traffic",
            "Virtual conferencing",
            "Collaborative document editing"],
        "correctAnswer": "Encrypt internet traffic"
    },
    {
        "id": 242,
        "questionText": "What is the purpose of instantiating objects from existing classes?",
        "options": [
            "To create new classes based on existing classes.",
            "To combine multiple classes into one.",
            "To create multiple instances of the same class with different data.",
            "To modify the behavior of existing classes."],
        "correctAnswer": "To create multiple instances of the same class with different data."
    },
    {
        "id": 243,
        "questionText": "What is bandwidth in the context of internet connections?",
        "options": [
            "The speed at which a website loads",
            "The quality of images and graphics on a webpage",
            "The number of web pages on a website",
            "The amount of data that can be transmitted over a network in a given time"],
        "correctAnswer": "The amount of data that can be transmitted over a network in a given time"
    },
    {
        "id": 244,
        "questionText": "Given the following code snippet, which line creates a subclass of the Animal class?\n\nclass Animal:\n    def __init__(self, name):\n        self.name = name\nclass Dog(Animal):\n    def bark(self):\n        print(\"Woof!\")",
        "options": [
            "Line 2: class Animal",
            "Line 7: def bark(self)",
            "Line 9: print(\"Woof!\")",
            "Line 5: class Dog"],
        "correctAnswer": "Line 5: class Dog"
    },
    {
        "id": 245,
        "questionText": "Which of the following statements about modifier methods is true?",
        "options": [
            "They are used to modify the state of objects by updating their attributes.",
            "They are only used for retrieving data from objects.",
            "They are used for deleting objects from memory.",
            "They are used to create new objects."],
        "correctAnswer": "They are used to modify the state of objects by updating their attributes."
    },
    {
        "id": 246,
        "questionText": "Which programming language is widely used for developing Android applications?",
        "options": [
            "Swift",
            "Kotlin",
            "C#",
            "Python"],
        "correctAnswer": "Kotlin"
    },
    {
        "id": 247,
        "questionText": "What is the primary purpose of initializing a new repository?",
        "options": [
            "To create a directory for storing code files",
            "To set up authentication and access control for the repository",
            "To configure the default branch and repository settings",
            "To connect to a remote code hosting service"],
        "correctAnswer": "To create a directory for storing code files"
    },
    {
        "id": 248,
        "questionText": "let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];\nlet sum = 0;\nfor (let i = 0; i < matrix.length; i++) {\n  for (let j = i; j < matrix[i].length - 1; j++) {\n    sum += matrix[i][j];\n  }\n}\nconsole.log(sum);\n\nWhat will be printed as the output of the above code?",
        "options": [
            "36",
            "45",
            "26",
            "8"],
        "correctAnswer": "8"
    },
    {
        "id": 249,
        "questionText": "In the documentation for a class, the constructor method(s) usually specify:",
        "options": [
            "The time complexity of creating an instance",
            "The internal design choices made when creating an instance",
            "The private variables used to create the instance",
            "How to create an instance of the class"],
        "correctAnswer": "How to create an instance of the class"
    },
    {
        "id": 250,
        "questionText": "Which logical operator evaluates to true if both operands are true?",
        "options": [
            "NOT",
            "OR",
            "XOR",
            "AND"],
        "correctAnswer": "AND"
    },
    {
        "id": 251,
        "questionText": "What does the term \"Semantic HTML\" refer to?",
        "options": [
            "HTML code optimized for search engines.",
            "HTML code with fancy styling.",
            "HTML tags with bright colors.",
            "HTML markup that accurately represents the meaning and structure of content."],
        "correctAnswer": "HTML markup that accurately represents the meaning and structure of content."
    },
    {
        "id": 252,
        "questionText": "let x = 10;\nlet y = 20;\nlet result = x <= y;\n\nWhat is the value of \"result\" in the above code?",
        "options": [
            "Error: Invalid comparison",
            "10",
            "False",
            "True"],
        "correctAnswer": "True"
    },
    {
        "id": 253,
        "questionText": "What is composition in object-oriented programming?",
        "options": [
            "The process of creating a new class from an existing class.",
            "The process of designing classes based on their relationships.",
            "The process of creating objects from a class.",
            "The process of combining multiple classes into one."],
        "correctAnswer": "The process of combining multiple classes into one."
    },
    {
        "id": 254,
        "questionText": "Name the loop will always execute before checking the condition?",
        "options": [
            "If conditional",
            "For loop",
            "While loop",
            "Do while loop"],
        "correctAnswer": "Do while loop"
    },
    {
        "id": 255,
        "questionText": "Which one of the following is a best practice for using parameters?",
        "options": [
            "Minimizing the use of default parameter values",
            "Passing all arguments as positional arguments",
            "Using single-letter variable names for parameters",
            "Keeping the number of parameters in a function manageable"],
        "correctAnswer": "Keeping the number of parameters in a function manageable"
    },
    {
        "id": 256,
        "questionText": "What should you consult to understand how to use a standard library function correctly?",
        "options": [
            "The official documentation",
            "The forums like StackOverflow",
            "ChatGPT",
            "Web search results"],
        "correctAnswer": "The official documentation"
    },
    {
        "id": 257,
        "questionText": "Which type of inheritance allows a class to inherit from more than one superclass?",
        "options": [
            "Multiple Inheritance",
            "Single Inheritance",
            "Hierarchical Inheritance",
            "Multilevel Inheritance"],
        "correctAnswer": "Multiple Inheritance"
    },
    {
        "id": 258,
        "questionText": "let i = 0;\nwhile (i < 5) {\n    output to console i ;\n    increment i;\n    if (i == 3) {\n        continue;\n    }\n    output to console \"Hello\";\n}\n\nWhat will be the console output of the above code?",
        "options": [
            "0 Hello 1 Hello 2 3 Hello 4 Hello",
            "0 Hello 1 Hello 2 Hello Hello 4 Hello",
            "0 Hello 1 Hello 2 Hello 3 Hello 4",
            "0 Hello 1 Hello 2 Hello 4 Hello"],
        "correctAnswer": "0 Hello 1 Hello 2 3 Hello 4 Hello"
    },
    {
        "id": 259,
        "questionText": "Which exception class is typically thrown when a method receives an invalid argument?",
        "options": [
            "NullPointerException",
            "IOException",
            "IndexOutOfBoundsException",
            "IllegalArgumentException"],
        "correctAnswer": "IllegalArgumentException"
    },
    {
        "id": 260,
        "questionText": "Which of the following costs is unique to cross-platform app development?",
        "options": [
            "Limitations in utilizing platform-specific features",
            "App stores requiring a higher fee",
            "Higher backend development costs",
            "Separate codebases for iOS and Android"],
        "correctAnswer": "Limitations in utilizing platform-specific features"
    },
    {
        "id": 261,
        "questionText": "Which one of the methods below can be used to prevent SQL Injection?",
        "options": [
            "Use an antivirus software",
            "Validate and sanitize user inputs",
            "Use digital certificates",
            "Use a firewall"],
        "correctAnswer": "Validate and sanitize user inputs"
    },
    {
        "id": 262,
        "questionText": "Why is it important to handle bad input and run-time errors within the program during integration testing?",
        "options": [
            "It reduces the need for writing test cases",
            "It makes the program execute faster",
            "It decreases the complexity of the testing process",
            "It improves the reliability and robustness of the software"],
        "correctAnswer": "It improves the reliability and robustness of the software"
    },
    {
        "id": 263,
        "questionText": "What is a buffer overflow?",
        "options": [
            "A method for encrypting user input to prevent unauthorized access",
            "A security vulnerability caused by writing data beyond allocated buffer boundaries",
            "A method for removing unnecessary characters from user input",
            "A technique for validating user input against specific criteria"],
        "correctAnswer": "A security vulnerability caused by writing data beyond allocated buffer boundaries"
    },
    {
        "id": 264,
        "questionText": "What's the process that helps by breaking down complex computer problems into more manageable parts?",
        "options": [
            "Decomparing",
            "Decomposing",
            "De-elevating",
            "Decompressing"],
        "correctAnswer": "Decomposing"
    },
    {
        "id": 265,
        "questionText": "Which type of software license allows users to modify and distribute the software freely?",
        "options": [
            "Shareware license",
            "Freeware license",
            "Open source license",
            "Proprietary license"],
        "correctAnswer": "Open source license"
    },
    {
        "id": 266,
        "questionText": "What are runtime errors in programming?",
        "options": [
            "Errors that occur during debugging",
            "Errors that occur during program compilation",
            "Errors that occur during program execution",
            "Errors that occur due to logical inconsistencies in code"],
        "correctAnswer": "Errors that occur during program execution"
    },
    {
        "id": 267,
        "questionText": "Which iteration structure is often used when solving problems that can be divided into smaller, similar subproblems?",
        "options": [
            "for loop",
            "recursion",
            "while loop",
            "for-each loop"],
        "correctAnswer": "recursion"
    },
    {
        "id": 268,
        "questionText": "What is the role of error handling in handling unexpected return values?",
        "options": [
            "To ignore unexpected return values and continue program execution",
            "To prevent unexpected return values from occurring",
            "To catch and handle errors or exceptions that may cause unexpected return values",
            "To log unexpected return values for later analysis"],
        "correctAnswer": "To catch and handle errors or exceptions that may cause unexpected return values"
    },
    {
        "id": 269,
        "questionText": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def get_radius(self):\n        return self.radius\n\n    def set_radius(self, new_radius):\n        self.radius = new_radius\ncircle1 = Circle(5)\n\nWhich method in the Circle class is the accessor method?",
        "options": [
            "set_radius(self, new_radius)",
            "get_radius()",
            "self.radius = radius",
            "Circle(5)"],
        "correctAnswer": "get_radius()"
    },
    {
        "id": 270,
        "questionText": "Which law protects the digital access and transfer of medical records from one party to another?",
        "options": [
            "COBRA",
            "FERPA",
            "COPPA",
            "HIPAA"],
        "correctAnswer": "HIPAA"
    },
    {
        "id": 271,
        "questionText": "Which of the following is true about a user-defined class?",
        "options": [
            "It cannot have both attributes and methods",
            "It can have attributes (data) and methods (functions)",
            "It can only have attributes but not methods",
            "It can only have methods but not attributes"],
        "correctAnswer": "It can have attributes (data) and methods (functions)"
    },
    {
        "id": 272,
        "questionText": "What is the difference between a class and an object?",
        "options": [
            "A class can have multiple instances, while an object can have multiple classes.",
            "A class is a runtime entity, while an object is a compile-time entity.",
            "A class can have methods, while an object can only have properties.",
            "A class defines the structure, while an object is an instance of the class."],
        "correctAnswer": "A class defines the structure, while an object is an instance of the class."
    },
    {
        "id": 273,
        "questionText": "During the testing phase of a software project (Scenario 1), which of the following steps would you NOT perform?",
        "options": [
            "Develop the software",
            "Identify test scenarios and test cases",
            "Report and prioritize defects for resolution",
            "Execute test cases and record results"],
        "correctAnswer": "Develop the software"
    },
    {
        "id": 274,
        "questionText": "In a program editor, what does the term \"syntax highlighting\" refer to?",
        "options": [
            "Automatically suggesting code completion options",
            "Changing the color scheme of the editor",
            "Highlighting the syntax errors in the code",
            "Highlighting different parts of the code with different colors"],
        "correctAnswer": "Highlighting different parts of the code with different colors"
    },
    {
        "id": 275,
        "questionText": "Which sorting algorithm has a best-case time complexity of O(n)?",
        "options": [
            "Merge sort",
            "Quick sort",
            "Insertion sort",
            "Heap sort"],
        "correctAnswer": "Insertion sort"
    },
    {
        "id": 276,
        "questionText": "What does scalability refer to in app development?",
        "options": [
            "The app's visual design appeal",
            "The app's ability to work offline",
            "The app's ability to handle growth in users or features",
            "The app's compatibility with older devices"],
        "correctAnswer": "The app's ability to handle growth in users or features"
    },
    {
        "id": 277,
        "questionText": "User stories are a common technique used to:",
        "options": [
            "Describe the functionality from the perspective of end users",
            "Define the technical specifications of a program",
            "Document the testing plan for a program",
            "Outline the development process for a program"],
        "correctAnswer": "Describe the functionality from the perspective of end users"
    },
    {
        "id": 278,
        "questionText": "Which characteristic is associated with the dynamic nature of objects?",
        "options": [
            "Objects defined at compile-time",
            "Objects are static entities",
            "Objects remain unchanged during runtime",
            "Objects can be created and modified during runtime"],
        "correctAnswer": "Objects can be created and modified during runtime"
    },
    {
        "id": 279,
        "questionText": "What does the code below display given:\n\nboy = TRUE \nyoung = FALSE\nIF NOT young AND boy \n{\n   DISPLAY (\"Sup!\") \n} \nELSE\n{ \n     IF NOT boy AND young \n     { \n       DISPLAY (\"Right on\") \n      } \n     ELSE\n       { \n         DISPLAY(\"Seriously?!\") \n       }\n }",
        "options": [
            "Right on",
            "Sup!",
            "Seriously?!",
            "Nothing - it has an error"],
        "correctAnswer": "Sup!"
    },
    {
        "id": 280,
        "questionText": "Which GUI object is suitable for displaying single lines of text or results of calculations?",
        "options": [
            "Radio Buttons",
            "Labels",
            "Dropdowns",
            "Text Boxes"],
        "correctAnswer": "Text Boxes"
    },
    {
        "id": 281,
        "questionText": "What is the primary purpose of searching in an array?",
        "options": [
            "To rearrange the elements in ascending order.",
            "To sort the array",
            "To determine if a specific element exists in the array.",
            "To count the number of elements in the array."],
        "correctAnswer": "To determine if a specific element exists in the array."
    },
    {
        "id": 282,
        "questionText": "What does the A stand for in the CIA triad?",
        "options": [
            "Availability",
            "Aggregation",
            "Accounting",
            "Agency"],
        "correctAnswer": "Availability"
    },
    {
        "id": 283,
        "questionText": "What does API stand for?",
        "options": [
            "Application Protocol Interface",
            "Application Program Interface",
            "Advanced Protocol Interface",
            "Advanced Programming Interface"],
        "correctAnswer": "Application Program Interface"
    },
    {
        "id": 284,
        "questionText": "How does the -- symbol in programming change a variable?",
        "options": [
            "divide by 2 to the value of itself",
            "subtract 1 from the value of itself",
            "add 1 to the value of itself",
            "multiply by 2 to the value of itself"],
        "correctAnswer": "subtract 1 from the value of itself"
    },
    {
        "id": 285,
        "questionText": "Which type of software system is more likely to require upfront licensing fees?",
        "options": [
            "Proprietary systems",
            "Neither open source nor proprietary systems",
            "Both open source and proprietary systems",
            "Open source systems"],
        "correctAnswer": "Proprietary systems"
    },
    {
        "id": 286,
        "questionText": "Which of the following is a best practice for maintaining integrity and security in software development?",
        "options": [
            "Use version control systems",
            "Debug programs without encryption",
            "Store passwords in plain text",
            "Make your code more difficult to read"],
        "correctAnswer": "Use version control systems"
    },
    {
        "id": 287,
        "questionText": "If the last value in a binary number is \"1\", what do we know about that number?",
        "options": [
            "It's an even number.",
            "It's an odd number.",
            "It's a whole number.",
            "It's less than 20."],
        "correctAnswer": "It's an odd number."
    },
    {
        "id": 288,
        "questionText": "What does a build system help achieve in terms of software development?",
        "options": [
            "Platform-dependent builds",
            "Error-free code writing",
            "Real-time code execution",
            "Consistency in builds"],
        "correctAnswer": "Consistency in builds"
    },
    {
        "id": 289,
        "questionText": "Which mechanism allows a class to inherit attributes and behaviors from another class?",
        "options": [
            "Encapsulation",
            "Polymorphism",
            "Inheritance",
            "Abstraction"],
        "correctAnswer": "Inheritance"
    },
    {
        "id": 290,
        "questionText": "What are the consequences of software duplication and copyright infringement?",
        "options": [
            "Increased competition in the software market",
            "Legal penalties and potential lawsuits",
            "Higher software prices for consumers",
            "Enhanced software security measures"],
        "correctAnswer": "Legal penalties and potential lawsuits"
    },
    {
        "id": 291,
        "questionText": "What is OWASP?",
        "options": [
            "A programming language commonly used for web development",
            "A nonprofit organization addressing web application security",
            "A software vulnerability scanner",
            "A government agency focused on software security"],
        "correctAnswer": "A nonprofit organization addressing web application security"
    },
    {
        "id": 292,
        "questionText": "All of the below statements are false except for one. Which one of the following statements is true about a two-dimensional array?",
        "options": [
            "It can only store integer values.",
            "It can have a different number of elements in each row.",
            "It cannot be resized once initialized.",
            "All elements in the array must have the same data type."],
        "correctAnswer": "It can have a different number of elements in each row."
    },
    {
        "id": 293,
        "questionText": "What is the value of the expression \"y -= 3\" if y is initially 8?",
        "options": [
            "11",
            "3",
            "8",
            "5"],
        "correctAnswer": "5"
    },
    {
        "id": 294,
        "questionText": "Which operator would you use to check if a user's age is not equal to 18?",
        "options": [
            "(>)",
            "(<)",
            "(==)",
            "(!=)"],
        "correctAnswer": "(!=)"
    },
    {
        "id": 295,
        "questionText": "How do you generate appropriate test data?",
        "options": [
            "Choose random inputs",
            "Only use inputs that aren't close to the boundary conditions",
            "Only test with valid inputs",
            "Test the extremes of the input domain"],
        "correctAnswer": "Test the extremes of the input domain"
    },
    {
        "id": 296,
        "questionText": "Which command is typically used to create a new repository in Git?",
        "options": [
            "git init",
            "git commit",
            "git push",
            "git clone"],
        "correctAnswer": "git init"
    },
    {
        "id": 297,
        "questionText": "What constitutes the most accurate definition of a variable in the context of programming?",
        "options": [
            "A variable is a symbolic name or identifier associated with a storage location that holds a data value.",
            "A variable is a self-contained block of code that performs a specific task or set of tasks.",
            "A variable is a reserved word that has a special meaning and is part of the programming language's syntax.",
            "A variable refers to a specific action or computation that can be performed on data."],
        "correctAnswer": "A variable is a symbolic name or identifier associated with a storage location that holds a data value."
    },
    {
        "id": 298,
        "questionText": "What is the primary focus of privacy-focused browsers?",
        "options": [
            "Optimizing browsing speed",
            "Displaying web content",
            "Supporting web development activities",
            "Enhancing user privacy and security"],
        "correctAnswer": "Enhancing user privacy and security"
    },
    {
        "id": 299,
        "questionText": "What is encryption in the context of software development?",
        "options": [
            "A technique to validate user input",
            "A method to secure software configuration settings",
            "A process of converting data into an unreadable format",
            "A way to test software for vulnerabilities"],
        "correctAnswer": "A process of converting data into an unreadable format"
    },
    {
        "id": 300,
        "questionText": "What is the purpose of instantiating a user-defined class?",
        "options": [
            "To access class-level variables and methods",
            "To modify the existing class definition",
            "To destroy the existing class object",
            "To create a new object based on the class blueprint"],
        "correctAnswer": "To create a new object based on the class blueprint"
    },
    {
        "id": 301,
        "questionText": "def calculate_area(radius):\n    return 3.14 * radius * radius\nr = float(input(\"Enter the radius: \"))\narea = calculate_area(r)\nprint(\"The area is:\", area)\n\nWhich statement represents the input to the function calculate_area?",
        "options": [
            "r = float(input(\"Enter the radius: \"))",
            "print(\"The area is:\", area)",
            "def calculate_area(radius):",
            "return 3.14 * radius * radius"],
        "correctAnswer": "def calculate_area(radius):"
    },
    {
        "id": 302,
        "questionText": "What is space complexity in the context of sorting algorithms?",
        "options": [
            "The size of the input data.",
            "The amount of additional memory used by the algorithm.",
            "The time it takes for the algorithm to complete.",
            "The number of comparisons made by the algorithm."],
        "correctAnswer": "The amount of additional memory used by the algorithm."
    },
    {
        "id": 303,
        "questionText": "What is a challenge in using customer feedback?",
        "options": [
            "Generating crash reports",
            "Understanding technical requirements",
            "Balancing conflicting opinions from different users",
            "Collecting any feedback at all"],
        "correctAnswer": "Balancing conflicting opinions from different users"
    },
    {
        "id": 304,
        "questionText": "Can a function return multiple values simultaneously?",
        "options": [
            "Only when the function is defined as a method within a class can it be structured to send out multiple values simultaneously.",
            "It depends on the programming language whether the function can send out multiple values simultaneously.",
            "No, a function can only have a single return statement but the return statement can send out an array or other data structure containing multiple values.",
            "Yes, in all programming languages, functions can send out multiple values simultaneously."],
        "correctAnswer": "No, a function can only have a single return statement but the return statement can send out an array or other data structure containing multiple values."
    },
    {
        "id": 305,
        "questionText": "What is the primary goal of documentation maintenance?",
        "options": [
            "Eliminating all comments from the code",
            "Keeping documentation accurate and relevant as code changes",
            "Updating documentation only when code is completely rewritten",
            "Creating new documentation for every code change"],
        "correctAnswer": "Keeping documentation accurate and relevant as code changes"
    },
    {
        "id": 306,
        "questionText": "What does instantiation involve in object-oriented programming?",
        "options": [
            "Creating a class",
            "Destroying an object",
            "Modifying an object's state",
            "Creating an object from a class"],
        "correctAnswer": "Creating an object from a class"
    },
    {
        "id": 307,
        "questionText": "What is the benefit of applying responsive design principles to web applications?",
        "options": [
            "Consistent visual design across devices",
            "Enhanced security for web application data",
            "Improved website loading speed",
            "Adaptation of layout and functionality to different screen sizes"],
        "correctAnswer": "Adaptation of layout and functionality to different screen sizes"
    },
    {
        "id": 308,
        "questionText": "let arr = [10, 20, 30, 40, 50];\nlet index = arr.findIndex((element) => element > 30);\nconsole.log(index);\n\nWhat will be the output of the code snippet above?",
        "options": [
            "2",
            "4",
            "1",
            "3"],
        "correctAnswer": "3"
    },
    {
        "id": 309,
        "questionText": "Which search method is suitable for finding a specific word in an unsorted book?",
        "options": [
            "Quick search",
            "Binary search",
            "Hash search",
            "Linear search"],
        "correctAnswer": "Linear search"
    },
    {
        "id": 310,
        "questionText": "Which of the following is NOT a common consideration when selecting a third-party library for integration?",
        "options": [
            "Community support and activity",
            "Price of the library",
            "License compatibility",
            "Code efficiency and performance"],
        "correctAnswer": "Price of the library"
    },
    {
        "id": 311,
        "questionText": "What is the practice of structuring and presenting data in a specific layout or style called?",
        "options": [
            "Data formatting",
            "Cross-platform compatibility",
            "Input validation",
            "Output generation"],
        "correctAnswer": "Data formatting"
    },
    {
        "id": 312,
        "questionText": "Which logical operator negates the result of the expression?",
        "options": [
            "OR",
            "XOR",
            "NOR",
            "NOT"],
        "correctAnswer": "NOT"
    },
    {
        "id": 313,
        "questionText": "What is the purpose of a Trigger in a database?",
        "options": [
            "Execute a set of SQL statements in response to specific events",
            "Create a virtual table",
            "Define the structure of a database table",
            "Optimize data retrieval speed"],
        "correctAnswer": "Execute a set of SQL statements in response to specific events"
    },
    {
        "id": 314,
        "questionText": "What is the index of the first element in an array?",
        "options": [
            "It depends on the array size.",
            "-1",
            "0",
            "1"],
        "correctAnswer": "0"
    },
    {
        "id": 315,
        "questionText": "What purpose do extensions and add-ons serve in specialty browsers?",
        "options": [
            "Optimizing workflows",
            "Ensuring regulatory compliance",
            "Customizing the user interface",
            "Enhancing browser functionality"],
        "correctAnswer": "Enhancing browser functionality"
    },
    {
        "id": 316,
        "questionText": "What does Big-O notation describe in the context of algorithms?",
        "options": [
            "The best-case scenario for an algorithm's performance.",
            "The exact runtime of an algorithm.",
            "The upper bound of an algorithm's time or space complexity.",
            "The lower bound of an algorithm's time complexity"],
        "correctAnswer": "The upper bound of an algorithm's time or space complexity."
    },
    {
        "id": 317,
        "questionText": "What is the purpose of merging branches in version control systems?",
        "options": [
            "To create a new branch from an existing branch.",
            "To combine the changes from one branch into another branch.",
            "To create a new repository from an existing repository.",
            "To revert all changes made in a branch."],
        "correctAnswer": "To combine the changes from one branch into another branch."
    },
    {
        "id": 318,
        "questionText": "What is a potential issue when using fixed-point numbers in arithmetic operations?",
        "options": [
            "Precision loss",
            "Difficulty in performing bitwise operations",
            "Type conversion errors",
            "Increased memory usage"],
        "correctAnswer": "Precision loss"
    },
    {
        "id": 319,
        "questionText": "What is the role of function overloading?",
        "options": [
            "It restricts the use of parameters in functions.",
            "It limits the use of arguments in a function.",
            "It allows multiple functions with the same name but different parameter lists.",
            "It enforces a single function for all data types."],
        "correctAnswer": "It allows multiple functions with the same name but different parameter lists."
    },
    {
        "id": 320,
        "questionText": "Which hosting option is typically the most budget-friendly?",
        "options": ["Shared hosting", "VPS hosting", "Dedicated server", "Cloud hosting"],
        "correctAnswer": "Shared hosting"
    },
    {
        "id": 321,
        "questionText": "All of the following can be used for nested loops except for one. Which one of the following loop structures cannot be used in a nested loop?",
        "options": ["while loop", "switch loop", "for loop", "do-while loop"],
        "correctAnswer": "switch loop"
    },
    {
        "id": 322,
        "questionText": "If x is defined at 6 what value with be returned? 30/x*3^2-8",
        "options": ["217", "316", "37", "45"],
        "correctAnswer": "37"
    },
    {
        "id": 323,
        "questionText": "Which type of error leads to unintended or incorrect program results but does not produce error messages?",
        "options": ["Syntax Error", "Runtime Error", "Logic Error", "Compile-Time Error"],
        "correctAnswer": "Logic Error"
    },
    {
        "id": 324,
        "questionText": "What is the primary goal of output validation?",
        "options": ["Enhancing user experience", "Reducing data size for storage efficiency", "Improving cross-browser compatibility", "Ensuring data is correctly formatted and secure"],
        "correctAnswer": "Ensuring data is correctly formatted and secure"
    },
    {
        "id": 325,
        "questionText": "i = 0\nwhile( i < 100)\n{\n   print(i)\n}\n\nHow many times will this run?",
        "options": ["99", "Infinite number of times", "0", "100"],
        "correctAnswer": "Infinite number of times"
    },
    {
        "id": 326,
        "questionText": "Which algorithmic technique involves breaking down a problem into smaller subproblems and solving each independently?",
        "options": ["Divide and Conquer", "Recursion", "Dynamic Programming", "Brute Force"],
        "correctAnswer": "Divide and Conquer"
    },
    {
        "id": 327,
        "questionText": "What does ADA stand for in the context of web accessibility?",
        "options": ["Americans with Disabilities Act", "American Digital Association", "Accessibility Design Act", "Accessible Development Association"],
        "correctAnswer": "Americans with Disabilities Act"
    },
    {
        "id": 328,
        "questionText": "Which unit is equivalent to 8 bits?",
        "options": ["Megabyte", "Kilobyte", "Byte", "Terabytes"],
        "correctAnswer": "Byte"
    },
    {
        "id": 329,
        "questionText": "Encapsulation helps in achieving which of the following?",
        "options": ["Data hiding and abstraction", "Code reusability", "Polymorphism", "Method overriding"],
        "correctAnswer": "Data hiding and abstraction"
    },
    {
        "id": 330,
        "questionText": "What vulnerability involves weak or flawed authentication and session management mechanisms?",
        "options": ["Broken Authentication", "Broken Access Control", "Injection", "Sensitive Data Exposure"],
        "correctAnswer": "Broken Authentication"
    },
    {
        "id": 331,
        "questionText": "Which data type will you most likely use for performing division (such as y = a / b)?",
        "options": ["Character", "Floating point", "Integer", "Boolean"],
        "correctAnswer": "Floating point"
    },
    {
        "id": 332,
        "questionText": "Given the following code snippet, what will be the output?\n\nmatrix ← [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\noutput to console(matrix[1][2])",
        "options": ["2", "[7,8,9]", "[4,5,6]", "6"],
        "correctAnswer": "6"
    },
    {
        "id": 333,
        "questionText": "What is the decimal equivalent of the binary number 1001?",
        "options": ["8", "12", "10", "9"],
        "correctAnswer": "9"
    },
    {
        "id": 334,
        "questionText": "Which of the following operators checks if two values are not equal?",
        "options": ["(>)", "(==)", "(!=)", "(<)"],
        "correctAnswer": "(!=)"
    },
    {
        "id": 335,
        "questionText": "Which one of the following is an example of an intellectual property right with regards to computer software?",
        "options": ["Creating a user defined class", "Using a Digital Trademark", "Encrypting sensitive data", "Signing a non-disclosure agreement"],
        "correctAnswer": "Using a Digital Trademark"
    },
    {
        "id": 336,
        "questionText": "Which object-oriented concept allows you to treat an object of a derived class as an object of its base class?",
        "options": ["Abstraction", "Inheritance", "Polymorphism", "Encapsulation"],
        "correctAnswer": "Polymorphism"
    },
    {
        "id": 337,
        "questionText": "Which programming language is often used for building interactive web applications and dynamic websites?",
        "options": ["PHP", "JavaScript", "Java", "Python"],
        "correctAnswer": "JavaScript"
    },
    {
        "id": 338,
        "questionText": "In the Request-Response Model of API communication, what typically happens after the client sends a request to the API server?",
        "options": ["The client immediately processes the response.", "The server terminates the connection with the client.", "The server processes the request and sends a response to the client.", "The client sends additional requests without waiting for a response."],
        "correctAnswer": "The server processes the request and sends a response to the client."
    },
    {
        "id": 339,
        "questionText": "What concept specifically addresses the challenges of storing and manipulating data, ensuring optimal memory allocation, and efficient execution of algorithms?",
        "options": ["DRY coding", "SDLC", "Big O notation", "Refactoring"],
        "correctAnswer": "Big O notation"
    },
    {
        "id": 340,
        "questionText": "What does \"visualizing\" refer to as a problem-solving technique prior to writing code?",
        "options": ["Creating mental or visual representations of the problem and its potential solutions", "Choosing the appropriate programming language for the task", "Estimating the time required for coding", "Determining the hardware and software requirements"],
        "correctAnswer": "Creating mental or visual representations of the problem and its potential solutions"
    },
    {
        "id": 341,
        "questionText": "The repeating of instructions in programming is sometimes called what?",
        "options": ["Cloning", "Continuation", "Iteration", "Duplication"],
        "correctAnswer": "Iteration"
    },
    {
        "id": 342,
        "questionText": "Which of the following tools can be used for automated documentation generation?",
        "options": ["Excel", "Microsoft Word", "Sphinx", "PowerPoint"],
        "correctAnswer": "Sphinx"
    },
    {
        "id": 343,
        "questionText": "Which of the following is a valid integer?",
        "options": ["0.5", "0.75", "-25", "0.25"],
        "correctAnswer": "-25"
    },
    {
        "id": 344,
        "questionText": "Which tool is commonly used for inspecting, debugging, and analyzing web pages and applications?",
        "options": ["GitHub", "Google Drive", "Dropbox", "Browser Developer Tools"],
        "correctAnswer": "Browser Developer Tools"
    },
    {
        "id": 345,
        "questionText": "What is the purpose of the \"git pull\" command?",
        "options": ["To discard all local changes and reset to the last commit", "To revert the last commit in the local repository", "To create a new branch in the local repository", "To fetch the latest changes from a remote repository and merge them into the local branch"],
        "correctAnswer": "To fetch the latest changes from a remote repository and merge them into the local branch"
    },
    {
        "id": 346,
        "questionText": "What SQL keyword is used to delete data from a database table?",
        "options": ["REMOVE", "ERASE", "DELETE", "DROP"],
        "correctAnswer": "DELETE"
    },
    {
        "id": 347,
        "questionText": "Which core component of a browser is responsible for displaying web content?",
        "options": ["Security features", "Extensions and add-ons", "Optimized workflows", "Rendering engine"],
        "correctAnswer": "Rendering engine"
    },
    {
        "id": 348,
        "questionText": "Which one of the following is an example of a float assignment?",
        "options": ["x = \"-2.0\"", "x = \"-2\"", "x = -2", "x = -2.0"],
        "correctAnswer": "x = -2.0"
    },
    {
        "id": 349,
        "questionText": "Which one of the following describes works that used to be copyrighted but are now free to use?",
        "options": ["Public domain", "Creative commons", "Open access", "Open source"],
        "correctAnswer": "Public domain"
    },
    {
        "id": 350,
        "questionText": "What role does a \"commit\" play in a version control repository?",
        "options": ["Creating a new branch", "Connecting to a remote repository", "Deleting files from the repository", "Capturing a snapshot of project changes with a message"],
        "correctAnswer": "Capturing a snapshot of project changes with a message"
    },
    {
        "id": 351,
        "questionText": "When restoring a previous version of code, what happens to the changes made in the current version?",
        "options": ["They are temporarily saved as a separate branch.", "They are automatically committed as a new version.", "They are merged with the restored version.", "They are permanently discarded."],
        "correctAnswer": "They are permanently discarded."
    },
    {
        "id": 352,
        "questionText": "Which technique is commonly used to achieve responsiveness in web design according to W3C standards?",
        "options": ["JavaScript pop-ups", "Iframe embedding", "Flash animation", "Media queries"],
        "correctAnswer": "Media queries"
    },
    {
        "id": 353,
        "questionText": "All of these are concerns for spreading viruses EXCEPT ONE. Which one of the following is NOT a concern for spreading viruses?",
        "options": ["SQL Injection", "Unpatched software", "Drive-by downloads", "Email attachments"],
        "correctAnswer": "SQL Injection"
    },
    {
        "id": 354,
        "questionText": "Which of these is the best way to protect your data in your computer system?",
        "options": ["Having up to date screen savers", "Having up to date virus protection", "Only downloading expensive closed-source apps and software", "Having a computer that is less than two years old"],
        "correctAnswer": "Having up to date virus protection"
    },
    {
        "id": 355,
        "questionText": "Which of the following is an example of social engineering?",
        "options": ["Creating fake websites", "Impersonating a trusted entity", "Sending spam emails", "Replicating a computer virus"],
        "correctAnswer": "Impersonating a trusted entity"
    },
    {
        "id": 356,
        "questionText": "What is the purpose of creating a subclass of an existing class in object-oriented programming?",
        "options": ["To create an instance of the existing class", "To inherit the properties and methods of the existing class", "To override the existing properties and methods of the class", "To add new properties and methods to the existing class"],
        "correctAnswer": "To inherit the properties and methods of the existing class"
    },
    {
        "id": 357,
        "questionText": "Write an expression to correctly calculate the remainder when dividing 20 by 7.",
        "options": ["7 % 20", "20 / 7", "7 / 20", "20 % 7"],
        "correctAnswer": "20 % 7"
    },
    {
        "id": 358,
        "questionText": "Which type of loop is represented by the pseudocode below?\n\nFOR index FROM 10 TO 1 STEP -1\n    PRINT \"Countdown: \" + index\nEND FOR",
        "options": ["For loop", "Do-while loop", "Repeat-until loop", "While loop"],
        "correctAnswer": "For loop"
    },
    {
        "id": 359,
        "questionText": "Which search algorithm is more suitable for large-sized arrays?",
        "options": ["Linear search", "The efficiency depends on the elements in the array", "Binary and linear searches have the same efficiency", "Binary search"],
        "correctAnswer": "Binary search"
    },
    {
        "id": 360,
        "questionText": "Why is \"Cross-Browser Compatibility\" important in web development?",
        "options": ["To improve search engine rankings.", "To minimize rendering discrepancies across different web browsers.", "To enhance website speed.", "To ensure consistent website aesthetics."],
        "correctAnswer": "To minimize rendering discrepancies across different web browsers."
    },
    {
        "id": 361,
        "questionText": "In general, in which scenario would you prefer using an abstract class over an interface?",
        "options": ["When you want to achieve multiple inheritances.", "When you want to enforce that a class should implement specific methods.", "When you want to define a contract for implementing classes.", "When you want to provide a common implementation for multiple classes."],
        "correctAnswer": "When you want to provide a common implementation for multiple classes."
    },
    {
        "id": 362,
        "questionText": "Which programming language is commonly used for developing business software?",
        "options": ["Python", "C#", "JavaScript", "Java"],
        "correctAnswer": "Java"
    },
    {
        "id": 363,
        "questionText": "What is the ultimate benefit of applying industry standards in documentation?",
        "options": ["Creating perfect, error-free code", "Reducing the need for testing", "Improving code maintainability, collaboration, and user experience", "Streamlining the development process"],
        "correctAnswer": "Improving code maintainability, collaboration, and user experience"
    },
    {
        "id": 364,
        "questionText": "What is the primary benefit of using well-documented APIs?",
        "options": ["They enable developers to understand and utilize the API's functionality effectively.", "They simplify the development process by automating common tasks.", "They ensure compatibility with all programming languages and frameworks.", "They provide free access to premium features and resources."],
        "correctAnswer": "They enable developers to understand and utilize the API's functionality effectively."
    },
    {
        "id": 365,
        "questionText": "What is the complexity of an algorithm?",
        "options": ["The efficiency of the algorithm in solving a problem", "The time and space required for the algorithm to run", "The number of variables used in the algorithm", "The total number of steps in the algorithm"],
        "correctAnswer": "The time and space required for the algorithm to run"
    },
    {
        "id": 366,
        "questionText": "What term describes a user who spends significantly more on in-app purchases than the average user?",
        "options": ["Affiliate", "LTV", "Subscriber", "Whale"],
        "correctAnswer": "Whale"
    },
    {
        "id": 367,
        "questionText": "What is the purpose of UML diagrams in the context of class relationships?",
        "options": ["Identifying runtime errors", "Visualizing and representing relationships between classes", "Testing code performance", "Representing code implementation details"],
        "correctAnswer": "Visualizing and representing relationships between classes"
    },
    {
        "id": 368,
        "questionText": "How can decomposition of a programming problem aid in code maintenance and troubleshooting?",
        "options": ["It automates the debugging process", "It allows for easier identification and isolation of issues within specific procedures", "It eliminates the need for error handling and exception mechanisms", "It reduces the need for regular updates and improvements"],
        "correctAnswer": "It allows for easier identification and isolation of issues within specific procedures"
    },
    {
        "id": 369,
        "questionText": "Which cloud service model allows developers to focus on coding and deploying applications without managing the underlying infrastructure?",
        "options": ["PaaS (Platform as a Service)", "DaaS (Data as a Service)", "SaaS (Software as a Service)", "IaaS (Infrastructure as a Service)"],
        "correctAnswer": "PaaS (Platform as a Service)"
    },
    {
        "id": 370,
        "questionText": "What does the term \"Theme\" refer to in GUI design?",
        "options": ["Synchronizing data between the GUI and application logic", "A collection of visual elements defining the overall appearance", "Adapting the GUI to different languages", "Designing interfaces for different screen sizes"],
        "correctAnswer": "A collection of visual elements defining the overall appearance"
    },
    {
        "id": 371,
        "questionText": "What is an object in object-oriented programming?",
        "options": ["A piece of code that performs a specific task.", "An instance of a class with its own state and behavior.", "A function that can be called from other parts of the program.", "A special type of data structure."],
        "correctAnswer": "An instance of a class with its own state and behavior."
    },
    {
        "id": 372,
        "questionText": "What is data serialization in the context of API communication?",
        "options": ["A mechanism for securing API endpoints", "A method for hiding the response data from the client", "The conversion of data into a specific format suitable for transmission", "A process for selecting the most valuable API"],
        "correctAnswer": "The conversion of data into a specific format suitable for transmission"
    },
    {
        "id": 373,
        "questionText": "Which programming language provides a comprehensive standard library with a wide range of built-in functions?",
        "options": ["C++", "PHP", "JavaScript", "Python"],
        "correctAnswer": "Python"
    },
    {
        "id": 374,
        "questionText": "All of the following sorting algorithms directly modify the input array EXCEPT ONE. Which one of the following sorting algorithm does NOT directly modifies the input array?",
        "options": ["Selection sort", "Merge sort", "Bubble sort", "In-place sorting"],
        "correctAnswer": "In-place sorting"
    },
    {
        "id": 375,
        "questionText": "In the example x = \"a\", what data type is the value a?",
        "options": ["char", "int", "boolean", "float"],
        "correctAnswer": "char"
    },
    {
        "id": 376,
        "questionText": "What is the primary benefit of version control in platforms like GitHub?",
        "options": ["Document editing", "Real-time collaboration", "File synchronization", "Tracking code changes and managing revisions"],
        "correctAnswer": "Tracking code changes and managing revisions"
    },
    {
        "id": 377,
        "questionText": "In terms of efficiency, which Big-O notation represents the most favorable scenario?",
        "options": ["O(1)", "O(log n)", "O(n^2)", "O(n)"],
        "correctAnswer": "O(1)"
    },
    {
        "id": 378,
        "questionText": "What is encapsulation in object-oriented programming?",
        "options": ["The bundling of data and methods that operate on that data into a single unit.", "The process of creating new data types.", "The practice of exposing all internal details of a class.", "A type of data type."],
        "correctAnswer": "The bundling of data and methods that operate on that data into a single unit."
    },
    {
        "id": 379,
        "questionText": "Which data type is suitable for representing numbers with decimal points and fractional parts?",
        "options": ["Float", "Integer", "Boolean", "String"],
        "correctAnswer": "Float"
    },
    {
        "id": 380,
        "questionText": "What is the primary concern when dealing with resource constraints in data storage and manipulation?",
        "options": ["Minimizing resource usage.", "Ignoring resource usage.", "Using any available resources.", "Maximizing resource usage."],
        "correctAnswer": "Minimizing resource usage."
    },
    {
        "id": 381,
        "questionText": "Which relational operator is used to check if two values are equal?",
        "options": ["!=", "==", "<", ">"],
        "correctAnswer": "=="
    },
    {
        "id": 382,
        "questionText": "Which of the following is not a characteristic of the Waterfall methodology?",
        "options": ["Extensive documentation", "Flexible response to changes", "Sequential stages", "Testing completed near the end"],
        "correctAnswer": "Flexible response to changes"
    },
    {
        "id": 383,
        "questionText": "What is integration testing?",
        "options": ["Testing the user interface of a program", "Testing individual components of a program in isolation", "Testing the performance of a program", "Testing the interactions between different components of a program"],
        "correctAnswer": "Testing the interactions between different components of a program"
    },
    {
        "id": 384,
        "questionText": "If x = 10 and y = 3, what is the value of the expression \"x / y\"",
        "options": ["3.3333", "2", "1", "3"],
        "correctAnswer": "3.3333"
    },
    {
        "id": 385,
        "questionText": "All of the following are service offering cloud based file storage AND real-time synchronization EXCEPT ONE. Which one of the following service does NOT offer both cloud-based file storage and synchronization?",
        "options": ["JSFiddle", "GitHub", "Dropbox", "Google Drive"],
        "correctAnswer": "JSFiddle"
    },
    {
        "id": 386,
        "questionText": "What is the concept of recursion in programming?",
        "options": ["The use of a function within a for loop", "The use of a function that calls itself at the end", "The use of a function that returns multiple values", "The use of a function that has no exit condition"],
        "correctAnswer": "The use of a function that calls itself at the end"
    },
    {
        "id": 387,
        "questionText": "What is a trustworthy practice to ensure data integrity and security when using external storage devices?",
        "options": ["Use any available USB drive", "Format the drive without scanning for viruses", "Use trustworthy thumb drives", "Use a thumb drive you found on campus"],
        "correctAnswer": "Use trustworthy thumb drives"
    },
    {
        "id": 388,
        "questionText": "What is the purpose of including examples and code snippets in documentation?",
        "options": ["To replace the need for descriptive text in the documentation", "To demonstrate how to use different functionalities", "To confuse readers with unnecessary code", "To increase the length of the documentation"],
        "correctAnswer": "To demonstrate how to use different functionalities"
    },
    {
        "id": 389,
        "questionText": "int[] numbers = {1, 2, 3, 4, 5};\nfor (int i = 0; i < numbers.length; i++) {\n    System.out.println(numbers[i]);\n}\n\nWhat will be the starting value of the index variable i in the for loop?",
        "options": ["1", "0", "undefined", "depends on the length of the 'numbers' array"],
        "correctAnswer": "0"
    },
    {
        "id": 390,
        "questionText": "When encountering a syntax error, what should you do to locate the source of the error?",
        "options": ["Ignore the error and run the code again", "Review the code surrounding the reported error", "Rewrite the program", "Change programming languages"],
        "correctAnswer": "Review the code surrounding the reported error"
    },
    {
        "id": 391,
        "questionText": "Which feature in an IDE allows developers to identify and fix errors in the code step by step?",
        "options": ["Debugging", "Auto-Formatting", "Auto-Completion", "Code Snippets"],
        "correctAnswer": "Debugging"
    },
    {
        "id": 392,
        "questionText": "What is a common use case for a two-dimensional array in data science?",
        "options": ["Performing string operations.", "Storing a list of integers", "Storing tabular data, such as a dataset", "Representing a list of items."],
        "correctAnswer": "Storing tabular data, such as a dataset"
    },
    {
        "id": 393,
        "questionText": "What does program-level documentation typically provide an overview of?",
        "options": ["User interface design", "External libraries used in the project", "The entire software program or project", "Individual code functions"],
        "correctAnswer": "The entire software program or project"
    },
    {
        "id": 394,
        "questionText": "Which of the following describes how polymorphism is achieved in object-oriented programming?",
        "options": ["Inheritance and method overriding", "Classes and access modifiers", "Abstract classes and access modifiers", "Abstract classes and interfaces"],
        "correctAnswer": "Inheritance and method overriding"
    },
    {
        "id": 395,
        "questionText": "All of the following are strategies for narrowing down the potential causes of a problem in your code EXCEPT for ONE. Which one of the following approaches would NOT be a strategy for narrowing down the potential causes of a problem in your code?",
        "options": ["Analyze error messages", "Test and validate", "Evaluate and improve", "Reproduce the issue"],
        "correctAnswer": "Evaluate and improve"
    },
    {
        "id": 396,
        "questionText": "How can parameterized queries help prevent SQL injection?",
        "options": ["By encrypting SQL queries before execution", "By validating user input against predefined SQL query patterns", "By allowing unrestricted SQL code execution", "By separating user input from SQL code and automatically handling data escaping"],
        "correctAnswer": "By separating user input from SQL code and automatically handling data escaping"
    },
    {
        "id": 397,
        "questionText": "Accessor methods in object-oriented programming are also known as?",
        "options": ["getters", "modifiers", "setters", "readers"],
        "correctAnswer": "getters"
    },
    {
        "id": 398,
        "questionText": "What type of error is typically detected during the compilation phase and prevents the program from running?",
        "options": ["Semantic Error", "Logic Error", "Syntax Error", "Runtime Error"],
        "correctAnswer": "Syntax Error"
    },
    {
        "id": 399,
        "questionText": "What is the primary reason to choose an interface over an abstract class?",
        "options": ["To encapsulate common behavior and provide a base implementation that can be inherited by subclasses.", "To provide a default implementation or share common behavior among related classes", "To define a contract or set of capabilities to which a class must adhere.", "To maintain state and store common data that can be accessed by subclasses."],
        "correctAnswer": "To define a contract or set of capabilities to which a class must adhere."
    },
    {
        "id": 400,
        "questionText": "Which concept allows you to create multiple branches to experiment with different versions of code and easily switch between them?",
        "options": ["Forking", "Versioning", "Merging", "Branching"],
        "correctAnswer": "Branching"
    },
    {
        "id": 401,
        "questionText": "What ethical principle aligns with the transparency and collaboration of open source systems?",
        "options": ["User freedom and knowledge sharing", "Restriction of software distribution", "Intellectual property protection", "Vendor-controlled software development"],
        "correctAnswer": "User freedom and knowledge sharing"
    },
    {
        "id": 402,
        "questionText": "What does the term \"API\" stand for in the context of client collaboration platforms?",
        "options": ["Access Permission Identifier", "Automated Platform Integration", "Application Programming Interface", "Advanced Project Integration"],
        "correctAnswer": "Application Programming Interface"
    },
    {
        "id": 403,
        "questionText": "Which of the following best describes the purpose of the string length method?",
        "options": ["Determines whether the string contains a specific substring", "Converts the string to uppercase or lowercase letters", "Retrieves the total number of characters in the string", "Splits the string into an array of substrings based on a delimiter"],
        "correctAnswer": "Retrieves the total number of characters in the string"
    },
    {
        "id": 404,
        "questionText": "When storing the status of a light switch (on/off), which data type is best?",
        "options": ["string", "boolean", "float", "integer"],
        "correctAnswer": "boolean"
    },
    {
        "id": 405,
        "questionText": "public class Person {\n    private String name;\n    private int age;\n    public void setName(String name) {\n        this.name = name;\n    }\n    public void setAge(int age) {\n        this.age = age;\n    }\n}\nPerson person1 = new Person();\nperson1.setName(\"John\");\nperson1.setAge(25);\n\nWhich method in the Person class is the modifier method?",
        "options": ["this.age = age;", "setAge()", "person1.setAge(25);", "Person()"],
        "correctAnswer": "setAge()"
    },
    {
        "id": 406,
        "questionText": "What does the \"fork\" operation in collaborative platforms like GitHub involve?",
        "options": ["Uploading local changes to a remote repository", "Creating a personal copy of someone else's repository", "Creating a new branch in your local repository", "Merging changes from a different repository"],
        "correctAnswer": "Creating a personal copy of someone else's repository"
    },
    {
        "id": 407,
        "questionText": "All of the following are types of user inputs that should be validated EXCEPT ONE. Which one of the following types of user input does NOT need to be validated for compliance with data format, data types, and length?",
        "options": ["Mouse clicks", "Passwords", "URLs", "Usernames"],
        "correctAnswer": "Mouse clicks"
    },
    {
        "id": 408,
        "questionText": "What is the purpose of data validation in file and database I/O?",
        "options": ["To prevent SQL injection attacks", "To secure the database connection", "To ensure the accuracy and integrity of data", "To optimize database performance"],
        "correctAnswer": "To ensure the accuracy and integrity of data"
    },
    {
        "id": 409,
        "questionText": "Which Boolean operator returns true if at least one of its operands is true?",
        "options": ["NOT", "AND", "XOR", "OR"],
        "correctAnswer": "OR"
    },
    {
        "id": 410,
        "questionText": "Which factor should be considered when selecting an algorithm for an array-related task",
        "options": ["Efficiency and accuracy", "The length of the array", "The choice of data type", "The size of the elements"],
        "correctAnswer": "Efficiency and accuracy"
    },
    {
        "id": 411,
        "questionText": "Which command is used to retrieve changes from a remote repository to the local repository?",
        "options": ["git fetch", "git commit", "git add", "git push"],
        "correctAnswer": "git fetch"
    },
    {
        "id": 412,
        "questionText": "What does a defense-in-depth approach to security involve?",
        "options": ["Relying on a single security layer", "Implementing input validation only", "Having a firewall in place", "Multiple layers of security measures"],
        "correctAnswer": "Multiple layers of security measures"
    },
    {
        "id": 413,
        "questionText": "What is the suitable data type to represent a true/false condition?",
        "options": ["integer", "string", "boolean", "float"],
        "correctAnswer": "boolean"
    },
    {
        "id": 414,
        "questionText": "Which type of web API is accessible to developers and users without restrictions, typically provided by companies or organizations to enable integration with their services or platforms?",
        "options": ["Private API", "Public API", "Composite API", "Partner API"],
        "correctAnswer": "Public API"
    },
    {
        "id": 415,
        "questionText": "Which of the following is an important aspect of project closing?",
        "options": ["Gathering feedback and documenting lessons learned", "Developing the software solution", "Identifying risks and their mitigation strategies", "Conducting code reviews"],
        "correctAnswer": "Gathering feedback and documenting lessons learned"
    },
    {
        "id": 416,
        "questionText": "Which of the following activities poses the greatest personal cybersecurity risk?",
        "options": ["Making a purchase at an online store that uses public key encryption to transmit credit card information", "Withdrawing money from a bank account using an automated teller machine (ATM)", "Entering your credit card number at a website you found by following a link sent by text.", "Paying a bill using a secure electronic payment system"],
        "correctAnswer": "Entering your credit card number at a website you found by following a link sent by text."
    },
    {
        "id": 417,
        "questionText": "What is the result of adding 128 kilobytes and 256 kilobytes?",
        "options": ["48 Mb", "Kilobytes cannot be added", "384 Kb", "49 152 Kb"],
        "correctAnswer": "384 Kb"
    },
    {
        "id": 418,
        "questionText": "Which method of debugging involves strategically inserting print statements to display variable values and observe control flow?",
        "options": ["Hand-tracing code", "Print statement debugging", "Collaborative debugging", "Real-time debugging"],
        "correctAnswer": "Print statement debugging"
    },
    {
        "id": 419,
        "questionText": "What type of search is less efficient in arrays when looking for a specific element?",
        "options": ["Binary Search", "Hash-based Search", "Depth-First Search", "Linear Search"],
        "correctAnswer": "Linear Search"
    },
    {
        "id": 420,
        "questionText": "Convert the binary number 0100 to decimal.",
        "options": ["4", "2", "10", "5"],
        "correctAnswer": "4"
    },
    {
        "id": 421,
        "questionText": "What is the primary purpose of restoring previous versions of code?",
        "options": ["To create a new commit history", "To undo changes made in a project and revert to a prior state", "To permanently delete all subsequent commits", "To merge conflicting commits automatically"],
        "correctAnswer": "To undo changes made in a project and revert to a prior state"
    },
    {
        "id": 422,
        "questionText": "Which aspect of the CIA triad ensures that authorized users can access information and systems without interruption?",
        "options": ["Confidentiality", "Authentication", "Availability", "Integrity"],
        "correctAnswer": "Availability"
    },
    {
        "id": 423,
        "questionText": "When should code smells be addressed in the software development process?",
        "options": ["At the end of the project", "As soon as they are detected", "Only during code reviews", "During user acceptance testing"],
        "correctAnswer": "As soon as they are detected"
    },
    {
        "id": 424,
        "questionText": "class Employee {\n    constructor(name, age, department) {\n        this.name = name;\n        this.age = age;\n        this.department = department;\n    }\n    changeDepartment(newDepartment) {\n        this.department = newDepartment;\n    }\n}\nlet john = new Employee(\"John Doe\", 25, \"Sales\");\njohn.changeDepartment(\"Marketing\");\n\nWhat is happening in the last line of this code?",
        "options": ["A new instance of the Employee class is created.", "The department attribute of the John object is being modified", "The Deparment method is being defined.", "The Employee class is being defined."],
        "correctAnswer": "The department attribute of the John object is being modified"
    },
    {
        "id": 425,
        "questionText": "When should data sanitization be performed in the input handling process?",
        "options": ["As late as possible in the process", "As early as possible in the process", "Just before storing the data", "After client-side validation"],
        "correctAnswer": "As early as possible in the process"
    },
    {
        "id": 426,
        "questionText": "What does the validation tools check for in HTML and CSS code?",
        "options": ["Aesthetics and design principles.", "Syntax errors and compliance with W3C standards.", "Browser compatibility.", "Website performance."],
        "correctAnswer": "Syntax errors and compliance with W3C standards."
    },
    {
        "id": 427,
        "questionText": "Which among the following variable names can not be used due to its status as a reserved word?",
        "options": ["x", "a2", "bool", "apple"],
        "correctAnswer": "bool"
    },
    {
        "id": 428,
        "questionText": "What should be considered when designing test cases for boundary testing",
        "options": ["Exclude combinations of boundary values", "Focus only on positive scenarios", "Include only the exact boundary values", "Consider both valid and invalid inputs"],
        "correctAnswer": "Consider both valid and invalid inputs"
    },
    {
        "id": 429,
        "questionText": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n    def setRadius(self, newRadius):\n        self.radius = newRadius\n    def getRadius(self):\n        return self.radius\n\ncircle1 = Circle(5)\ncircle1.setRadius(10)\nradius = circle1.getRadius()\n\nWhich one of the following choices is a modifier methods in the Circle class?",
        "options": ["setRadius()", "There are no modifier methods in the code", "__init__()", "Circle(5)"],
        "correctAnswer": "setRadius()"
    },
    {
        "id": 430,
        "questionText": "How does a build system contribute to the reproducibility of software builds?",
        "options": ["By optimizing software performance through runtime profiling and analysis", "By automatically generating user manuals and technical documentation", "By providing code refactoring and code completion capabilities", "By recording and managing build configurations and dependencies"],
        "correctAnswer": "By recording and managing build configurations and dependencies"
    },
    {
        "id": 431,
        "questionText": "Which design pattern ensures that a class has only one instance and provides a global point of access to it?",
        "options": ["Decorator Pattern", "Singleton Pattern", "Observer Pattern", "Factory Method Pattern"],
        "correctAnswer": "Singleton Pattern"
    },
    {
        "id": 432,
        "questionText": "Which one of the following is the smallest unit of storage capacity?",
        "options": ["Terabyte", "Kilobyte", "Gigabyte", "Megabyte"],
        "correctAnswer": "Kilobyte"
    },
    {
        "id": 433,
        "questionText": "Which cloud computing model provides virtualized computing resources as a service?",
        "options": ["Software as a Service (SaaS)", "Remote Desktop Services (RDS)", "Infrastructure as a Service (IaaS)", "Platform as a Service (PaaS)"],
        "correctAnswer": "Infrastructure as a Service (IaaS)"
    },
    {
        "id": 434,
        "questionText": "Which of the following allows for a portion of a copyrighted material to be used in special situations such as educational purposes?",
        "options": ["Digital Millennium Copyright Act", "Fair Recording Standards Act", "Digital Licensing Act", "Fair Use Act"],
        "correctAnswer": "Fair Use Act"
    },
    {
        "id": 435,
        "questionText": "When analyzing the efficiency of an algorithm, which of the following factors should be considered?",
        "options": ["Memory usage only", "Scalability only", "Memory usage, execution speed, and scalability", "Execution speed only"],
        "correctAnswer": "Memory usage, execution speed, and scalability"
    },
    {
        "id": 436,
        "questionText": "What is the process of modifying the behavior of an existing class in object-oriented programming called?",
        "options": ["Abstraction", "Inheritance", "Encapsulation", "Polymorphism"],
        "correctAnswer": "Polymorphism"
    },
    {
        "id": 437,
        "questionText": "Which keyword is used to declare a variable that can hold a single character?",
        "options": ["char", "string", "integer", "boolean"],
        "correctAnswer": "char"
    },
    {
        "id": 438,
        "questionText": "What should you do if your work has been used without your permission online?",
        "options": ["Fill out the incident form on copyright.gov.", "Call the police and file a report", "Contact the website developer directly", "Send a DMCA takedown request to the service provider."],
        "correctAnswer": "Send a DMCA takedown request to the service provider."
    },
    {
        "id": 439,
        "questionText": "What is the base of the binary number system?",
        "options": ["16", "10", "8", "2"],
        "correctAnswer": "2"
    },
    {
        "id": 440,
        "questionText": "let matrix = [[1, 2], [3, 4]];\nconsole.log(matrix[1][1]);\n\nWhat will be printed as the output of the above code?",
        "options": ["4", "3", "1", "2"],
        "correctAnswer": "4"
    },
    {
        "id": 441,
        "questionText": "marks = 75\nif (marks >= 90):\n    print(\"Excellent\")\nelse if (marks >= 70):\n    print(\"Good\")\nelse:\n    print(\"Average\")\n\nWhat is the output to the above code?",
        "options": ["Error: Missing closing bracket", "Average", "Excellent", "Good"],
        "correctAnswer": "Good"
    },
    {
        "id": 442,
        "questionText": "Which database application is known for its support of relational databases and SQL?",
        "options": ["Oracle Databases", "MongoDB", "Code.org's App Lab", "Google Sheets"],
        "correctAnswer": "Oracle Databases"
    },
    {
        "id": 443,
        "questionText": "Which project management tool visually represents tasks over time, often showing dependencies?",
        "options": ["Scrum Board", "Risk Register", "Kanban Board", "Gantt Chart"],
        "correctAnswer": "Gantt Chart"
    },
    {
        "id": 444,
        "questionText": "Why is understanding Big-O notation important in computer science and programming?",
        "options": ["It allows developers to compare and analyze the efficiency of algorithms.", "It quantifies the lower bound of an algorithm's performance.", "It provides a guarantee of the best-case scenario for algorithm performance.", "It helps write code more quickly."],
        "correctAnswer": "It allows developers to compare and analyze the efficiency of algorithms."
    },
    {
        "id": 445,
        "questionText": "Which of the following is a part of the CIA information protection concept that ensures that information is correct and has not been altered?",
        "options": ["Accounting", "Availability", "Integrity", "Confidentiality"],
        "correctAnswer": "Integrity"
    },
    {
        "id": 446,
        "questionText": "What does WCAG stand for?",
        "options": ["W3C Control and Accessibility Guidelines", "Web Content Accessibility Guidelines", "Web Compliance and Accessibility Group", "World Consortium for Accessibility and Guidelines"],
        "correctAnswer": "Web Content Accessibility Guidelines"
    },
    {
        "id": 447,
        "questionText": "Which of the following is an example of encapsulation in a user-defined class",
        "options": ["Creating multiple instances of the class", "Grouping related data and methods together", "Inheriting properties and behaviors from another class", "Keeping data private and providing access through methods"],
        "correctAnswer": "Keeping data private and providing access through methods"
    },
    {
        "id": 448,
        "questionText": "What is the purpose of a rendering context in graphics development?",
        "options": ["To define coordinate systems", "To create and control the display of graphical content", "To store image data", "To create vector graphics"],
        "correctAnswer": "To create and control the display of graphical content"
    },
    {
        "id": 449,
        "questionText": "Convert the decimal number 0110",
        "options": ["4", "5", "6", "9"],
        "correctAnswer": "6"
    },
    {
        "id": 450,
        "questionText": "What is the purpose of overloading in programming?",
        "options": ["Creating new data types.", "Providing a specific implementation for a method inherited from a base class", "Customizing the behavior of inherited methods", "Defining multiple methods with the same name but different parameters."],
        "correctAnswer": "Defining multiple methods with the same name but different parameters."
    },
    {
        "id": 451,
        "questionText": "Which of the following is a set of established guidelines and best practices outlining specific requirements for data security, aligning with the CIA triad principles?",
        "options": ["Legal Compliance", "Risk Tolerance", "Adaptability", "Human Factor"],
        "correctAnswer": "Legal Compliance"
    },
    {
        "id": 452,
        "questionText": "What approach should be used to identify algorithmic errors in code?",
        "options": ["Analyzing error messages", "Ignoring the issue", "Examining Code Logic", "Conducting tests"],
        "correctAnswer": "Examining Code Logic"
    },
    {
        "id": 453,
        "questionText": "What does the term \"freemium\" refer to in app monetization?",
        "options": ["Offering users a free trial period, followed by a subscription", "Providing the app for free with optional in-app purchases", "Displaying advertisements in the app", "Charging users a one-time fee to download the app"],
        "correctAnswer": "Providing the app for free with optional in-app purchases"
    },
    {
        "id": 454,
        "questionText": "What is the main goal of responsive design?",
        "options": ["Optimizing website loading speed", "Enhancing search engine optimization", "Adapting to different screen sizes and devices", "Providing a consistent visual design"],
        "correctAnswer": "Adapting to different screen sizes and devices"
    },
    {
        "id": 455,
        "questionText": "What does the term \"latency\" refer to in the context of web performance?",
        "options": ["The responsiveness of a web server", "The size of images on a webpage", "The delay or lag in data transmission over a network", "The number of web pages on a website"],
        "correctAnswer": "The delay or lag in data transmission over a network"
    },
    {
        "id": 456,
        "questionText": "How can logging help in handling unexpected return values?",
        "options": ["By capturing information for analysis and troubleshooting", "By providing meaningful error messages to users", "By automatically fixing unexpected return values", "By generating stack traces for debugging"],
        "correctAnswer": "By capturing information for analysis and troubleshooting"
    },
    {
        "id": 457,
        "questionText": "What is the main advantage of compiled code?",
        "options": ["More interactive debugging", "Compilation guarantees security", "Easier development process", "Platform-specific optimizations"],
        "correctAnswer": "Platform-specific optimizations"
    },
    {
        "id": 458,
        "questionText": "In which data structure is the order of elements guaranteed?",
        "options": ["Set", "Array", "Graph", "Hash map"],
        "correctAnswer": "Array"
    },
    {
        "id": 459,
        "questionText": "Which of the following expressions is evaluated first in this expression, 4 + 8 / 2 * 3 - 5, according to the precedence of operations?",
        "options": ["Division", "Addition", "Subtraction", "Multiplication"],
        "correctAnswer": "Division"
    },
    {
        "id": 460,
        "questionText": "What is the purpose of a program editor?",
        "options": ["To format and modify code", "To debug and fix code errors", "To collaborate with team members", "To compile and execute code"],
        "correctAnswer": "To format and modify code"
    },
    {
        "id": 461,
        "questionText": "What is the purpose of boundary checks when accessing elements in a two-dimensional array?",
        "options": ["To improve array performance.", "To ensure the array is completely filled.", "To verify that the indices fall within the defined dimensions", "To prevent accidental modification of elements."],
        "correctAnswer": "To verify that the indices fall within the defined dimensions"
    },
    {
        "id": 462,
        "questionText": "let result = 1;\nfor (let i = 1; i <= 4; i++) {\n    for (let j = 1; j <= i; j++) {\n        result *= i - j + 1;\n    }\n}\nconsole.log(result);\n\nWhat will be the output of the above code?",
        "options": ["4896", "21", "288", "61"],
        "correctAnswer": "288"
    },
    {
        "id": 463,
        "questionText": "How can parallel processing be beneficial when working with large two-dimensional arrays?",
        "options": ["It allows for manual manipulation of data.", "It enables data compression", "It simplifies data visualization.", "It distributes tasks across multiple processing units for faster computation."],
        "correctAnswer": "It distributes tasks across multiple processing units for faster computation."
    },
    {
        "id": 464,
        "questionText": "let arr = [3, 5, 2, 1, 4];\narr.reverse();\nconsole.log(arr);\n\nWhat will be the output of the code snippet above?",
        "options": ["[4, 1, 2, 5, 3]", "[5, 4, 3, 2, 1]", "[3, 5, 2, 1, 4]", "[1, 2, 3, 4, 5]"],
        "correctAnswer": "[4, 1, 2, 5, 3]"
    },
    {
        "id": 465,
        "questionText": "Which data structure is indexed by numerical indices starting from 0?",
        "options": ["Tree", "Stack", "Array", "Hash Map"],
        "correctAnswer": "Array"
    },
    {
        "id": 466,
        "questionText": "What does it mean when a function returns None?",
        "options": ["The function returns a value of zero", "The function returns a value of false", "The function encountered an error during execution", "The function is not designed to return any value"],
        "correctAnswer": "The function is not designed to return any value"
    },
    {
        "id": 467,
        "questionText": "Which project management role is responsible for overseeing the project from start to finish, ensuring it stays on schedule and within budget?",
        "options": ["Quality Assurance Specialist", "Scrum Master", "Project Manager", "Developer"],
        "correctAnswer": "Project Manager"
    },
    {
        "id": 468,
        "questionText": "initialize sum at 0\nFor each number i from 1 to 10\n    If i is odd\n        Add i to sum\n    Else\n        Exit the loop\n    End If\nEnd For\nOutput to console(sum)\n\nWhat will be the output of the above code?",
        "options": ["25", "0", "1", "55"],
        "correctAnswer": "1"
    },
    {
        "id": 469,
        "questionText": "How do software defects relate to security vulnerabilities?",
        "options": ["Software defects are security vulnerabilities", "Software defects can lead to security vulnerabilities", "Security vulnerabilities cause software defects", "Software defects and security vulnerabilities are unrelated"],
        "correctAnswer": "Software defects can lead to security vulnerabilities"
    },
    {
        "id": 470,
        "questionText": "class Vehicle \n    constructor(this, make, model) \n        this.make  assigned to make\n        this.model assigned to model\n    method:  getInfo() \n        return concatenateStrings(this.make, \" \", this.model)\nclass Car extends Vehicle \n    constructor(this, make, model, color) \n        super(make, model)\n        this.color assigned to color\n    getInfo() \n        return concatenateStrings(super.getInfo(), \", Color: \", this.color)\nconst CAR assigned to new Car(\"Toyota\", \"Camry\", \"Red\");\nsend to console CAR.getInfo()\n\nWhat is the output of the program?",
        "options": ["Camry, Toyota Color: Red", "Color: Red, Camry, Toyota", "Color: Red, Toyota, Camry", "Toyota Camry, Color: Red"],
        "correctAnswer": "Toyota Camry, Color: Red"
    },
    {
        "id": 471,
        "questionText": "Given the following lines of code:\n\nint a = 4;\nint b = 3;\na += 2 * b;\n\nDetermine the value of a",
        "options": ["6", "10", "4", "18"],
        "correctAnswer": "10"
    },
    
]

def get_random_question():
    """Get a random question that hasn't been used yet"""
    # Get questions that haven't been used yet
    used_questions = session.get('questions_used', [])
    
    # If we've used all questions, reset the used questions array
    if len(used_questions) >= len(all_questions):
        session['questions_used'] = []
        used_questions = []
    
    unused_questions = [q for q in all_questions if q['id'] not in used_questions]
    
    # Pick a random question from unused questions
    selected_question = random.choice(unused_questions)
    
    # Mark this question as used
    used_questions.append(selected_question['id'])
    session['questions_used'] = used_questions
    
    return selected_question

@app.route('/')
def index():
    # Initialize session variables if they don't exist
    if 'correct_answers' not in session:
        session['correct_answers'] = 0
    if 'total_answered' not in session:
        session['total_answered'] = 0
    if 'questions_used' not in session:
        session['questions_used'] = []
    if 'current_question' not in session:
        session['current_question'] = get_random_question()
    if 'answer_submitted' not in session:
        session['answer_submitted'] = False
    if 'user_answer' not in session:
        session['user_answer'] = ""
    
    # Calculate score percentage
    total = session['total_answered']
    score_percentage = round((session['correct_answers'] / total) * 100) if total > 0 else 0
    
    return render_template('tsa-quiz.html', 
                          question=session['current_question'],
                          answer_submitted=session['answer_submitted'],
                          user_answer=session['user_answer'],
                          correct_answers=session['correct_answers'],
                          total_answered=session['total_answered'],
                          score_percentage=score_percentage)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form.get('answer')
    
    # Only process if an answer was actually submitted
    if user_answer:
        session['user_answer'] = user_answer
        session['answer_submitted'] = True
        session['total_answered'] = session['total_answered'] + 1
        
        if user_answer == session['current_question']['correctAnswer']:
            session['correct_answers'] = session['correct_answers'] + 1
    
    return redirect(url_for('index'))

@app.route('/next_question')
def next_question():
    session['current_question'] = get_random_question()
    session['user_answer'] = ""
    session['answer_submitted'] = False
    return redirect(url_for('index'))

@app.route('/reset_stats')
def reset_stats():
    session['correct_answers'] = 0
    session['total_answered'] = 0
    session['questions_used'] = []
    session['current_question'] = get_random_question()
    session['user_answer'] = ""
    session['answer_submitted'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)