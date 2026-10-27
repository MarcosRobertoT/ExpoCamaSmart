create database if not exists expo;
use expo;

CREATE TABLE if not exists medicoes(
	id int not null auto_increment primary key,
    horario datetime not null,
    batimento int not null,
    respiracao int not null,
    temperatura decimal(4,1) not null,
    origem_dados varchar(20) not null
);