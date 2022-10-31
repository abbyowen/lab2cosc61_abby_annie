-- procedures.sql
-- COSC 61, Professor Palmer 
-- Authors: Abby Owen and Annie Revers
-- Creates the procedure that determines whether or not a manuscript is accepted or rejected

DROP PROCEDURE IF EXISTS AcceptReject;
DELIMITER //
CREATE PROCEDURE AcceptReject(IN ManId int, OUT Decision varchar(10))
  BEGIN
    IF (SELECT AVG(A_Rating + C_Rating + M_Rating + E_Rating + Recommendation) FROM Review WHERE ManuscriptId = ManId > 40) THEN 
		SELECT "Accept" INTO Decision;
	ELSE
		SELECT "Reject" INTO Decision;
	END IF;
  END//
DELIMITER ;


CALL AcceptReject(2, @decision);
SELECT @decision;