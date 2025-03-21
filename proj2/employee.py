import json

class Employee:
    def __init__(self,  action_id: int, emp_id: int, emp_FN: str, emp_LN: str, emp_dob: str, emp_city: str, action: str):
        self.action_id = action_id
        self.emp_id = emp_id
        self.emp_FN = emp_FN
        self.emp_LN = emp_LN
        self.emp_dob = emp_dob
        self.emp_city = emp_city
        self.action = action
        
    @staticmethod
    def from_line(line):
        return Employee(
            action_id=line[0],
            emp_id=line[1],
            emp_FN=line[2],
            emp_LN=line[3],
            emp_dob=str(line[4]),  # Convert DATE to string for JSON serialization
            emp_city=line[5],
            action=line[6]
        )

    def to_json(self):
        return json.dumps(self.__dict__)
