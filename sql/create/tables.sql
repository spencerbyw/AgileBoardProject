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
  email text not null references TeamMember(email),
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

);
-- Bridges Board->[]<-Card
create table isBackloggedOn(

);
-- Bridges Category-[]<-Card
create table categorizedAs(

);
-- Bridges Board->[]<-Team
create table runBy(

);
-- Bridges Team->[]<-SeniorDev
create table hasLeader(

);
-- Bridges Team-[]<-TeamMember
create table composedOf(

);
-- Bridges TeamMember-[]-Card
create table assignedTo(

);
