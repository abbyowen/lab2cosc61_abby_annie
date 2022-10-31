-- tables.sql
-- COSC 61, Professor Palmer 
-- Authors: Abby Owen and Annie Revers
-- Creates tables based off of our schema/ERD

use F003WV0_db;

DROP TABLE IF EXISTS AuthorGroup;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Manuscript;
DROP TABLE IF EXISTS Issue;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Editor;
DROP TABLE IF EXISTS ReviewerICodeGroup;
DROP TABLE IF EXISTS Reviewer;
DROP TABLE IF EXISTS ICode;
DROP TABLE IF EXISTS SysUser;


CREATE TABLE SysUser
   ( UniversalId    int NOT NULL AUTO_INCREMENT,
	 UserType       char(15) NOT NULL,
     PRIMARY KEY (UniversalId)
   );

CREATE TABLE 	ICode 
  ( ICodeId   		int NOT NULL AUTO_INCREMENT,
    InterestName   	varchar(100) NOT NULL,
    PRIMARY KEY (ICodeId)
  );
  


CREATE TABLE 	Editor 
  ( EditorId   		int NOT NULL,
    EditorFirstName varchar(100) NOT NULL,
    EditorLastName  varchar(100) NOT NULL,
    PRIMARY KEY (EditorId)
  );


CREATE TABLE 	Issue 
  ( IssueId   		int NOT NULL AUTO_INCREMENT,
    PublicationYear numeric(4, 0) NOT NULL,
    PeriodNumber  	int NOT NULL,
    CHECK (PeriodNumber = 1 OR PeriodNumber = 2 OR PeriodNumber = 3 OR PeriodNumber = 4),
    PageCount		int NOT NULL DEFAULT 0,
    PRIMARY KEY (IssueId)
  );
  
  CREATE TABLE 	Manuscript 
  ( ManuscriptId   	int AUTO_INCREMENT,
    Title   		varchar(100) NOT NULL,
    DateRecieved    datetime DEFAULT CURRENT_TIMESTAMP, 
    DateUpdated     datetime DEFAULT CURRENT_TIMESTAMP,
    ManStatus       varchar(45) DEFAULT "Recieved",
    StartingPage    numeric(3, 0) NULL,
    PageCount       numeric(3, 0) NOT NULL,
    ICodeId         int NULL,
    EditorId        int NULL,
    IssueId			int NULL,
    PRIMARY KEY (ManuscriptId),
    FOREIGN KEY (ICodeId) REFERENCES ICode(ICodeId),
    FOREIGN KEY (EditorId) REFERENCES Editor(EditorId),
    FOREIGN KEY (IssueId) REFERENCES Issue(IssueId)
  );
  
  CREATE TABLE Author
  ( AuthorId		int NOT NULL,
	AuthorFirstName	varchar(45) NOT NULL,
    AuthorLastName	varchar(45) NOT NULL,
    AuthorAffiliation varchar(45) NULL, 
    AuthorEmail		varchar(45) NULL,
    PRIMARY KEY (AuthorId)
	);
  
  CREATE TABLE AuthorGroup
  ( ManuscriptId	int NOT NULL,
	AuthorId		int NOT NULL,
    OrderNum		int NOT NULL,
    PRIMARY KEY (ManuscriptId, AuthorId), 
    FOREIGN KEY (ManuscriptId) REFERENCES Manuscript(ManuscriptId),
    FOREIGN KEY (AuthorId) REFERENCES Author(AuthorId)
	);

CREATE TABLE Reviewer
  ( ReviewerId		int NOT NULL,
	ReviewerFirstName varchar(45) NOT NULL,
    ReviewerLastName  varchar(45) NOT NULL,
    ReviewerEmail	  varchar(45) NOT NULL, 
    ReviewerAffiliation varchar(45) NOT NULL,
    PRIMARY KEY (ReviewerId)
	);

 CREATE TABLE ReviewerICodeGroup
  ( ReviewerId		int NOT NULL,
	ICodeId			int NOT NULL,
    PRIMARY KEY (ReviewerId, ICodeId), 
    FOREIGN KEY (ReviewerId) REFERENCES Reviewer(ReviewerId),
    FOREIGN KEY (ICodeId) REFERENCES ICode(ICodeId)
	);


CREATE TABLE Review
  ( ReviewerId		int NOT NULL,
	ManuscriptId 	int NOT NULL,
    A_Rating       	int NULL,
    CHECK (A_Rating <= 10 AND A_Rating >= 0),
	C_Rating       	int NULL,
    CHECK (C_Rating <= 10 AND C_Rating >= 0),
	M_Rating       	int NULL,
    CHECK (M_Rating <= 10 AND M_Rating >= 0),
	E_Rating       	int NULL,
    CHECK (E_Rating <= 10 AND E_Rating >= 0),
    Recommendation	int NULL, 
    CHECK (Recommendation <= 10 AND Recommendation >= 0),
    FeedbackDate    datetime NULL,
    PRIMARY KEY (ReviewerId, ManuscriptId),
    FOREIGN KEY (ReviewerId) REFERENCES Reviewer(ReviewerId),
    FOREIGN KEY (ManuscriptId) REFERENCES Manuscript(ManuscriptId)
    );