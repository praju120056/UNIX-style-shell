# 🖥️ UNIX-Style Shell in C

A simple yet functional UNIX-style shell implementation in **C** that mimics basic command-line operations found in traditional UNIX terminals. This project was built to deepen my understanding of process handling, system calls, and terminal interfaces in C.

---

## 📌 Features

✅ Command Execution  
✅ Built-in Commands: `cd`, `exit`, `clear`  
✅ Support for basic UNIX commands: `ls`, `cp`, `mv`, `cat`, `pwd`, `mkdir`, `rmdir`, `touch`  
✅ Command-line prompt with dynamic current working directory display  
✅ Graceful error handling and input sanitization  

---

## 📂 Project Structure  
 
├── main.c # Core shell loop and command parsing  
├── commands.h # Header file with function prototypes  
├── commands.c # Implementation of built-in command functions  
├── Makefile # Compilation instructions  
└── README.md # Project documentation  


---

## ⚙️ How It Works

1. **Displays a prompt** showing the current working directory.
2. **Reads user input** and tokenizes it to identify commands and arguments.
3. **Checks for built-in commands** (`cd`, `exit`, `clear`) and executes them internally.
4. For other commands, it **forks a child process** and uses `execvp()` to run external programs.
5. **Waits for child process termination** before continuing the loop.

---

## 🚀 Getting Started

### 📥 Clone the Repository  

git clone https://github.com/praju120056/UNIX-style-shell.git  
cd UNIX-style-shell


🛠️ Compile the Program  
make

▶️ Run the Shell  
./shell

📸 Demo

/home/user$ ls
main.c  commands.c  commands.h  shell  Makefile  
/home/user$ mkdir testdir  
/home/user$ ls
main.c  commands.c  commands.h  shell  Makefile  testdir  
/home/user$ cd testdir  
/home/user/testdir$ pwd  
/home/user/testdir  
/home/user/testdir$ exit  

---

## 🎯 What I Learned
Process management using fork() and execvp()

Inter-process communication via parent-child processes

Handling system calls in C

Input parsing and string tokenization

Implementing custom command-line utilities

---

## 📌 To-Do (Optional Enhancements)
Implement piping (|) and redirection (>, <)

Add support for background process execution (&)

Command history feature

Auto-completion of commands

---

## 📚 References
UNIX and Linux System Programming Handbook

Linux man pages

---

## 🧑‍💻 Author
Prajakth N Kumar
GitHub | LinkedIn

---

📜 License
This project is licensed under the MIT License — feel free to use, modify, and distribute.

⭐️ If you found this useful, drop a star on the repo!
