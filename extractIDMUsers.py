#!/usr/bin/python

import os
import sys
import getpass
import ipahttp
import warnings


def print_usage():
    print "Usage: ldap_by_users.py <TYPE> --ADMIN,ALL <output-file.txt> "
    print "This script generates a comma delimited file of all LDAP users"
    print "from specified IDM server and related group, sudo, and hbac memberships."
    sys.exit(1)

def print_error():
    print "Error: Incorrect report type specified. Options are"
    print "--ADMIN (all admin users)"
    print "--ALL (all users)"
    sys.exit(1)

try:
    outfile = str(sys.argv[2])
    admin_flg = str(sys.argv[1])
    #print admin_flg
    #if admin_flg != "--ADMIN" or admin_flg != "--ALL":
        #print_error()
except:
    print_usage()



#mute all ldap cert errors - we know host is safe on int network

warnings.filterwarnings("ignore")

#login to ldap server via IPA API

LDAP_UN = getpass.getpass(prompt='Enter Username:')
LDAP_PW = getpass.getpass(prompt='Enter Password:')
#IDM = input("IDM server:")
ipa = ipahttp.ipa('<IPA_SERVER>')
#ipa = ipahttp.ipa(IDM)
ipa.login(LDAP_UN, LDAP_PW)


#print header row
s = ","

file = open(outfile, "w")
line = "uid" + s + "employeenumber" + s + "gecos" + s + "memberof_group" + s + "memberof_sudorule" + s + "memberof_hbacrule" + s + "nsaccountlock" + s + \
    "memberofindirect_sudorule" + s + "memberofindirect_hbacrule" + s + "memberof_role" + s + "memberofindirect_role"
file.write(line + "\n")



userids = ipa.user_find()
#put all userids into list
for u in userids['result']['result']:
    #get info from user_show for each userid in list
    userinfo = (ipa.user_show(u['uid'][0]))

    #todo: optimize this/remove redundancy

    try:
        uid = str(userinfo['result']['result']['uid'][0])
    except:
        uid = "none"
    try:
        dn = str(userinfo['result']['result']['gecos'][0])
    except:
        dn = "none"
    try:
        group = ""
        for v in userinfo['result']['result']['memberof_group']:
            group = group + " " + v
        group1 = str(group)
    except:
        group1 = "none"
    try:
        sudo = ""
        for s in userinfo['result']['result']['memberof_sudorule']:
            sudo = sudo + " " + s
        sudo1 = str(sudo)
    except:
        sudo1 = "none"
    try:
        hbac = ""
        for h in userinfo['result']['result']['memberof_hbacrule']:
            hbac = hbac + " " + h
        hbac1 = str(hbac)
    except:
        hbac1 = "none"
    try:
        accountlock = str(userinfo['result']['result']['nsaccountlock'])
    except:
        accountlock = "none"
    try:
        indsudo = ""
        for ind in userinfo['result']['result']['memberofindirect_sudorule']:
            indsudo = indsudo + " " + ind
        indsudo1 = str(indsudo)
    except:
        indsudo1 = "none"
    try:
        indhbac = ""
        for indh in userinfo['result']['result']['memberofindirect_hbacrule']:
            indhbac = indhbac + " " + indh
        indhbac1 = str(indhbac)
    except:
        indhbac1 = "none"
    try:
        dirrole = ""
        for drr in userinfo['result']['result']['memberof_role']:
            dirrole = dirrole + " " + drr
        dirrole1 = str(dirrole)
    except:
        dirrole1 = "none"
    try:
        indirrole = ""
        for idrr in userinfo['result']['result']['memberofindirect_role']:
            indirrole = indirrole + " " + idrr
        indirrole1 = str(indirrole)
    except:
        indirrole1 = "none"
    try:
        emplid = ""
        for em in userinfo['result']['result']['employeenumber']:
            emplid = emplid + " " + em
        emplid1 = str(emplid)
        emplid1 = emplid1.replace('"', '') 
    except:
        emplid1 = "none"

    if admin_flg == "--ALL":
        eachline = ""
        eachline = (uid + "," + emplid1 + "," + dn + "," + group1 + "," + sudo1 + "," + hbac1 + "," + accountlock + "," + indsudo1 + "," + indhbac1 + "," + dirrole1 + "," + indirrole1)
        file.write(eachline + "\n")
    if admin_flg == "--ADMIN":
        if sudo1 != "none" or indsudo1 != "none":
            #if sudo1 != "none" or indsudo1 != "none":
            #print uid,sudo1,indsudo1 
            eachline1 = ""
            eachline1 = (uid + "," + emplid1 + "," + dn + "," + group1 + "," + sudo1 + "," + hbac1 + "," + accountlock + "," + indsudo1 + "," + indhbac1 + "," + dirrole1 + "," + indirrole1)
            file.write(eachline1 + "\n")   
    else:
        continue
file.close()