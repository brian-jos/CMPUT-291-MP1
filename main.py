import sqlite3
import sys # get db through command line, source 6
import random # help generate a more unique sale id
from getpass import getpass # only used to hide password input, source 2
from datetime import datetime # only used to validate date input, source 3

'''
to do
- improve sql queries to be simpler 
- improve sql query for system option 2 (task 2 on spec) to not have to remove NULL entries
- increase domain size of bid and rid with better randomization method
- try to find ways to break inputs or data

sources
1 -> https://www.w3schools.com/python/python_ref_string.asp
2 -> https://stackoverflow.com/questions/9202224/getting-command-line-password-input-in-python
3 -> https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
4 -> https://www.w3schools.com/python/python_try_except.asp
5 -> https://thispointer.com/python-how-to-convert-datetime-object-to-string-using-datetime-strftime/
6 -> https://www.python-course.eu/python3_passing_arguments.php
7 -> https://dbader.org/blog/python-check-if-file-exists
8 -> https://stackoverflow.com/questions/289680/difference-between-2-dates-in-sqlite
9 -> https://www.sqlitetutorial.net/sqlite-functions/sqlite-ifnull/
10 -> https://www.programiz.com/python-programming/methods/string/format
11 -> https://stackoverflow.com/questions/34734572/tabs-in-print-are-not-consistent-python
'''

# helper: creates an sqlite3 connection from database and returns its connections
def _open_sql():
        database = sys.argv[1] # get database name from command line input        
        conn = sqlite3.connect(database)
        c = conn.cursor()
        return conn, c;

# helper: gets results from the query and closes the connection
def _close_sql(conn, c):
        results = c.fetchall() # gets results from query     
        conn.commit()
        conn.close()
        return results;

# helper: check for an existing value in the database
def _existing_value(table, column, value):
        conn, c = _open_sql()

        # look for value in specific table and column
        query = '''SELECT *
                   FROM {}
                   WHERE {} LIKE '{}';
                   '''.format(table, column, value)
        c.execute(query)
        
        results = _close_sql(conn, c)

        # no values found, return false
        if (len(results) == 0):
                return 0;
        
        return 1; # return true

# helper: gets user input for option in a menu
def _get_menu_option(num_options):
        # gets option and loops until valid
        option = _verify_option(input("\nChoose option: "), num_options)
        while (not option):
                print("Invalid option range.");
                option = _verify_option(input("Choose option: "), num_options)
                
        return option

# helper: checks for valid option input
def _verify_option(option, num_choices):
        # option is a digit, if not return false
        if (not option.isdigit()):
                return 0;

        # option is within range of choices, if not return false
        if (int(option) < 1 or int(option) > num_choices):
                return 0;

        return int(option); # returns inputted option

# helper: checks for existing email and its password
def _valid_login(curr_email, pwd):
        conn, c = _open_sql()

        # select matching email and correct password
        query = '''SELECT *
                   FROM users
                   WHERE email LIKE '{}'
                   AND pwd = '{}';
                   '''.format(curr_email, pwd)
        c.execute(query)

        results = _close_sql(conn, c)

        # no results, return false
        if (len(results) == 0):
                return 0;
        
        # no errors, return true
        return 1;

# helper: checks if input for selection matches a result
def _check_selected(selected_value, results):
        # cycle through results for a non case senstive match 
        selected = 0
        for result in results:
                if (selected_value.lower() == result[0].lower()):
                        selected = 1
                        selected_value = result[0]
        
        # no matches
        if (not selected):
                return 0;

        return selected_value;

# login menu: login menu and option prompt
def login_menu():
        print("----- LOGIN MENU -----")
        print("1: Registered login")
        print("2: Unregistered login")
        print("3: Exit program")

        # get user input for option
        num_options = 3
        option = _get_menu_option(num_options)
        
        # option choice
        if (option == 1): # login for registered
                curr_email = registered_login()
        elif (option == 2): # login for unregistered
                curr_email = unregistered_login()
        else: # exit program
                print("\nExiting program...")
                exit()

        # return valid email, or 0 for invalid email
        return curr_email;

# login option 1: registered user options
def registered_login():
        # get email input and check for matching email
        curr_email = input("\nEmail: ")
        while (not _existing_value('users', 'email', curr_email)):
                print("Not an existing email.")
                curr_email = input("Email: ")
                
        # get password input and check for matching email and correct password
        pwd = getpass() # hide password input, source 2
        while (not _valid_login(curr_email, pwd)):
                print("Incorrect password.")
                pwd = getpass()

        return curr_email; # no errors, return valid email

# login option 2: unregistered user options
def unregistered_login():
        # get email input and check domain
        curr_email = input("\nEmail: ")
        while (len(curr_email) < 1 or len(curr_email) > 20 or \
        _existing_value('users', 'email', curr_email)):
                print("Invalid email length or email already exists.")
                curr_email = input("Email: ")

        # name input and domain check
        name = input("Name: ")
        while (len(name) < 1 or len(name) > 16):
                print("Invalid name length.")
                name = input("Name: ")

        # city input and domain check
        city = input("City: ")
        while (len(city) < 1 or len(city) > 15):
                print("Invalid city length.")
                city = input("City: ")

        # gender input and domain check
        gender = input("Gender: ")
        while (len(gender) != 1):
                print("Invalid gender length.")
                gender = input("Gender: ")

        # password input and domain check
        pwd = getpass() # hide password input, source 2
        while ((len(pwd) < 1 or len(pwd) > 4) and pwd != '\n'):
                print("Invalid password length.")
                pwd = getpass()

        conn, c = _open_sql()

        # insert new user into the database
        query = '''INSERT INTO users
                   VALUES ('{}', '{}', '{}', '{}', '{}');
                   '''.format(curr_email, name, pwd, city, gender)
        c.execute(query)
        
        _close_sql(conn, c)

        # return valid email
        return curr_email;

# system menu: display system menu and option prompt
def system_menu(curr_email):
        print("\n---- SYSTEM MENU ----")
        print("1: List products")
        print("2: Search for sales")
        print("3: Post a sale")
        print("4: Search for users")
        print("5: Logout")
        print("6: Exit program")

        # option input
        num_options = 6
        option = _get_menu_option(num_options)

        # option choice
        if (option == 1): # list products
                list_products(curr_email)
        elif (option == 2): # search for sales
                search_sales(curr_email)
        elif (option == 3): # post a sale
                post_sale(curr_email)
        elif (option == 4): # search for users
                search_users(curr_email)
        elif (option == 5): # logout
                print()
                return 0; # logs out, return 0 for login_status
        else: # exit program
                print("\nExiting program...")
                exit()

        # still logged in, return 1 for login_status
        return 1;

# system option 1: list products; improve query to not use distinct
def list_products(curr_email):
        conn, c = _open_sql()

        # task 1, selects products with active sales, order by sale counts
        c.execute('''SELECT p.pid, p.descr, COUNT(distinct pr.rid), AVG(pr.rating), COUNT(distinct s.sid)
                     FROM sales s, products p
                     LEFT OUTER JOIN previews pr ON pr.pid = p.pid
                     WHERE p.pid = s.pid AND s.edate > datetime('now')
                     GROUP BY p.pid
                     ORDER BY COUNT(distinct s.sid) DESC;
                     ''')

        results = _close_sql(conn, c)

        # no products found
        if (len(results) == 0):
                print("No products found.")
                return;

        # display products
        print("#1: prodID, #2: prodDescr, #3: numPRev, #4: avgPRating, #5: numSales") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select product
        selected_pid = _check_selected(input("\nSelect product by identification number: "), results)
        while (not selected_pid):
                print('No matching product.')
                selected_pid = _check_selected(input("Select product by identification number: "), results)
                        
        # open product selection menu
        product_selection(selected_pid, curr_email)

        return;

# product selection: display product menu and option prompt
def product_selection(selected_pid, curr_email):
        print("\nSelected: {}".format(selected_pid))
        print("1: Write a product review")
        print("2: List reviews of product")
        print("3: List active sales of product")
        print("4: Exit menu")
        print("5: Exit program")

        # option input
        num_options = 5
        option = _get_menu_option(num_options)

        # option choice
        if (option == 1): # write review
                write_product_review(selected_pid, curr_email)
        elif (option == 2): # list product reviews
                list_product_reviews(selected_pid)
        elif (option == 3): # list product sales
                list_product_sales(selected_pid, curr_email)
        elif (option == 4): # exit menu
                return;
        else: # exit program
                print("\nExiting program...")
                exit()

        return;

# product option 1: write product review; extend rid domain to be "unlimited"
def write_product_review(selected_pid, curr_email):
        print()

        # set pid to select pid
        pid = selected_pid

        # set reviewer to current user
        reviewer = curr_email

        # check for valid rating input
        while (1):
                try:
                        rating = float(input('Rating (must be float compatible): '))
                        if (rating < 1 or rating > 5):
                                raise Exception()
                        break;
                except:
                        print("Invalid rating format or value.")

        # get review text input and check domain
        rtext = input("Review text: ")
        while (len(rtext) < 1 or len(rtext) > 20):
               print("Invalid review text length.")
               rtext = input("Review text: ")

        # set review date to current datetime
        rdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # generate unique rid with max domain 2; domain should be "unlimited"
        rid = random.randint(1, 99)
        while (_existing_value('previews', 'rid', rid)):
                rid = random.randint(1, 99)
                
        conn, c = _open_sql()

        # task 1a, add product review into database
        query = '''INSERT INTO previews
                   VALUES ({}, '{}', '{}', {}, '{}', '{}');
                   '''.format(rid, pid, reviewer, rating, rtext, rdate)
        c.execute(query)
        
        _close_sql(conn, c)
        
        return;

# product option 2: list product reviews
def list_product_reviews(selected_pid):
        conn, c = _open_sql()

        # task 1b, selects product reviews
        query = '''SELECT *
                   FROM previews pr
                   WHERE pr.pid LIKE '{}';
                   '''.format(selected_pid)
        c.execute(query)
        
        results = _close_sql(conn, c)

        if (len(results) == 0):
                print("No product reviews found.")
                return;

        # display product reviews
        print("#1: prevID, #2: prodID, #3: prevReviewer, #4: prevRating, #5: prevRText, " + \
              "#6: prevRDate") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        return;

# product option 3: list product sales
def list_product_sales(selected_pid, curr_email):
        # datetime() for sql data is based off when the data is inserted into the database
        # need to recreate database each time and quickly list the products for accurate time
        # finding difference between dates, source 8
        time_left = '''CAST(julianday(s.edate) - julianday('now') AS int) AS days,
                       CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int) AS hours,
                       CAST(60*((24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)))
                       - (CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int))) AS int) AS minutes
                       '''
        
        conn, c = _open_sql()

        # task 1c, selects active sales, order by remaining time
        query = '''SELECT s.sid, s.descr, IFNULL(MAX(b.amount), s.rprice), {}
                   FROM sales s
                   LEFT OUTER JOIN bids b ON b.sid = s.sid
                   WHERE s.pid LIKE '{}' AND s.edate > datetime('now')
                   GROUP BY s.sid 
                   ORDER BY julianday(s.edate) - julianday('now');
                   '''.format(time_left, selected_pid)
        c.execute(query)
        
        results = _close_sql(conn, c)

        if (len(results) == 0):
                print("No sales found.")
                return;


        # display sales
        print("#1: saleID, #2: saleDescr, #3: maxBAmount/saleRPrice, #4: daysLeft, #5: hoursLeft, " + \
              "#6: minutesLeft") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select sale
        selected_sid = _check_selected(input("\nSelect sale by identification number: "), results)
        while (not selected_sid):
                print('No matching sale.')
                selected_sid = _check_selected(input("Select sale by identification number: "), results)

        # open sale selection menu
        sale_selection(selected_sid, curr_email)
                
        return;

# system option 2: search for sales; improve sql query
def search_sales(curr_email):
        # input keywords, creates list split by spaces
        keywords = input("\nKeyword(s) input (seperated by spaces): ").split()
        
        # check for empty input
        while (len(keywords) == 0):
                print("Invalid keyword length.")
                keywords = input("Keyword(s) input (seperated by spaces): ").split()
        
        time_left = '''CAST(julianday(s.edate) - julianday('now') AS int) AS days,
                       CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int) AS hours,
                       CAST(60*((24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)))
                       - (CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int))) AS int) AS minutes
                       '''

        keyword_condition = ""
        for i in range(len(keywords)):
                # union for additional keywords
                if (i > 0):
                        keyword_condition += 'UNION ALL '

                # selection query for each keyword
                keyword_condition += '''SELECT s.sid, s.descr, IFNULL(MAX(b.amount), s.rprice), {}
                                        FROM sales s
                                        LEFT OUTER JOIN products p ON p.pid = s.pid
                                        LEFT OUTER JOIN bids b ON b.sid = s.sid
                                        WHERE s.edate > datetime('now')
                                        AND (s.descr LIKE '%{}%' OR p.descr LIKE '%{}%')
                                        UNION ALL 
                                        SELECT s.sid, s.descr, IFNULL(b.amount, s.rprice), {}
                                        FROM sales s
                                        LEFT OUTER JOIN products p ON p.pid = s.pid
                                        LEFT OUTER JOIN bids b ON b.sid = s.sid
                                        WHERE s.edate > datetime('now')
                                        AND (s.descr LIKE '%{}%' OR p.descr LIKE '%{}%')
                                        '''.format(time_left, keywords[i], keywords[i], time_left, keywords[i], keywords[i])

        conn, c = _open_sql()

        # task 2, select sales matching the keywords, order by keyword count
        query = '''SELECT *
                   FROM ({})
                   GROUP BY sid, descr
                   ORDER BY COUNT(*) DESC;
                   '''.format(keyword_condition)
        c.execute(query)
        
        original_results = _close_sql(conn, c)

        # copy results except all NULL column result to prevent crashing
        results = []
        for result in original_results:
                if (result[0] != None):
                        results.append(result)
        
        # no sales found
        if (len(results) == 0):
                print("No sales found.")
                return;

        # display sales
        print("#1: saleID, #2: saleDescr, #3: maxBAmount/saleRPrice, #4: daysLeft, #5: hoursLeft, " + \
              "#6: minutesLeft") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select sale
        selected_sid = _check_selected(input("\nSelect sale by identification number: "), results)
        while (not selected_sid):
                print('No matching sale.')
                selected_sid = _check_selected(input("Select sale by identification number: "), results)

        # open sale menu
        sale_selection(selected_sid, curr_email)
        
        return;

# sale selection: display sale selection menu and option prompt; improve sql query
def sale_selection(selected_sid, curr_email):
        print("\nSelected: {}".format(selected_sid))
        print("Detailed information:")
        
        conn, c = _open_sql()

        # task 3, select associated sale and find more detailed information
        query = '''SELECT s.lister, numRev, avgRat, s.descr, s.edate, s.cond,
                   IFNULL(MAX(b.amount), s.rprice), p.descr, COUNT(pr.pid),
                   IFNULL(AVG(pr.rating), "Product has not been reviewed")
                   FROM (SELECT COUNT(r.reviewee) AS numRev, AVG(r.rating) AS avgRat
                        FROM sales s
                        LEFT OUTER JOIN reviews r ON r.reviewee = s.lister
                        WHERE s.sid LIKE '{}'), sales s
                   LEFT OUTER JOIN bids b ON b.sid = s.sid
                   LEFT OUTER JOIN products p ON p.pid = s.pid
                   LEFT OUTER JOIN previews pr ON pr.pid = s.pid
                   WHERE s.sid LIKE '{}'
                   '''.format(selected_sid, selected_sid)
        c.execute(query)
        
        results = _close_sql(conn, c)

        if (len(results) == 0):
                print("No sales found.")
                return;

        # display detailed info
        print("#1: saleLister, #2: numUReviews, #3: avgURating, #4: saleDescr, #5: saleEDate, " + \
              "#6: saleCond, #7: maxBAmount/saleRPrice, #8: prodDescr, #9: numPrev, #10: avgPRating") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6", "#7", "#8", "#9", "#10")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # display selection options
        print("\nSelection Options:")
        print("1: Place bid on sale")
        print("2: List seller's active sales")
        print("3: List reviews of the seller")
        print("4: Exit menu")
        print("5: Exit program")

        # option input
        num_options = 5
        option = _get_menu_option(num_options)
                
        # option choice
        if (option == 1): # place bid on sale
                bid_on_sale(selected_sid, curr_email)
        elif (option == 2): # list active seller sales
                list_seller_sales(selected_sid, curr_email)
        elif (option == 3): # list seller reviews
                list_seller_reviews(selected_sid)
        elif (option == 4): # exit menu
                return;
        else: # exit program
                print("\nExiting program...")
                exit()

        return;

# sale option 1: bid on sale; extend bid domain to 20
def bid_on_sale(selected_sid, curr_email):
        print()

        # set bidder to current user
        bidder = curr_email

        # set sid to select sid
        sid = selected_sid

        # set bdate to current datetime
        bdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # check for valid amount input
        while (1):
                try:
                        amount = float(input('Amount (must be float compatible): '))
                        break;
                except:
                        print("Invalid amount format.")

        # generate unique bid with max domain 4; increase domain up to 20
        bid = 'B0{}'.format(random.randint(1, 99))
        while (_existing_value('bids', 'bid', bid)):
                bid = 'B0{}'.format(random.randint(1, 99))
                       
        conn, c = _open_sql()

        # task 3a, insert bid into database
        query = '''INSERT INTO bids
                   VALUES ('{}', '{}', '{}', '{}', {});
                   '''.format(bid, bidder, sid, bdate, amount)
        c.execute(query)
        
        _close_sql(conn, c)
        
        return;

# sale option 2: list seller sales
def list_seller_sales(selected_sid, curr_email):
        conn, c = _open_sql()

        # task 3b, select active sales, order by time left
        query = '''SELECT s.sid, s.lister, s.pid, s.edate, s.descr, s.cond, s.rprice
                   FROM (SELECT s.lister
                        FROM sales s
                        WHERE s.sid LIKE '{}') AS seller, sales s
                   WHERE s.lister LIKE seller.lister AND s.edate > datetime('now')
                   ORDER BY julianday(s.edate) - julianday('now');
                   '''.format(selected_sid)
        c.execute(query)
        
        results = _close_sql(conn, c)

        if (len(results) == 0):
                print("No sales found.")
                return;
        
        # display sales
        print("#1: saleID, #2: saleLister, #3: prodID, #4: saleEdate, " + \
              "#5: saleDescr, #6: saleCond, #7: saleRPrice") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6", "#7")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select sale
        selected_sid = _check_selected(input("\nSelect sale by identification number: "), results)
        while (not selected_sid):
                print('No matching sale.')
                selected_sid = _check_selected(input("Select sale by identification number: "), results)

        # open sale menu
        sale_selection(selected_sid, curr_email)
                
        return;

# sale option 3: list reviews of seller
def list_seller_reviews(selected_sid): # here
        conn, c = _open_sql()

        # task 3c, select seller's reviews
        query = '''SELECT r.reviewer, r.reviewee, r.rating, r.rtext, r.rdate
                   FROM (SELECT s.lister
                        FROM sales s
                        WHERE s.sid LIKE '{}') AS seller, reviews r
                   WHERE r.reviewee LIKE seller.lister;
                   '''.format(selected_sid)
        c.execute(query)
        
        results = _close_sql(conn, c)

        # no results found
        if (len(results) == 0):
                print("No reviews found.")
                return;

        # display reviews
        print("#1: revReviewer, #2: revReviewee, #3: revRating, " + \
              "#4: revRText, #5: revRDate") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        return;

# system option 3: post a sale
def post_sale(curr_email):
        # pid input and check domain
        pid = input("\nProduct ID (Use empty input for none): ")
        while (len(pid) > 4):
                print("Invalid product ID length.")
                pid = input("Product ID (Use empty input for none): ")

        # for empty input
        if (len(pid) == 0):
                pid = ''

        # edate input, using try and except to error check, source 4
        while (1):
                try: 
                        edate = input("End date and time (YYYY-MM-DD HH:MM:SS): ")
                        datetime.strptime(edate, "%Y-%m-%d %H:%M:%S") # validate time input, source 3
                        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # current day to string, source 5
                        if (edate <= today or len(edate) != len(today)):
                                raise Exception()
                        break;
                except:
                        print("Wrong datetime format or date is not in the future.")

        # description input and check domain
        descr = input("Description: ")
        while (len(descr) < 1 or len(descr) > 25):
                print("Invalid description length.")
                descr = input("Description: ")

        # condition input and check domain
        cond = input("Condition: ")
        while (len(cond) < 1 or len(cond) > 10):
                print("Invalid condition length.")
                cond = input("Condition: ")
        
        # reserved price and check domain
        rprice = input("Reserved Price (Use empty input for none): ")
        while (len(rprice) > 0 and not rprice.isdigit()):
                print("Invalid reserved price length or non-digit.")
                rprice = input("Reserved Price (Use empty input for none): ")

        
                
        # for empty input
        if (len(rprice) == 0):
                rprice = "0"
        rprice = int(rprice)

        # set lister to current email 
        lister = curr_email

        # generates unique sid with max domain of 4
        sid = 'S0{}'.format(random.randint(1, 99))
        while (_existing_value('sales', 'sid', sid)):
                sid = 'S0{}'.format(random.randint(1, 99))
        
        conn, c = _open_sql()

        # task 4, insert sale into database
        query = '''INSERT INTO sales
                   VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {});
                   '''.format(sid, lister, pid, edate, descr, cond, rprice)
        c.execute(query)
        
        _close_sql(conn, c)

        return;

# system option 4: search for users
def search_users(curr_email):
        # input keyword
        keyword = input("\nEnter a keyword: ")
        while (len(keyword) == 0):
                print("Invalid keyword length.")
                keyword = input("Enter a keyword: ")
        
        conn, c = _open_sql()

        # task 5, select user matching keyword in email or name
        query = '''SELECT email, name, city
                   FROM users
                   WHERE email LIKE '%{}%'
                   OR name LIKE '%{}%';
                   '''.format(keyword, keyword)
        c.execute(query)
        
        results = _close_sql(conn, c)

        
        # no users found
        if (len(results) == 0):
                print("No users found.")
                return;

        # display users
        print("#1: userEmail, #2: userName, #3: userCity") # legend
        print("|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select user
        selected_email = _check_selected(input("\nSelect user by email: "), results)
        while (not selected_email):
                print("No matching user.")
                selected_email = _check_selected(input("Select user by email: "), results)

        # open user selection menu
        user_selection(selected_email, curr_email)

        return;

# user selection: display user selection menu and option prompt
def user_selection(selected_email, curr_email):
        print("\nSelected: {}".format(selected_email))
        print("1: Write a user review")
        print("2: List their active sales")
        print("3: List reviews of the user")
        print("4: Exit menu")
        print("5: Exit program")

        # option input
        num_options = 5
        option = _get_menu_option(num_options)

        # option choice
        if (option == 1): # write review
                write_user_review(selected_email, curr_email)
        elif (option == 2): # list active sales
                list_user_sales(selected_email, curr_email)
        elif (option == 3): # list user reviews
                list_user_reviews(selected_email)
        elif (option == 4): # exit menu
                return;
        else: # exit program
                print("\nExiting program...")
                exit()

        return;

# user option 1: write user review
def write_user_review(selected_email, curr_email):
        print()

        # set reviewer to current user
        reviewer = curr_email

        # set reviewee to selected email
        reviewee = selected_email

        # check for valid rating input
        while (1):
                try:
                        rating = float(input('Rating (must be float compatible): '))
                        if (rating < 1 or rating > 5):
                                raise Exception()
                        break;
                except:
                        print("Invalid rating format or value.")

        # get rtext input and check domain
        rtext = input("Review text: ")
        while (len(rtext) < 1 or len(rtext) > 20):
               print("Invalid review text length.")
               rtext = input("Review text: ")

        # set rdate to current datime
        rdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn, c = _open_sql()

        # task 5a, insert user review into database
        query = '''INSERT INTO reviews
                   VALUES ('{}', '{}', {}, '{}', '{}');
                   '''.format(reviewer, reviewee, rating, rtext, rdate)
        c.execute(query)
                        
        _close_sql(conn, c)
        
        return;

# user option 2: list user sales
def list_user_sales(selected_email, curr_email):
        time_left = '''CAST(julianday(s.edate) - julianday('now') AS int) AS days,
                       CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int) AS hours,
                       CAST(60*((24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)))
                       - (CAST(24*(julianday(s.edate) - julianday('now')
                       - CAST(julianday(s.edate) - julianday('now') AS int)) AS int))) AS int) AS minutes
                       '''
        
        conn, c = _open_sql()

        # task 5b, select user's active sales
        query = '''SELECT s.sid, s.descr, IFNULL(MAX(b.amount), s.rprice), {}
                   FROM sales s
                   LEFT OUTER JOIN bids b ON b.sid = s.sid
                   WHERE s.lister LIKE '{}' AND s.edate > datetime('now')
                   GROUP BY s.sid 
                   ORDER BY julianday(s.edate) - julianday('now');
                   '''.format(time_left, selected_email)
        
        c.execute(query)
        
        results = _close_sql(conn, c)

        # no results
        if (len(results) == 0):
                print('No sales found.')
                return;

        # display sales 
        print("#1: saleID, #2: saleDescr, #3: maxBAmount/saleRPrice, #4: daysLeft, #5: hoursLeft, " + \
              "#6: minutesLeft") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5", "#6")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        # select sale
        selected_sid = _check_selected(input("\nSelect sale by identification number: "), results)
        while (not selected_sid):
                print('No matching sale.')
                selected_sid = _check_selected(input("Select sale by identification number: "), results)

        # open sale menu
        sale_selection(selected_sid, curr_email)
                
        return;

# user option 3: list user reviews
def list_user_reviews(selected_email):
        conn, c = _open_sql()

        # task 5c, select user's reviews
        query = '''SELECT *
                   FROM reviews r
                   WHERE r.reviewee LIKE '{}';
                   '''.format(selected_email)
        c.execute(query)
        
        results = _close_sql(conn, c)

        if (len(results) == 0):
                print("No user reviews found.")
                return;
        
        # display reviews
        print("#1: revReviewer, #2: revReviewee, #3: revRating, #4: revRText, #5: revRDate") # legend
        print("|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|"\
              .format("#1","#2","#3","#4","#5")) # display columns
        for result in results:
                for column in result:
                        if (column == None): # prevent crashing when formatting None type
                                column = "None"
                        print("|{:<20}".format(column),  end = "")
                print("|")

        return;

def main():
        try: # checking for existing file, source 7
                open(sys.argv[1])
        except:
                print('Database file not found.')
                exit()

        # program is running
        print('\nREQUIREMENT 1: Python 3.5, and use "python3" in the terminal.')
        print("REQUIREMENT 2: Stretch the terminal to fit the width of your screen.")
        while (1):
                curr_email = login_menu()
                login_status = 1
                while (login_status and curr_email): # logged in and valid email both are not 0 
                        login_status = system_menu(curr_email) 
        
main()
