'''
This module is used to control the front and back ends of the overall application.
Timetables are calculated and SQLite and the html web interface are
interacted with via this module.
'''


import sqlite3
import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def setup_db():
    '''
    Upon loading the web page this function is called and the databases used by
    the application are created.
    '''

    # Connection to the database is established.
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS department(
    name varchar(50)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS class(
    code varchar(50),
    name varchar(50),
    day varchar(50),
    time varchar(50),
    department varchar(50),
    dems varchar(50),
    skills varchar(5000),
    pref_dem varchar(50))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS demonstrator(
    number varchar(50),
    name varchar(50),
    department varchar(50),
    pref_class Varchar(50),
    availability varchar(600),
    skills varchar(5000),
    exp varchar(5000))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS demAllocation(
    department varchar(50),
    class varchar(50),
    demonstrators varchar(5000))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS credential(
    staff_id varchar(50),
    password varchar(100),
    seniority varchar(50))
    """)
    c.execute("SELECT * FROM credential")
    cred = c.fetchall()
    if len(cred) == 0:
        c.execute("INSERT INTO credential VALUES ('471', 'seacrest81', 'dem')")
        c.execute("INSERT INTO credential VALUES ('725', 'coolcoolcoolcool', 'dem')")
        c.execute("INSERT INTO credential VALUES ('456', 'allterrain', 'lecturer')")
        c.execute("INSERT INTO credential VALUES ('654', 'eltigre', 'lecturer')")
        c.execute("INSERT INTO credential VALUES ('321', 'winger', 'dep')")
        c.execute("INSERT INTO credential VALUES ('643', 'bazinga', 'dep')")
        conn.commit()
    # Connection to the database is closed after the necessary SQL is executed.
    c.close()
    conn.close()
    return render_template('landing_page.html')

# the functions purge and fill_db have been deactivated on the frontend as they are dev only tools.
@app.route('/purge')
def purge():
    '''
    The function drops all tables and creates a replacement in order to empty all
    values from the database. Was used in testing the application.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    c.execute("DROP TABLE department")
    c.execute("DROP TABLE class")
    c.execute("DROP TABLE demonstrator")
    c.execute("DROP TABLE credential")

    c.execute("""
    CREATE TABLE IF NOT EXISTS department(
    name varchar(50))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS class(
    code varchar(50),
    name varchar(50),
    day varchar(50),
    time varchar(50),
    department varchar(50),
    dems varchar(50),
    skills Varchar(5000),
    pref_dem varchar(50))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS demonstrator(
    number varchar(50),
    name varchar(50),
    department varchar(50),
    pref_class Varchar(50),
    availability varchar(600),
    skills varchar(5000),
    exp varchar(5000))
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS credential(
    staff_id varchar(50),
    password varchar(100),
    seniority varchar(50))
    """)

    c.close()
    conn.close()
    return render_template('landing_page.html')

@app.route('/fill_database')
def fill_db():
    '''
    The function fills the database with test values. Also used in testing for ease.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    # Inserts test departments.
    c.execute("INSERT INTO department VALUES ('CIS')")

    # Inserts test classes.
    c.execute("INSERT INTO class VALUES ('CS101', 'Intro to CIS', 'Monday', '9', 'CIS', '2', 'python,java,sql', '321')")
    c.execute("INSERT INTO class VALUES ('CS201', 'Data Structures', 'Wednesday', '10', 'CIS', '2', 'data structures,algorithms', '456')")
    c.execute("INSERT INTO class VALUES ('CS301', 'Database Management', 'Tuesday', '16', 'CIS', '1', 'database management,sql', '456')")
    c.execute("INSERT INTO class VALUES ('CS401', 'Software Engineering', 'Friday', '12', 'CIS', '7', 'software engineering,agile methodologies', '512')")

    # Inserts test demonstrators.
    c.execute("INSERT INTO demonstrator VALUES ('471', 'Jeff Winger', 'CIS', 'CS101', 'Monday9,Monday10,Monday16,Friday16', 'machine learning,java,python', 'python,teaching,10,months.java,working,5,years.machine learning,studying,2,years')")
    c.execute("INSERT INTO demonstrator VALUES ('725', 'Abed Nadir', 'CIS', 'CS401', 'Friday12,Friday13,Friday14', 'software development,agile methodologies', 'agile methodologies,working,8,months.software engineering,working,5,years')")
    c.execute("INSERT INTO demonstrator VALUES ('512', 'Annie Edison', 'CIS', 'CS201', 'Wednesday10,Wednesday11,Friday12', 'programming,algorithms', 'programming,teaching,6,months.algorithms,studying,3,years')")
    c.execute("INSERT INTO demonstrator VALUES ('643', 'Leonard Hofstadter', 'CIS', 'CS301', 'Tuesday16,Thursday9,Thursday10', 'database management,sql', 'database management,teaching,2,years.sql,working,4,years')")
    c.execute("INSERT INTO demonstrator VALUES ('123', 'Britta Perry', 'CIS', 'CS101', 'Monday9,Tuesday14,Thursday16', 'java,python,sql', 'java,teaching,8,months.java,working,2,years')")
    c.execute("INSERT INTO demonstrator VALUES ('456', 'Troy Barnes', 'CIS', 'CS401', 'Wednesday10,Thursday13,Friday12', 'software development,agile methodologies', 'software engineering,studying,1,year.python,working,3,months')")
    c.execute("INSERT INTO demonstrator VALUES ('789', 'Shirley Bennett', 'CIS', 'CS201', 'Monday9,Wednesday10,Friday12', 'programming,algorithms', 'programming,teaching,1,year')")
    c.execute("INSERT INTO demonstrator VALUES ('987', 'Pierce Hawthorne', 'CIS', 'CS301', 'Tuesday16,Thursday11,Friday12', 'database management,sql', 'database management,working,5,years.sql,studying,2,months')")
    c.execute("INSERT INTO demonstrator VALUES ('654', 'Ben Chang', 'CIS', 'CS101', 'Tuesday16,Wednesday10,Thursday15', 'sql', 'java,teaching,10,months.python,working,4,years')")
    c.execute("INSERT INTO demonstrator VALUES ('321', 'Craig Pelton', 'CIS', 'CS401', 'Monday9,Wednesday10,Friday12', 'software development,agile methodologies', 'software engineering,working,7,years.html,studying,3,months')")

    # Creates test login details for staff.
    c.execute("INSERT INTO credential VALUES ('471', 'seacrest81', 'dem')")
    c.execute("INSERT INTO credential VALUES ('725', 'coolcoolcoolcool', 'dem')")
    c.execute("INSERT INTO credential VALUES ('456', 'allterrain', 'lecturer')")
    c.execute("INSERT INTO credential VALUES ('654', 'eltigre', 'lecturer')")
    c.execute("INSERT INTO credential VALUES ('321', 'winger', 'dep')")
    c.execute("INSERT INTO credential VALUES ('643', 'bazinga', 'dep')")
    conn.commit()
    c.close()
    conn.close()
    return render_template('landing_page.html')


@app.route('/go_to_create_timetable')
def go_to_create_timetable():
    '''
    Function that loads the create timetable html page and supplies it with the departments
    saved in the database.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM department")
    list_of_deps = c.fetchall()
    # Adds the database values into a list making it more palatable for the recipient.
    deps = []
    for dep in list_of_deps:
        deps.append(dep)
    return render_template('create_timetable.html', deps=deps)


@app.route('/create_timetable', methods=['POST'])
def create_single_timetable():
    '''
    Function that calculates and forms a timetable for a single department.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    # Starts by clearing demAllocation which is a table used as a one time storage during timtable calculation.
    c.execute("DELETE FROM demAllocation")
    conn.commit()
    c.close()
    conn.close()

    # Loads the department as selected by the user then sends it to rate and allocate function.
    data = request.get_json()
    dep = json.loads(data)
    name = dep["name"]
    rate_and_allocate(name)

    # Return table is created and is the variable set to be returned to the create timetable page.
    # It is being formatted as Monday-Friday, 9am-5pm and in html to make it easier to display on the otherside.
    return_table = '<table><tr><th></th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th></tr>'
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['9', '10', '11', '12', '13', '14', '15', '16', '17']

    '''
    Fills the values in the table with daytime e.g. Monday9 so later
    they can be replaced with classes at the corresponding times.return_table
    Whilst also creating the heading e.g.9 - 10 on the y axis of the table.
    '''
    for time in times:
        return_table += '<tr><th>'+time+'</th>'
        for day in days:
            return_table += '<td>'+day+time+'</td>'
        return_table += '</tr>'

    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class WHERE department = ?", (name,))
    classes = c.fetchall()
    c.execute("SELECT * FROM demonstrator WHERE department = ?", (name,))
    dems = c.fetchall()

    '''
    Creates a dictionary that holds all the values of demonstrators in
    the department as to make handling the data easier.
    Using the staff ID as the key and a dictionary with their data further
    split into a dictionary as the value.
    '''
    dem_values = {}
    for dem in dems:
        dem_values[dem[0]] = {'name':dem[1], 'dep':dem[2], 'pref_class': dem[3], 'avail':dem[4], 'skills': listify_skills(dem[5]), 'exp': listify_exp(dem[6])}

    '''
    Creates a dictionary that holds all the values of classes in
    the department as to make handling the data easier.
    Using the class code as the key and a dictionary with its data further
    split into a dictionary as the value.
    '''
    class_values = {}
    for clas in classes:
        class_values[clas[0]] = {'name': clas[1], 'time': clas[2]+clas[3], 'dep': clas[4], 'nod': clas[5], 'skills': listify_skills(clas[6])}

    # This for loop is used to take the demonstrator allocations held in the table demAllocation and
    #create a string using the allocations to fill in the corresponding day+time value in return_table.
#New
    for time in times:
        for day in days:
            slot = ''   # Is used as the string that replaces the day+time in the return_table.
            classes_at_time = []    # Used to store classes at time slot.
            for clas in class_values:
                # Checks if a class is at the slots time.
                if class_values[clas]['time'] == day+time:
                    classes_at_time.append(clas)
            
            '''
            For loop used to run through classes at time and fill the slot with the
            corresponding classes and their info.
            '''
            for clas in classes_at_time:
                string_of_dems = ''
                c.execute("SELECT demonstrators FROM demAllocation WHERE class = ?", (clas,))
                tuple_class_dems = c.fetchall()
                class_dems = []

                if len(tuple_class_dems) == 0 or int(class_values[clas]['nod']) == 0:
                    class_dems.append('No demonstrator available')
                else:
                    class_dems = tuple_class_dems[0][0].split(',')
                
                for dem in class_dems:
                    if dem == 'No demonstrator available':
                        string_of_dems += 'No demonstrator available, '
                    else:
                        string_of_dems += dem + '-' + dem_values[dem]['name'] + ', '
                string_of_dems = string_of_dems[:-2]
                slot += "Class code: " + clas + ",  Demonstrators: " + string_of_dems + " | "

            return_table = return_table.replace(day+time, slot)
#Old
    '''
    for clas in class_values:
        string_of_dems = ''
        c.execute("SELECT demonstrators FROM demAllocation WHERE class = ?", (clas,))
        tuple_class_dems = c.fetchall()
        class_dems = tuple_class_dems[0][0].split(',') # Reformats to make it usable.

        for dem in class_dems:
        # Used to fill in empties first then actual values.
            if dem == 'No demonstrator available':
                string_of_dems += 'No demonstrator available, '
            elif dem == '':
                string_of_dems += 'No demonstrators requested, '
            else:
                string_of_dems += dem + '-' + dem_values[dem]['name'] +', '
        # Removes comma space at the end of each string.
        string_of_dems = string_of_dems[:-2]
        # Replaces slot with class info.
        return_table = return_table.replace(class_values[clas]['time'], clas+'Demonstrators: '+string_of_dems)
    '''
    # For loop to replace the unused day+time slots with blank value so timetable is not cluttered.
    for time in times:
        for day in days:
            return_table = return_table.replace(day+time, '')      
    c.close()
    conn.close()
    return return_table + '</table>'


@app.route('/create_multi_timetable', methods=['POST'])
def create_multi_timetable():
    '''
    Function that creates a timetable for a user who has selected multiple departments.
    Same process followed as create_timetable function above but adapted for multiple
    departments to be used at once.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("DELETE FROM demAllocation") # Starts by clearing previous use of demAllocation table.
    conn.commit()
    c.close()
    conn.close()

    # Takes the users departments and sends each to rate and allocate function to fill demAllocation
    # with relevant ratings an allocations for departments.
    data = request.get_json()
    dep = json.loads(data)
    names = dep["departments"]
    for name in names:
        rate_and_allocate(name)

    # Establishes the variable to be returned by creating a html styled table that has the days of the week as headings.
    return_table = '<table><tr><th></th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th></tr>'
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    times = ['9', '10', '11', '12', '13', '14', '15', '16', '17']

    '''
    Then creates the vertical headings on the y axis of the table and populates each cell
    with it's corresponding day+time e.g. Wednesday13 so it can later be replaced with
    info about a class at that time.
    '''
    for time in times:
        return_table += '<tr><th>'+time+'</th>'
        for day in days:
            return_table += '<td>'+day+time+'</td>'
        return_table += '</tr>'

    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    dem_values = {}
    class_values = {}
    # Fetches all of the values of classes and demonstrators in the user selected departments.
    for name in names:
        c.execute("SELECT * FROM class WHERE department = ?", (name,))
        classes = c.fetchall()
        c.execute("SELECT * FROM demonstrator WHERE department = ?", (name,))
        dems = c.fetchall()

        '''
        Creates a dictionary that holds all the values of demonstrators in
        the departments as to make handling the data easier.
        Using the staff ID as the key and a dictionary with their data further
        split into a dictionary as the value.
        '''
        for dem in dems:
            dem_values[dem[0]] = {'name':dem[1], 'dep':dem[2], 'pref_class': dem[3], 'avail':dem[4], 'skills': listify_skills(dem[5]), 'exp': listify_exp(dem[6])}

        '''
        Creates a dictionary that holds all the values for classes in
        the departments as to make handling the data easier.
        Using the class code as the key and a dictionary with their data further
        split into a dictionary as the value.
        '''
        for clas in classes:
            class_values[clas[0]] = {'name': clas[1], 'time': clas[2]+clas[3], 'dep': clas[4], 'nod': clas[5], 'skills': listify_skills(clas[6])}

    '''
    For loop that is used to loop through the time slots and fill each slot with relevant class info.
    Had to change the logic slightly from the single department timetable replace method would
    fail to account for two classes at the same time.
    '''
    for time in times:
        for day in days:
            slot = ''   # Is used as the string that replaces the day+time in the return_table.
            classes_at_time = []    # Used to store classes at time slot.
            for clas in class_values:
                # Checks if a class is at the slots time and if the class is part of the departments called.
                if class_values[clas]['time'] == day+time and class_values[clas]['dep'] in names:
                    classes_at_time.append(clas)
            
            '''
            For loop used to run through classes at time and fill the slot with the
            corresponding classes and their info.
            '''
            for clas in classes_at_time:
                string_of_dems = ''
                c.execute("SELECT demonstrators FROM demAllocation WHERE class = ?", (clas,))
                tuple_class_dems = c.fetchall()
                class_dems = []

                if len(tuple_class_dems) == 0 or int(class_values[clas]['nod']) == 0:
                    class_dems.append('No demonstrator available')
                else:
                    class_dems = tuple_class_dems[0][0].split(',')
                
                for dem in class_dems:
                    if dem == 'No demonstrator available':
                        string_of_dems += 'No demonstrator available, '
                    else:
                        string_of_dems += dem + '-' + dem_values[dem]['name'] + ', '
                string_of_dems = string_of_dems[:-2]
                slot += "Class code: " + clas + ",  Demonstrators: " + string_of_dems + " | "

            return_table = return_table.replace(day+time, slot)

    # Removes unused time slots to declutter table.
    for time in times:
        for day in days:
            return_table = return_table.replace(day+time, '')      

    c.close()
    conn.close()

    return return_table + '</table>'


def rate_and_allocate(department_name):
    '''
    Function used to take a department name find each class and demonstrator in
    said department then rate the demonstrators suitability using the scoring system.
    And then allocate the most suited (highest rated) demonstrators to the class.
    Fills demAllocation table so the allocations can be accessed in the original
    function.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class WHERE department = ?", (department_name,))
    classes = c.fetchall()
    c.execute("SELECT * FROM demonstrator WHERE department = ?", (department_name,))
    dems = c.fetchall()

    '''
    This for loop in for loop is used to fill ratings dictionary with demonstrators
    and their ratings for each class in the department. The outer key value pair is
    the demonstrator's staff ID as the key and an inner dictionary as the value.
    The inner dictionary uses the class code as the key to recieve the value. Where the
    value is that demonstrators suitability rating for the class. And initially
    setting each rating as 100.
    '''
    ratings = {}
    for dem in dems:
        class_ratings = {}
        for clas in classes:
            class_ratings[clas[0]] = 100
        ratings[dem[0]] = class_ratings

    '''
    Creates a dictionary that holds all the values of demonstrators in
    the departments as to make handling the data easier.
    Using the staff ID as the key and a dictionary with their data further
    split into a dictionary as the value.
    '''
    dem_values = {}
    for dem in dems:
        dem_values[dem[0]] = {'name':dem[1], 'dep':dem[2], 'pref_class': dem[3], 'avail':dem[4], 'skills': listify_skills(dem[5]), 'exp': listify_exp(dem[6])}

    '''
    Creates a dictionary that holds all the values for classes in
    the departments as to make handling the data easier.
    Using the class code as the key and a dictionary with their data further
    split into a dictionary as the value.
    '''
    class_values = {}
    for clas in classes:
        class_values[clas[0]] = {'name': clas[1], 'time': clas[2]+clas[3], 'dep': clas[4], 'nod': clas[5], 'skills': listify_skills(clas[6]), 'pref_dem':clas[7]}

    '''Loops through the demonstrators and assesses their suitablity for each class
    by seeing which conditions they match or not.
    '''
    for dem in dem_values:
        for clas in class_values:
            # Starts by assessing availability. Marking a dem as 0 if not available in order to make them unselectable.
            if class_values[clas]['time'] not in dem_values[dem]['avail']:
                ratings[dem][clas] = 0
                continue

            # Makes a dem unmissable if they are the requested or preferred demonstrator of the class.
            if class_values[clas]['pref_dem'] == dem:
                ratings[dem][clas] = 10000
                continue
            '''
            Assesses skills required point deductions for missing skills.
            Deductions vary depending on how many skills are missing from required skills list.
            '''
            total_req_skills = len(class_values[clas]['skills'])

            # Skips if there are no required skills.
            if total_req_skills > 0:
                req_skills_met = 0
                # Counts the required skills met by a dem for a class.
                for demSkill in dem_values[dem]['skills']:
                    if demSkill in class_values[clas]['skills']:
                        req_skills_met += 1

                # A series of rating deductions based on number of required skills not there.
                if total_req_skills == 1:
                    if req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                elif total_req_skills == 2:
                    if req_skills_met == 1:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                elif total_req_skills == 3:
                    if req_skills_met == 2:
                        ratings[dem][clas] = ratings[dem][clas] - 20
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                    elif req_skills_met == 1:
                        ratings[dem][clas] = ratings[dem][clas] - 35
                elif total_req_skills == 4:
                    if req_skills_met == 3:
                        ratings[dem][clas] = ratings[dem][clas] - 15
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 60
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                elif total_req_skills == 5:
                    if req_skills_met == 4:
                        ratings[dem][clas] = ratings[dem][clas] - 10
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 70
                    elif req_skills_met == 3:
                        ratings[dem][clas] = ratings[dem][clas] - 20
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 30
                else:
                    if req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 80
                    elif req_skills_met == total_req_skills:
                        pass
                    elif req_skills_met > total_req_skills - 2:
                        ratings[dem][clas] = ratings[dem][clas] - 10
                    elif req_skills_met > total_req_skills - 4:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 50

            '''
            Assesses demonstrator experience based on the skills requested.
            Point alterations vary depending on exp. Uses different multipliers
            for types of experience.
            '''
            for exp in dem_values[dem]['exp']:
                if exp['type'] == 'working':
                    m = 1
                elif exp['type'] == 'teaching':
                    m = 0.75
                else:
                    m = 0.5
                if exp['topic'] in class_values[clas]['skills']:
                    if int(exp['length']) > 7 and exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 30 * m
                    elif int(exp['length']) > 3 and exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 20 * m
                    elif exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 15 * m
                    if int(exp['length']) > 7 and exp['mOrY'] == 'months':
                        ratings[dem][clas] = ratings[dem][clas] + 10 * m
                    elif exp['mOrY'] == 'months':
                        ratings[dem][clas] = ratings[dem][clas] + 5 * m
            # Assess preferred classes giving point buff to dem.
            if dem_values[dem]['pref_class'] == 'NA':
                continue
            elif dem_values[dem]['pref_class'] == clas:
                ratings[dem][dem_values[dem]['pref_class']] += 10

    '''
    Now the rating is done, time for the allocating.
    '''
    classes = 0
    rounds = 0
    no_of_classes = len(class_values)
    allocations = {}
    highest_nod = 0

    '''
    Firstly the allocations dict is populated with classes a key and a list for
    demonstrators allocated to be later appended and highest Number Of Dems(nod)
    is set for each class.
    '''
    for clas in class_values:
        allocations[clas] = []
        if int(class_values[clas]['nod']) > highest_nod:
            highest_nod = int(class_values[clas]['nod'])
    '''
    Now allocations are made. Rounds and classes are used as indexes for the loop.
    rounds is used to count how many demonstrator allocations are needed to fulfill a
    class' requested nod. Highest_nod marking the endpoint and upper limit. Then classes
    counts the number of classes which is also used to track the number of loops required.
    '''
    while rounds < highest_nod:
        for clas in class_values:
            classes += 1
            '''
            Once the classes have all been satisfied the round can increase. And the classes reset
            for a new round to commence.
            '''
            if classes == no_of_classes:
                rounds += 1
                classes = 0
            # Skips class if requested nod is 0 as no allocation is needed for 0.
            if int(class_values[clas]['nod'])==0:
                continue
            # Skips for a class if it's rounds aka allocations is met as it is fulfilled.
            if len(allocations[clas]) >= int(class_values[clas]['nod']):
                continue

            # Used to loop and find the highest rating dem for a class so they can be allocated so long as they are available.
            highest_rating_value = 0
            highest_rating_staff_num = ""
            for dem in dem_values:
                #REMOVED(ratings[dem][clas] > highest_rating_value and len(allocations[clas]) == 0 and class_values[clas]['time'] in dem_values[dem]['avail']) or 
                if ratings[dem][clas] > highest_rating_value and dem not in allocations[clas] and class_values[clas]['time'] in dem_values[dem]['avail']:
                    highest_rating_value = ratings[dem][clas]
                    highest_rating_staff_num = dem

            # If none available aka rating = 0 then skipped else will begin allocating.
            if highest_rating_value == 0:
                if int(class_values[clas]['nod']) == 0:
                    allocations[clas].append('No demonstrator requested')
                else:
                    allocations[clas].append('No demonstrator available')
            else:
                # Tracks which dem is being allocated.
                allocations[clas].append(highest_rating_staff_num)

                '''
                Removing the class' time for the dem's availability to avoid double booking a dem.
                This is made awkward by the varying syntax hence the following elifs.
                '''
                if ',' + class_values[clas]['time'] in dem_values[highest_rating_staff_num]['avail']:
                    dem_values[highest_rating_staff_num]['avail'] = dem_values[highest_rating_staff_num]['avail'].replace(','+class_values[clas]['time'], '')

                elif class_values[clas]['time']+',' in dem_values[highest_rating_staff_num]['avail']:
                    dem_values[highest_rating_staff_num]['avail'] = dem_values[highest_rating_staff_num]['avail'].replace(class_values[clas]['time']+',', '')

                else:
                    dem_values[highest_rating_staff_num]['avail'] = dem_values[highest_rating_staff_num]['avail'].replace(class_values[clas]['time'], '')

    # This loop takes the allocations dict and lists and inserts the department, class and allocated dems to the demAllocation table.
    for allo in allocations:
        string_of_dems = ''
        for i in allocations[allo]:
            string_of_dems += i + ','
        string_of_dems = string_of_dems[:-1]
        c.execute("INSERT INTO demAllocation VALUES(?, ?, ?)", (class_values[allo]['dep'], allo, string_of_dems,))
        conn.commit()


@app.route('/single_analysis', methods=['POST'])
def single_analysis():
    '''
    This function analyses the allocation of demonstrators for single departments, by responding to the front-end
    with a table stating who the best rated demonstrator and the worst rated demonstartor for
    the class was.
    '''
    data = request.get_json()
    dep = json.loads(data)
    analyse = dep["name"]

    '''The return value is formatted to display in a HTML div. This is for ease so the data
    processing is all done on this end.
    '''
    return_value = "<p>Analysis of demonstrator's suitablity:</p><table><tr><th>Class</th><th>Available Demonstrators</th><th>Analysis</th></tr>"
    rate_dict = rate(analyse)
    dem_values = rate_dict["dem_values"]                                                                                                            # May need changed to match dict value in HTML....
    class_values = rate_dict["class_values"]
    ratings = rate_dict["ratings"]

    # For loop is used to fill in the details of which demonstrator was best and worst rated for the class.

    for clas in class_values:
        return_value += "<tr><th>" + clas + "</th>"
        avail_dems_ret_value = ''
        for dem in dem_values:
            # Dem has to be available to have score > 0.
            if ratings[dem][clas] > 0:
                skills = ''
                exps = ''
                for skill in dem_values[dem]['skills']:
                    skills += skill +', '
                for exp in dem_values[dem]['exp']:
                    exps += exp['type']+' in '+exp['topic']+' for '+exp['length']+' '+exp['mOrY']+', '
                skills = skills[:-2]
                exps = exps[:-2]
                avail_dems_ret_value += dem + "- " + dem_values[dem]['name'] + " Skills: " + skills + " Experience: " + exps
        # If statement filters out instances where there are no dems available at that time.
        if avail_dems_ret_value == '':
            return_value += "<td></td><td>No demonstrators available.</td></tr>"
        else:
            return_value += "<td>" + avail_dems_ret_value + "</td><td>"
            best_rating = ''
            best_rating_score = 0
            worst_rating = ''
            worst_rating_score = 10000
            for dem in dem_values:
                if ratings[dem][clas] > best_rating_score:
                    best_rating = dem
                    best_rating_score = ratings[dem][clas]
                if ratings[dem][clas] < worst_rating_score and ratings[dem][clas] > 0:
                    worst_rating = dem
                    worst_rating_score = ratings[dem][clas]
            return_value += "Highest rated available demonstrator for class: " + best_rating + ". Lowest rated available demonstrator for class: " + worst_rating + "</td></tr>"
    return return_value + "</table>"

@app.route('/multi_analysis', methods = ['POST'])
def multi_analysis():
    '''
    This function analyses the allocation of demonstrators for multiple departments, by responding to the front-end
    with a table stating who the best rated demonstrator and the worst rated demonstartor for
    the class was.
    '''
    data = request.get_json()
    dep = json.loads(data)
    analyse = dep["departments"]
    '''
    Same as single analysis, the data is processed into a HTML table foramt so it can be plugged directly into div
    on the front_end side.
    '''
    return_value = "<p>Analysis of demonstrator's suitablity:</p><table><tr><th>Class</th><th>Available Demonstrators</th><th>Analysis</th></tr>"

    '''
    Same process as single analysis too just slightly adjusted to manage multiple departments, that is what
    the while loop and i counter is for. While loop is used to process the dem and class values and ratings into
     there own dicts. So the data is easier to handle.
    '''
    i = 0
    while i < len(analyse):
        # Initialises the dicts.
        if i == 0:
            rate_dict = rate(analyse[i])
            dem_values = rate_dict['dem_values']
            class_values = rate_dict['class_values']
            ratings = rate_dict['ratings']
            i += 1
            continue
        # Fills the dicts after they have been initialised.
        rate_dict = rate(analyse[i])                                    # Line may not be necessary since rate dict is established in if statement above...........................
        for dem in rate_dict['dem_values']:
            dem_values[dem] = rate_dict['dem_values'][dem]
        for clas in rate_dict['class_values']:
            class_values[clas] = rate_dict['class_values'][clas]
        for dem in rate_dict['ratings']:
            ratings[dem] = rate_dict['ratings'][dem]
        i += 1

    '''
    Once the values have been put into the dicts the data can be analysed easily in
    that same manner as above in single analysis.
    '''
    for clas in class_values:
        return_value += "<tr><th>" + clas + "</th>"
        avail_dems_ret_value = ''
        for dem in dem_values:
            if dem_values[dem]['dep'] != class_values[clas]['dep']:
                continue
            if ratings[dem][clas] > 0:
                skills = ''
                exps = ''
                for skill in dem_values[dem]['skills']:
                    skills += skill + ', '
                for exp in dem_values[dem]['exp']:
                    exps += exp['type']+' in '+exp['topic']+' for '+exp['length']+' '+exp['mOrY']+', '
                skills = skills[:-2]
                exps = exps[:-2]
                avail_dems_ret_value += dem + "- " + dem_values[dem]['name'] + " Skills: " + skills + " Experience: " + exps
        if avail_dems_ret_value == '':
            return_value += "<td></td><td>No demonstrators available.</td></tr>"
        else:
            return_value += "<td>" + avail_dems_ret_value + "</td><td>"
            best_rating = ''
            best_rating_score = 0
            worst_rating = ''
            worst_rating_score = 10000
            for dem in dem_values:
                if dem_values[dem]['dep'] != class_values[clas]['dep']:
                    continue
                if ratings[dem][clas] > best_rating_score:
                    best_rating = dem
                    best_rating_score = ratings[dem][clas]
                if ratings[dem][clas] < worst_rating_score and ratings[dem][clas] > 0:
                    worst_rating = dem
                    worst_rating_score = ratings[dem][clas]
        return_value += "Highest rated available demonstrator for class: " + best_rating + ". Lowest rated available demonstrator for class: " + worst_rating + "</td></tr>"
    return return_value + "</table>"

'''if avail_dems_ret_value == '':
            return_value += "<td></td><td>No demonstrators available.</td></tr>"
        else:
            return_value += "<td>" + avail_dems_ret_value + "</td><td>"
            best_rating = ''
            best_rating_score = 0
            worst_rating = ''
            worst_rating_score = 10000
            for dem in dem_values:
                if ratings[dem][clas] > best_rating_score:
                    best_rating = dem
                    best_rating_score = ratings[dem][clas]
                if ratings[dem][clas] < worst_rating_score and ratings[dem][clas] > 0:
                    worst_rating = dem
                    worst_rating_score = ratings[dem][clas]
            return_value += "Highest rated available demonstrator for class: " + best_rating + ". Lowest rated available demonstrator for class: " + worst_rating + "</td></tr>"
    return return_value + "</table>"'''
def rate(department_name):
    '''
    This function is the exact same as the first half of the rate and allocate function. Used by the analysis
    functions above to just rate the allocations. It returns the values as a dict for ease of use in the
    analysis functions.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class WHERE department = ?", (department_name,))
    classes = c.fetchall()
    c.execute("SELECT * FROM demonstrator WHERE department = ?", (department_name,))
    dems = c.fetchall()

    ratings = {}
    for dem in dems:
        class_ratings = {}
        for clas in classes:
            class_ratings[clas[0]] = 100
        ratings[dem[0]] = class_ratings

    dem_values = {}
    for dem in dems:
        dem_values[dem[0]] = {'name':dem[1], 'dep':dem[2], 'pref_class': dem[3], 'avail':dem[4], 'skills': listify_skills(dem[5]), 'exp': listify_exp(dem[6])}
    
    class_values = {}
    for clas in classes:
        class_values[clas[0]] = {'name': clas[1], 'time': clas[2]+clas[3], 'dep': clas[4], 'nod': clas[5], 'skills': listify_skills(clas[6]), 'pref_dem':clas[7]}

    #loop through the dems and assess their suitablity for each class by seeing which conditions they match or not
    for dem in dem_values:
        for clas in class_values:
            #Assess availability
            if class_values[clas]['time'] not in dem_values[dem]['avail']:
                ratings[dem][clas] = 0
                continue
            # Assess preferred demonstrator
            if class_values[clas]['pref_dem'] == dem:
                ratings[dem][clas] = 10000
                continue
            #Assess skills required
            total_req_skills = len(class_values[clas]['skills'])
            if total_req_skills > 0:
                req_skills_met = 0
                for demSkill in dem_values[dem]['skills']:
                    if demSkill in class_values[clas]['skills']:
                        req_skills_met += 1

                if total_req_skills == 1:
                    if req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                elif total_req_skills == 2:
                    if req_skills_met == 1:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                elif total_req_skills == 3:
                    if req_skills_met == 2:
                        ratings[dem][clas] = ratings[dem][clas] - 20
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 50
                    elif req_skills_met == 1:
                        ratings[dem][clas] = ratings[dem][clas] - 35
                elif total_req_skills == 4:
                    if req_skills_met == 3:
                        ratings[dem][clas] = ratings[dem][clas] - 15
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 60
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                elif total_req_skills == 5:
                    if req_skills_met == 4:
                        ratings[dem][clas] = ratings[dem][clas] - 10
                    elif req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 70
                    elif req_skills_met == 3:
                        ratings[dem][clas] = ratings[dem][clas] - 20
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 30
                else:
                    if req_skills_met == 0:
                        ratings[dem][clas] = ratings[dem][clas] - 80
                    elif req_skills_met == total_req_skills:
                        pass
                    elif req_skills_met > total_req_skills - 2:
                        ratings[dem][clas] = ratings[dem][clas] - 10
                    elif req_skills_met > total_req_skills - 4:
                        ratings[dem][clas] = ratings[dem][clas] - 25
                    else:
                        ratings[dem][clas] = ratings[dem][clas] - 50
            #Assess experience
            for exp in dem_values[dem]['exp']:
                if exp['type'] == 'working':
                    m = 1
                elif exp['type'] == 'teaching':
                    m = 0.75
                else:
                    m = 0.5
                if exp['topic'] in class_values[clas]['skills']:
                    if int(exp['length']) > 7 and exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 30*m
                    elif int(exp['length']) > 3 and exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 20*m
                    elif exp['mOrY'] == 'years':
                        ratings[dem][clas] = ratings[dem][clas] + 15*m
                    if int(exp['length']) > 7 and exp['mOrY'] == 'months':
                        ratings[dem][clas] = ratings[dem][clas] + 10*m
                    elif exp['mOrY'] == 'months':
                        ratings[dem][clas] = ratings[dem][clas] + 5*m
            #Assess preferred classes
            if dem_values[dem]['pref_class'] == 'NA':
                continue
            elif dem_values[dem]['pref_class'] == clas:
                ratings[dem][dem_values[dem]['pref_class']] += 10
    ret_dict = {}
    ret_dict["dem_values"] = dem_values
    ret_dict["class_values"] = class_values
    ret_dict["ratings"] = ratings
    return(ret_dict)


def listify_skills(skills_string):
    '''
    Function that makes a comma separated string of skills into a list. Used to unformat the values saved
    as a string storing demonstrators/classes required skills in the database into an easy to use list.
    '''
    skills_list = []
    if ',' in skills_string:
        skills_list = skills_string.split(',')
    else:
        skills_list.append(skills_string)
    return skills_list


def listify_exp(exp_string):
    '''
    Function used to turn the string of demonstrator experiences held in the database into a list. By
    separating the string first at the '.', splits them down a single experience. Then splitting them at
    the ',' to split the experience into the 4 key parts tha the system can then use and putting the data
    into a list of dicts for ease of use.
    '''
    if exp_string == '':
        return exp_string
    exp_list = []
    if '.' in exp_string:
        exp_dot_split = exp_string.split('.')
        for exp in exp_dot_split:
            exp_comma_split = exp.split(',')
            exp_list.append({'topic':exp_comma_split[0], 'type':exp_comma_split[1], 'length':exp_comma_split[2], 'mOrY':exp_comma_split[3]})
    else:
        exp_comma_split = exp_string.split(',')
        exp_list.append({'topic':exp_comma_split[0], 'type':exp_comma_split[1], 'length':exp_comma_split[2], 'mOrY':exp_comma_split[3]})
    return exp_list


@app.route('/go_to_login_page')
def go_to_login_page():
    '''
    Function that when called will bring up the login page on the front-end for the user to see.
    '''
    return render_template('login_page.html')


@app.route('/login', methods=['POST'])
def login():
    '''
    Function that takes a user's login attempt and checks the credentials provided with that of those in
    the credentials table of the database.
    '''
    data = request.get_json()
    details = json.loads(data)
    staff_id = details["staff_id"]
    password = details['password']

    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credential WHERE staff_id = ? AND password = ?", (staff_id, password,))
    check = c.fetchall()
    c.close()
    conn.close()
    # If there is a matching pair of staff Id and password then the return value is select + the user's role.
    if len(check) > 0:
        return 'select_' + check[0][2]
    # Otherwise an incorrect pair returns incorrect.
    return 'incorrect'


@app.route('/logout')
def logout():
    '''
    Function that logs a user out of the system and takes them back to the landing page.
    '''
    return render_template('landing_page.html')


@app.route('/select_lecturer')
def select_lecturer():
    '''
    Function that when called will bring up the lecturer home page on the front-end for the user to see.
    '''
    return render_template('lecturer_home_page.html')


@app.route('/select_dem')
def select_dem():
    '''
    Function that when called will bring up the demonstrator home page on the front-end for the user to see.
    '''
    return render_template('demonstrator_home_page.html')


@app.route('/select_dep')
def select_dep():
    '''
    Function that when called will bring up the department head home page on the front-end for the user to see.
    '''
    return render_template('dep_head_home_page.html')


@app.route('/go_to_add_dep')
def go_to_add_dep():
    '''
    Function that when called will bring up the add department page on the front-end for the user to see.
    '''
    return render_template('add_dep.html')


@app.route('/add_dep', methods=['POST'])
def add_dep():
    '''
    A function that is used to store a department inputted by the user into the database.
    '''
    data = request.get_json()
    dep = json.loads(data)
    name = dep["name"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    # The if satement checks if a department already exists before inserting to avoid duplicates.
    if does_dep_exist(name):
        return 'Department already exists.'

    # If a department is not already in the database then it can be inserted.
    c.execute("INSERT INTO department VALUES (?)", (name,))
    conn.commit()
    c.close()
    conn.close()
    return 'Department successfully added!'


def does_dep_exist(dep):
    '''
    Function used to make the check on the department table. Returns true if it does already exist
    and false if it is new.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM department WHERE name = ?", (dep,))
    check = c.fetchall()
    if len(check) > 0:
        return True
    return False


@app.route('/view_dep')
def view_dep():
    '''
    Function that collects all of the stored departments from the database and returns a list of departments
    for the front-end to process and display for the user.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM department")
    list_of_deps = c.fetchall()
    deps = []
    for dep in list_of_deps:
        deps.append(dep)
    return render_template('view_dep.html', deps=deps)


@app.route('/manage_dep')
def manage_dep():
    '''
    Function used to retrieve the departments stored in the database and return them to
    the front-end along with rendering the manage dep page. So the front-end can take
    the values and display the department info and manage departments functionality to the user.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM department")
    list_of_deps = c.fetchall()
    deps = []
    for dep in list_of_deps:
        deps.append(dep[0])
    return render_template('manage_dep.html', deps=deps)


@app.route('/delete_dep', methods=['POST'])
def delete_dep():
    '''
    Function that takes the user selected department and deletes said department and the classes in the
    department from the database.
    '''
    data = request.get_json()
    dep = json.loads(data)
    name = dep["name"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("DELETE FROM department WHERE name = (?)", (name,))
    c.execute("DELETE FROM class WHERE department = (?)", (name,))
    conn.commit()
    c.close()
    conn.close()
    return 'Department successfully removed!'


@app.route('/edit_dep', methods = ['POST'])
def edit_dep():
    '''
    Function that replaces the current department details with the new ones that
    the user has chosen. It replaces the department name in department, class and
    demonstrator tables.
    '''
    data = request.get_json()
    dep = json.loads(data)
    old_name = dep["old_name"]
    new_name = dep["new_name"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("UPDATE department SET name = ? WHERE name = (?)", (new_name, old_name,))
    c.execute("UPDATE class SET department = ? WHERE department = (?)", (new_name, old_name,))
    c.execute("UPDATE demonstrator SET department = ? WHERE department = (?)", (new_name, old_name,))
    conn.commit()
    c.close()
    conn.close()
    return 'Department successfully updated!'


@app.route('/go_to_add_class')
def go_to_add_class():
    '''
    Function that retrieves the stored department and demonstrator details and returns a list of departments
    for the front-end to process and display for the user appropriately in the add class page. The department
    and demonstrator details are used as options for selection during the add class process.
    '''
    deps_and_dems = {}
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM department")
    list_of_deps = c.fetchall()
    deps = []
    for dep in list_of_deps:
        deps.append(dep[0])
    deps_and_dems['deps'] = deps

    c.execute("SELECT number, name FROM demonstrator")
    list_of_dems = c.fetchall()
    dems = {}
    for dem in list_of_dems:
        dems[dem[0]] = dem[1]
    deps_and_dems['dems'] = dems
    return render_template('add_class.html', deps_and_dems=deps_and_dems)


@app.route('/add_class', methods=['POST'])
def add_class():
    '''
    Function that inserts a class into the database. Only inserting the class once it
    has been confirmed to not already be in the database, as to avoid duplicates.
    '''
    data = request.get_json()
    clas = json.loads(data)

    name = clas["name"]
    code = clas["code"]
    dep = clas["dep"]
    day = clas["day"]
    time = clas["time"]
    nod = clas["nod"]
    skills = make_string(clas["skills"])
    pref_dem = clas["pref_dem"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    # Checks if class already exists in the class table fo the database.
    if does_class_exist(code):
       return 'Class with the same class code already exists.'

    # If it is not a repeat the class is inserted.
    c.execute("INSERT INTO class VALUES (?,?,?,?,?,?,?,?)", (code, name, day, time, dep, nod, skills, pref_dem,))
    conn.commit()
    c.close()
    conn.close()
    return 'Class successfully added!'


def make_string(list):
    '''
    Function that converts a list into a string of comma separated values.
    '''
    s=""
    for value in list:
        s += value + ','
    s = s[:-1]
    return s


def does_class_exist(cc):
    '''
    Function that accepts the class code and searches for it in the class table of the
    database. Returning true if it already exists and false if it does not.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class WHERE code = ?", (cc,))
    check = c.fetchall()
    if len(check) > 0:
        return True
    return False


@app.route('/view_class')
def view_class():
    '''
    Function that retrieves the class data held in the class table of the database and
    packs it into a list of dicts so the front-end can easily read and then display the
    information of each class. The view class page is also produced by the front-end
    for the user.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class")
    list_of_classes = c.fetchall()
    list_of_dicts = []
    for clas in list_of_classes:
        dict = {'code':clas[0], 'name':clas[1],'day':clas[2],'time':clas[3],'dep':clas[4],'nod':clas[5],'skills':clas[6],'pref_dem':clas[7]}
        list_of_dicts.append(dict)
    return render_template('view_class.html', clas=list_of_dicts)


@app.route('/manage_class')
def manage_class():
    '''
    Function that retrieves the class and demonstrator data held in the class table of
    the database and packs it into a dict that holds a list of dicts so the front-end
    can easily read and then display the information of each class and demonstrator.
    The manage class page is also produced by the front-end for the user.
    '''
    classes_and_dems = {}
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM class")
    list_of_classes = c.fetchall()
    list_of_dicts = []
    for clas in list_of_classes:
        dict = {'code':clas[0], 'name':clas[1],'day':clas[2],'time':clas[3],'dep':clas[4],'nod':clas[5],'skills':clas[6],'pref_dem':clas[7]}
        list_of_dicts.append(dict)
    classes_and_dems['classes'] = list_of_dicts

    c.execute("SELECT number, name FROM demonstrator")
    list_of_dems = c.fetchall()
    dems = {}
    for dem in list_of_dems:
        dems[dem[0]] = dem[1]
    classes_and_dems['dems'] = dems
    return render_template('manage_class.html', classes_and_dems=classes_and_dems)


@app.route('/edit_class', methods=['POST'])
def edit_class():
    '''
    Function that carries out the editing of a classes details. The class being altered,
    the value to change and the new value are all sent by the front-end and then the
    necessary change is made to the saved data in the database, returning a successful
    response message upon completion.
    '''
    data = request.get_json()
    input = json.loads(data)
    class_to_edit = input["code"]
    new_value = input["new_value"]
    value_to_change = input["value"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    if value_to_change == 'name':
        c.execute("UPDATE class SET name = ? WHERE code = ?", (new_value, class_to_edit,))
    if value_to_change == 'pref_dem':
        c.execute("UPDATE class SET pref_dem = ? WHERE code = ?", (new_value, class_to_edit,))
    if value_to_change == 'day':
        c.execute("UPDATE class SET day = ? WHERE code = ?", (new_value, class_to_edit,))
    if value_to_change == 'time':
        c.execute("UPDATE class SET time = ? WHERE code = ?", (new_value, class_to_edit,))
    if value_to_change == 'dems':
        c.execute("UPDATE class SET dems = ? WHERE code = ?", (new_value, class_to_edit,))
    if value_to_change == 'skills':
        new_value = make_string(new_value)
        c.execute("UPDATE class SET skills = ? WHERE code = ?", (new_value, class_to_edit,))
    conn.commit()
    c.close()
    conn.close()
    return 'Edit successful'


@app.route('/delete_class', methods=['POST'])
def delete_class():
    '''
    Function that carries out the deletion of a class from the database. The class being
    deleted is sent by the front-end and then the deletion is made to the saved data in
    the database, returning a successful response message upon completion.
    '''
    data = request.get_json()
    clas = json.loads(data)
    code = clas["code"]
    day = clas["day"]
    time = clas["time"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("DELETE FROM class WHERE code = (?) AND day = (?) AND time =(?)", (code, day, time,))
    c.execute("UPDATE demonstrator SET pref_class = 'NA' WHERE pref_class = ?", (code,))
    conn.commit()
    c.close()
    conn.close()
    return 'Class successfully removed!'


@app.route('/go_to_add_dem')
def go_to_add_dem():
    '''
    Function that retrieves the stored department and class details and returns a dict of list of dicts
    for the front-end to process and display for the user appropriately in the add demonstrator page.
    The department and class details are used as options for selection during the add dem process.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()

    c.execute("SELECT * FROM department")
    list_of_deps = c.fetchall()
    deps = []
    for dep in list_of_deps:
        deps.append(dep[0])

    c.execute("SELECT code, name FROM class")
    list_of_classes = c.fetchall()
    deps_and_classes = {'deps':deps, 'clas':list_of_classes}

    return render_template('add_dem.html', deps_and_classes = deps_and_classes)


@app.route('/add_dem', methods=['POST'])
def add_dem():
    '''
    Function that inserts ro updates a demonstrator's details into the database. Updating if
    the demonstrator already exits and inserting if the demonstrator is new. Returning a
    success message when completed.
    '''
    data = request.get_json()
    dem = json.loads(data)
    name = dem["name"]
    staff_id = dem["staff_id"]
    dep = dem["dep"]
    pref_class = dem["pClass"]
    skills = make_string(dem["skills"])
    exp = make_exp_csv(dem["exp"])
    avail = make_string(dem["avail"])

    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    if does_dem_exist(staff_id):
        c.execute("UPDATE demonstrator SET name = ?, department = ?, pref_class = ?, availability = ?, skills = ?, exp = ? WHERE number = ?", (name, dep, pref_class, avail, skills, exp, staff_id,))
        conn.commit()
        c.close()
        conn.close()
        return 'Demonstrator details updated.'
    
    c.execute("INSERT INTO demonstrator VALUES (?,?,?,?,?,?,?)", (staff_id, name, dep, pref_class, avail, skills, exp,))
    conn.commit()
    c.close()
    conn.close()

    return 'Demonstrator successfully added!'


def make_exp_csv(exp):
    '''
    Function that accepts the values for experience and formats it as comma, full stop separated
    values so it can be stored as a string in the database.
    '''
    csv = ""
    for e in exp:
        csv += e['topic'] + "," + e['env'] + "," + e['exp_len'] + "," + e['exp_my'] + "."
    csv = csv[:-1]
    return csv


def does_dem_exist(cc):
    '''
    Function that checks the demonstrator table in the database for the staff id provided and
    returns true if that number already exists and false if it is new.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM demonstrator WHERE number = ?", (cc,))
    check = c.fetchall()
    if len(check) > 0:
        return True
    return False


@app.route('/view_dem')
def view_dem():
    '''
    Function that retrieves the demonstrator data held in the demonstrator table of the
    database and packs it into a list of dicts so the front-end can easily read and then
    display the information. The view demonstrator page is also produced by the front-end
    for the user.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM demonstrator")
    list_of_dems = c.fetchall()
    list_of_dicts = []
    for dem in list_of_dems:
        dict = {'staff_id':dem[0], 'name':dem[1],'dep':dem[2],'pref_class':dem[3],'avail':dem[4],'skills':dem[5],'exp':dem[6]}
        list_of_dicts.append(dict)
    return render_template('view_dem.html', dems=list_of_dicts)


@app.route('/manage_dem')
def manage_dem():
    '''
    Function that retrieves the demonstrator data held in the demonstrator table of
    the database and packs it into a list of dicts so the front-end can easily read
    and then display the information of each demonstrator. The manage demonstrator
    page is also produced by the front-end for the user.
    '''
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("SELECT * FROM demonstrator")
    list_of_dems = c.fetchall()
    list_of_dicts = []
    for dem in list_of_dems:
        dict = {'staff_id':dem[0], 'name':dem[1],'dep':dem[2],'pref_class':dem[3],'avail':dem[4],'skills':dem[5],'exp':dem[6]}
        list_of_dicts.append(dict)
    return render_template('manage_dem.html', dems=list_of_dicts)


@app.route('/delete_demonstrator', methods=['POST'])
def delete_dem():
    '''
    Function that carries out the deletion of a demonstrator from the database. The
    demonstrator being deleted is sent by the front-end and then the deletion is
    made to the saved data in the database, returning a successful response message
    upon completion.
    '''
    data = request.get_json()
    dem = json.loads(data)
    staff_id = dem["staff_id"]
    conn = sqlite3.connect('Timetable.db')
    c = conn.cursor()
    c.execute("DELETE FROM demonstrator WHERE number = (?)", (staff_id,))
    c.execute("DELETE FROM credential WHERE staff_id = (?)", (staff_id,))
    conn.commit()
    c.close()
    conn.close()
    return 'Demonstrator successfully removed!'


if __name__== '__main__':
    app.run(debug=True)
