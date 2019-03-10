import sys
import argparse
import requests
import json
from .user_info import *
from .user_rating import *
from .contest_list import *
from .problems import *
from .blog import *
from .ratingchange import *
from .bloguser import *
from .userstatus import *
from .conteststatus import *
from .compare import *

def get_req(url):
    return requests.get(url)

def get_parser():
    parser = argparse.ArgumentParser(description="Codeforces CLI")

    # Add parameters
    parser.add_argument('-u','--user', help="Handle of user")
    parser.add_argument('-g','--graph', help="Provides rating chart of user");
    parser.add_argument('-c','--contest',type=int,help="id of contest to display");
    parser.add_argument('--gym', action='store_true', help="Optional argument to list gym contests");
    parser.add_argument('-p','--problem', action='store_true', help="Retrieve all problems");
    parser.add_argument('--tag', help="Tag of problems to retrieve");
    parser.add_argument('-b','--blog',help="View the blog entry specified by id")
    parser.add_argument('-rc', '--ratingchange', help="Get Rating change of contest id")
    parser.add_argument('--handle', help="Specify handle for rating change")
    parser.add_argument('-bu','--bloguser',help="Get blog entries of user")
    parser.add_argument('-us','--userstatus', help="Get submissions of specified user")
    parser.add_argument('--fr', help="1-based index of the first submission to return")
    parser.add_argument('--count', help="Number of returned submissions")
    parser.add_argument('-cs','--cstatus',help="Get contest submissions")
    parser.add_argument('--compare', nargs=2, help="Compare two users. Write handles separated by ;")
    # return parser
    return parser

def main(argv=None):
    
    if argv is None:
        argv = sys.argv

    # Get Arguments
    parser = get_parser()
    args = parser.parse_args(argv[1:])

    user = args.user
    graph = args.graph
    contest = args.contest
    gym = args.gym
    problem = args.problem
    tag = args.tag
    blogid = args.blog
    cid = args.ratingchange
    handle = args.handle
    bloguser_ = args.bloguser
    user_status = args.userstatus
    from_ = args.fr
    count = args.count
    cstatus = args.cstatus
    comp = args.compare
    
    if user:
        res = get_req("http://codeforces.com/api/user.info?handles={0}".format(user))
        user_info(json.loads(res.text))
    elif graph:
        res = get_req("http://codeforces.com/api/user.rating?handle={0}".format(graph))
        user_rating(json.loads(res.text))
    elif contest:
        if gym:
            res = get_req("http://codeforces.com/api/contest.list?gym=true");
        else:
            res = get_req("http://codeforces.com/api/contest.list");
        contest_list(json.loads(res.text), contest)
    elif problem:
        if tag:
            res = get_req("https://codeforces.com/api/problemset.problems?tags={}".format(tag))
        else:
            res = get_req("https://codeforces.com/api/problemset.problems")
        p_main(json.loads(res.text))
    elif blogid:
        res = get_req("https://codeforces.com/api/blogEntry.view?blogEntryId={}".format(blogid))
        comm = get_req("https://codeforces.com/api/blogEntry.comments?blogEntryId={}".format(blogid))
        blog(json.loads(res.text), json.loads(comm.text))
    elif cid:
        res = get_req("https://codeforces.com/api/contest.ratingChanges?contestId={}".format(cid))
        if handle:
            rath(json.loads(res.text), handle)
        else:
            ratc(json.loads(res.text))
    elif bloguser_:
        res = get_req("https://codeforces.com/api/user.blogEntries?handle={}".format(bloguser_))
        bloguser(json.loads(res.text))
    elif user_status:
        if not from_ and not count:
            res = get_req("https://codeforces.com/api/user.status?handle={}".format(user_status))
        else:
            if not from_:
                from_ = 1
            if not count:
                count = 10
            res = get_req("https://codeforces.com/api/user.status?handle={}&from={}&count={}".format(user_status, from_, count))
        userstatus(json.loads(res.text))
    elif cstatus:
        if not from_ and not count:
            if handle:
                res = get_req("https://codeforces.com/api/contest.status?contestId={}&handle={}".format(cstatus, handle))
            else:
                res = get_req("https://codeforces.com/api/contest.status?contestId={}".format(cstatus))
        else:
            if not from_:
                from_ = 1
            if not count:
                count = 10
            if handle:
                res = get_req("https://codeforces.com/api/contest.status?contestId={}&handle={}&from={}&count={}".format(cstatus, handle, from_, count))
            else:
                res = get_req("https://codeforces.com/api/contest.status?contestId={}&from={}&count={}".format(cstatus,from_, count))
        conteststatus(json.loads(res.text))
    elif comp:
        res = get_req("http://codeforces.com/api/user.info?handles={};{}".format(comp[0],comp[1]))
        compare(json.loads(res.text))

if __name__=='__main__':
    sys.exit(main(sys.argv))