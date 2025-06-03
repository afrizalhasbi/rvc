def numtostr(row):
    # Mapping of digits to words in Indonesian
    digit_to_word = {
        "1": " satu ",
        "2": " dua ",
        "3": " tiga ",
        "4": " empat ",
        "5": " lima ",
        "6": " enam ",
        "7": " tujuh ",
        "8": " delapan ",
        "9": " sembilan "
    }
    
    text = row.get("text", "")
   
    for digit, word in digit_to_word.items():
        text = text.replace(digit, word)

    while "  " in text:
      text = text.replace("  ", " ")
    row['text'] = text.strip().lower()
    return row
