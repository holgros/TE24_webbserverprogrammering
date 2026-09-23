# Demonstrera filhantering genom en enkel besöksräknare
from flask import Flask
app = Flask(__name__)
FILE_PATH = "counter.txt" # lägg eventuellt till sökväg via undermapp vid behov

@app.route("/")
def show_nbr_visitors():
    try: # använd undantagshantering när du har med filer att göra!
        with open(FILE_PATH, 'r', encoding='utf-8') as f: # läsa från filen
            number = int(f.read()) # läs och typkonvertera besökarsantalet från fil
            number = number + 1 # öka med ett
        with open(FILE_PATH, 'w', encoding='utf-8') as f: # skriva till filen
            f.write(str(number))
    except:
        return "Fel vid filhantering!"
    return f"Välkommen till sidan! Denna sida har laddats {str(number)} gånger."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # filerna servas via din IP-adress i det lokala nätverket