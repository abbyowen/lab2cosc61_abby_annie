# views.sql
# COSC 61, Professor Palmer 
# Authors: Abby Owen and Annie Revers
# Creates the necessary views from the assignment, plus many others that help us with Trigger 2


# LeadAuthorManuscripts

DROP VIEW IF EXISTS LeadAuthorManuscripts;
CREATE VIEW LeadAuthorManuscripts AS
SELECT a.ManuscriptId, AuthorLastName, a.AuthorId, ManStatus, DateUpdated FROM
(SELECT ManuscriptId, AuthorId FROM AuthorGroup WHERE OrderNum = 1) a
LEFT JOIN (SELECT AuthorLastName, AuthorId FROM Author) b
ON a.AuthorId = b.AuthorId
LEFT JOIN (SELECT ManStatus, ManuscriptId, DateUpdated FROM Manuscript) c 
ON a.ManuscriptId = c.ManuscriptId
ORDER BY AuthorLastName ASC, AuthorId ASC, DateUpdated DESC;

SELECT * FROM LeadAuthorManuscripts;

# AnyAuthorManuscripts

DROP VIEW IF EXISTS AnyAuthorManuscripts;
CREATE VIEW AnyAuthorManuscripts AS 
SELECT a.ManuscriptId, AuthorLastName, a.AuthorId, ManStatus FROM
(SELECT ManuscriptId, AuthorId FROM AuthorGroup) a
LEFT JOIN (SELECT AuthorLastName, AuthorId FROM Author) b
ON a.AuthorId = b.AuthorId
LEFT JOIN (SELECT ManStatus, ManuscriptId, DateUpdated FROM Manuscript) c 
ON a.ManuscriptId = c.ManuscriptId
ORDER BY AuthorLastName ASC, DateUpdated DESC;

SELECT * FROM AnyAuthorManuscripts;

# PublishedIssues

DROP VIEW IF EXISTS PublishedIssues;
CREATE VIEW PublishedIssues AS 
SELECT PublicationYear, PeriodNumber, Title, StartingPage, issues.IssueId FROM 
(SELECT IssueId, PublicationYear, PeriodNumber FROM Issue WHERE PageCount >= 75 AND PageCount <= 100) issues
LEFT JOIN (SELECT Title, StartingPage, IssueId FROM Manuscript) mans
ON issues.IssueId = mans.IssueId
ORDER BY PublicationYear DESC, IssueId ASC, StartingPage ASC;

SELECT * FROM PublishedIssues;

# ReviewQueue

DROP VIEW IF EXISTS ReviewQueue;
CREATE VIEW ReviewQueue AS
SELECT mans.ManuscriptId, AuthorId, GROUP_CONCAT(ReviewerId) FROM 
(SELECT ManuscriptId, DateUpdated FROM Manuscript WHERE ManStatus = "Under Review") mans
LEFT JOIN (SELECT AuthorId, ManuscriptId FROM AuthorGroup WHERE OrderNum = 1) author
ON mans.ManuscriptId = author.ManuscriptId
LEFT JOIN (SELECT ReviewerId, ManuscriptId FROM Review ) revs 
ON revs.ManuscriptId = author.ManuscriptId
GROUP BY ManuscriptId, AuthorId
ORDER BY DateUpdated DESC;

SELECT * FROM ReviewQueue;

# WhatsLeft
DROP VIEW IF EXISTS WhatsLeft;
CREATE VIEW WhatsLeft AS 
SELECT ManuscriptId, ManStatus, DateUpdated FROM Manuscript;

SELECT * FROM WhatsLeft;

# ReviewStatus



DROP FUNCTION IF EXISTS ViewRevId;
DELIMITER $$
CREATE FUNCTION ViewRevId()    
RETURNS INT
DETERMINISTIC 
BEGIN
# see stackoverflow.com/questions/14511760 and read ALL the info TWICE or MORE.  wh 04/13/2017
    RETURN @rev_id;
END$$

DELIMITER ;

SET @rev_id = 15;
SET @test = ViewRevId();
SELECT @test;

DROP VIEW IF EXISTS ReviewStatus;
CREATE VIEW ReviewStatus AS 
SELECT FeedbackDate, reviews.ManuscriptId, Title, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation FROM 
(SELECT FeedbackDate, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation FROM Review WHERE ReviewerId = ViewRevId()) reviews
LEFT JOIN (SELECT Title, ManuscriptId FROM Manuscript) titles
ON titles.ManuscriptId = reviews.ManuscriptId;


SELECT * FROM ReviewStatus;

# HELPER VIEWS FOR TRIGGER 2

# OtherReviewers
# Gives us the Other Reviewers that Review all of the Manuscripts that the Reviewer to be deleted Reviews

DROP VIEW IF EXISTS OtherReviewers;
CREATE VIEW OtherReviewers AS 
SELECT other_reviewers.ManuscriptId, ReviewerId FROM 
(SELECT ManuscriptId FROM Review WHERE ReviewerId = ViewRevId()) mans
LEFT JOIN (SELECT ReviewerId, ManuscriptId FROM Review WHERE ReviewerId != ViewRevId()) other_reviewers
ON mans.ManuscriptId = other_reviewers.ManuscriptId;

SELECT * FROM OtherReviewers;

# ReviewerManuscripts
# Gets only the ManuscriptId from the ReviewStatus View

DROP VIEW IF EXISTS ReviewerManuscripts;
CREATE VIEW ReviewerManuscripts AS
SELECT ManuscriptId AS RManuscripts FROM ReviewStatus;

SELECT * FROM ReviewerManuscripts;

# SoleReviewerManuscript
# Gets the manuscripts that are only reviewed by the reviewer that will be deleted

DROP VIEW IF EXISTS SoleReviewerManuscript;
CREATE VIEW SoleReviewerManuscript AS
SELECT RManuscripts FROM 
ReviewerManuscripts LEFT JOIN OtherReviewers 
ON ReviewerManuscripts.RManuscripts = OtherReviewers.ManuscriptId
WHERE ReviewerId IS NULL;

SELECT * FROM SoleReviewerManuscript;

# SoleICodeView
# Gets the ICodes for the Manuscripts that only have the Reviewer that will be deleted

DROP VIEW IF EXISTS SoleICodeView;
CREATE VIEW SoleICodeView AS
SELECT ICodeId, ManuscriptId FROM 
SoleReviewerManuscript LEFT JOIN Manuscript
ON SoleReviewerManuscript.RManuscripts = Manuscript.ManuscriptId;

SELECT * FROM SoleICodeView;

# NoOtherReviewersWithICode
# Gets the ManuscriptIds that don't have reviewers with its ICode (Must be rejected)

DROP VIEW IF EXISTS NoOtherReviewersWithICode;
CREATE VIEW NoOtherReviewersWithICode AS 
SELECT SoleICodeView.ICodeId, ReviewerId, ManuscriptId FROM 
SoleICodeView LEFT JOIN ReviewerICodeGroup 
ON SoleICodeView.ICodeId = ReviewerICodeGroup.ICodeId
WHERE ReviewerId IS NULL;

SELECT * FROM NoOtherReviewersWithICode;

# ExistsReviewersWithICode
# Gets the ManuscriptIds that has potential other reviewers (Must be set back to "Recieved" (Our version of "Submitted"))

DROP VIEW IF EXISTS ExistReviewersWithICode;
CREATE VIEW ExistReviewersWithICode AS 
SELECT SoleICodeView.ICodeId, ReviewerId, ManuscriptId FROM 
SoleICodeView LEFT JOIN ReviewerICodeGroup 
ON SoleICodeView.ICodeId = ReviewerICodeGroup.ICodeId
WHERE ReviewerId IS NOT NULL;

SELECT * FROM ExistReviewersWithICode;









