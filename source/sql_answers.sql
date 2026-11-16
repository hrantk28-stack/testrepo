-- Task 1
SELECT DISTINCT Launch_Site FROM SPACEXTBL ORDER BY Launch_Site;
--  Launch_Site
--  CCAFS LC-40
-- CCAFS SLC-40
--   KSC LC-39A
--  VAFB SLC-4E

-- Task 2
SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' ORDER BY Date LIMIT 5;
--       Date Time (UTC) Booster_Version Launch_Site                                                       Payload  PAYLOAD_MASS__KG_     Orbit        Customer Mission_Outcome     Landing_Outcome
-- 2010-06-04   18:45:00  F9 v1.0  B0003 CCAFS LC-40                          Dragon Spacecraft Qualification Unit                  0       LEO          SpaceX         Success Failure (parachute)
-- 2010-12-08   15:43:00  F9 v1.0  B0004 CCAFS LC-40 Dragon demo flight C1, two CubeSats, barrel of Brouere cheese                  0 LEO (ISS) NASA (COTS) NRO         Success Failure (parachute)
-- 2012-05-22    7:44:00  F9 v1.0  B0005 CCAFS LC-40                                         Dragon demo flight C2                525 LEO (ISS)     NASA (COTS)         Success          No attempt
-- 2012-10-08    0:35:00  F9 v1.0  B0006 CCAFS LC-40                                                  SpaceX CRS-1                500 LEO (ISS)      NASA (CRS)         Success          No attempt
-- 2013-03-01   15:10:00  F9 v1.0  B0007 CCAFS LC-40                                                  SpaceX CRS-2                677 LEO (ISS)      NASA (CRS)         Success          No attempt

-- Task 3
SELECT SUM(PAYLOAD_MASS__KG_) AS total_kg FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';
--  total_kg
--     45596

-- Task 4
SELECT AVG(PAYLOAD_MASS__KG_) AS average_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';
--  average_kg
-- 2534.666667

-- Task 5
SELECT MIN(Date) AS first_ground_landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';
-- first_ground_landing
--           2015-12-22

-- Task 6
SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;
-- Booster_Version
--     F9 FT B1022
--     F9 FT B1026
--  F9 FT  B1021.2
--  F9 FT  B1031.2

-- Task 7
SELECT CASE WHEN Mission_Outcome LIKE 'Success%' THEN 'Success' ELSE 'Failure' END AS mission_result, COUNT(*) AS launches FROM SPACEXTBL GROUP BY mission_result;
-- mission_result  launches
--        Failure         1
--        Success       100

-- Task 8
SELECT DISTINCT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);
-- Booster_Version  PAYLOAD_MASS__KG_
--   F9 B5 B1048.4              15600
--   F9 B5 B1049.4              15600
--   F9 B5 B1051.3              15600
--   F9 B5 B1056.4              15600
--   F9 B5 B1048.5              15600
--   F9 B5 B1051.4              15600
--   F9 B5 B1049.5              15600
--   F9 B5 B1060.2              15600
--   F9 B5 B1058.3              15600
--   F9 B5 B1051.6              15600
--   F9 B5 B1060.3              15600
--   F9 B5 B1049.7              15600

-- Task 9
SELECT CASE substr(Date,6,2) WHEN '01' THEN 'January' WHEN '02' THEN 'February' WHEN '03' THEN 'March' WHEN '04' THEN 'April' WHEN '05' THEN 'May' WHEN '06' THEN 'June' WHEN '07' THEN 'July' WHEN '08' THEN 'August' WHEN '09' THEN 'September' WHEN '10' THEN 'October' WHEN '11' THEN 'November' WHEN '12' THEN 'December' END AS month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE substr(Date,1,4) = '2015' AND Landing_Outcome = 'Failure (drone ship)' ORDER BY Date;
--   month      Landing_Outcome Booster_Version Launch_Site
-- January Failure (drone ship)   F9 v1.1 B1012 CCAFS LC-40
--   April Failure (drone ship)   F9 v1.1 B1015 CCAFS LC-40

-- Task 10
SELECT Landing_Outcome, COUNT(*) AS launches, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY launches DESC, Landing_Outcome;
--        Landing_Outcome  launches  rank
--             No attempt        10     1
--   Failure (drone ship)         5     2
--   Success (drone ship)         5     2
--     Controlled (ocean)         3     3
--   Success (ground pad)         3     3
--    Failure (parachute)         2     4
--   Uncontrolled (ocean)         2     4
-- Precluded (drone ship)         1     5
