-- Entities
CREATE TABLE Board(
  title VARCHAR(50) NOT NULL,
  description TEXT,
  PRIMARY KEY(title)
);
--
CREATE TABLE Team(
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(name)
);
--
CREATE TABLE Category(
  id SERIAL,
  title VARCHAR(50),
  description TEXT,
  PRIMARY KEY(id)
);
--
CREATE TABLE Card(
  id SERIAL,
  due_date DATE,
  priority VARCHAR(5),
  description TEXT,
  title VARCHAR(50),
  PRIMARY KEY(id)
);
--
CREATE TABLE TeamMember(
  name VARCHAR(50),
  email TEXT,
  role VARCHAR(50),
  password TEXT,
  hireDate DATE,
  PRIMARY KEY(email)
);
--
CREATE TABLE SeniorDev(
  email TEXT,
  dateBecameSenior DATE check(dateBecameSenior < now()),
  PRIMARY KEY(email),
  FOREIGN KEY (email) REFERENCES TeamMember (email) ON DELETE CASCADE
);
--
CREATE TABLE Intern(
  email TEXT,
  school VARCHAR(50),
  PRIMARY KEY(email),
  FOREIGN KEY (email) REFERENCES TeamMember (email) ON DELETE CASCADE
);
--
CREATE TABLE JuniorDev(
  email TEXT,
  almaMater VARCHAR(50),
  PRIMARY KEY(email),
  FOREIGN KEY (email) REFERENCES TeamMember (email) ON DELETE CASCADE
);

-- Relationships
-- Bridges Board-[]<-Category
CREATE TABLE boardContains(
  board_title VARCHAR(50),
  category_id INTEGER,
  PRIMARY KEY(board_title, category_id),
  FOREIGN KEY (board_title) REFERENCES Board (title) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES Category (id) ON DELETE CASCADE
);
-- Bridges Board->[]<-Card
CREATE TABLE isBackloggedOn(
  board_title VARCHAR(50),
  card_id INTEGER,
  PRIMARY KEY(board_title, card_id),
  FOREIGN KEY (board_title) REFERENCES Board (title) ON DELETE CASCADE,
  FOREIGN KEY (card_id) REFERENCES Card (id) ON DELETE CASCADE
);
-- Bridges Category-[]<-Card
CREATE TABLE categorizedAs(
 category_id INTEGER REFERENCES Category(id),
 card_id INTEGER REFERENCES Card(id),
 PRIMARY KEY (category_id, card_id),
 FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE,
 FOREIGN KEY (card_id) REFERENCES Card(id) ON DELETE CASCADE
);
-- Bridges Board->[]<-Team
CREATE TABLE runBy(
  board_title VARCHAR(50) REFERENCES Board(title),
  team_name VARCHAR(50) REFERENCES Team(name),
  PRIMARY KEY(board_title, team_name),
  FOREIGN KEY (board_title) REFERENCES Board(title) ON DELETE CASCADE,
  FOREIGN KEY (team_name) REFERENCES Team(name) ON DELETE CASCADE
);
-- Bridges Team->[]<-SeniorDev
CREATE TABLE hasLeader(
  team_name VARCHAR(50) REFERENCES Team(name),
  dev_email TEXT REFERENCES SeniorDev(email),
  PRIMARY KEY(team_name, dev_email),
  FOREIGN KEY (team_name) REFERENCES Team(name) ON DELETE CASCADE,
  FOREIGN KEY (dev_email) REFERENCES SeniorDev(email) ON DELETE CASCADE
);
-- Bridges Team-[]<-TeamMember
CREATE TABLE composedOf(
  team_name VARCHAR(50) REFERENCES Team(name),
  member_email TEXT REFERENCES TeamMember(email),
  PRIMARY KEY(team_name, member_email),
  FOREIGN KEY (team_name) REFERENCES Team(name) ON DELETE CASCADE,
  FOREIGN KEY (member_email) REFERENCES TeamMember(email) ON DELETE CASCADE
);
-- Bridges TeamMember-[]-Card
CREATE TABLE assignedTo(
  member_email TEXT REFERENCES TeamMember(email),
  card_id INTEGER REFERENCES Card(id),
  PRIMARY KEY(member_email, card_id),
  FOREIGN KEY (member_email) REFERENCES TeamMember(email) ON DELETE CASCADE,
  FOREIGN KEY (card_id) REFERENCES Card(id) ON DELETE CASCADE
);
