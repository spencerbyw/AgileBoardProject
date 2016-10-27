-- Entities
create table Board(

);
--
create table Team(

);
--
create table Category(

);
--
create table Card(

);
--
create table TeamMember(

);
--
create table SeniorDev(

);
--
create table Intern(

);
--
create table JuniorDev(

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
