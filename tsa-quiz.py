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