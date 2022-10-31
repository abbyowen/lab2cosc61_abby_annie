-- triggers.sql
-- COSC 61, Professor Palmer 
-- Authors: Abby Owen and Annie Revers
-- Has 4 triggers, including the 3 necessary from the specs and one additional that we deemed necessary to keep track of when status updates are made

-- Trigger --1 
-- We use the ICode table because the only time we insert an ICode is when a Reviewer has this ICODE
DROP TRIGGER IF EXISTS after_manuscript_submit;
DELIMITER $$
CREATE TRIGGER after_manuscript_submit BEFORE INSERT 
ON Manuscript
    FOR EACH ROW 
		IF (SELECT COUNT(ICodeId) FROM ReviewerICodeGroup WHERE ICodeId = NEW.ICodeId < 3) THEN
             set @msg = concat('LAB2: Not enough reviewers for ICode id ', cast(NEW.ICodeId as char));
			 signal sqlstate '45000' set message_text = @msg;
		END IF; $$
DELIMITER ;



-- Trigger --2 
-- NOTE: We do not have this trigger throw and exception as it stopped the runtime within our query 
DROP TRIGGER IF EXISTS delete_reviewer;
DELIMITER $$
CREATE TRIGGER delete_reviewer BEFORE DELETE 
ON Reviewer
    FOR EACH ROW 
        BEGIN
        SET @rev_id = OLD.ReviewerId;
        DELETE FROM ReviewerICodeGroup WHERE ReviewerId = OLD.ReviewerId;
        IF (SELECT EXISTS(SELECT 1 FROM ExistReviewersWithICode)) THEN
			UPDATE 
				Manuscript M, 
				ExistReviewersWithICode Acc
			SET M.ManStatus = "Recieved"
			WHERE M.ManuscriptId  = Acc.ManuscriptId;
		END IF;
        
        IF (SELECT EXISTS(SELECT 1 FROM NoOtherReviewersWithICode)) THEN
			UPDATE 
				Manuscript M, 
				NoOtherReviewersWithICode Rej
			SET M.ManStatus = "Rejected"
			WHERE M.ManuscriptId  = Rej.ManuscriptId;
		END IF;
		
        DELETE FROM Review WHERE ReviewerId = OLD.ReviewerId;
        END$$
		
        
DELIMITER ;

-- Trigger --3 
-- Update Accepted Manuscript to Typesetting
DROP TRIGGER IF EXISTS before_manuscript_accept;
DELIMITER $$
CREATE TRIGGER before_manuscript_accept BEFORE UPDATE 
ON Manuscript
    FOR EACH ROW 
		IF NEW.ManStatus = "Accepted" THEN
			 SET NEW.ManStatus = 'Typesetting';
		END IF; $$
DELIMITER ;


-- Trigger --4 
-- Update DateUpdated to current time whenever a status is changed
DROP TRIGGER IF EXISTS update_status_date;
DELIMITER $$
CREATE TRIGGER update_status_date BEFORE UPDATE ON Manuscript
FOR EACH ROW
BEGIN
   IF (NEW.ManStatus != OLD.ManStatus) THEN
      SET NEW.DateUpdated = NOW();
   END IF;
END;$$
DELIMITER ;

-- Trigger --5
-- Add page numbers when manuscript moves to typesetting (HACK FROM SLACK MESSAGE FROM PROF PALMER)
DROP TRIGGER IF EXISTS update_pages_ready;
DELIMITER $$
CREATE TRIGGER update_pages_ready BEFORE UPDATE ON Manuscript
FOR EACH ROW 
BEGIN 
	IF (NEW.ManStatus = "Typesetting") THEN 
        SET NEW.ManStatus = "Ready";
		SET NEW.PageCount = RAND()*(20 - 5)+5;
	END IF;
END;$$
DELIMITER ;