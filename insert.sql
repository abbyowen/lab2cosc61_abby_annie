# insert.sql
# COSC 61, Professor Palmer 
# Authors: Abby Owen and Annie Revers
# Performs inserts of test data into our tables 

######################
# Author Inserts
# Must first insert into the SysUser table, then into the Author table
######################

INSERT INTO SysUser (UserType)
VALUES
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author");
INSERT INTO SysUser (UserType)
VALUES  
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author");

INSERT INTO SysUser (UserType)
VALUES
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author");

INSERT INTO SysUser (UserType)
VALUES
  ("author"),
  ("author"),
  ("author"),
  ("author"),
  ("author");

# Author inserts

INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName, AuthorAffiliation)
VALUES
  (1, "Marshall","Jarvis","Adipiscing Fringilla Porttitor PC"),
  (2, "Philip","Terry","Dictum Augue Corp."),
  (3, "Jeremy","Murray","Mi Lacinia Institute"),
  (4, "Larissa","Hardin","Nec Tempus Foundation"),
  (5, "Yvette","Chan","Donec Felis Industries"),
  (6, "Regina","Ortiz","Erat Institute"),
  (7, "Honorato","Barlow","Ipsum Phasellus Ltd"),
  (8, "Chiquita","Zamora","Suspendisse Ac Inc."),
  (9, "Caldwell","Lancaster","Non Enim Institute"),
  (10, "Holly","Douglas","Sed Tortor Associates");
INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName,AuthorAffiliation)
VALUES
  (11, "Hamilton","Fisher","Vitae Erat Company"),
  (12, "Coby","Stein","Leo Limited"),
  (13, "Orli","Callahan","Lectus Cum PC"),
  (14, "Miriam","Guerra","Mauris Suspendisse Limited"),
  (15, "Astra","Vaughan","Turpis Non LLC"),
  (16, "Nehru","Clements","A Feugiat Tellus Associates"),
  (17, "Gillian","Stark","Ipsum Non Corporation"),
  (18, "Leandra","Velazquez","Eu Euismod Institute"),
  (19, "Samantha","Brewer","Risus Associates"),
  (20, "Martina","Johns","Congue Elit Institute");
INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName, AuthorAffiliation)
VALUES
  (21, "Laura","Sweeney","Facilisis Foundation"),
  (22, "Barrett","Kelley","Morbi Non Sapien PC"),
  (23, "Colorado","Mullins","Pede Blandit PC"),
  (24, "Amethyst","Jones","Pede Et Risus Inc."),
  (25, "Astra","Cantrell","Integer PC");

INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName, AuthorAffiliation, AuthorEmail)
VALUES
  (26, "Dante","Boyd","Tincidunt Orci Quis Associates", "danteboyd@quis.com"),
  (27, "Ruby","Berg","Auctor Nunc Nulla Institute", "rubyberg@gmail.com"),
  (28, "Paula","Howard","Mauris Blandit Industries", "paulahoward@gmail.com"),
  (29, "Sage","Bolton","Cursus Diam Institute", "sagebolton@aol.com"),
  (30, "Nita","Anderson","Et Commodo PC", "nita@me.com");
  

SELECT * FROM Author;

######################
# Editor Inserts
# Must first insert into the SysUser table, then into the Editor table
######################

INSERT INTO SysUser (UserType)
VALUES
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor");
INSERT INTO SysUser (UserType)
VALUES
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor");
INSERT INTO SysUser (UserType)
VALUES
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor"),
  ("editor");


INSERT INTO Editor (EditorId, EditorFirstName, EditorLastName)
VALUES
  (31, "Gray","Waters"),
  (32, "Ursula","Chavez"),
  (33, "Griffith","Robinson"),
  (34, "Caleb","Galloway"),
  (35, "Carson","Casey"),
  (36, "Michelle","Gibson"),
  (37, "Perry","Gilliam"),
  (38, "Lilah","Ramos"),
  (39, "Zane","Levy"),
  (40, "Dahlia","Dunlap");
INSERT INTO Editor (EditorId, EditorFirstName, EditorLastName)
VALUES
  (41, "Owen","Strickland"),
  (42, "Linda","Fitzpatrick"),
  (43, "Keefe","Travis"),
  (44, "Tatum","Sandoval"),
  (45, "Charde","Craft"),
  (46, "Wing","Dickson"),
  (47, "Burke","Hartman"),
  (48, "Daquan","Gilmore"),
  (49, "Vanna","Torres"),
  (50, "Clark","Anthony");
INSERT INTO Editor (EditorId, EditorFirstName, EditorLastName)
VALUES
  (51, "Audrey","Dickerson"),
  (52, "Nash","Burnett"),
  (53, "Wynter","Davidson"),
  (54, "Quentin","White"),
  (55, "Jordan","Carlson");

SELECT * FROM Editor;

######################
# Issue Inserts 
######################

INSERT INTO Issue (PublicationYear, PeriodNumber, PageCount)
VALUES
  ("2016",3, 95),
  ("2003",4, 40),
  ("2019",3, 76);


INSERT INTO Issue (PublicationYear, PeriodNumber)
VALUES
  ("2020",3),
  ("2009",1),
  ("2018",4),
  ("2022",3),
  ("2008",3),
  ("2015",1),
  ("2011",2);


SELECT * FROM Issue;

######################
# ICode Inserts 
######################

INSERT INTO ICode (InterestName)
VALUES
  ("ML"),
  ("english"),
  ("biology"),
  ("chemistry"),
  ("biology"),
  ("art history"), 
  ("databases"), 
  ("dartmouth");

SELECT * FROM ICode;

######################
# Manuscript Inserts 
######################

INSERT INTO Manuscript (Title, PageCount, ManStatus)
VALUES
  ("Hi Annie, hope you are having a great day",96,"Recieved"),
  ("What lives in a pond",78,"Published"),
  ("Cabins for dummies",57,"Ready"),
  ("Fun sample title",15,"Rejected"),
  ("Sock wrestling",16,"Typesetting");
INSERT INTO Manuscript (Title, PageCount, ICodeId, ManStatus)
VALUES
 ("Random loud noise",44, 4, "Recieved");
INSERT INTO Manuscript (Title, PageCount, ICodeId, ManStatus)
VALUES
  ("Two hours to go", 15, 8, "Recieved"),
  ("Extension", 15, 8, "Recieved");


INSERT INTO Manuscript (Title, PageCount, ManStatus)
VALUES
  ("gang",82,"Rejected"),
  ("Test title 5",66,"Under Review"),
  ("Test title 6",56,"Under Review"),
  ("Test title 7",65,"Under Review"),
  ("Test title 8",22,"Published");

INSERT INTO Manuscript (Title, ICodeId, EditorId, PageCount, ManStatus)
VALUES
  ("All about databases", 1, 47, 70,"Accepted"),
  ("Machine Learning: A history", 4, 38, 61,"Recieved"),
  ("Biology for beginners", 3, 46, 72,"Typesetting"),
  ("The science behind hot tubs", 5, 34, 10,"Ready");

INSERT INTO Manuscript (Title, EditorId, PageCount, ManStatus)
VALUES
  ("Test title 1", 39, 70,"Published"),
  ("Test title 2", 40, 61,"Recieved"),
  ("Test title 100", 41, 72,"Typesetting"),
  ("Test title 100000", 42, 10,"Ready");
  
INSERT INTO Manuscript (Title, ICodeId, EditorId, IssueId, StartingPage, PageCount, ManStatus)
VALUES
  ("Help me I am tired", 1, 47, 1, 1, 70,"Accepted"), 
  ("I have a headache", 4, 38, 2, 10, 61,"Recieved"),
  ("happy weekend", 3, 46, 3, 34, 72,"Typesetting"),
  ("scrubbin and tubbin", 5, 33, 1, 71, 10,"Ready");
SELECT * FROM Manuscript;

######################
# Reviewer Inserts
######################
INSERT INTO SysUser (UserType)
VALUES
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer");
INSERT INTO SysUser (UserType)
VALUES
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer");
INSERT INTO SysUser (UserType)
VALUES
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer"),
  ("reviewer");



INSERT INTO Reviewer (ReviewerId, ReviewerFirstName, ReviewerLastName, ReviewerAffiliation, ReviewerEmail)
VALUES
  (56, "Raven","Carson","Dolor Tempus Non Associates", "rc@gmail.com"),
  (57, "Irma","Fitzgerald","Dictum Phasellus Incorporated", "if@gmail.com"),
  (58, "Barclay","Weiss","Non Hendrerit Consulting", "bw@gmail.com"),
  (59, "Erin","Sargent","Facilisis Lorem Company", "es@gmail.com"),
  (60, "Jaime","Mejia","Vel Corp.", "jm@gmail.com"),
  (61, "Laurel","Peters","Mi Felis Associates", "lp@gmail.com"),
  (62, "Jamalia","Horn","Phasellus Corporation", "jh@gmail.com"),
  (63, "Brendan","Clements","Et Institute", "bc@gmail.com"),
  (64, "Suki","Huber","Mollis Vitae Associates", "sh@gmail.com"),
  (65, "Fletcher","Olson","Aliquet Diam Corporation", "fo@gmail.com");
INSERT INTO Reviewer (ReviewerId, ReviewerFirstName, ReviewerLastName, ReviewerAffiliation, ReviewerEmail)
VALUES
  (66, "Neil","Serrano","Augue Scelerisque Consulting", "ns@gmail.com"),
  (67, "Elvis","Ellison","Purus Sapien Gravida Inc.", "ee@gmail.com"),
  (68, "Chantale","Ayala","Mauris Limited", "ca@gmail.com"),
  (69, "Wang","May","Viverra Ltd", "wm@gmail.com"),
  (70, "Leila","Clark","Vel Arcu Ltd", "lc@gmail.com"),
  (71, "Carol","Hoffman","Aenean LLP", "ch@gmail.com"),
  (72, "Jordan","Carter","In Industries", "jc@gmail.com"),
  (73, "Nell","Pittman","Congue Incorporated", "np@gmail.com"),
  (74, "Lisandra","Ware","Nunc Industries", "lw@gmail.com"),
  (75, "Nicole","Pacheco","Sed Turpis Corp.", "np@gmail.com");
INSERT INTO Reviewer (ReviewerId, ReviewerFirstName, ReviewerLastName, ReviewerAffiliation, ReviewerEmail)
VALUES
  (76, "Drew","Spencer","Nulla Facilisis Company", "ds@gmail.com"),
  (77, "Clayton","Goodwin","Non Feugiat Nec Corp.", "cg@gmail.com"),
  (78, "Bryar","Howard","Imperdiet Erat Nonummy Company", "bh@gmail.com"),
  (79, "Prescott","Vang","Donec Egestas Industries", "pv@gmail.com"),
  (80, "Jerome","Ford","Vitae Limited", "jf@gmail.com"); 

SELECT * FROM Reviewer;

######################
# Review Inserts 
######################
# Reviews inserted for help with triggers 
# Manuscript 8 has only 1 reviewer and this reviewer is the only reviewer with this ICode - 15, meaning it will be rejected when reviewer 15 is deleted
INSERT INTO Review (ReviewerId, ManuscriptId)
VALUES 
	(76, 15),
    (80, 1),
    (73, 5),
    (75, 1),
    (66, 3);
INSERT INTO Review (ReviewerId, ManuscriptId)
VALUES 
	(76, 9),
    (80, 10),
    (73, 4);

INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(69, 2, 1, 2, 3, 4, 10, CURRENT_TIMESTAMP),
    (71, 4, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(69, 4, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(71, 2, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(69, 1, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(69, 6, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(69, 7, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(75, 2, 2, 3, 4, 5, 10, CURRENT_TIMESTAMP);


######################
# TRIGGER 2 SETUP Inserts
######################
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(71, 8, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);
INSERT INTO Review (ReviewerId, ManuscriptId, A_Rating, C_Rating, M_Rating, E_Rating, Recommendation, FeedbackDate)
VALUES 
	(71, 16, 2, 3, 4, 5, 0, CURRENT_TIMESTAMP);

	
SELECT * FROM Review;

######################
# ReviewerICodeGroup
######################

INSERT INTO ReviewerICodeGroup (ReviewerId, ICodeId)
VALUES 
	(56, 1),
    (57, 1),
    (58, 1),
    (66, 2),
    (68, 2),
    (69, 2), 
    (66, 3), 
    (67, 3), 
    (68, 3), 
    (80, 4),
    (75, 4),
    (65, 4),
    (68, 5),
    (60, 5), 
    (69, 5), 
    (71, 6), 
    (72, 6),
    (75, 6),
    (76, 7), 
    (77, 7), 
    (79, 7), 
    # Reviewer 15 is the ONLY Reviewer with ICode 8 (helpful for our trigger)
    # All others have sufficient number of ICodes
    # Also, unable to insert manuscript of ICode 8 after we run our triggers, because there are not 3 reviewers for this ICode
    (70, 8);

SELECT * FROM ReviewerICodeGroup;

######################
# Author Group Inserts
######################

INSERT INTO AuthorGroup (AuthorId, ManuscriptId, OrderNum)
VALUES 
	(26, 10, 1),
    (5, 10, 2), 
    (27, 4, 1), 
    (28, 5, 1), 
    (28, 6, 2),
    (5, 7, 2);

INSERT INTO AuthorGroup (AuthorId, ManuscriptId, OrderNum)
VALUES 
	(14, 8, 1),
    (15, 9, 2);
INSERT INTO AuthorGroup (AuthorId, ManuscriptId, OrderNum)
VALUES 
	(16, 9, 1);

SELECT * FROM AuthorGroup;