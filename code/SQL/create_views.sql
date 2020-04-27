/* Gordon Petry, Michael Williams, Jason Kantner and Casey Lishko
 * Database Systems
 * 4/11/20
 * create_views.sql
 */

/*Shows the total points that could be earned by each category*/
CREATE VIEW pt_tot_category AS
SELECT C.Cname, SUM(A.Point_Value) AS Total_Points
FROM Actions AS A JOIN Categories AS C
ON A.Ccode = C.Ccode
GROUP BY C.CCode
ORDER BY C.Cname;

/*Shows the total actions under each category.*/
CREATE VIEW tot_act_cat AS
SELECT C.Cname, COUNT(A.Acode) as Count_Action
FROM Actions AS A
JOIN Categories AS C
ON C.Ccode = A.Ccode
GROUP BY C.Ccode
ORDER BY C.Cname;

/*Shows the total actions each municipality did*/
CREATE VIEW tot_act_mun AS
SELECT M.Mname, COUNT(CA.Acode) AS Count_Action
FROM Complete_Actions AS CA JOIN Municipalities AS M
ON CA.Mcode = M.Mcode
GROUP BY M.Mcode
ORDER BY M.Mname;

/*Shows the total points each municipality received*/
CREATE VIEW tot_pts_mun AS
SELECT M.Mname, C.Total_Points
FROM Certification AS C JOIN Municipalities AS M
ON C.Mcode = M.Mcode
ORDER BY M.Mname;

/*Shows the total number of categories each municipality fulfilled*/
CREATE VIEW tot_cat_mun AS
SELECT M.Mname, COUNT(DISTINCT A.Ccode) AS Count_Category
FROM Complete_Actions AS CA JOIN Actions A
ON CA.Acode = A.Acode
JOIN Municipalities AS M
ON CA.Mcode = M.Mcode
GROUP BY M.Mcode
ORDER BY M.Mname;

/*Shows the total number of actions each county did*/
CREATE VIEW tot_act_cty AS
SELECT C.CTYname, COUNT(CA.Acode) AS Count_Action
FROM Municipalities AS M JOIN Complete_Actions AS CA
ON M.Mcode = CA.Mcode
JOIN Counties AS C
ON C.CTYcode = M.CTYcode
GROUP BY C.CTYname
ORDER BY C.CTYname;

/*Shows the total points each county received*/
CREATE VIEW tot_pts_cty AS
SELECT cy.CTYname, SUM(cert.Total_Points) AS Total_Points
FROM Certification AS cert JOIN Municipalities AS mun
ON cert.Mcode = mun.Mcode JOIN Counties as cy
ON cy.CTYcode = mun.CTYcode
GROUP BY mun.CTYcode, cy.CTYname
ORDER BY cy.CTYname;


/*Shows the total number of categories each county fulfilled*/
CREATE VIEW tot_cat_cty AS
SELECT CY.CTYname, COUNT(DISTINCT A.Ccode)AS Count_Category
FROM Municipalities AS M JOIN Complete_Actions AS CA
ON M.Mcode = CA.Mcode
JOIN Actions A
ON CA.Acode = A.Acode
JOIN Counties as CY
ON CY.CTYcode = M.CTYcode
GROUP BY CY.CTYname
ORDER BY CY.CTYname;

/*Shows the number of bronze stars per county*/
CREATE VIEW bronze_stars_cty AS
SELECT CY.CTYname, COUNT(C.Bronze_Silver) AS Total_Bronze
FROM Certification AS C
JOIN Municipalities AS M
ON M.Mcode = C.Mcode
JOIN Counties AS CY
ON CY.CTYcode = M.CTYcode
WHERE Bronze_Silver = 'Bronze'
GROUP BY CY.CTYname
ORDER BY CY.CTYname;

/*Shows count silver stars per county.*/
CREATE VIEW silver_stars_cty AS
SELECT CY.CTYname, COUNT(
	CASE C.Bronze_Silver WHEN 'Silver'
	THEN 1 ELSE NULL END) AS Total_Silver
FROM Certification AS C
JOIN Municipalities AS M
ON M.Mcode = C.Mcode
JOIN Counties AS CY
ON CY.CTYcode = M.CTYcode
GROUP BY CY.CTYname
ORDER BY CY.CTYname;

/*Shows the number of non-priorty actions per category*/
CREATE VIEW no_priority_cat AS
SELECT C.Cname, COUNT(A.Priority) AS Total_NonPriority_Actions
FROM Actions AS A JOIN Categories AS C
ON C.Ccode = A.Ccode
WHERE Priority IS NOT True
GROUP BY Cname
ORDER BY Cname;

/*Shows the number of priority actions per category*/
CREATE VIEW yes_priority_cat AS
SELECT C.Cname, COUNT(
	CASE WHEN A.Priority IS True
	THEN 1 ELSE NULL END) AS Total_Priority_Actions
FROM Actions AS A JOIN Categories AS C
ON C.Ccode = A.Ccode
GROUP BY Cname
ORDER BY Cname;

/*Shows the number of not required actions per category*/
CREATE VIEW no_required_cat AS
SELECT C.Cname, COUNT(A.Required) AS Total_NonRequired_Actions
FROM Actions AS A JOIN Categories AS C
ON C.Ccode = A.Ccode
WHERE Required IS NOT True
GROUP BY Cname
ORDER BY Cname;

/*Shows the number of required actions per category*/
CREATE VIEW yes_required_cat AS
SELECT C.Cname, COUNT(
	CASE WHEN A.Required IS True
	THEN 1 ELSE NULL END) AS Total_Required_Actions
FROM Actions AS A JOIN Categories AS C
ON C.Ccode = A.Ccode
GROUP BY Cname
ORDER BY Cname;
