import sys
import csv
import re
import pickle


def main(path):
    if not path:  # Exit program if the path is not specified as a sysarg
        sys.exit("Path Not Specified")

    employees = []  # A list of all employees
    dictionary = {}  # A dictionary of all employees

    with open(path) as dataFile:
        data_reader = csv.reader(dataFile, delimiter=',')
        line = 0
        for row in data_reader:
            if line == 0:
                line += 1
                continue
            employees.append(Person(row[0], row[1], row[2], row[3], row[4]))
            line += 1
    for person in employees:
        person = format_person(person)
        dictionary[person.idNum] = person

    pickle.dump(dictionary, open('employee.p', 'wb'))  # Write the dictionary to a pickle file
    employee_list = pickle.load(open('employee.p', 'rb'))  # Read the pickle file
    for i in employee_list:
        employee_list[i].display()


def format_person(person):
    # This ensures that the employee name is correctly formatted
    person.first = person.first.capitalize()
    if person.mi == '':
        person.mi = 'X'
    elif len(person.mi) > 1:
        person.mi = person.mi[0]
    else:
        person.mi = person.mi.capitalize()
    person.last = person.last.capitalize()

    # This ensures that the ID number is correctly formatted
    while not re.match(r"[A-Za-z][A-Za-z][0-9][0-9][0-9][0-9]", person.idNum):
        print("ID is invalid:", person.idNum)
        print("ID is two letters followed by 4 digits")
        person.idNum = input("Please enter a valid id for %s %s: " % (person.first, person.last))

    # This ensures that the phone number is correctly formatted
    while not re.match(r"(\d{3})-(\d{3})-(\d{4})", person.phone):
        print("Phone number %s is invalid")
        print("Phone number must be in form 123-456-7890")
        person.phone = input("Please enter phone number for %s %s: " % (person.first, person.last))

    return person


class Person:
    def __init__(self, last, first, mi, idNum, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.idNum = idNum
        self.phone = phone

    def display(self):
        print('\nEmployee id:', self.idNum)
        print('        ', self.first, self.mi, self.last)
        print('        ', self.phone)


if __name__ == '__main__':
    main(sys.argv[1])


