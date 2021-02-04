# COBOL / Postgres / Open Enterprise/Government (Rough Draft)

I started thinking about Cobol recently. It's the only C I ever got in a Computer Science class. There are a few things that lead me to that including my experiences with Oracle VS Postgres. and how Every government from the state on down has been ripped off and bullied by Oracle and the consultants that rely on Oracle to make money. This has driven most small governments to migrate to SQLServer on Micro$oft (King County in the early 2000s, Washington county just recently), In my opinion dangerous at best (Wanna Cry).

Recently Amazon demonstrated what most of us have known for decades. Postgresql is an enterprise capable database on par with Oracle, DBII and SQL Server. Once they made it closed source enough to monitize they used their Postgres dirivitive to eliminate their use of Oracle products.

While this puts Amazon in an extremely powerful position on par with Oracle, Microsoft, and IBM in relation to Enterprise and Government organizations it seems more appropriate to take the lessons they present and think seriously about business and government software on securable systems which are not owned by a Monopolistic gang of bullies who are regularly cost taxpayers Billions of dollars while not performing (Oracle VS OHP) or creating serious security concerns (Microsoft).

### Open Source COBOL, Postgresql and Linux 
This is what I want to explore.

#### Creating lxd containers for GNUCobol 2.2
It is my intention to create 2 containers one running Ubuntu-LTS (18.04) and the current LTS like version of Centos (7)

## Ubuntu
GNUCobol claims that Ubuntu 18.04 will install version 2.2 in their documentation however on 18.04 only OPENCobol (1.1) is in the default repos. 2.2 is the default on Ubuntu 19.04 so we can install it using [TaskFastForwardSelectUbuntuPackages this method.]  

## Status 
Currently I am having issues with any of the 3 SQL precompilers to work with GnuCobol and postgres on ubuntu (18.04) or osx (mohave). I should document this rathole.....  
## Linkdumb

* I am not alone :) http://www.simotime.com/sys76p01.htm