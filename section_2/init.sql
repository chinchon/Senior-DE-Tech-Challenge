create table members (
  member_id text primary key,
  first_name text,
  last_name text, 
  email text,
  date_of_birth text
);

create table items (
  item_id serial primary key,
  item_name text, 
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

-- TODO implement a for loop to load data recursively
copy public.members from '/app/data/successful/applications_dataset_1.csv' delimiter ',' csv header;
copy public.members from '/app/data/successful/applications_dataset_2.csv' delimiter ',' csv header;
