alter table creator_os.events
    alter column event_id drop identity;

alter table creator_os.events
    alter column event_id type text
    using event_id::text;

grant select, insert, update, delete
on table creator_os.events
to service_role;