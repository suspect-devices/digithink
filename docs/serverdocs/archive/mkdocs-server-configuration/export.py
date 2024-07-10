#!/usr/bin/python
# vim:set fileencoding=utf-8 sw=2 ai:

import datetime
import re
import psycopg2

SQL = '''
  select
      name, version, to_timestamp(time/1000000)::date, author, text
    from
      wiki w
    where
      version = (select max(version) from wiki where name = w.name)
    order by version
'''

con = psycopg2.connect(database='tracdb', user='tracuser',
                    password='password')

with con:

    cur = con.cursor()
    cur.execute(SQL)

    rows = cur.fetchall()

    for row in rows:
      name = row[0]
      version = row[1]
      time = row[2]
      author = row[3]
      text = row[4]
      print(name,version,time,author)

      text = re.sub('\r\n', '\n', text)
      text = re.sub(r'{{{(.*?)}}}', r'`\1`', text)
      def indent4(m):
         return '\n    ' + m.group(1).replace('\n', '\n    ')
      text = re.sub(r'(?sm){{{\n(.*?)\n}}}', indent4, text)
      text = re.sub(r'(?m)^====\s+(.*?)\s+====$', r'#### \1', text)
      text = re.sub(r'(?m)^===\s+(.*?)\s+===$', r'### \1', text)
      text = re.sub(r'(?m)^==\s+(.*?)\s+==$', r'## \1', text)
      text = re.sub(r'(?m)^=\s+(.*?)\s+=$', r'# \1', text)
      text = re.sub(r'^       * ', r'****', text)
      text = re.sub(r'^     * ', r'***', text)
      text = re.sub(r'^   * ', r'**', text)
      text = re.sub(r'^ * ', r'*', text)
      text = re.sub(r'^ \d+. ', r'1.', text)

      a = []
      for line in text.split('\n'):
        if not line.startswith('    '):
          line = re.sub(r'\[(https?://[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](\1)', line)
          line = re.sub(r'\[(wiki:[^\s\[\]]+)\s([^\[\]]+)\]', r'[\2](/\1/)', line)
          line = re.sub(r'\!(([A-Z][a-z0-9]+){2,})', r'\1', line)
          line = re.sub(r'\'\'\'(.*?)\'\'\'', r'*\1*', line)
          line = re.sub(r'\'\'(.*?)\'\'', r'_\1_', line)
        a.append(line)
      text = '\n'.join(a)

      fp = open('%s.md' % name, 'w')
      print('<!-- Name: %s -->' % name,file=fp)
      print('<!-- Version: %d -->' % version,file=fp)
      print('<!-- Last-Modified: %s -->' % time.strftime('%Y/%m/%d %H:%M:%S'),file=fp)
      print('<!-- Author: %s -->' % author,file=fp)
      fp.write(str(text))
      fp.close()
