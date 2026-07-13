
web_database = {
    "sorting algorithm": "Algorithm to arrange info in a data structure",
    "python function": "Defined using def keyword and performs an effect",
    "deepseeds": "Seeds deep-rooted in AI, all the way from Mile 6"
}

def search_web(query) -> str:
    """
    Agent tool to "search" the web that takes parameter 'query' and tries to match it with any entries on the web, or in this case our dictionary
    """ # DOCSTRING

    print("[TOOL] Executing search_web...\n")

    # llm searches the web through api

    search_q = query.lower()
    if search_q in web_database:
        return web_database[search_q]
    else:
        return ("No results found for ", query)


def read_file(path) -> str:
    """
    Agent tool to read a given file by passing the path to that file to this method as an argument.
    """

    print("[TOOL] Executing read_file...\n")

    try:
        with open (path,"r") as fl:
            content = fl.read()
            fl.close()
        return content
    except FileNotFoundError:
        return "File '" + path + "' does not exist"

def write_file(path, content) -> str:
    """
    Agent tool to write a particular piece of content ot a file given the file's 'path' and 'content' to be written to the file
    """

    print("[TOOL] Executing write_file...\n")

    try:
        with open (path, "w") as fl:
            fl.write(content)
            fl.close
        return "Write to file succesful!"
    except Exception as e:
        return "Error writing to file: " + str(e)

def run_python(code) -> str:
    """
    Agent tool to run generated python code. It takes the code as an argument 'code' and runs it.
    """

    print("[TOOL] Executing run_python...\n")
    if code:
        return "Code ran successfully!"
    else:
        return "We need some code!"

def send_email(to, subject, body) -> str:
    """
    Agent tool to send emails to a recipient with the subject and body of the email. All passed in their separate arguments
    """

    print("[TOOL] Executing send_email...\n")

    print("------------------------------------------------")
    print("To: ", to, "\nSubject: ", subject, "\nBody: ", body)


# Main Function

loop = True

while loop:
    print ("\n=== DAY 02: AGENT TOOLKIT SIMULATOR ===")
    print ("1. Search Web (Mock Database)")
    print ("2. Read a Local File")
    print ("3. Write/Create a Local File")
    print ("4. Run Python Script (Simulated)")
    print ("5. Send Email (print Statement Log)")
    print ("6. Exit Simulator")

    user_choice = int(input("\nEnter your choice: "))

    if user_choice == 6:
        print("Well done AI!")
        break

    elif user_choice == 1:
        user_query = input("Search for something: ")
        print(search_web(user_query))
        
    elif user_choice == 2:
        user_path = input("Enter path to text file: ")
        print(read_file(user_path))
        
    elif user_choice == 3:
        user_path, user_content = input("Enter path to text file: "), input("Enter content to be put into file: ")
        print(write_file(user_path, user_content))
        
    elif user_choice == 4:
        user_code = input("Enter your one line snippet of code: ")
        print(run_python(user_code))
        
    elif user_choice == 5:
        email_rep, email_subj, email_body = input("Enter the email of the recipient: "), input("Enter the subject of the email: "), input("Enter the body of the email: ")
        print(send_email(email_rep, email_subj, email_body))

    else:
        print("Invalid choice. Try agian")