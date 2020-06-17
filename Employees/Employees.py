import csv
from datetime import datetime
import numpy as np
from collections import namedtuple
import itertools
import operator
from tkinter import filedialog
from tkinter import *

Range = namedtuple('Range', ['start', 'end'])

class Employees:
    def __init__(self,file):
        self.file = file

    def _date_convertion(self,dates):
        """
        Function used to convert strings into datetime objects based on matching format
        """
        date_string = "%Y-%m-%d"
        return [datetime.strptime(x, date_string).date() if x != 'NULL' else datetime.now().date() for x in dates]

    def _trnsp(self,a_list):
        """
        takes list of lists as in input and returns transposed version of the list
        Dates provided in string format are converted to datetime object
        """
        numpy_array = np.array(a_list)
        transpose = numpy_array.T
        transpose_list = transpose.tolist()
        transpose_list[2] = self._date_convertion(transpose_list[2])
        transpose_list[3] = self._date_convertion(transpose_list[3])
        return transpose_list


    def _days_worked(self, employees):
        """
        Input: Takes as input the dictionnary from pairs function and calculates the overlap of days worked on a project. Will return 0 when there is no overlap.
        Output: Provides a dictionnairy with all of the pairs of employees who worked togather as a key and the days spent working togather as a value
        """
        worked_days = {}
        emp_index = {}

        for x in [x[0] for x in zip(*np.unique(employees[1], return_counts=True)) if x[1] > 1]:
            emp_index[x] = []
        for proj in emp_index.keys():
            for index,x in enumerate(employees[1]):
                if x == proj:
                    emp_index[proj].append(index)

        
        for projects in emp_index.keys():
            for x in itertools.combinations(emp_index[projects], 2):
                emp_1_id = employees[0][x[0]]
                emp_2_id = employees[0][x[1]]
                r1 = Range(start=employees[2][x[0]], end=employees[3][x[0]] )
                r2 = Range(start=employees[2][x[1]], end=employees[3][x[1]] )

                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days + 1
                worked_days[f'{emp_1_id}/{emp_2_id}-{x}-{projects}'] = max(0, delta)
        return worked_days

    def output(self):
        with open(self.file, newline="") as f:
            reader = csv.reader(f)
            reader.__next__()#remove the headers
            transpose_list = self._trnsp(list(reader))
        worked_days = self._days_worked(transpose_list)
        a = max(worked_days.items(), key=operator.itemgetter(1))
        return [a[0].split('-')[0].split('/')[0],a[0].split('-')[0].split('/')[1],a[0].split('-')[2], a[1]]
        #return f"Employee ID#1 {a[0].split('-')[0].split('/')[0]}, Employee ID#2 {a[0].split('-')[0].split('/')[1]}, Project ID {a[0].split('-')[2]}, Days Worked togather {a[1]}"
