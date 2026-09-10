grant usage on schema creator_os to service_role;

grant select, insert, update, delete
on table
    creator_os.signals,
    creator_os.opportunities,
    creator_os.content_ideas,
    creator_os.discoveries,
    creator_os.discovery_approvals
to service_role;