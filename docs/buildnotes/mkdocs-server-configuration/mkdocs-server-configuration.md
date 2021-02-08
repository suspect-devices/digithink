# Mkdocs Server Configuration.
For the past several years I have been using Trac to maintain server notes and create a todo sort of ticketing system for our systems. Trac is kind of a pain to setup and maintain and though I work well with the wiki (documenting as I go), and the ticketing communicates the work being done, I have not been able to get others to contribute to the documentation. I tried the trac extention to allow markdown to be embedded in the wiki pages but its kind of jenky.

Recently I started documenting my builds and projects in markdown and then storing them along with any configuration files and scripts in Github or Bitbucket repositories.



### Converting Trac Wiki Entries to Markdown
I was able to convert the 50 or so wiki pages on serverdocs and clean them up. 

#### Ruby
I found a [gist (and three refinements)](https://gist.github.com/somebox/619537), which even though I don't ruby well I was able to adapt to pg-ruby. It isnt perfect but it worked.
 
#### Python 
I found this python based script which needs to be adapted for postgres and python 3. It does not handle tables.
[Gist with python script trac2down.py](https://gist.githubusercontent.com/sgk/1286682/raw/b744dd2e47a68d60373ad39df87cfe8256f517af/trac2down.py)


