-- Entities
create table Board(
  title varchar(50) not null,
  description text,
  primary key(title)
);
--
create table Team(
  name varchar(50) not null,
  primary key(name)
);
--
create table Category(
  id serial,
  title varchar(50),
  description text,
  primary key(id)
);
--
create table Card(
  id serial,
  due_date date,
  priority varchar(5),
  description text,
  title varchar(50),
  primary key(id)
);
--
create table TeamMember(
  name varchar(50),
  email text,
  role varchar(50),
  password text,
  hireDate date,
  primary key(email)
);
--
create table SeniorDev(
  email text,
  dateBecameSenior date,
  primary key(email),
  foreign key (email) references TeamMember (email) on delete cascade
);
--
create table Intern(
  email text,
  school varchar(50),
  primary key(email),
  foreign key (email) references TeamMember (email) on delete cascade
);
--
create table JuniorDev(
  email text,
  almaMater varchar(50),
  primary key(email),
  foreign key (email) references TeamMember (email) on delete cascade
);

-- Relationships
-- Bridges Board-[]<-Category
create table contains(
  board_title varchar(50),
  category_id integer,
  primary key(board_title, category_id),
  foreign key (board_title) references Board (title) on delete cascade,
  foreign key (category_id) references Category (id) on delete cascade
);
-- Bridges Board->[]<-Card
create table isBackloggedOn(
  board_title varchar(50),
  card_id integer,
  primary key(board_title, card_id),
  foreign key (board_title) references Board (title) on delete cascade,
  foreign key (card_id) references Card (id) on delete cascade
);
-- Bridges Category-[]<-Card
create table categorizedAs(
 category_id integer references Category(id),
 card_id integer references Card(id),
 primary key (category_id, card_id),
 foreign key (category_id) references Category(id) on delete cascade,
 foreign key (card_id) references Card(id) on delete cascade
);
-- Bridges Board->[]<-Team
create table runBy(
  board_title varchar(50) references Board(title),
  team_name varchar(50) references Team(name),
  primary key(board_title, team_name),
  foreign key (board_title) references Board(title) on delete cascade,
  foreign key (team_name) references Team(name) on delete cascade
);
-- Bridges Team->[]<-SeniorDev
create table hasLeader(
  team_name varchar(50) references Team(name),
  dev_email text references SeniorDev(email),
  primary key(team_name, dev_email),
  foreign key (team_name) references Team(name) on delete cascade,
  foreign key (dev_email) references SeniorDev(email) on delete cascade
);
-- Bridges Team-[]<-TeamMember
create table composedOf(
  team_name varchar(50) references Team(name),
  member_email text references TeamMember(email),
  primary key(team_name, member_email),
  foreign key (team_name) references Team(name) on delete cascade,
  foreign key (member_email) references TeamMember(email) on delete cascade
);
-- Bridges TeamMember-[]-Card
create table assignedTo(
  member_email text references TeamMember(email),
  card_id integer references Card(id),
  primary key(member_email, card_id),
  foreign key (member_email) references TeamMember(email) on delete cascade,
  foreign key (card_id) references Card(id) on delete cascade
);
