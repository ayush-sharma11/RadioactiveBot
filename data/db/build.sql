CREATE TABLE IF NOT EXISTS guilds (
    GuildID integer PRIMARY KEY,
    GuildName text DEFAULT "",
    GuildOwnerID integer DEFAULT 0,
    GuildMemberCount integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS exp (
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    UserID integer PRIMARY KEY,
    UserName text DEFAULT "",
    UserServer text DEFAULT ""
);
