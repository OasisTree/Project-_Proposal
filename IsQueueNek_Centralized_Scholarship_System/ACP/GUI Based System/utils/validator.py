def check_text(prompt):
    if prompt == "" or prompt.isspace():
        return None
    return prompt

def check_input(prompt):
    try:
        return float(prompt)
    except ValueError:       
        return None