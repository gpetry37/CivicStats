/* Gordon Petry, Michael Williams, Jason Kantner and Casey Lishko
 * Database Systems
 * 4/8/2020
 * Stage V(a)
 * create_tables.sql
 */

CREATE TABLE Counties (
CTYcode SERIAL NOT NULL,
CTYname VARCHAR(30) NOT NULL,
PRIMARY KEY (CTYcode)
);

CREATE TABLE Categories (
Ccode SERIAL NOT NULL,
Cname VARCHAR(50) NOT NULL,
PRIMARY KEY (Ccode)
);

CREATE TABLE Municipalities (
Mcode SERIAL NOT NULL,
Mname VARCHAR(30) NOT NULL,
CTYcode SERIAL NOT NULL,
PRIMARY KEY (Mcode),
FOREIGN KEY (CTYcode) REFERENCES Counties (CTYcode) ON DELETE CASCADE
);

CREATE TABLE Certification (
Mcode SERIAL NOT NULL,
Certification_Date DATE NOT NULL,
Total_Points INT NOT NULL,
Num_Gold_Stars INT NOT NULL,
Bronze_Silver VARCHAR(10) NOT NULL,
PRIMARY KEY (Mcode),
FOREIGN KEY (Mcode) REFERENCES Municipalities (Mcode) ON DELETE CASCADE
);

CREATE TABLE Actions(
Acode SERIAL NOT NULL UNIQUE,
Ccode SERIAL NOT NULL,
Aname VARCHAR(100) NOT NULL,
Point_Value INT NOT NULL,
Priority BOOLEAN NOT NULL,
Required BOOLEAN NOT NULL,
PRIMARY KEY (Acode, Ccode, Aname),
FOREIGN KEY (Ccode) REFERENCES Categories (Ccode) ON DELETE CASCADE
);

CREATE TABLE Complete_Actions(
Acode SERIAL NOT NULL,
Mcode SERIAL NOT NULL,
PRIMARY KEY (Acode, Mcode),
FOREIGN KEY (Mcode) REFERENCES Municipalities(Mcode) ON DELETE CASCADE,
FOREIGN KEY (Acode) REFERENCES Actions (Acode) ON DELETE CASCADE
);
