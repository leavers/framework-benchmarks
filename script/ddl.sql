create table test.sc_student
(
	_id bigint generated always as identity
		constraint sc_student_pk
			primary key,
	student_id varchar(32) not null,
	student_name varchar(32) not null,
	student_gender varchar(1),
	student_birthday date
);

alter table test.sc_student owner to postgres;

create unique index sc_student_student_id_uindex
	on test.sc_student (student_id);