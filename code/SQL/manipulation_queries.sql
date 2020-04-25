/*Gordon Petry, Michael Williams, Jason Kantner and Casey Lishko
 * Database Systems
 * 4/11/20
 * create_views.sql 
 */

/*The below query is used to delete information from specified tables.

DELETE
FROM table_name
WHERE attribute = ...; */

DELETE
FROM Counties
WHERE CTYcode = '2';


/*The below query is used to update information from specified tables.
UPDATE table_name
SET attribute = ...
WHERE original_attribute =
*/

UPDATE Categories
SET Cname = 'Community Animals'
WHERE Ccode = '1';


/*The following is used to compare categories within a municipality*/

/*USED FOR X AXIS*/
SELECT Cname
FROM CATEGORIES
WHERE Cname = 'Energy' AND Cname = 'Food';

/*Gets sum of points for a specific category in a specific municipality*/
SELECT SUM(Point_Value)
FROM MUNICIPALITIES JOIN COMPLETE_ACTIONS
ON MUNICIPALITIES.Mcode = COMPLETE_ACTIONS.Mcode
JOIN ACTIONS
ON COMPLETE_ACTIONS.Acode = ACTIONS.Acode
JOIN CATEGORIES
ON ACTIONS.Ccode = CATEGORIES.Ccode
WHERE Mname = 'Atlantic City' AND Cname = 'Food';

/*Gets count of priority actions for a specific category in a specific municipality*/
SELECT COUNT(Priority)
FROM MUNICIPALITIES JOIN COMPLETE_ACTIONS
ON MUNICIPALITIES.Mcode = COMPLETE_ACTIONS.Mcode
JOIN ACTIONS
ON COMPLETE_ACTIONS.Acode = ACTIONS.Acode
JOIN CATEGORIES
ON ACTIONS.Ccode = CATEGORIES.Ccode
WHERE Mname = 'Atlantic City' AND Cname = 'Food';

/*Gets count of required actions for a specific category in a specific municipality*/
SELECT COUNT(Required)
FROM MUNICIPALITIES JOIN COMPLETE_ACTIONS
ON MUNICIPALITIES.Mcode = COMPLETE_ACTIONS.Mcode
JOIN ACTIONS
ON COMPLETE_ACTIONS.Acode = ACTIONS.Acode
JOIN CATEGORIES
ON ACTIONS.Ccode = CATEGORIES.Ccode
WHERE Mname = 'Atlantic City' AND Cname = 'Food';

/*The following is used for comparing multiple municipalities*/

/*USED FOR X AXIS*/
SELECT Mname
FROM MUNICIPALITIES
WHERE Mname = 'Camden City' AND Mname = 'Sea Isle City';

/*Selects total number of actions from a municipality*/
SELECT COUNT(CA.Acode)
FROM MUNICIPALITIES AS M JOIN COMPLETE_ACTIONS AS CA
ON M.Mcode = CA.Mcode
WHERE M.Mname = 'Camden City';

/*Selects total points from a municipality
SELECT Total_Points
FROM MUNICIPALITIES JOIN CERTIFIED
ON MUNICIPALITES.Mcode = CERTIFIED.Mcode
WHERE Mname = '...';*/

/*Selects number of bronze/silver from a specific municipality*/
SELECT Bronze_Silver
FROM MUNICIPALITIES JOIN CERTIFICATION
ON MUNICIPALITIES.Mcode = CERTIFICATION.Mcode
WHERE Mname = 'Camden City';

/*Selects certification date from a municipality*/
SELECT Certification_Date
FROM MUNICIPALITIES JOIN CERTIFICATION
ON MUNICIPALITIES.Mcode = CERTIFICATION.Mcode
WHERE Mname = 'Camden City';


/*The following is used to compare counties*/

/*USED FOR X AXIS*/
SELECT CTYname
FROM COUNTIES
WHERE CTYname = 'Burlington' AND CTYname = 'Union';

/*Selects # of certified municipalities per county*/
SELECT COUNT(C.Mcode)
FROM COUNTIES AS CY JOIN MUNICIPALITIES AS M
ON CY.CTYcode = M.CTYcode
JOIN CERTIFICATION AS C
ON M.Mcode = C.Mcode
WHERE CY.CTYname = 'Burlington';

/*Select total points from a specific county*/
SELECT SUM(Total_Points)
FROM COUNTIES JOIN MUNICIPALITIES
ON COUNTIES.CTYcode = MUNICIPALITIES.CTYcode
JOIN CERTIFICATION
ON MUNICIPALITIES.Mcode = CERTIFICATION.Mcode
WHERE CTYname = 'Atlantic';

/*Select number of total actions in a specific county*/
SELECT COUNT(CA.Acode)
FROM COUNTIES AS CY JOIN MUNICIPALITIES AS M
ON CY.CTYcode = M.CTYcode
JOIN COMPLETE_ACTIONS AS CA
ON M.Mcode = CA.Mcode
WHERE CTYname = 'Union';

/*Select # of bronze certified municipalities for a specific county*/
SELECT COUNT(C.Mcode)
FROM COUNTIES AS CY JOIN MUNICIPALITIES AS M
ON CY.CTYcode = M.CTYcode
JOIN CERTIFICATION AS C
ON M.Mcode = C.Mcode
WHERE CY.CTYname = 'Union' AND C.Bronze_Silver = 'Bronze';

/*Select # of silver certified municipalities for a specific county*/
SELECT COUNT(C.Mcode)
FROM COUNTIES AS CY JOIN MUNICIPALITIES AS M
ON CY.CTYcode = M.CTYcode
JOIN CERTIFICATION AS C
ON M.Mcode = C.Mcode
WHERE CY.CTYname = 'Union' AND C.Bronze_Silver = 'Silver';
