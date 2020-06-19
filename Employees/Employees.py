import csv
from datetime import datetime
import numpy as np
from collections import namedtuple
import itertools
import operator
from tkinter import filedialog
from tkinter import *
import dateparser

Range = namedtuple('Range', ['start', 'end'])
 
class Employees:
    def __init__(self,file):
        self.file = file


    def _data_convertor(self,a_list):
        """
        Function that takes the input from a csv file as a list of lists and returns the pair(s) of employees that worked most days togather
        Input: list of lists
        Output: Dictionary with the two employee IDs as key,  all projects they worked togather and total of days worked togather as values
        """

        # Transponse the list and convert strings to datetime objects
        numpy_array = np.array(a_list)
        transpose = numpy_array.T
        transpose_list = transpose.tolist()
        transpose_list[2] = [dateparser.parse(x).date() if x != 'NULL' else datetime.now().date() for x in transpose_list[2]]
        transpose_list[3] = [dateparser.parse(x).date() if x != 'NULL' else datetime.now().date() for x in transpose_list[3]]

  
        emp_id ={}
        # find all employees that worked togather on projects
        for projects in [unqs[0] for unqs in zip(*np.unique(transpose_list[1], return_counts=True)) if unqs[1] > 1]:
            emp_id[projects] = [[],[]]
            for index,x in enumerate(transpose_list[1]):
                if x == projects:
                    emp_id[projects][0].append(transpose_list[0][index])
                    emp_id[projects][1].append([transpose_list[2][index],transpose_list[3][index]])

        emp_tuples = {}
        # Check how many days each unique pair of employees worked togather
        for project in emp_id.keys():
            for keys in [x for x in itertools.combinations(emp_id[project][0], 2)]:
                emp1_id = keys[0]
                emp2_id = keys[1]

                emp1_index = emp_id[project][0].index(emp1_id)
                emp2_index = emp_id[project][0].index(emp2_id)

                emp1_dates = emp_id[project][1][emp1_index]
                emp2_dates = emp_id[project][1][emp2_index]
                days_overlap = self._date_overlap([emp1_dates,emp2_dates])
                if keys not in [tuple(sorted(current_key, reverse=True)) for current_key in emp_tuples.keys()] and keys not in [tuple(sorted(current_key, reverse=False)) for current_key in emp_tuples.keys()]:
                    emp_tuples[keys] = {}
                    emp_tuples[keys][project] = days_overlap
                    emp_tuples[keys]["total"] = days_overlap
                else:
                    emp_tuples[tuple(sorted(keys, reverse=True))][project] = days_overlap
                    emp_tuples[tuple(sorted(keys, reverse=True))]["total"] += days_overlap
        output = {}
        # Return only the pair(s) that have the most days worked togather
        for key,value in emp_tuples.items():
            if max([emp_tuples[emp_key]["total"] for emp_key in emp_tuples.keys()]) > 0:
                if value["total"] == max([emp_tuples[emp_key]["total"] for emp_key in emp_tuples.keys()]):
                    output[key] = value
            else: output = "No employees worked togather"
        return output

    def _date_overlap(self,date_list):
        """
        Function which checks the overlap between two sets of dates.
        Input: 
            List of lists that contains two sets of date time objects in the format : [<start Date>, <end Date>]
        Output: 
            Integer: Overlap between the dates in days. If the dates do not overlap it will return 0
        """
        set1 = Range(start=date_list[0][0], end=date_list[0][1])
        set2 = Range(start=date_list[1][0], end=date_list[1][1])
        latest_start = max(set1.start, set2.start)
        earliest_end = min(set1.end, set2.end)
        delta = (earliest_end - latest_start).days + 1
        return max(0, delta)


    def output(self): 
        """
        
        """
        with open(self.file, newline="") as f:
            reader = csv.reader(f)
            reader.__next__() # remove the headers
            worked_days = self._data_convertor(list(reader))
        return worked_days
