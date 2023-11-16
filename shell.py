import tysont

while True:
    text = input("tysont > ")
    result, error = tysont.run('<stdin>', text)
    if error:
        print(error.as_string())
    else:
        print(result)
