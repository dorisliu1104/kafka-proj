CREATE TABLE employee (
    employeeID SERIAL PRIMARY KEY,
    firstName varchar(50),
    lastName varchar(50),
    dob date,
    city varchar(50)
);

CREATE TABLE employeeCdc (
    actionId SERIAL PRIMARY KEY,
    employeeID INT,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    dob DATE,
    city VARCHAR(100),
    action VARCHAR(10)
);

CREATE OR REPLACE FUNCTION recordCdc()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO employeeCdc (employeeID, firstName, lastName, dob, city, action)
        VALUES (NEW.employeeID, NEW.firstName, NEW.lastName, NEW.dob, NEW.city, 'INSERT');
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO employeeCdc (employeeID, firstName, lastName, dob, city, action)
        VALUES (NEW.employeeID, NEW.firstName, NEW.lastName, NEW.dob, NEW.city, 'UPDATE');
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO employeeCdc (employeeID, firstName, lastName, dob, city, action)
        VALUES (OLD.employeeID, OLD.firstName, OLD.lastName, OLD.dob, OLD.city, 'DELETE');
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER employeeInsertTrigger
AFTER INSERT OR UPDATE OR DELETE ON employee
FOR EACH ROW EXECUTE FUNCTION recordCdc();