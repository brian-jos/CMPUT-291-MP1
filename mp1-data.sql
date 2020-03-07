-- Data prepapred by Amir Salimi
  
PRAGMA foreign_keys = ON;

insert into users values ('mc@gmail.com','Michael Choi','abcd','Edmonton','M');
insert into users values ('tedwalsh@td.com','Ted Walsh','7632','Calgary','M');
insert into users values ('hm@mah.com','Harry Mah','1453','Waterloo, ON','M');
insert into users values ('ks@gmail.com','Kaitlyn Scott','pqwe','Toronto, ON','F');
insert into users values ('angels@gmail.com','Angel Silverman','anlo','Edmonton','F');
insert into users values ('mk@abc.com','Maximillion Kung','0931','Burnaby, BY','F');
insert into users values ('davood@gmail.com','Davood Rafiei','1234','Edmonton','M');
insert into users values ('amr@yahoo.ca','Amir Salimi','123445','Edmonton','O');
insert into users values ('amrv2@yahoo.ca','Amir Salimi','123445','Edmonton','O');
insert into users values ('chomsky@mit.edu','Noam Chomsky','420420','MIT','N');

insert into products values ('N01', 'Nikon F100');
insert into products values ('N02', 'Nikon D3500');
insert into products values ('B01', 'BMW M8');
insert into products values ('PS01', 'ps4xbox');
insert into products values ('PS02', 'ps4xbox');
insert into products values ('P01', 'Porsche 91');
insert into products values ('P02', 'Porsche 98');
insert into products values ('K01', 'kettle');
insert into products values ('K02', 'kettle2');
insert into products values ('K03', 'kettle sold as item only');


insert into sales values ('S01', 'mc@gmail.com', 'N01',  datetime('now','-365 days'), 'ticket ps4', 'Mint', 1400);
insert into sales values ('S02', 'mc@gmail.com', 'N02',  datetime('now','-730 days'), 'xbox Voucher', 'Used', 698);
insert into sales values ('S03', 'hm@mah.com', 'N02', datetime('now','+3 days'), ' xxboxx x', 'New', 10); -- active
insert into sales values ('S04', 'ks@gmail.com', 'P01', datetime('now','-1 days'), 'tick ps4', 'ticket', 3000);
insert into sales values ('S042', 'ks@gmail.com', 'P01', datetime('now','-1 days'), 'vouch  xBoX', 'ticket', 3000);
insert into sales values ('S041', 'ks@gmail.com', 'P01', datetime('now','+4 days'), 'vouch', 'voucher', 3000);  -- active
insert into sales values ('S05', 'angels@gmail.com', 'N02', datetime('now','+1 minute'), 'ticket', 'very old', 30);  -- active 1 min from database creation
insert into sales values ('S051', 'angels@gmail.com', 'N02', datetime('now','+3 days','-10 minute'), 'ticket', 'very old', 30);  -- active
insert into sales values ('S052', 'angels@gmail.com', 'N02',datetime('now','+3 days','+10 minute'), 'ticket', 'very old', 30);  -- active
insert into sales values ('S06', 'davood@gmail.com', 'B01', datetime('now','+1 days','+6 hour','1 minute'), 'voucher', 'useful voucher', 424); -- active
insert into sales values ('S07', 'davood@gmail.com', 'PS01', datetime('now','+100 days','-6 hour','-10 minute'), 'ps4 xbox', 'old console', 424); -- active
insert into sales values ('S08', 'ks@gmail.com', 'PS01', datetime('now','-100 days'), 'PS4 xbox', 'mint', 10000);
insert into sales values ('S09', 'chomsky@mit.edu', 'K01', datetime('now','+100 days','-1 hour','-11 minute'), 'ok kettle', 'new', 1); -- active
insert into sales values ('S091', 'chomsky@mit.edu', 'K01', datetime('now','+100 days''+2 hour','+41 minute'), 'good kettle', 'new', 2); -- active
insert into sales values ('S092', 'davood@gmail.com', 'N01', datetime('now','+100 days'), 'great camera', 'new', 3); -- active
insert into sales values ('S093', 'davood@gmail.com', 'K02', datetime('now','+300 days'), 'a kettle', 'new', 100); -- active
insert into sales values ('S010', 'amrv2@yahoo.ca', 'PS02', datetime('now','+300 days'), 'lorum ipsum', 'new', 100); -- active


insert into bids values ('B01', 'hm@mah.com', 'S01', '2016-04-01', 1405.02);
insert into bids values ('B02', 'ks@gmail.com', 'S01', '2016-04-02', 1407.99);
insert into bids values ('B03', 'hm@mah.com', 'S02', '2018-09-11', 299);
insert into bids values ('B04', 'davood@gmail.com', 'S02', '2018-09-12', 999);
insert into bids values ('B05', 'angels@gmail.com', 'S03', '2016-01-03', 499);
insert into bids values ('B06', 'tedwalsh@td.com', 'S04', '2019-05-19', 3000);
insert into bids values ('B07', 'ks@gmail.com', 'S04', '2019-05-20', 4000);
insert into bids values ('B08', 'ks@gmail.com', 'S04', '2019-05-21', 100); 
insert into bids values ('B09', 'tedwalsh@td.com', 'S04', '2019-06-22', 101);
insert into bids values ('B091', 'tedwalsh@td.com', 'S042', '2019-06-22', 8001);
insert into bids values ('B101', 'angels@gmail.com', 'S06', '2020-01-0', 421);
insert into bids values ('B102', 'angels@gmail.com', 'S06', '2020-01-07', 422);
insert into bids values ('B103', 'angels@gmail.com', 'S06', '2020-01-07', 424);
insert into bids values ('B11', 'amr@yahoo.ca', 'S07', '2018-09-12', 25);
insert into bids values ('B111', 'amr@yahoo.ca', 'S08', '2018-09-12', 50);

insert into reviews values ('mc@gmail.com', 'tedwalsh@td.com', 3.9, 'great guy!', '2016-05-02');
insert into reviews values ('ks@gmail.com', 'tedwalsh@td.com', 4, 'great guy!', '2016-05-02');
insert into reviews values ('davood@gmail.com', 'tedwalsh@td.com', 4, 'great guy!', '2016-05-02');
insert into reviews values ('mk@abc.com', 'tedwalsh@td.com', 4.1, 'great guy!', '2016-05-02');  
insert into reviews values ('tedwalsh@td.com', 'ks@gmail.com', 4, 'great guy!', '2016-05-02');
insert into reviews values ('mc@gmail.com', 'ks@gmail.com', 4, 'great guy!', '2016-05-02');
insert into reviews values ('angels@gmail.com', 'ks@gmail.com', 4.2, 'great guy!', '2016-05-02'); 
insert into reviews values ('hm@mah.com', 'mc@gmail.com', 5, '', datetime('now','-4 years'));
insert into reviews values ('angels@gmail.com', 'mc@gmail.com', 5, '', datetime('now','-3 years'));
insert into reviews values ('mc@gmail.com', 'davood@gmail.com', 3.9, 'great guy!', '2016-05-02');
insert into reviews values ('hm@mah.com', 'davood@gmail.com', 5, '', datetime('now','-4 years'));
insert into reviews values ('angels@gmail.com', 'davood@gmail.com', 5, '', datetime('now','-3 years'));
insert into reviews values ('tedwalsh@td.com', 'davood@gmail.com', 5, 'great prof!', '2016-05-02');  
insert into reviews values ('mc@gmail.com', 'amr@yahoo.ca', 1, 'bad', '2016-05-02');
insert into reviews values ('hm@mah.com', 'amr@yahoo.ca', 1, 'slow', datetime('now','-4 years'));
insert into reviews values ('angels@gmail.com', 'amr@yahoo.ca', 1, 'tired', datetime('now','-3 years'));
insert into reviews values ('mc@gmail.com', 'amrv2@yahoo.ca', 5, 'bad', '2016-05-02');
insert into reviews values ('hm@mah.com', 'amrv2@yahoo.ca', 5, 'slow', datetime('now','-4 years'));
insert into reviews values ('angels@gmail.com', 'amrv2@yahoo.ca', 5, 'tired', datetime('now','-3 years'));
insert into reviews values ('mc@gmail.com', 'hm@mah.com', 2, 'bad', '2016-05-02');
insert into reviews values ('hm@mah.com', 'hm@mah.com', 2, 'slow', datetime('now','-4 years'));
insert into reviews values ('angels@gmail.com', 'hm@mah.com', 2, 'tired', datetime('now','-3 years'));
insert into reviews values ('tedwalsh@td.com', 'chomsky@mit.edu', 1, '!', '2016-05-02');
insert into reviews values ('angels@gmail.com', 'chomsky@mit.edu', 1, 'ok!', '2016-05-02'); 

insert into previews values (1, 'N01', 'hm@mah.com', 1, 'definitly used',  datetime('now','-6 months'));
insert into previews values (2, 'N01', 'hm@mah.com', 1, 'unused',  datetime('now','-4 months'));
insert into previews values (3, 'N02','ks@gmail.com', 3, 'great quality',  datetime('now','-5 months'));
insert into previews values (4, 'N02','ks@gmail.com', 5, 'great quality',  datetime('now','-5 months'));
insert into previews values (5, 'P02', 'mk@abc.com', 4.1, 'amazing car', datetime('now','-6 months'));
insert into previews values (6, 'P02', 'mk@abc.com', 3.8, 'amazing car', datetime('now','-5 months'));
insert into previews values (61, 'P02', 'mk@abc.com', 4.2, 'amazing car', datetime('now','-5 months'));
insert into previews values (7, 'PS01', 'mk@abc.com', 5, 'a console', datetime('now','-12 months'));
insert into previews values (8, 'PS01', 'mk@abc.com', 5, 'xbox+ps4?', datetime('now','-12 months'));
insert into previews values (9, 'PS01', 'mk@abc.com', 4, '3rd time buying', datetime('now','-1 months'));
insert into previews values (10, 'PS01', 'mk@abc.com',3.9, 'addicted', datetime('now','-1 months'));
insert into previews values (11, 'K01', 'mk@abc.com',5, 'addicted', datetime('now','-1 months'));
insert into previews values (12, 'K01', 'hm@mah.com',5, 'addicted', datetime('now','-2 months'));
insert into previews values (13, 'K01', 'chomsky@mit.edu',5, 'addicted', datetime('now','-3 months'));
