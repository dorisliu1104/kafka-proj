import json

class Employee:
    def __init__(self, 
                 emp_dept: str = '', 
                 emp_dept_div: str = '', 
                 emp_pcn: str = '', 
                 emp_pos_title: str = '', 
                 emp_flsa_status: str = '', 
                 emp_hire_date: str = '', 
                 emp_date_in_title: str = '', 
                 emp_salary: int = 0):
        self.emp_dept = emp_dept
        self.emp_dept_div = emp_dept_div
        self.emp_pcn = emp_pcn
        self.emp_pos_title = emp_pos_title
        self.emp_flsa_status = emp_flsa_status
        self.emp_hire_date = emp_hire_date
        self.emp_date_in_title = emp_date_in_title
        self.emp_salary = emp_salary
        
    @staticmethod
    def from_csv_line(line):
        return Employee(
            emp_dept=line[0], 
            emp_dept_div=line[1], 
            emp_pcn=line[2], 
            emp_pos_title=line[3], 
            emp_flsa_status=line[4], 
            emp_hire_date=line[5], 
            emp_date_in_title=line[6], 
            emp_salary=int(float(line[7]))
        )

    def to_json(self):
        return json.dumps(self.__dict__)
