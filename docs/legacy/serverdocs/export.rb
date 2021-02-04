#!/usr/bin/env ruby

# Convert Trac DB Wiki pages to Markdown source files

# This script is based on http://github.com/seven1m/trac_wiki_to_github which
# converted all pages from a Trac DB to GitHub Wiki format (as Textile).
#
#

OUT_PATH = '/var/trac/markdown'

require 'pg'

con = PG.connect :dbname => 'trac_db', :user => 'trac_db_admin', :password => 'trac2016'
pages =  con.exec 'select name, text from wiki w2 where version = (select max(version) from wiki where name = w2.name);'

pages.each do |row|
   title=row['name'].to_s.gsub(/\s/, '')+'.md'
   body=row['text'].to_s
#   print (File.join(OUT_PATH, title))
   File.open(File.join(OUT_PATH, title), 'w') do |file|
    
    body.gsub!(/\{\{\{([^\n]+?)\}\}\}/, '`\1`')
    body.gsub!(/\{\{\{(.+?)\}\}\}/m){|m| m.each_line.map{|x| "\t#{x}".gsub(/[\{\}]{3}/,'')}.join}
    body.gsub!(/\=\=\=\=\s(.+?)\s\=\=\=\=/, '#### \1')
    body.gsub!(/\=\=\=\s(.+?)\s\=\=\=/, '### \1')
    body.gsub!(/\=\=\s(.+?)\s\=\=/, '## \1')
    body.gsub!(/\=\s(.+?)\s\=[\s\n]*/, '# \1')
    body.gsub!(/\[(http[^\s\[\]]+)\s([^\[\]]+)\]/, '[\2](\1)')
    body.gsub!(/\!(([A-Z][a-z0-9]+){2,})/, '\1')
    body.gsub!(/'''(.+)'''/, '*\1*')
    body.gsub!(/''(.+)''/, '_\1_')
    body.gsub!(/^\s\*/, '*')
    body.gsub!(/^\s\d\./, '1.')
    body.gsub!(/\{\{\{([^\n]+?)\}\}\}/, '\n```\1```\n')
#    body.gsub!(/\{\{\{([^\n]+?)\}\}\}/, '`\1`')
    body.gsub!(/'''(.+?)'''/, '**\1**')
    body.gsub!(/''(.+?)''/, '*\1*')
    body.gsub!(/((^\|\|[^\n\r]+\|\|[ \t]*\r?(\n|$))+)/m) do |m|
      m = m.each_line.map do |x|
        x.gsub(/\t/, ' ')
          .gsub(/(\|\|){2,}/){|k| k.gsub(/\|\|/, '||   ')}
        .gsub(/ {3,}/, '   ')
      end.join
      lines = m.each_line.to_a
      line1 = lines.shift
      line2 = line1.dup.gsub(/[^\n\r\|]/, '-')
      lines.unshift(line1, line2)
      c = lines.join
      c = c.each_line.map do |x|
        x.gsub(/\=\s?(.+?)\s?=/, ' \1 ')
          .gsub(/\|\|/, '|')
      end.join
    end
    body.gsub!(/^\{\{\{(.+?)^\}\}\}/m, '```\1```')
    body.gsub!(/\=\=\=\=\s(.+?)\s\=\=\=\=/, '#### \1')
    body.gsub!(/\=\=\=\s(.+?)\s\=\=\=/, '### \1')
    body.gsub!(/\=\=\s(.+?)\s\=\=/, '## \1')
    body.gsub!(/\=\s(.+?)\s\=[\s\n]*/, '# \1')
    body.gsub!(/\[(http[^\s\[\]]+)\s([^\[\]]+)\]/, '[\2](\1)')
    body.gsub!(/\!(([A-Z][a-z0-9]+){2,})/, '\1')
    body.gsub!(/^\s\*/, '*')
    body.gsub!(/^\s\d\./, '1.')
     
    file.write(body)
  end
end
