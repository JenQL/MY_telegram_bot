import requests
from bs4 import BeautifulSoup
from datetime import datetime


target_numbers = ["1814", "4272", "8292", "3603","6232","1199"]


# Function to fetch 4D results (example scraping logic)
def get_4d_results(date_str=None):
    body_dict = {}
    names = ['Magnum', 'DaMaCai']

    # If no date provided, default to today
    if date_str:
        try:
            # Expecting YYYY-MM-DD format
            today = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            
        except ValueError:
            email_body = f"Invalid date format: {date_str}. Use YYYY-MM-DD."
            return email_body
    else:
        today = datetime.today().strftime("%Y-%m-%d")    

    urls = [f"https://www.4dpredict.app/magnum4d/?d={today}", f"https://www.4dpredict.app/damacai4d/?d={today}"]

    
    
    for url, name in zip(urls,names):
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        prize_rows = soup.find_all("tr", class_="is-size-2 has-text-weight-bold")   
        if not prize_rows:
            email_body = f"No results available for {today}. Skipping alert."
            
            return email_body
            
#             print(f"No results available for {today}. Skipping alert.")
            #exit()  # Stop script if no results
        else:
            prizes = prize_rows[0].find_all("td")
            first, second, third = [td.text.strip() for td in prizes]


        special_prizes = extract_section(soup, "SPECIAL")
        consolation_prizes = extract_section(soup, "CONSOLATION")

        if special_prizes==[]:
            special_prizes = extract_section(soup, "STARTER")

        #Monitor numbers
        results = [first, second, third] + special_prizes + consolation_prizes   # add special/consolation if needed

        matched = [num for num in results if num in target_numbers]

        if matched:
            alert_message = f"Congratulation!! Your numbers appeared: {', '.join(matched)}"
        else:
            alert_message = "No target numbers appeared today."
    #         exit()  # Stop script if no hit

        body_dict[name] = {
            f"4D Results Alert - {name}": url,
            "first": first,
            "second": second,
            "third": third,
            "special": special_prizes,
            "consolation": consolation_prizes,
            "alert": alert_message
        }

    email_body = compile_results(today,body_dict['Magnum'],body_dict['DaMaCai'])   
    return email_body


def extract_section(soup, header_text):
    section = []
    # Find header cell by checking text content (strip whitespace, uppercase)
    header = soup.find("td", class_="titlebet mu",
                       string=lambda t: t and t.strip().upper().startswith(header_text.upper()))


    if header:
        # Walk through sibling rows after the header row
        for row in header.find_parent("tr").find_next_siblings():
            # Stop when another header row appears
            if row.find("td", class_="titlebet mu"):
                break
            # Collect only valid 4-digit numbers
            for td in row.find_all("td"):
                val = td.text.strip()
                if val.isdigit() and len(val) == 4:
                    section.append(val)
                    
    return section



# Example: compile results before sending
def compile_results(today,magnum, damacai):
    body = []
    body.append(f"🎲 Daily 4D Results {today}\n")

    # Magnum
    body.append("Magnum:")
    body.append(f"1st: {magnum['first']}, 2nd: {magnum['second']}, 3rd: {magnum['third']}")
    body.append(f"Special: {', '.join(magnum['special'])}")
    body.append(f"Consolation: {', '.join(magnum['consolation'])}")
    body.append(f"**Alert**: {magnum['alert']}")


    # Damacai
    body.append("Damacai:")
    body.append(f"1st: {damacai['first']}, 2nd: {damacai['second']}, 3rd: {damacai['third']}")
    body.append(f"Special: {', '.join(damacai['special'])}")
    body.append(f"Consolation: {', '.join(damacai['consolation'])}")
    body.append(f"**Alert**: {damacai['alert']}")

    return "\n".join(body)

