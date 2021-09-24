drop table if exists entries;
create table entries (id integer primary key autoincrement,title varchar(10) not null,text varchar(10) not null);
insert into entries(id,title,text) values(1,"2","3");