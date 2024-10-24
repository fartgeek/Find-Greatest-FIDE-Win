from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


games = []

def main(FIDE_ID, rating_type=0):  # 0 is standard, 1 is rapid, and 2 is blitz
    main_url = f"https://ratings.fide.com/calculations.phtml?id_number={FIDE_ID}"

    month = format_month(datetime.now().month)
    year = str(datetime.now().year)
    driver = webdriver.Safari() # EDIT: If you don't have Safari, use the webdriver of your browser. 

    while int(year) >= 2008: # there doesn't seem to be any records before 2008 on the website.
        secondary_url = f"&period={year}-{month}-01&rating={rating_type}"
        URL = main_url + secondary_url
        print(f"Checking URL: {URL}")

        driver.get(URL)

       
        sleep(1) # Change this number to whatever number you feel like. I think it will probably work if you shorten it to even .1 or .2...

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        calc_output = soup.find('div', class_='calc_output')

        if calc_output:
            table = calc_output.find('table', class_='calc_table')

            if table:

                # Iterate over each row in the table (skipping the first four header rows)
                rows = table.find_all('tr')[4:]
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 8:  # Ensure the row has the expected number of columns
                        opponent_name = columns[0].text.strip()  # Opponent's name
                        opponent_rating = columns[3].text.strip()  # Opponent's rating
                        # If the opponent's rating is more than 400 points higher or lower, then the rating looks like this: '1943 *'
                        opponent_rating = opponent_rating.split()[0]  # 1943 * -> 1943
                        game_result = columns[5].text.strip()  # Game result

                        if game_result == '1.00':
                            games.append({
                                'opponent': opponent_name,
                                'rating': opponent_rating,
                                'month': month,
                                'year': year
                            })

            else:
                print("Table not found inside the 'calc_output' div.")
        else:
            print("Div with class 'calc_output' not found on the page.")

        month, year = go_one_month_back(month, year)

    driver.quit()
    opponent_name = ""
    highest_rating = 0
    month = ""
    year = ""
    for game in games:
        if int(game.get('rating')) > highest_rating:
            highest_rating = int(game.get('rating'))
            opponent_name = game.get('opponent')
            month = game.get('month')
            year = game.get('year')

        print(game)

    print("Best WIN:", opponent_name, highest_rating, month, year)



def format_month(month):
    return str(month).zfill(2)

def go_one_month_back(month, year):
    month_int = int(month)
    if month_int > 1:
        return format_month(month_int - 1), year
    else:
        return '12', str(int(year) - 1)


# Example usage
if __name__ == "__main__":
    FIDE_ID = '2039877'  # Example: Levy Rozman. Replace with desired FIDE ID.
    main(FIDE_ID)

