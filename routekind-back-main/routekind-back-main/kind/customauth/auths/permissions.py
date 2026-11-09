
# USERS
CREATE_USERS_PERM = 'create.users'
UPDATE_USERS_PERM = 'update.users'
DELETE_USERS_PERM = 'delete.users'
LIST_USERS_PERM = 'list.users'
# SET_USERS_STATUS_PERM = 'set_status.users'
READ_OWN_USER_PERM = 'read_own.users'
UPDATE_OWN_USER_PERM = 'update_own.users'
DELETE_OWN_USER_PERM = 'update_own.users'


BASE_PERMISSIONS = (
    # USERS
    CREATE_USERS_PERM,
    UPDATE_USERS_PERM,
    DELETE_USERS_PERM,
    LIST_USERS_PERM,
    DELETE_OWN_USER_PERM,
    # SET_USERS_STATUS_PERM,
    READ_OWN_USER_PERM,
    UPDATE_OWN_USER_PERM,
    # ROLES
    "create.roles",
    "update.roles",
    "delete.roles",
    "list.roles",
    "read_own.roles",
    # PERMISSIONS
    "list.permissions",
    "read_own.permissions",
    # TOKEN
    "create.tokens",
    "delete.tokens",
    "list.tokens",
    "read_own.tokens",
)


