## $Id$
## CDSware Search Interface.

## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

## read config variables:
#include "config.wml"
#include "configbis.wml"

## start Python:
<protect>## $Id$
<protect>## DO NOT EDIT THIS FILE! IT WAS AUTOMATICALLY GENERATED FROM CDSware WML SOURCES.</protect>

## fill config variables:
pylibdir = "<LIBDIR>/python"

import sys
sys.path.append('%s' % pylibdir)
from cdsware.config import *
from cdsware.dbquery import run_sql
from cdsware.webpage import page, create_error_box
from cdsware.webuser import getUid

def get_collid(c):
    "Return collection ID for given collection name.  Return None if no match found."
    collid = None
    res = run_sql("SELECT id FROM collection WHERE name=%s", (c,), 1)
    if res:
        collid = res[0][0]
    return collid 

def index(req, c=cdsname, as="0", verbose="1"):
    "Display search interface page for collection c by looking in the collection cache."
    uid = getUid(req)
    try:
        as = int(as)
    except:
        as = 0
    try:
        verbose = int(verbose)
    except:
        verbose = 1
    if type(c) is list:
        c = c[0]
    req.content_type = "text/html"
    req.send_http_header()
    # deduce collection id:
    collid = get_collid(c)
    if type(collid) is not int:
         return page(title="Not found: %s" % c,
                     body="""<p>Sorry, collection <strong>%s</strong> does not seem to exist.
                             <p>You may want to start browsing from <a href="%s">%s</a>.""" % (c, weburl, cdsname),
                     description="CERN Document Server - Not found: %s " % c,
                     keywords="CDS, CDSware",
                     uid=uid)
    # display collection interface page:
    try:
        fp = open("%s/collections/%d/navtrail-as=%d.html" % (cachedir, collid, as), "r")
        c_navtrail = fp.read()
        fp.close()
        fp = open("%s/collections/%d/body-as=%d.html" % (cachedir, collid, as), "r")
        c_body = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-lt.html" % (cachedir, collid), "r")
        c_portalbox_lt = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-lb.html" % (cachedir, collid), "r")
        c_portalbox_lb = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-rt.html" % (cachedir, collid), "r")
        c_portalbox_rt = fp.read()
        fp.close()
        fp = open("%s/collections/%d/portalbox-rb.html" % (cachedir, collid), "r")
        c_portalbox_rb = fp.read()
        fp.close()
        return page(title=c,
                    body=c_body,
                    navtrail=c_navtrail,
                    description="CERN Document Server - %s" % c,
                    keywords="CDS, CDSware, %s" % c,
                    uid=uid,
                    cdspagerightstripeadd=c_portalbox_rt)
    except:        
        if verbose >= 9:
            req.write("<br>c=%s" % c)
            req.write("<br>as=%s" % as)        
            req.write("<br>collid=%s" % collid)
            req.write("<br>uid=%s" % uid)
        return page(title="Internal Error",
                    body = create_error_box(req) + 
                           """<p>You may want to start browsing from <a href="%s">%s</a>.""" % \
                           (weburl, cdsname),
                    description="CERN Document Server - Internal Error", 
                    keywords="CDS, CDSware, Internal Error",
                    uid=uid)
         
    return "\n"    
