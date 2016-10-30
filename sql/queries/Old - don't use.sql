
/* A team member */
INSERT INTO TeamMember(name,email,role,password,hireDate) VALUES ("alex rhodes","alex@email.com","??","password","2016-10-25");
INSERT INTO TeamMember(name,email,role,password,hireDate) VALUES ("Caleb Hutchison","caleb@email.com","??","password","2016-10-21");
/*team member role*/
INSERT INTO SeniorDev(dateBecameSenior,email) VALUES ("2016-10-25","alex@email.com");
INSERT INTO JuniorDev(almaMater,email) VALUES ("Arizona State Univesity","caleb@email.com");

/*Team */
INSERT INTO Team(name) VALUES ("Team 1");

/*Team leader */
INSERT INTO teamHasLeader (email,teamName) VALUES ("alex@email.com","team 1");

/*Team member */
INSERT INTO teamComposedOf(email,teamName) VALUES("caleb@email.com","team 1");
INSERT INTO teamComposedOf(email,teamName) VALUES("alex@email.com","team 1");

/*Board */
INSERT INTO Board(title,description) VALUES ("test board","This board is a test board.");

/*Board team relation */
INSERT INTO boardRunBy(title,teamName) VALUES("test board", "team 1");

/*Board Category */
INSERT INTO Category(id,title,description) VALUES ("to do","cards that are not yet started");
INSERT INTO Category(id,title,description) VALUES ("in work","cards that are in work and not complete");
INSERT INTO Category(id,title,description) VALUES ("complete","cards that are complete");

/*category board relationship*/
INSERT INTO boardContains(categoryId,boardTitle) VALUES ("to do","test board");
INSERT INTO boardContains(categoryId,boardTitle) VALUES ("in work","test board");
INSERT INTO boardContains(categoryId,boardTitle) VALUES ("complete","test board");

INSERT INTO Card(id,due_date,priority,description,title) VALUES ("2016-11-10","HIGH","this is a test card","Card 0");
INSERT INTO Card(id,due_date,priority,description,title) VALUES ("2016-11-09","MED","this is another test card","Card 1");
INSERT INTO Card(id,due_date,priority,description,title) VALUES ("2016-12-01","LOW","a test card","Card 2");
INSERT INTO Card(id,due_date,priority,description,title) VALUES ("2016-12-01","LOW","a card that is backlogged","Card 3");

/*add cards to category*/
INSERT INTO categorizedAs(cardId,categoryId) VALUES (0,1);
INSERT INTO categorizedAs(cardId,categoryId) VALUES (1,1);
INSERT INTO categorizedAs(cardId,categoryId) VALUES (2,2);

/*backlog a card*/
INSERT INTO backLog(boardTitle,cardId) VALUES("test board",3)

/*assign cards */
INSERT INTO assignedTo (cardId,email) VALUES (0,"caleb@email");
INSERT INTO assignedTo (cardId,email) VALUES (1,"alex@email");
INSERT INTO assignedTo (cardId,email) VALUES (2,"caleb@email");

/*SELECT STATEMENTS */

/*When a team member logs in, select the boards that they are associated with */
SELECT * FROM Board b,
runBy rb, Team t, teamComposedOf tco, teamMember tm
WHERE b.title = rb.title
AND t.name = rb.name
AND tco.teamName = t.name
AND tco.email = tm.email
AND tm.email = "caleb@email.com";


/*Load categories and cards for the board when that user selects a board to view*/
SELECT * FROM Category AS cat
JOIN boardContains AS bc ON bc.categoryId = cat.id
JOIN Board AS b ON board.title = bc.title
categorizedAs AS ca ON ca.categoryId = cat.id
JOIN Card AS card ON card.Id = ca.cardId
WHERE 1;

/* count high priority cards by team member */
SELECT tm.name, count(*) AS numCards
FROM teamMember AS tm, assignedTo AS ato, card AS c
WHERE tm.email = ato.email AND c.id = ato.id
AND c.priority = "HIGH"
GROUP BY tm.name;

/*count past due cards per team member */
SELECT tm.name, count(*) AS numCards
FROM teamMember AS tm, assignedTo AS ato, card AS c
WHERE tm.email = ato.email AND c.id = ato.id
AND c.due_date < GETDATE()
GROUP BY tm.name;

/* past due cards in "to do" category*/
SELECT * FROM Cards c, categorizedAs ca, Category cat
WHERE c.id = ca.cardId
AND ca.categoryId = cat.categoryId
AND c.due_date < GETDATE()
AND cat.title = "to do";

/*Cards that are high priority that are backlogged */
SELECT * FROM Cards c, isBackloggedOn bl, Board b
WHERE c.id = bl.cardId
AND b.boardTitle = bl.boardTitle
AND c.priority = "HIGH";

/* Select team mates who are interns */
SELECT * FROM TeamMember tm, Intern it, Team t, teamComposedOf tco
WHERE tm.email = tco.email
AND tco.teamName = t.name
AND it.email = tm.email
WHERE 1;

/* how many cards are in each category for a board */
SELECT c.id, COUNT(tab1.cardNumber)
FROM(
	SELECT cat.id AS cid, card.id AS cardNumber
	FROM Category cat, Card card, categorizedAs ca
	WHERE cat.id = ca.categoryId
	AND card.id = ca.cardId) tab1,
Category c
WHERE c.id = tab1.cid
GROUP BY c.id
