DROP TABLE IF EXISTS MenuItem;
DROP TABLE IF EXISTS MilkKind;
DROP TABLE IF EXISTS CoffeeType;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Staff;

CREATE TABLE Staff
(
	StaffID		VARCHAR(10)		PRIMARY KEY,
	Password	VARCHAR(30)		NOT NULL,
	FirstName	VARCHAR(30)		NOT NULL,
	LastName	VARCHAR(30)		NOT NULL,
	Age			INTEGER			NOT NULL CHECK (Age > 21),
	Salary		DECIMAL(9,2)	NOT NULL CHECK (Salary > 0)
);

CREATE TABLE Category
(
	CategoryID		SERIAL	PRIMARY KEY,
	CategoryName	VARCHAR(10) UNIQUE NOT NULL,
	CategoryDesc	VARCHAR(40)	NOT NULL
);

CREATE TABLE CoffeeType
(
	CoffeeTypeID	SERIAL	PRIMARY KEY,
	CoffeeTypeName	VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE MilkKind
(
	MilkKindID		SERIAL	PRIMARY KEY,
	MilkKindName	VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE MenuItem
(
	MenuItemID		SERIAL			PRIMARY KEY,
	Name			VARCHAR(30)		NOT NULL,
	Description		VARCHAR(150),
	CategoryOne		INTEGER			NOT NULL REFERENCES Category,
	CategoryTwo		INTEGER			REFERENCES Category,
	CategoryThree	INTEGER			REFERENCES Category,
	CoffeeType		INTEGER			REFERENCES CoffeeType,
	MilkKind		INTEGER			REFERENCES MilkKind,
	Price			DECIMAL(6,2)	NOT NULL,
	ReviewDate		DATE,
	Reviewer		VARCHAR(10) 	REFERENCES Staff
);

INSERT INTO Staff VALUES ('ajones','098','Anna','Jones',25,41000);
INSERT INTO Staff VALUES ('ganderson','987','Glen','Anderson',30,49500.80);
INSERT INTO Staff VALUES ('jwalker','876','James','Walker',22,38890.50);
INSERT INTO Staff VALUES ('janedoe','765','Jane','Doe',26,43900.20);
INSERT INTO Staff VALUES ('johndoe','654','John','Doe',22,38000);
INSERT INTO Staff VALUES ('njohnson','543','Neil','Johnson',27,4500);
INSERT INTO Staff VALUES ('nbrown','432','Nicole','Brown',41,68100.90);
INSERT INTO Staff VALUES ('rtatum','321','Robert','Tatum',39,62400);
INSERT INTO Staff VALUES ('rmarrick','210','Ryu','Marrick',36,59900.20);
INSERT INTO Staff VALUES ('tcolemen','109','Tom','Coleman',24,48000);

INSERT INTO Category VALUES (1,'Breakfast','Menu item to be offered for breakfast');
INSERT INTO Category VALUES (2,'Lunch','Menu item to be offered for lunch');
INSERT INTO Category VALUES (3,'Dinner','Menu item to be offered for dinner');

INSERT INTO CoffeeType VALUES (1,'Espresso');
INSERT INTO CoffeeType VALUES (2,'Latte');
INSERT INTO CoffeeType VALUES (3,'Cappuccino');
INSERT INTO CoffeeType VALUES (4,'LongBlack');
INSERT INTO CoffeeType VALUES (5,'ColdBrew');

INSERT INTO MilkKind VALUES (1,'Whole');
INSERT INTO MilkKind VALUES (2,'Skim');
INSERT INTO MilkKind VALUES (3,'Soy');
INSERT INTO MilkKind VALUES (4,'Almond');
INSERT INTO MilkKind VALUES (5,'Oat');

INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('French Toast','A sliced bread soaked in beaten eggs, milk, and cream, then pan-fried with butter',1,NULL,NULL,NULL,NULL,9.90,'10/01/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Eggs Benedict','An English muffin, toasted, and topped with bacon, poached eggs, and classic French hollandaise sauce',1,2,NULL,NULL,NULL,12.80,'18/02/2024','janedoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Poke Bowl','Cubes of marinated fish tossed over rice and topped with vegetables and Asian-inspired sauces',1,2,3,NULL,NULL,15.90,'28/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Orange Juice','A fresh, sweet, and juicy drink with orange bits made from freshly squeezed oranges',1,2,3,NULL,NULL,6.50,'01/03/2024','janedoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('White Coffee','A full-flavored concentrated form of coffee served in small, strong shots with whole milk',1,2,NULL,1,1,3.50,'22/03/2024','rtatum');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Black Coffee',NULL,1,2,3,4,NULL,4.30,NULL,NULL);
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Coffee Drink',NULL,1,2,NULL,3,3,3.50,'28/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Seafood Cleopatra','Salmon topped with prawns in a creamy seafood sauce. Served with salad and chips',3,NULL,NULL,NULL,NULL,25.90,'20/02/2024','johndoe');
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Iced Coffee','A glass of cold espresso, milk, ice cubes, and a scoop of ice cream',1,2,NULL,2,1,7.60,NULL,NULL);
INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price,ReviewDate,Reviewer) VALUES 
	('Coffee Pancake','A short stack of pancakes flecked with espresso powder and mini chocolate chips',1,NULL,NULL,NULL,NULL,8.95,'08/04/2014','janedoe');

COMMIT;


CREATE OR REPLACE FUNCTION check_staff_login(
    p_staffID VARCHAR, 
    p_password VARCHAR
)
RETURNS TABLE (
    staff_id VARCHAR,
    staff_password VARCHAR,
    staff_firstname VARCHAR,
    staff_lastname VARCHAR,
    staff_age INT,
    staff_salary DECIMAL(9,2)
)
AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        staffid,
        password AS staff_password,
        firstname,
        lastname,
        age,
        salary
    FROM 
        Staff 
    WHERE 
        StaffID = p_staffID AND Password = p_password;
END;
$$ LANGUAGE plpgsql;






CREATE OR REPLACE FUNCTION viewingmenuitemlist(sid varchar(10)) RETURNS
TABLE (
id INTEGER,
name VARCHAR(30),
description VARCHAR(150),
category VARCHAR(10),
option VARCHAR(10),
price DECIMAL(6,2),
reviewdate VARCHAR(10),
reviewer VARCHAR(8))
AS $$
BEGIN

RETURN QUERY
SELECT 
m.menuitemid as id, 
m.name, 
COALESCE(m.description, '') AS description, 
CASE 
WHEN cat2.categoryname is NULL THEN cat1.categoryname
WHEN cat3.categoryname is NULL THEN cat1.categoryname || '|' || cat2.categoryname
WHEN cat3.categoryname is not NULL THEN cat1.categoryname || '|' || cat2.categoryname || '|' || cat3.categoryname
END AS category, 
CASE 
	WHEN (c.coffeetypename is NULL) and (mk.milkkindname is NULL) THEN ''
	WHEN (c.coffeetypename is not NULL) and (mk.milkkindname is NULL) THEN c.coffeetypename
	WHEN (c.coffeetypename is not NULL) and (mk.milkkindname is not NULL) THEN c.coffeetypename || ' - ' || mk.milkkindname
END AS option,
m.price, 
CAST(TO_CHAR(m.reviewdate, 'dd-mm-yyyy') as VARCHAR(10)) as reviewdate,
CAST(s.firstname || ' ' || s.lastname AS VARCHAR(30))
as reviewer
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE m.reviewer = sid
ORDER BY reviewdate, description, price DESC;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION findingmenuitems(searchstring VARCHAR(30)) RETURNS
TABLE (
id INTEGER,
name VARCHAR(30),
description VARCHAR(150),
category VARCHAR(10),
option VARCHAR(10),
price DECIMAL(6,2),
reviewdate VARCHAR(10),
reviewer VARCHAR(8))
AS $$
BEGIN

RETURN QUERY
SELECT 
m.menuitemid as id, 
m.name, 
COALESCE(m.description, '') AS description, 
CASE 
WHEN cat2.categoryname is NULL THEN cat1.categoryname
WHEN cat3.categoryname is NULL THEN cat1.categoryname || '|' || cat2.categoryname
WHEN cat3.categoryname is not NULL THEN cat1.categoryname || '|' || cat2.categoryname || '|' || cat3.categoryname
END AS category, 
CASE 
	WHEN (c.coffeetypename is NULL) and (mk.milkkindname is NULL) THEN ''
	WHEN (c.coffeetypename is not NULL) and (mk.milkkindname is NULL) THEN c.coffeetypename
	WHEN (c.coffeetypename is not NULL) and (mk.milkkindname is not NULL) THEN c.coffeetypename || ' - ' || mk.milkkindname
END AS option,
m.price, 
COALESCE(CAST(TO_CHAR(m.reviewdate, 'dd-mm-yyyy') as VARCHAR(10)), '') as reviewdate,
COALESCE((CAST(s.firstname || ' ' || s.lastname AS VARCHAR(30))), '') as reviewer
FROM menuitem m LEFT OUTER JOIN category cat1 ON (m.categoryone = cat1.categoryid) 
				LEFT OUTER JOIN category cat2 ON (m.categorytwo = cat2.categoryid)
				LEFT OUTER JOIN category cat3 ON (m.categorythree = cat3.categoryid)
				LEFT OUTER JOIN coffeetype c ON (m.coffeetype = c.coffeetypeid)
				LEFT OUTER JOIN milkkind mk ON (m.milkkind = mk.milkkindid)
				LEFT OUTER JOIN staff s ON (m.reviewer = s.staffid)
WHERE (m.name ILIKE '%' || searchstring || '%' OR 
	   m.description ILIKE '%' || searchstring || '%' OR 
	   cat1.categoryname ILIKE '%' || searchstring || '%' OR 
	   cat2.categoryname ILIKE '%' || searchstring || '%' OR 
	   cat3.categoryname ILIKE '%' || searchstring || '%' OR 
	   c.coffeetypename ILIKE '%' || searchstring || '%' OR 
	   mk.milkkindname ILIKE '%' || searchstring || '%' or 
	   s.firstname ILIKE '%' || searchstring || '%' or 
	   s.lastname ILIKE '%' || searchstring || '%') And 
	   				(m.reviewdate >= (CURRENT_DATE - INTERVAL '10 years') or m.reviewdate is null)
ORDER BY s.firstname desc, m.reviewdate desc;

END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE addmenuitem(
    a_name VARCHAR(30),
    a_description VARCHAR(150),
    a_categoryOne VARCHAR(10),
    a_categoryTwo VARCHAR(10),
    a_categoryThree VARCHAR(10),
    a_coffeetype VARCHAR(10),
    a_milkkind VARCHAR(10),
    a_price DECIMAL(6,2)
) 
LANGUAGE plpgsql
AS
$$

DECLARE 
coffee_id INT; 
milkkind_id INT;

BEGIN
	SELECT coffeetypeid INTO coffee_id FROM coffeetype WHERE coffeetypename = INITCAP(TRIM(a_coffeetype));
	SELECT milkkindid INTO milkkind_id FROM milkkind WHERE milkkindname = INITCAP(TRIM(a_milkkind));
    IF coffee_id IS NOT NULL AND milkkind_id IS NULL THEN
        RAISE EXCEPTION 'You must select milk type along with coffee type';
    END IF;
    IF a_price <= 0 THEN
        RAISE EXCEPTION 'Price cannot be zero';
    END IF;
	IF INITCAP(TRIM(u_categorytwo)) = INITCAP(TRIM(u_categoryone)) THEN
		RAISE EXCEPTION 'Please write a different category';
	END IF;
	IF INITCAP(TRIM(u_categorythree)) = INITCAP(TRIM(u_categorytwo)) THEN
		RAISE EXCEPTION 'Please write a different category';
	END IF;
	IF INITCAP(TRIM(u_categorythree)) = INITCAP(TRIM(u_categoryone)) THEN
		RAISE EXCEPTION 'Please write a different category';
	END IF;
    INSERT INTO menuitem (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price)
    VALUES (
        INITCAP(TRIM(a_name)), 
        INITCAP(TRIM(a_description)), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryOne))), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryTwo))), 
        (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(a_categoryThree))), 
        (SELECT coffeetypeid FROM coffeetype WHERE coffeetypename = INITCAP(TRIM(a_coffeetype))), 
        (SELECT milkkindid FROM milkkind WHERE milkkindname = INITCAP(TRIM(a_milkkind))), 
        a_price
    );
END;
$$; 



CREATE OR REPLACE PROCEDURE updatemenuitem(
	u_menuitemid INT,
	u_name VARCHAR(30),
	u_description VARCHAR(150),
	u_categoryone VARCHAR(10),
	u_categorytwo VARCHAR(10),
	u_categorythree VARCHAR(10),
	u_coffeetype VARCHAR(10),
	u_milkkind VARCHAR(10),
	u_price DECIMAL(6,2),
	u_reviewdate DATE,
	u_reviewer VARCHAR(30))
LANGUAGE plpgsql
AS $$

DECLARE 
coffee_id INT; 
milkkind_id INT;

BEGIN
	SELECT coffeetypeid INTO coffee_id FROM coffeetype WHERE coffeetypename = INITCAP(TRIM(u_coffeetype));
	SELECT milkkindid INTO milkkind_id FROM milkkind WHERE milkkindname = INITCAP(TRIM(u_milkkind));
    IF coffee_id IS NOT NULL AND milkkind_id IS NULL THEN
        RAISE EXCEPTION 'You must select milk type along with coffee type';
    END IF;
    IF u_price <= 0 THEN
        RAISE EXCEPTION 'Price cannot be zero ot negative';
    END IF;
	IF INITCAP(TRIM(u_categorytwo)) = INITCAP(TRIM(u_categoryone)) THEN
		RAISE EXCEPTION 'Please write a different category, cat2 = cat1';
	END IF;
	IF (u_categorythree != '' AND u_categorytwo != '') AND 
	   (INITCAP(TRIM(u_categorythree)) = INITCAP(TRIM(u_categorytwo))) THEN
		RAISE EXCEPTION 'Please write a different category, cat3 = cat2';
	END IF;
	IF  INITCAP(TRIM(u_categorythree)) = INITCAP(TRIM(u_categoryone)) THEN
		RAISE EXCEPTION 'Please write a different category, cat3 = cat1';
	END IF;

	UPDATE menuitem
	SET 
		name = INITCAP(TRIM(u_name)),
		description = TRIM(u_description), 
		categoryone = (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(u_categoryOne))),
		categorytwo = (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(u_categoryTwo))),
		categorythree = (SELECT categoryid FROM category WHERE categoryname = INITCAP(TRIM(u_categoryThree))),
		coffeetype = (SELECT coffeetypeid FROM coffeetype WHERE coffeetypename = INITCAP(TRIM(u_coffeetype))),
		milkkind = (SELECT milkkindid FROM milkkind WHERE milkkindname = INITCAP(TRIM(u_milkkind))),
		price = u_price, 
		reviewdate = NULLIF(u_reviewdate, ''),
		reviewer = NULLIF(u_reviewer, '')
	WHERE menuitemid = u_menuitemid;
END;
$$;


