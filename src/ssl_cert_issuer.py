import socket
import ssl
import datetime

domains = [
    'aifarms.illinois.edu',
    'ai.ncsa.illinois.edu',
    'caps.ncsa.illinois.edu',
    'digitalag.illinois.edu',
    'ceesd.illinois.edu',
    'digi-mat.ncsa.illinois.edu',
    'delta.ncsa.illinois.edu',
    'gravity.ncsa.illinois.edu',
    'campuscluster.illinois.edu',
    'iri.ncsa.illinois.edu',
    'linuxclustersinstitute.org',
    'reu.ncsa.illinois.edu',
    'ssa.ncsa.illinois.edu',
    'spin.ncsa.illinois.edu',
    'studentcluster.ncsa.illinois.edu',
    ]

for domain in domains:
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                cn = issuer['commonName']
                exp_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                print(f"Domain: {domain}\nSigning Authority: {cn}\nExpiration Date: {exp_date}\n")
    except Exception as e:
        print(f"Error checking {domain}: {e}\n")
