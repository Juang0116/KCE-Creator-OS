create schema if not exists creator_os;


create table if not exists creator_os.signals (
    signal_id text primary key,
    created_at timestamptz not null default now(),

    brand_id text,
    channel text,
    platform text,

    source text,
    title text,
    url text,

    payload jsonb not null default '{}'::jsonb
);


create table if not exists creator_os.opportunities (
    opportunity_id text primary key,
    created_at timestamptz not null default now(),

    signal_id text,

    brand_id text,
    channel text,
    platform text,

    total_score numeric(5,2),

    recommendation text,

    payload jsonb not null default '{}'::jsonb
);


create table if not exists creator_os.content_ideas (
    idea_id text primary key,
    created_at timestamptz not null default now(),

    opportunity_id text,
    signal_id text,

    brand_id text,
    channel text,
    platform text,

    concept text,

    payload jsonb not null default '{}'::jsonb
);


create table if not exists creator_os.discoveries (
    discovery_id text primary key,
    created_at timestamptz not null default now(),

    idea_id text,
    opportunity_id text,
    signal_id text,
    approval_id text,

    brand_id text,
    channel text,
    platform text,

    status text,

    payload jsonb not null default '{}'::jsonb
);


create table if not exists creator_os.discovery_approvals (
    approval_id text primary key,
    created_at timestamptz not null default now(),

    discovery_id text not null,

    idea_id text,

    status text not null default 'pending',

    decided_by text,
    decided_at timestamptz,

    notes text,

    payload jsonb not null default '{}'::jsonb
);


create table if not exists creator_os.events (
    event_id bigint generated always as identity primary key,
    created_at timestamptz not null default now(),

    event_type text not null,

    entity_type text,
    entity_id text,

    payload jsonb not null default '{}'::jsonb
);


create index if not exists idx_opportunities_signal_id
    on creator_os.opportunities(signal_id);


create index if not exists idx_content_ideas_opportunity_id
    on creator_os.content_ideas(opportunity_id);


create index if not exists idx_discoveries_idea_id
    on creator_os.discoveries(idea_id);


create index if not exists idx_discoveries_opportunity_id
    on creator_os.discoveries(opportunity_id);


create index if not exists idx_discoveries_signal_id
    on creator_os.discoveries(signal_id);


create index if not exists idx_discoveries_approval_id
    on creator_os.discoveries(approval_id);


create index if not exists idx_discoveries_status
    on creator_os.discoveries(status);


create index if not exists idx_discovery_approvals_discovery_id
    on creator_os.discovery_approvals(discovery_id);


create index if not exists idx_discovery_approvals_status
    on creator_os.discovery_approvals(status);


create index if not exists idx_events_entity
    on creator_os.events(entity_type, entity_id);