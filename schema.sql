create table if not exists meal_entries (
  id integer primary key autoincrement,
  title text not null,
  'description' text not null,
  'active' bool not null default 1
);
