from .ai import run

while True:
    print("Enter the message: ")
    message = input()
    response = run(message,False)
    print("Response: ",end="")
    print(response)