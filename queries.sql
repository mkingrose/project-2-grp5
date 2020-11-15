create table merged_data (
	country_code varchar not null,
	country varchar not null,
	year varchar not null,
	start_date date not null,
	event_name varchar not null,
	hazard_category varchar not null,
	hazard_type varchar not null,
	new_displacement varchar not null,
	country_2D varchar not null,
	continent varchar not null,
	population varchar not null
);
select * from merged_data