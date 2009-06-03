Getting HBase running OS X in n steps.
======================================

The goal is to get [HBase](http://hadoop.apache.org/hbase/) running on OS X
10.5. The installation will done on a single machine in a so-called
pseudo-distruted operation, as opposed to a standalone operation or a
fully-distributed operation.

HBase depends on
[Hadoop](http://hadoop.apache.org/), so we'll have that installed too when we're
done.

We will be using known-to-be-stable versions of both Hadoop and HBase (i.e.
0.19.1 and 0.19.3 respectively, which was current as of June 2 2009). You can
try your hand at [trunk](http://github.com/apache/hadoop/tree/trunk) if you are
feeling risky.

I prefer to run services as separate users, so I sudo up to the hadoop user.
Your taste and mileage may vary.

<pre>
$> sudo -u hadoop -i
</pre>

Pre-requisites
--------------

Is there anything we need to prepare before we can install HBase? Well, yes:
Hadoop. Also, we need a functioning Java 1.6.

### Java

I see this:

<pre>
$> java -version
java version "1.5.0_16"
Java(TM) 2 Runtime Environment, Standard Edition (build 1.5.0_16-b06-284)
Java HotSpot(TM) Client VM (build 1.5.0_16-133, mixed mode, sharing)
</pre>

Not good enough, but simple to fix [if your OS X is
updated](http://support.apple.com/downloads/Java_for_Mac_OS_X_10_5_Update_2):

<pre>
$> sudo ln -svf /System/Library/Frameworks/JavaVM.framework/Versions/1.6/Commands/java{,c} /usr/bin
</pre>

Much better:
<pre>
$> java -version
java version "1.6.0_07"
Java(TM) SE Runtime Environment (build 1.6.0_07-b06-153)
Java HotSpot(TM) 64-Bit Server VM (build 1.6.0_07-b06-57, mixed mode)
</pre>

Also, let's set the environmental variable $JAVA_HOME while we're at it:
<pre>
$> echo 'export JAVA_HOME="/System/Library/Frameworks/JavaVM.framework/Versions/1.6.0/Home"' >> ~/.bashrc
$> source ~/.bashrc
</pre>


### Hadoop

The reason that we need Hadoop (and specifically Hadoop's filesystem, HDFS) is
that HBase stores all data on HDFS.


Download hadoop-0.19.1.tar.gz from
[http://www.apache.org/dyn/closer.cgi/hadoop/core/](a mirror). Unpack.

<pre>
$> tar zxvf hadoop-0.19.1.tar.gz
$> cd hadoop-0.19.1
</pre>

In **conf/hadoop-env.sh**, set JAVA_HOME:
<pre>
export JAVA_HOME="/System/Library/Frameworks/JavaVM.framework/Versions/1.6.0/Home"
</pre>

In **conf/hadoop-site.xml**, set the properties *fs.default.name*, *dfs.replication*
and *mapred.job.tracker* like so:
<pre>
&lt;configuration&gt;
 &lt;property&gt;
   &lt;name&gt;fs.default.name&lt;/name&gt;
   &lt;value&gt;hdfs://localhost:9000&lt;/value&gt;
 &lt;/property&gt;

 &lt;property&gt;
   &lt;name&gt;mapred.job.tracker&lt;/name&gt;
   &lt;value&gt;localhost:9001&lt;/value&gt;
 &lt;/property&gt;

 &lt;property&gt;
   &lt;name&gt;dfs.replication&lt;/name&gt;
   &lt;value&gt;1&lt;/value&gt;
 &lt;/property&gt;
&lt;/configuration&gt;
</pre>

Here we're telling Hadoop where it will find the HDFS namenode and the
JobTracker (port 9000 and 9001 respectively, both on localhost). Also, we set
data replication to 1. Anything else would be ludicrous since we have only a
single node.

Also, keep the environment up to date:
<pre>
$> echo export HADOOP_HOME="'`pwd`'" >> ~/.bashrc
$> echo alias hadoop="$HADOOP_HOME/bin/hadoop" >> ~/.bashrc
$> echo alias dfs="hadoop dfs" >> ~/.bashrc
$> source ~/.bashrc
</pre>

Hadoop needs ssh access to perform its duties. Start sshd by enabling 'remote
login' in the System preferences, then generate a pair of passwordless ssh keys
like so:
<pre>
$> ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa-hadoop
$> cat ~/.ssh/id_dsa-hadoop.pub >> ~/.ssh/authorized_keys
$> ssh-add ~/.ssh/id_dsa-hadoop
# verify.
$> ssh localhost echo ok.
</pre>

(Optional) I like to compile Hadoop to make sure all jars are fresh and what not:
<pre>
$> ant package
</pre>

Format the namenode (careful now!):
<pre>
$> hadoop namenode -format
</pre>

Start Hadoop:
<pre>
$> $HADOOP_HOME/bin/start-all.sh 
</pre>

This should start the namenode and the jobtracker together with the datanode,
secondarynamenode and tasktracker. We only really need the namenode and datanode
(i.e. the HDFS), but we might as well get it all rolling while we're at it.

Verify that the DFS is up by creating a directory and listing the root:
<pre>
$> hadoop dfs -mkdir /user/hadoop
$> hadoop dfs -ls /
</pre>

Also, check the webberfaces for the [namenode](http://localhost:50070/) and
[tasktracker](http://localhost:50030/). Good?

Does something seem to be wack? Check the logs in **$HADOOP_HOME/logs**!


HBase
-----


Download hbase-0.19.3.tar.gz from
[http://www.apache.org/dyn/closer.cgi/hadoop/hbase/](a mirror). Unpack.

<pre>
$> tar zxvf hbase-0.19.3.tar.gz
$> cd hbase-0.19.3
</pre>

In **conf/hbase-env.sh**, set JAVA_HOME:
<pre>
export JAVA_HOME="/System/Library/Frameworks/JavaVM.framework/Versions/1.6.0/Home"
</pre>

In **conf/hbase-site, set *hbase.rootdir* to point to /hbase on HDFS:
<pre>
&lt;configuration&gt;
 &lt;property&gt;
   &lt;name&gt;hbase.rootdir&lt;/name&gt;
   &lt;value&gt;hdfs://localhost:9000/hbase&lt;/value&gt;
 &lt;/property&gt;
&lt;/configuration&gt;
</pre>

Note that we are setting up HBase on a single machine in what is known as a
pseudo-distributed operation. This means that the master and the (only)
regionserver are both running as a single process on localhost, a scenario which
is covered by the defaults (see *hbase.master* in **conf/hbase-default.xml**).

If you were to run a fully-distributed operation, you would need to define
hbase.master, etc. Please refer to [the
documention](http://hadoop.apache.org/hbase/docs/current/api/overview-summary.html#overview_description)
on how to do that.


Keep the environment updated:
<pre>
$> export HBASE_HOME="`pwd`"
$> echo export HBASE_HOME=$HBASE_HOME >> ~/.bashrc
$> echo alias hbase='"$HBASE_HOME/bin/hbase"' >> ~/.bashrc
$> source ~/.bashrc
</pre>

Start HBase:
<pre>
$> ${HBASE_HOME}/bin/start-hbase.sh
</pre>

This should have started a master and a regionserver.

Check the logs for lines like these:
<pre>
INFO org.apache.hadoop.hbase.master.HMaster: HMaster initialized on 127.0.0.1:60000
[..]
INFO org.apache.hadoop.hbase.regionserver.HRegionServer: HRegionServer started at: 127.0.0.1:52765
</pre>

Verify that things are OK by opening the shell and listing (the non-existant)
tables:

<pre>
$> hbase shell
hbase(main):001:0> list
0 row(s) in 0.2415 seconds
</pre>

Congratulations! You are running HBase on your local machine. What a joy.

Let us leave any actual usage for another day. Meanwhile, bask in your glory and
dream of what data you will want to store on your fresh HBase installation.
