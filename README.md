# Description

An example on how to use [CFEngine3]() with [Serf]() to provide orchestration
for CFE3 nodes. Furthermore it provides a CFE3 update policy to pull CFE3
related files from any source other than a CFE3 policy hub. As an example for
this a `masterfiles/tools/update_masterfiles.sh` script is provided that syncs
files from AWS S3.

# Requirements

* Virtualbox
* Vagrant
* AWS Account (optional)
* AWS CLI (optional)
* AWS S3 Bucket (optional)

The AWS related requirements are optional depending on your way of retrieving
CFE3 files.

# Virtual Machines

The `Vagrantfile` defines three virtual machines, using a private network:

* a `loadbalancer`, using nginx, and
* two application servers `app1` and `app2` that host a simple web application,
  which just shows that system IPv4 address.

The web application can be reached via the loadbalancer's url: `http://172.28.128.4/myapp`
And if vagrant didn't create the appropriate routes on your system, to reach
the VMs in their private network, you can also use: `http://localhost:8080/myapp`.

With this app you can check that the loadbalancer changes its configuration
when he sees a new application server or when one goes down. This can be
verified by reloading the page. After you start/stop an application server.

**Note that the example doesn't use serf's event triggers, this means for
changes to take affect you either have to wait until the next scheduled CFE3 run
on the loadbalancer or run CFE3 manually on it. After you started/stopped a
application server.**

# Getting started

First we clone the repository:

```
git clone <url>
cd cfe3-serf-example
```

Then we download the serf binary:

```
cd cfe3-files
./download-serf.sh
```

To ease the interaction with vagrant and syncing files to AWS S3 we create a
environment variables file with our AWS access and secret key and source it:

```
# env_vars 
export AWS_ACCESS_KEY_ID="CHANGEME"
export AWS_SECRET_ACCESS_KEY="CHANGEME"

===

source env_vars
```

Before we upload the CFE3 files to AWS S3 we need to specify the bucket name
in `masterfiles/controls/update_def.cf`, which contains a variable named
`masterfiles_update_script_args`. The value must be set to the name of the
bucket where the files should be uploaded to.

Now we can synchronize the CFE3 files to AWS S3 Bucket:

```
cd cfe3-files
./sync_to_s3.sh MYBUCKET
```

After that we are ready to launch the VMs (defined in the Vagrantfile):

```
vagrant up loadbalancer --provision
vagrant up app1 --provision
vagrant up app2 --provision
```

Note that currently we don't use serf's event triggers, thus you might want to
run `cf-agent -KI -D DEBUG` manually on the loadbalancer in order to pick up
changes quicker, instead of waiting for the next scheduled run.
