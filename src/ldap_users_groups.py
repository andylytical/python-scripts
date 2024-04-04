import ldap3
import pprint

ldap_server = "ldaps://ldap1.ncsa.illinois.edu"  # Replace with your LDAP server
# ldap_user = "cn=admin,dc=example,dc=com"  # Replace with your LDAP admin user
# ldap_password = "your-password"  # Replace with your LDAP admin user's password
ldap_user = None
ldap_password = None

search_base = 'ou=People,dc=ncsa,dc=illinois,dc=edu'
search_scope = ldap3.SUBTREE
attributes = ldap3.ALL_ATTRIBUTES
# attributes = ["description", "gidNumber", "businessCategory", "owner", "member"]

users_fn = 'jira_ldap_users.txt'
# users_fn = 'jira_ldap_users.test'


def read_user_list(file_path):
    with open(file_path, 'r') as file:
        return [ line.strip() for line in file ]


def get_user_groups( conn, username ):
    search_filter = f'(uid={username})'
    conn.search(search_base, search_filter, attributes=['memberOf'])
    # pprint.pprint( conn.entries )
    raw_glist = conn.entries[0].memberOf
    # pprint.pprint( raw_glist )
    for line in raw_glist:
        # pprint.pprint( line )
        gname = line.split(',')[0].split('=')[1]
        print( f'{username},{gname}' )


if __name__ == '__main__':

    users = read_user_list( users_fn )

    with ldap3.Connection(ldap_server, ldap_user, ldap_password) as conn:
        if not conn.bind():
            raise UserWarning ("Error: Could not bind to LDAP server")
        for user in users:
            # print( f'Looking up user {user}' )
            get_user_groups( conn, user )
