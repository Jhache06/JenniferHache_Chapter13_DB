import sqlite3
import matplotlib.pyplot as plt


# Step 1: Create a database and connect to it
def population_JH(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the population table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population (
            city TEXT,
            year INTEGER,
            population INTEGER
        )
    ''')

    return conn, cursor

# Step 2: Insert initial data for cities in Florida
def florida_cities(cursor):
    # Delete existing records to avoid duplicates
    cursor.execute('DELETE FROM population')

    cities = [
        ("Miami", 2023, 549710),
        ("Orlando", 2023, 436699),
        ("Tampa", 2023, 232288),
        ("West Palm Beach", 2023, 890665),
        ("St. Petersburg", 2023, 232288),
        ("Sarasota", 2023, 199867),
        ("Fort Lauderdale", 2023, 604551),
        ("Naples", 2023, 187090),
        ("Ocala", 2023, 114553),
        ("Palm Beach", 2023, 109456)
    ]
    for city in cities:
        cursor.execute('''
                INSERT INTO population (city, year, population)
                VALUES (?, ?, ?)
            ''', city)

# Step 3: Simulate population growth at a 2% annual rate for the next 20 years
def population_growth_rate(cursor):
    # Get the current population for each city in 2023
    cursor.execute('SELECT city, population FROM population WHERE year = 2023')
    data = cursor.fetchall()

    for city, initial_population in data:
        # Insert population data for the next 20 years with 2% growth rate
        for year in range(2024, 2044):
            new_population = int(initial_population * (1.02) ** (year - 2023))
            cursor.execute('''
                INSERT INTO population (city, year, population)
                VALUES (?, ?, ?)
            ''', (city, year, new_population))


# Step 4: Create a function to display population growth of a selected city
def population_growth(cursor):
    while True:
        # Get list of cities
        cursor.execute('SELECT DISTINCT city FROM population')
        cities = [row[0].lower() for row in cursor.fetchall()]  # Convert city names to lowercase

        # Display the header "List of cities"
        print("\nList of cities:")

        # Print a solid line under the header
        print("=" * 30)  # A solid line using 40 '=' characters

        # Display the city names with numbers
        for index, city in enumerate(cities, start=1):  # start=1 to start numbering from 1
            print(f"{index}. {city.capitalize()}")  # Print the city with a number

        # Ask the user to enter a city number or "quit" to exit
        entered_input = input("\nEnter the number of the city you want to view or 'quit' to exit: ").strip().lower()

        # Exit if the user types "quit"
        if entered_input == "quit":
            print("Program Finished")
            break

        # Check if the entered input is a number and valid
        if entered_input.isdigit():
            city_number = int(entered_input) - 1  # Convert input to index
            if 0 <= city_number < len(cities):
                selected_city = cities[city_number]

                # Find the original city name (case-sensitive) corresponding to the entered lowercase city name
                cursor.execute('SELECT DISTINCT city FROM population')
                all_cities = cursor.fetchall()
                original_city = next(city[0] for city in all_cities if city[0].lower() == selected_city)

                # Get population data for the selected city
                cursor.execute('SELECT year, population FROM population WHERE city = ? ORDER BY year', (original_city,))
                data = cursor.fetchall()

                years = [row[0] for row in data]
                populations = [row[1] for row in data]

                # Plotting the population growth
                plt.figure(figsize=(10, 6))
                plt.plot(years, populations, marker='o')
                plt.title(f"Population Growth in {original_city}")
                plt.xlabel('Year')
                plt.ylabel('Population')
                plt.grid(True)
                plt.show()
            else:
                print("Invalid city number. Please choose a number from the list.")
        else:
            print(f"City '{entered_input}' is not available. Please enter a valid number or 'quit' to exit.")

# Main function to execute the program
def main():
    db_name = "population_JH.db"
    conn, cursor = population_JH(db_name)

    # Insert initial data if it's a fresh database
    florida_cities(cursor)

    # Simulate population growth for the next 20 years
    population_growth_rate(cursor)

    # Commit changes and close the connection
    conn.commit()

    # Plot population growth for a selected city
    population_growth(cursor)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
