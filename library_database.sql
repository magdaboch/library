create view v_library_client as
select
    client_id,
       first_name,
       last_name
from library_client
left outer join first_name fn
    on library_client.lc_first_name_id = fn.fn_id
left outer join last_name ln
    on library_client.lc_last_name_id = ln.ln_id;

select * from v_library_client;

create view v_author as
select
    author_id,
       first_name,
       last_name
FROM author
left outer join first_name fn
    on author.author_first_name_id = fn.fn_id
left outer join last_name ln
    on author.author_last_name_id = ln.ln_id;

select * from v_author;

create function f_add_first_name(firstName varchar(20) character set utf8 COLLATE utf8_polish_ci)
returns int
    begin
        if (select fn_id from first_name WHERE lower(first_name) = lower(firstName)) is NULL
            THEN
                insert into first_name(first_name) values (firstName);
        end if;

        return (select fn_id from first_name where lower(first_name) = lower(firstName));
    end;

create function f_add_last_name(lastName varchar(50) character set utf8 COLLATE utf8_polish_ci)
returns int
    begin
        if (select ln_id from last_name where lower(last_name) = lower(lastName)) is NULL
            THEN
                insert into last_name(last_name) values (lastName);
        end if;

        return (select ln_id from last_name where lower(last_name) = lower(lastName));
    end;

insert into library_client(lc_first_name_id, lc_last_name_id)
values (f_add_first_name('Wania'), f_add_last_name('Jakaśtam'));

select * from v_library_client;

create trigger trg_rent_a_book
    after insert on rent_book
    for each row
begin
    update book_copy set book_copy_available = 0 where book_copy_id = NEW.rb_book_copy_id;
end;

drop trigger if exists trg_return_book;

create trigger trg_return_book
    after update on rent_book
    for each row
begin
    if (
        (select book_copy_available FROM book_copy WHERE book_copy_id = NEW.rb_book_copy_id) = 0
        and OLD.rb_return_date is null
        and NEW.rb_return_date is not null
        ) then
        update book_copy set book_copy_available = 1 where book_copy_id = NEW.rb_book_copy_id;
    end if;
end;

drop trigger if exists trg_return_date_hodor;
create trigger trg_return_date_hodor
    before update
    on rent_book
    for each row
begin
    if (NEW.rb_return_date <= OLD.rb_date) THEN
        SIGNAL SQLSTATE '45000' SET
        MYSQL_ERRNO = 37455,
        MESSAGE_TEXT = 'Error: Nie można oddać książki przed datą wypożyczenia';
    end if;

    if (NEW.rb_return_date > NOW()) THEN
        SIGNAL SQLSTATE '45000' SET
        MYSQL_ERRNO = 37465,
        MESSAGE_TEXT = 'Error: Nie można oddać daty z późneszą datą';
    end if;
end;

create trigger v_rent_book_status_replecment
    AFTER Update
    on book_copy
    for each row
begin
    if( old.book_copy_available = 0 and new.book_copy_available = 1)
    then
        update rent_book set rb_return_date = now()
        where rb_book_copy_id = OLD.bc_book_id
        and rb_return_date is null;
     end if;
end;