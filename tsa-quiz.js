import { useState, useEffect } from 'react';

export default function RandomQuiz() {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [answerSubmitted, setAnswerSubmitted] = useState(false);
  const [correctAnswers, setCorrectAnswers] = useState(0);
  const [totalAnswered, setTotalAnswered] = useState(0);
  const [questionsUsed, setQuestionsUsed] = useState([]);

  // All questions from the document
  const allQuestions = [
    {
      id: 1,
      questionText: "Which software development methodology follows a linear and sequential approach, often with clearly defined stages?",
      options: ["Agile", "Waterfall", "Spiral", "Scrum"],
      correctAnswer: "Waterfall"
    },
    {
      id: 2,
      questionText: "What type of error occurs when the code is grammatically correct and running smoothly, but does not convey the intended meaning of the program?",
      options: ["Logic Error", "Runtime Error", "Semantic Error", "Syntax Error"],
      correctAnswer: "Logic Error"
    },
    {
      id: 3,
      questionText: "Which of the following is the correct hexadecimal representation for the binary number 110011?",
      options: ["66", "CC", "33", "99"],
      correctAnswer: "33"
    },
    {
      id: 4,
      questionText: "What is the main benefit of cloud computing?",
      options: ["Cost-efficiency", "Local infrastructure management", "Physical presence requirement", "Scalability and flexibility"],
      correctAnswer: "Scalability and flexibility"
    },
    {
      id: 5,
      questionText: "What is SQL injection?",
      options: [
        "A security vulnerability caused by inserting malicious SQL code through user input",
        "A technique for securely executing SQL queries with user input",
        "A process of cleaning and validating user input against SQL syntax",
        "A method for preventing unauthorized access to databases"
      ],
      correctAnswer: "A security vulnerability caused by inserting malicious SQL code through user input"
    },
    {
      id: 6,
      questionText: `x = 7
if (x % 2 == 0):
    print("Even")
elif (x % 3 == 0):
    print("Multiple of 3")
else:
    print("Neither")

What is the output to the above code?`,
      options: ["Even", "Neither", "Error: Invalid operator", "Multiple of 3"],
      correctAnswer: "Neither"
    },
    {
      id: 7,
      questionText: "Why is it essential to understand the requirements for constructing new objects?",
      options: [
        "To complicate code readability",
        "To reduce the risk of errors and unexpected behavior",
        "To minimize documentation usage",
        "To introduce inconsistencies in code"
      ],
      correctAnswer: "To reduce the risk of errors and unexpected behavior"
    },
    {
      id: 8,
      questionText: "What is the term for delivering media content in real-time without downloading it?",
      options: ["Content Delivery Networks (CDNs)", "Relational databases", "Streaming services", "File hosting"],
      correctAnswer: "Streaming services"
    },
    {
      id: 9,
      questionText: "What is the purpose of order of operation in software programming?",
      options: [
        "how many mathematical operations are required",
        "which mathematical operation to perform first",
        "which mathematical operations are valid",
        "which mathematical operation are NOT valid"
      ],
      correctAnswer: "which mathematical operation to perform first"
    },
    {
      id: 10,
      questionText: "Which of the following are an example of multi-factor authentication?",
      options: [
        "Asking for a code sent to a phone number",
        "Answering a security question",
        "Solving a Captcha puzzle",
        "Asking for the password to be entered twice"
      ],
      correctAnswer: "Asking for a code sent to a phone number"
    },
    {
      id: 11,
      questionText: "What is the purpose of error recovery in handling runtime errors?",
      options: [
        "To teach the program to automatically fix runtime errors",
        "To prevent the occurrence of runtime errors",
        "To provide alternative paths or fallback actions when runtime errors occur",
        "To display error messages to the user"
      ],
      correctAnswer: "To provide alternative paths or fallback actions when runtime errors occur"
    },
    {
      id: 12,
      questionText: "How can software defects contribute to security vulnerabilities?",
      options: [
        "By ensuring the confidentiality, integrity, and availability of software systems",
        "By improving the performance and usability of software systems",
        "By facilitating easier integration with other software components",
        "By introducing coding errors or design flaws that can be exploited by attackers"
      ],
      correctAnswer: "By introducing coding errors or design flaws that can be exploited by attackers"
    },
    {
      id: 13,
      questionText: "How can version control systems be useful in documentation?",
      options: [
        "They track changes and provide a revision history",
        "They eliminate the need for documentation",
        "They can automatically generate documentation",
        "They restrict access to documentation files"
      ],
      correctAnswer: "They track changes and provide a revision history"
    },
    {
      id: 14,
      questionText: "The phase in the SDLC (system design life cycle) where the system is monitored, maintained, and updated is called:",
      options: ["Testing", "Implementation", "Maintenance", "Planning"],
      correctAnswer: "Maintenance"
    },
    {
      id: 15,
      questionText: "Which strategy involves utilizing online resources and collaborating with colleagues to find solutions?",
      options: ["Test assumptions", "Debugging techniques", "Research and collaborate", "Divide and conquer"],
      correctAnswer: "Research and collaborate"
    }
  ];

  const getRandomQuestion = () => {
    // If we've used all questions, reset the used questions array
    if (questionsUsed.length >= allQuestions.length) {
      setQuestionsUsed([]);
    }
    
    // Get questions that haven't been used yet
    const unusedQuestions = allQuestions.filter(q => !questionsUsed.includes(q.id));
    
    // Pick a random question from unused questions
    const randomIndex = Math.floor(Math.random() * unusedQuestions.length);
    const selectedQuestion = unusedQuestions[randomIndex];
    
    // Mark this question as used
    setQuestionsUsed([...questionsUsed, selectedQuestion.id]);
    
    return selectedQuestion;
  };

  // Initialize with a random question
  useEffect(() => {
    setCurrentQuestion(getRandomQuestion());
  }, []);

  const handleAnswerChange = (e) => {
    setUserAnswer(e.target.value);
  };

  const submitAnswer = () => {
    setAnswerSubmitted(true);
    setTotalAnswered(totalAnswered + 1);
    
    if (userAnswer === currentQuestion.correctAnswer) {
      setCorrectAnswers(correctAnswers + 1);
    }
  };

  const nextQuestion = () => {
    setCurrentQuestion(getRandomQuestion());
    setUserAnswer('');
    setAnswerSubmitted(false);
  };

  const resetStats = () => {
    setCorrectAnswers(0);
    setTotalAnswered(0);
    setQuestionsUsed([]);
    setCurrentQuestion(getRandomQuestion());
    setUserAnswer('');
    setAnswerSubmitted(false);
  };

  if (!currentQuestion) {
    return <div className="text-center p-6">Loading questions...</div>;
  }

  return (
    <div className="flex flex-col p-6 max-w-2xl mx-auto bg-gray-50 rounded-lg shadow-md">
      <div className="mb-4 flex justify-between items-center">
        <span className="text-sm font-medium">Random Question Mode</span>
        <span className="text-sm font-medium">Score: {correctAnswers}/{totalAnswered} ({totalAnswered > 0 ? Math.round((correctAnswers/totalAnswered)*100) : 0}%)</span>
      </div>
      
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">{currentQuestion.questionText}</h2>
        <div className="space-y-2">
          {currentQuestion.options.map((option, index) => (
            <label key={index} className="flex items-center space-x-2 p-2 border rounded hover:bg-gray-100">
              <input
                type="radio"
                name="answer"
                value={option}
                checked={userAnswer === option}
                onChange={handleAnswerChange}
                disabled={answerSubmitted}
                className="form-radio h-5 w-5 text-blue-600"
              />
              <span>{option}</span>
            </label>
          ))}
        </div>
      </div>
      
      {answerSubmitted ? (
        <div className="mb-6">
          <div className={`p-4 rounded ${userAnswer === currentQuestion.correctAnswer ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {userAnswer === currentQuestion.correctAnswer ? 
              'Correct!' : 
              `Incorrect. The correct answer is: ${currentQuestion.correctAnswer}`
            }
          </div>
          <div className="mt-4 flex space-x-4">
            <button
              onClick={nextQuestion}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Next Question
            </button>
            <button
              onClick={resetStats}
              className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Reset Stats
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={submitAnswer}
          disabled={!userAnswer}
          className={`px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            userAnswer ? 'bg-blue-600 text-white hover:bg-blue-700' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          Submit Answer
        </button>
      )}
    </div>
  );
}