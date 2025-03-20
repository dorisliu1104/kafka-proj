CREATE TABLE department_employee(
    department VARCHAR(100),
    department_division   VARCHAR(100),
    position_title VARCHAR(100),
    hire_date DATE,
    salary decimal
);

CREATE TABLE public.department_employee_salary (
    department varchar(100) NOT NULL,
    total_salary int4 NULL,
    CONSTRAINT department_employee_salary_pk PRIMARY KEY (department)
);
