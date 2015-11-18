drop table if exists users;

create table users (
    id integer primary key autoincrement,
    username text not null collate nocase unique,
    password text not null,
    salt text not null
);

drop table if exists tasks;

create table tasks (
  id integer primary key autoincrement,
  user_id integer not null,
  parent_id integer,
  title text not null,
  points integer,
  status integer,
  idx integer,
  foreign key(user_id) references users(id),
  foreign key(parent_id) references tasks(id)
);

create index user_tasks_idx on tasks(user_id);

create index user_parent_tasks_idx on tasks(user_id, parent_id);