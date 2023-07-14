import ldap3

ldap_server = "ldaps://ldap1.ncsa.illinois.edu"  # Replace with your LDAP server
#ldap_user = "cn=admin,dc=example,dc=com"  # Replace with your LDAP admin user
#ldap_password = "your-password"  # Replace with your LDAP admin user's password
ldap_user = None
ldap_password = None

search_base = 'dc=ncsa,dc=illinois,dc=edu'
search_scope = ldap3.SUBTREE
#attributes = ldap3.ALL_ATTRIBUTES
attributes = ["description", "gidNumber", "businessCategory", "owner", "member"]

group_list = [
    'caiiwp ',
    'grp_aifarms_wp ',
    'grp_caps ',
    'grp_ceesd_wp ',
    'grp_digi_mat ',
    'grp_reu_intl ',
    'grp_web_delta ',
    'grp_web_digitalag ',
    'grp_web_gravity ',
    'grp_web_iccp ',
    'grp_web_lci ',
    'grp_web_reu ',
    'grp_web_ssa ',
]

with ldap3.Connection(ldap_server, ldap_user, ldap_password) as conn:
    if not conn.bind():
        print("Error: Could not bind to LDAP server")
    else:
        for group_name in group_list:
            search_filter = f"(cn={group_name})"
            result = conn.search(search_base, search_filter, search_scope, attributes=attributes)
            if not result:
                print(f"Error: Could not find group {group_name}")
            else:
                entry = conn.entries[0]
                print(f"Group: {group_name}")
                print(f"Description: {entry.description}")
                # print(f"GID number: {entry.gidNumber}")
                # print(f"Business category: {entry.businessCategory}")
                print(f"Owner: {entry.owner}")
                print(f"Members: {entry.member}")
