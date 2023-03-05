create table members (
  member_id serial primary key,
  first_name text,
  last_name text, 
  email text,
  date_of_birth timestamp
);

create table items (
  item_id serial primary key,
  item_name, 
  merchant_id int,
  cost float,
  weight_kg int
);

create table merchants (
  merchant_id serial primary key,
  merchant_name text
);

create table transactions (
  transaction_id serial primary key,
  item_id int,
  total_item_price float,
  total_itme_weight float
);

