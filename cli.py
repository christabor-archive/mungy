from pyquery import PyQuery as pq
import mungy
import os

mung = mungy.Munger()

file_dir = '{}/'.format(os.getcwd())

ref_type = raw_input('Which type? \n1. URL \n2. File \n')

if ref_type in ['1', '1.']:
    url = raw_input('Enter a URL: ')
    # Table to dict
    pqdoc = pq(url=url)
else:
    files = '\n'.join([f for f in os.listdir(file_dir) if f.endswith('.html')])
    filename = raw_input('Choose a file: \n{}\n'.format(files))
    pqdoc = pq(filename='{}/{}'.format(file_dir, filename))


choice_type = raw_input('Select the type of html node you '
                        'want to convert: \n1. Table \n2. List\n')

if choice_type in ['1', '1.']:
    results = []
    # Add any number of tables.
    for table in pqdoc.find('table'):
        mung.table_to_dict_values(pq(table).html())
else:
    results = mung.html_to_lists(pqdoc)

save = raw_input('save json file? Y/N\n').lower()

content = mung.to_json(results)
if save == 'y':
    title = raw_input('Please enter a filename (without filetype) ==> ')
    with open('{}{}.json'.format(file_dir, title), 'wb') as _json:
        _json.write(content)
        _json.write('\n')
        _json.close()
    print 'Successfully saved json file "{}.json\n"'.format(title)
else:
    print content
