/* Gordon Petry, Michael Williams, Jason Kantner and Casey Lishko
 * Database Systems
 * 4/11/20
 * create_views.sql
 */

/*Good?*/
CREATE VIEW pt_tot_category AS
SELECT C.Cname, SUM(A.Point_Value)
FROM Actions AS A JOIN Categories AS C
ON A.Ccode = C.Ccode
GROUP BY C.Cname;

/*Good*/
CREATE VIEW tot_act_mun AS
SELECT M.Mname, COUNT(CA.Acode)
FROM Complete_Actions AS CA JOIN Municipalities AS M
ON CA.Mcode = M.Mcode
GROUP BY M.Mname;

/*Good*/
CREATE VIEW tot_pts_mun AS
SELECT M.Mname, C.Total_Points
FROM Certification AS C JOIN Municipalities AS M
ON C.Mcode = M.Mcode;

/*Good*/
CREATE VIEW tot_cat_mun AS
SELECT M.Mname, COUNT(DISTINCT A.Ccode)
FROM Complete_Actions AS CA JOIN Actions A
ON CA.Acode = A.Acode
JOIN Municipalities AS M
ON CA.Mcode = M.Mcode
GROUP BY M.Mname;

/*Good*/
CREATE VIEW tot_act_cty AS
SELECT C.CTYname, COUNT(CA.Acode)
FROM Municipalities AS M JOIN Complete_Actions AS CA
ON M.Mcode = CA.Mcode
JOIN Counties AS C
ON C.CTYcode = M.CTYcode
GROUP BY C.CTYname;

/*Good*/
CREATE VIEW tot_pts_cty AS
SELECT CY.CTYname, C.Total_Points
FROM Municipalities AS M JOIN Certification AS C
ON M.Mcode = C.Mcode
JOIN Counties as CY
ON CY.CTYcode = M.CTYcode
GROUP BY CY.CTYname, C.Total_Points;

/*Good*/
CREATE VIEW tot_cat_cty AS
SELECT CY.CTYname, COUNT(DISTINCT A.Ccode)
FROM Municipalities AS M JOIN Complete_Actions AS CA
ON M.Mcode = CA.Mcode
JOIN Actions A
ON CA.Acode = A.Acode
JOIN Counties as CY
ON CY.CTYcode = M.CTYcode
GROUP BY CY.CTYname;

/*-----------------------------------*/

CREATE VIEW no_gold_stars AS
SELECT Mcode, Num_Gold_Stars
FROM Certification
WHERE Num_Gold_Stars = 0;

CREATE VIEW many_gold_stars AS
SELECT Mcode, Num_Gold_Stars
FROM Certification
WHERE Num_Gold_Stars >= 1;

CREATE VIEW bronze_stars AS
SELECT Mcode, Bronze_Silver
FROM Certification
WHERE Bronze_Silver = 'Bronze';

CREATE VIEW silver_stars AS
SELECT Mcode, Bronze_Silver
FROM Certification
WHERE Bronze_Silver = 'Silver';

CREATE VIEW no_priority AS
SELECT Acode, Aname, Ccode
FROM Actions
WHERE Priority IS NOT TRUE;

CREATE VIEW yes_priority AS
SELECT Acode, Aname, Ccode
FROM Actions
WHERE Priority IS TRUE;

CREATE VIEW no_required AS
SELECT Acode, Aname, Ccode
FROM Actions
WHERE Required IS NOT TRUE;

CREATE VIEW yes_required AS
SELECT Acode, Aname, Ccode
FROM Actions
WHERE Required IS TRUE;

CREATE VIEW small_pt_act AS
SELECT Acode, Aname, Point_Value
FROM Actions
WHERE Point_Value <= 10;

CREATE VIEW large_pt_act AS
SELECT Acode, Aname, Point_Value
FROM Actions
WHERE Point_Value > 10;

CREATE VIEW pt_tot_act AS
SELECT Acode, SUM(Point_Value)
FROM Actions
GROUP BY Acode;

CREATE VIEW not_completed_actions AS
SELECT A.Acode, A.Aname
FROM Actions AS A LEFT JOIN Complete_Actions AS CA
ON A.Acode = CA.Acode;


