#!/usr/bin/env python2.7

from subprocess import check_output, CalledProcessError
from sys import argv, exit
from argparse import ArgumentParser
from io import open
import json
import os.path


def get_memberlist(serf_path):
    """ Get a list of serf members. """
    try:
        if os.path.isfile(serf_path):
            output = check_output([serf_path, "members"]).split("\n")[:-1]
        else:
            print("Couldn't find {}".format(serf_path))
            exit(1)
    except (CalledProcessError, OSError) as e:
        print("Failed to get member list: {}".format(repr(e)))
        exit(1)

    return output


def parse_memberlist(memberlist):
    """ 
    Parse the list of serf members by turning it into a dict.
    See ansibles docs for developing dynamic inventory sources for more details.
    """
    parsed = {"_meta": {"hostvars": {}}}
    alive = list()
    left = list()
    failed = list()
    for member in memberlist:
        member = member.split()
        tags = member[3].split(",")
        tagsdict = dict()
        for tag in tags:
            tag_split = tag.split("=")
            tagsdict.update(dict({tag_split[0] : tag_split[1]}))
            if not parsed.has_key("tag_{}_{}_{}".format(
                tag_split[0], tag_split[1], member[2])):
                parsed.update(
                    dict(
                        {
                            "tag_{}_{}_{}".\
                            format(
                                tag_split[0], tag_split[1], member[2]) : list()}))
            parsed[
                    "tag_{}_{}_{}".\
                    format(tag_split[0], tag_split[1], member[2])
                ].\
                append(
                    {"ip": member[1].split(":")[0], "name": member[0]})

        if member[2] == "alive":
            alive.append({"ip": member[1].split(":")[0], "name": member[0], "tags": tagsdict})
        elif member[2] == "left":
            left.append({"ip": member[1].split(":")[0], "name": member[0], "tags": tagsdict})
        else:
            failed.append({"ip": member[1].split(":")[0], "name": member[0], "tags": tagsdict})

        parsed["_meta"]["hostvars"].update(
            dict(
                {
                    member[1].split(":")[0] : 
                    dict(
                        {
                            "name": member[0],
                            "ip": member[1].split(":")[0],
                            "port": member[1].split(":")[1],
                            "state": member[2],
                            "tags": tagsdict})}))

    parsed.update(dict({"alive": alive}))
    parsed.update(dict({"left": left}))
    parsed.update(dict({"failed": failed}))
    return parsed


if __name__ == "__main__":
    # Parse cmdline arguments.
    parser = ArgumentParser(description="Dump serf memberlist in JSON")
    parser.add_argument(
        "-s", dest="serf_path", default="serf",
        help = "If serf is not on your path, provide the full path to it here")
#    parser.add_argument("output", metavar="OUT", type=str,
#        help = "The path to a file to write the JSON formatted list to")

    args = parser.parse_args()

    # Get a list of members and parse it.
    memberlist = parse_memberlist(get_memberlist(args.serf_path))

    print(
        json.dumps(
            memberlist, ensure_ascii = False, indent = 2, sort_keys = True))
