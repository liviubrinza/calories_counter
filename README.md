# Calories Tracker Application (calories_counter)
Python Flask application for tracking calories consumed on a daily basis

Usage:
Python installed with additional modules described in <code>requirements.txt</code>

# Running the application
Startup command for development (only accessible locally): <code>flask --app app run</code>

Startup command for LAN usage (accessible over LAN): <code>flask --app app run --host=0.0.0.0</code>

# Functionalities
- Reads the content of <code>products.csv</code> containing all the products details for 100g: name, calories, protein, fats, carbs
- The list of products can be altered in the <code>products.html</code> page
- Handles daily trackers for 2 people (names are currently hardcoded in the <code>app.py</code> source file
- In the daily tracker, the following pieces of information are shown:
  - Daily consumption statistics: total calories, total protein, total fats, total carbs, and overal consumption percentages
  - A piechert showing the daily macro split
  - A table containing the consumed products, quantities, and their macro breackdown
  - Buttons for persisting the daily consumption table
  - Resetting the daily tracker alltogether
- In the daily tracker, products can be:
  - Searched for
  - Added to the daily consumption table
  - Removed fromthe daily consumption table
  - Quantity of a product altered in the daily consumption table
 
