-- Entities
create table Board(
  title varchar(50) not null on delete cascade,
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
  id serial on delete cascade,
  title varchar(50),
  description text,
  primary key(id)
);
--
create table Card(
  id serial on delete cascade,
  due_date date,
  priority varchar(5),
  description text,
  title varchar(50),
  primary key(id)
);
--
create table TeamMember(
  name varchar(50),
  email text on delete cascade,
  role varchar(50),
  password text,
  hireDate date,
  primary key(email)
);
--
create table SeniorDev(
  email text not null references TeamMember(email) on delete cascade,
  dateBecameSenior date,
  primary key(email)
);
--
create table Intern(
  email text not null references TeamMember(email),
  school varchar(50),
  primary key(email)
);
--
create table JuniorDev(
  email text not null references TeamMember(email),
  almaMater varchar(50),
  primary key(email)
);

-- Relationships
-- Bridges Board-[]<-Category
create table contains(
  board_title varchar(50) references Board(title),
  category_id serial references Category(id),
  primary key(board_title, category_id)
);
-- Bridges Board->[]<-Card
create table isBackloggedOn(
  board_title varchar(50) references Board(title),
  card_id serial references Card(id),
  primary key(board_title, card_id)
);
-- Bridges Category-[]<-Card
create table categorizedAs(
 category_id serial references Category(id),
 card_id serial references Card(id)
 primary key(category_id, card_id)
);
-- Bridges Board->[]<-Team
create table runBy(
  board_title varchar(50) references Board(title),
  team_name varchar(50) references Team(name)
  primary key(board_title, team_name)
);
-- Bridges Team->[]<-SeniorDev
create table hasLeader(
  team_name varchar(50) references Team(name),
  dev_email text references SeniorDev(email),
  primary key(team_name, dev_email)
);
-- Bridges Team-[]<-TeamMember
create table composedOf(
  team_name varchar(50) references Team(name),
  member_email text references TeamMember(email),
  primary key(team_name, member_email)
);
-- Bridges TeamMember-[]-Card
create table assignedTo(
  member_email text references TeamMember(email),
  card_id serial references Card(id),
  primary key(member_email, card_id)
);
