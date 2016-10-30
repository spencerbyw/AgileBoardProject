
/* A team member */
INSERT INTO TeamMember(name,email,role,password,hireDate) VALUES ('alex rhodes','alex@email.com','Senior Developer','password','2016-10-25');
INSERT INTO TeamMember(name,email,role,password,hireDate) VALUES ('Caleb Hutchison','caleb@email.com','Senior Quality Engineer','password','2016-10-21');
/*team member role*/
INSERT INTO SeniorDev(dateBecameSenior,email) VALUES ('2016-10-25','alex@email.com');
INSERT INTO JuniorDev(almaMater,email) VALUES ('Arizona State Univesity','caleb@email.com');

/*Team */
INSERT INTO Team(name) VALUES ('Team 1');

/*Team leader */
INSERT INTO hasLeader (dev_email,team_name) VALUES ('alex@email.com','Team 1');

/*Team member */
INSERT INTO composedOf(member_email,team_name) VALUES('caleb@email.com','Team 1');
INSERT INTO composedOf(member_email,team_name) VALUES('alex@email.com','Team 1');

/*Board */
INSERT INTO board(title,description) VALUES ('test board','This board is a test board.');

/*Board team relation */
INSERT INTO runBy(board_title,team_name) VALUES('test board', 'Team 1');

/*Board Category */
INSERT INTO Category(title,description) VALUES ('to do','cards that are not yet started');
INSERT INTO Category(title,description) VALUES ('in work','cards that are in work and not complete');
INSERT INTO Category(title,description) VALUES ('complete','cards that are complete');

/*category board relationship*/
INSERT INTO boardcontains(category_id,board_title) VALUES (21,'test board');
INSERT INTO boardcontains(category_id,board_title) VALUES (22,'test board');
INSERT INTO boardcontains(category_id,board_title) VALUES (23,'test board');

INSERT INTO Card(due_date,priority,description,title) VALUES ('2016-11-10','HIGH','this is a test card','Card 0');
INSERT INTO Card(due_date,priority,description,title) VALUES ('2016-11-09','MED','this is another test card','Card 1');
INSERT INTO Card(due_date,priority,description,title) VALUES ('2016-12-01','LOW','a test card','Card 2');
INSERT INTO Card(due_date,priority,description,title) VALUES ('2016-12-01','LOW','a card that is backlogged','Card 3');

/*add cards to category*/
INSERT INTO categorizedAs(category_id,card_id) VALUES (21,51);
INSERT INTO categorizedAs(category_id,card_id) VALUES (22,52);
INSERT INTO categorizedAs(category_id,card_id) VALUES (22,53);

/*backlog a card*/
INSERT INTO isBackloggedOn(board_title,card_id) VALUES('test board',54)

/*assign cards */
INSERT INTO assignedTo (card_id,member_email) VALUES (51,'caleb@email.com');
INSERT INTO assignedTo (card_id,member_email) VALUES (52,'alex@email.com');
INSERT INTO assignedTo (card_id,member_email) VALUES (53,'caleb@email.com');

/*SELECT STATEMENTS */

/*When a team member logs in, select the boards that they are associated with */
SELECT * FROM Board b,
runBy rb, Team t, composedOf tco, teamMember tm 
WHERE b.title = rb.board_title
AND t.name = rb.team_name
AND tco.team_name = t.name 
AND tco.member_email = tm.email
AND tm.email = 'caleb@email.com';


/*Load categories and cards for the board when that user selects a board to view*/
SELECT * FROM Category AS cat 
JOIN boardContains AS bc ON bc.category_id = cat.id
JOIN Board AS b ON b.title = bc.board_title
JOIN categorizedAs AS ca ON ca.category_id = cat.id
JOIN Card AS card ON card.Id = ca.card_id
WHERE b.title = 'test board';

/* count high priority cards by team member */
SELECT tm.name, count(*) AS numCards 
FROM teamMember AS tm, assignedTo AS ato, card AS c
WHERE tm.email = ato.member_email AND c.id = ato.card_id
AND c.priority = 'HIGH'
GROUP BY tm.name;   

/*count past due cards per team member */
SELECT tm.name, count(*) AS numCards 
FROM teamMember AS tm, assignedTo AS ato, card AS c
WHERE tm.email = ato.member_email AND c.id = ato.card_id
AND c.due_date < NOW()
GROUP BY tm.name; 

/* past due cards in 'to do' category*/
SELECT * FROM Card c, categorizedAs ca, Category cat 
WHERE c.id = ca.card_id 
AND ca.category_id = cat.id
AND c.due_date < NOW()
AND cat.title = 'to do';

/*Cards that are high priority that are backlogged */
SELECT * FROM Card c, isBackloggedOn bl, Board b
WHERE c.id = bl.card_id 
AND b.title = bl.board_title
AND c.priority = 'HIGH';

/* Select team mates who are interns */
SELECT * FROM TeamMember tm, Intern it, Team t, composedOf tco
WHERE tm.email = tco.member_email 
AND tco.team_name = t.name 
AND it.email = tm.email;

/* how many cards are in each category for a board */
SELECT c.id, COUNT(tab1.cardNumber)
FROM(
	SELECT cat.id AS cid, card.id AS cardNumber
	FROM Category cat, Card card, categorizedAs ca
	WHERE cat.id = ca.category_id
	AND card.id = ca.card_id) tab1, 
Category c
WHERE c.id = tab1.cid
GROUP BY c.id'




