/* Gordon Petry, Michael Williams, Jason Kantner and Casey Lishko
 * Database Systems
 * 4/11/20
 * create_views.sql
 */


CREATE VIEW pt_tot_category AS
SELECT Ccode, SUM(DISTINCT Point_Value)
FROM Actions
GROUP BY Ccode;

CREATE VIEW tot_act_mun AS
SELECT Mcode, COUNT(Acode)
FROM Complete_Actions
GROUP BY Mcode;

CREATE VIEW tot_pts_mun AS
SELECT Mcode, Total_Points
FROM Certification;

CREATE VIEW tot_cat_mun AS
SELECT Mcode, COUNT(DISTINCT Ccode)
FROM Complete_Actions JOIN Actions
ON Complete_Actions.Acode = Actions.Acode
GROUP BY Mcode;

CREATE VIEW tot_act_cty AS
SELECT CTYcode, COUNT(Acode)
FROM Municipalities JOIN Complete_Actions
ON Municipalities.Mcode = Complete_Actions.Mcode
GROUP BY CTYcode;

CREATE VIEW tot_pts_cty AS
SELECT CTYcode, Total_Points
FROM Municipalities JOIN Certification
ON Municipalities.Mcode = Certification.Mcode
GROUP BY CTYcode, Total_Points;

CREATE VIEW tot_cat_cty AS
SELECT CTYcode, COUNT(DISTINCT Ccode)
FROM Municipalities JOIN Complete_Actions
ON Municipalities.Mcode = Complete_Actions.Mcode
JOIN Actions
ON Complete_Actions.Acode = Actions.Acode
GROUP BY CTYcode;

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


