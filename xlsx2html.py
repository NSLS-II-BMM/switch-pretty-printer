
from openpyxl import load_workbook
import json, datetime
from mac_vendor_lookup import MacLookup

maclookup = MacLookup()
#print('populating MAC vendor table')
#mactable.update_vendors()  # <- This can take a few seconds for the download

class Ports():
    '''A class for reading a spreadsheet generated by BNL ITD explaining
    the behavior on the ports of each managed network switch and
    writing a useful HTML file summarizing that data.

    Example
    =======

    from xlsx2html import Ports
    m = Ports()
    m.spreadsheet = '06BM port info.xlsx'
    m.html = 'test.html'
    m.read_spreadsheet()  # read data from spreadsheet
    m.make_html()         # write data to an html file

    '''
    def __init__(self):
        self.spreadsheet = '06BM port info.xlsx'
        self.switch_data = {}
        self.html = 'test.html'
        ## port_roles is not right for ID lines
        #                    0      1      2       3       4    5    6    7    8     9
        self.port_roles = ['SCI', 'CAM', 'INST', 'EPICS', '4', '5', '6', '7', '8', 'MGMT',]
        

    def read_spreadsheet(self, spreadsheet=None):
        '''Read spreadsheet data, storing its contents in a dict '''
        if spreadsheet is None:
            spreadsheet = self.spreadsheet
        if spreadsheet is None:
            print('You need to specify the path to a spreadsheet')
            return()
        print(f'Reading data from {spreadsheet}')
        workbook = load_workbook(spreadsheet, read_only=True);
        worksheet = workbook.active
        for row in worksheet.rows:
            #            if row[1].value.split('/')[1] == 'Port':
            #                continue
            
            try:
                if row[1].value.split('/')[1] != '1': # skip Ports like 1/3/1 and such
                    continue
                pnum = row[1].value.split('/')[2]
                this = {'Port number' : pnum,
                        'Link'        : row[2].value,
                        'Duplex'      : row[3].value,
                        'Speed'       : row[4].value,
                        'Tag'         : row[5].value,
                        'VLAN'        : row[6].value,
                        'MAC address' : row[7].value,
                        'Name'        : row[8].value,
                        'IP address'  : row[9].value,
                        'notes'       : row[10].value,
                }
                if row[0].value in self.switch_data:
                    self.switch_data[row[0].value].append(this)
                else:
                    self.switch_data[row[0].value] = [this,]
            except:
                pass

    def to_json(self, filename='ports.json'):
        '''Save spreadsheet data to a JSON file''' 
        with open(filename, 'w') as fp:
            json.dump(self.switch_data, fp)

        
    def make_html(self):
        '''Write the contents of the spreadsheet to a pretty html file'''
        if self.switch_data == {}:
            print('It seems you have not yet read a spreadsheet')
            return()

        ##########
        # header #
        ##########
        page = '''
<html>
  <head>
    <link rel="stylesheet" href="ports.css" />
  </head>

  <body>'''

        for sw in self.switch_data.keys():

            ## h1 for this switch + grid wrapper div
            page = page + f'\n\n    <h1>{sw}</h1>\n    <h2>{datetime.date.today().strftime("%B %d, %Y")}</h2>\n      <div class="wrapper">\n'

            ## generate a div for the table explaining each port
            for i,this in enumerate(self.switch_data[sw]):
                if i == 0:
                    text = '        <div class="box box1">' + self.oneport(this) + '        </div>\n'
                    #print(text, '\n')
                elif i == 1:
                    text = '        <div class="box box2">' + self.oneport(this) + '        </div>\n'
                    #print(text, '\n')
                else:
                    text = '        <div class="box">' + self.oneport(this) + '        </div>\n'
                    #print(text, '\n')
                page = page + text
            ## close the wrapper div
            page = page  + '      </div>'

        ##########
        # footer #
        ##########
        page = page + '''
  </body>
</html>

'''
        with open(self.html, 'w') as fh:
            fh.write(page)
        print(f'Wrote html to {self.html}')

    def regularize_mac_address(self, mac):
        #if ':' in mac:
        #    return mac.lower()
        if mac.lower() == 'no mac':
            return ''
        mac = mac.replace('.','').replace(':','')
        return '.'.join(mac[i:i+4] for i in range(0,12,4)).lower()
        #return ':'.join(mac[i:i+2] for i in range(0,12,2)).lower()
        
    def oneport(self, this):
        '''Generate a table that will will one div of the output html file.
        This table contains the data from a single port.  The div looks
        something like this:

        +--------------------------+
        | Port     VLAN: ###       |
        | number   Tag: yes/no     |
        |          Speed: speed    |
        |                          |
        | IP address on this port  |
        |  DNS name on this port   |
        | MAC address on this port |
        +--------------------------+

        '''
        form = '''
          <table>
            <tr>
              <td rowspan= 4><span class="port">{portn}</span></td>
              <td><span class="minor">VLAN:</span></td>
              <td><span class="minor">{vlan} {role}</span></td>
            </tr>
            <tr>
              <td><span class="minor">Tag:</span></td>
              <td><span class="minor">{tag}</span></td>
            </tr>
            <tr>
              <td><span class="minor">Speed:</span></td>
              <td><span class="minor">{speed}</span></td>
            </tr>
            <tr><td></td></tr>
            <tr>
              <td colspan=3 align=center><span class="major">{ip}</span></td>
            </tr>
            <tr>
              <td colspan=3 align=center><span class="name">{name}</span></td>
            </tr>
            <tr>
              <td colspan=3 align=center><span class="mac">{mac}</span></td>
            </tr>
            <tr>
              <td colspan=3 align=center><span class="vendor">{vendor}</span></td>
            </tr>
            <tr>
              <td colspan=3 align=center><span class="notes">{notes}</span></td>
            </tr>
          </table>
'''

        if this['VLAN'] < 10 :
            role = ''
        else:
            n = this['VLAN'] % 10
            role = f' / {self.port_roles[n]}'
        this_ip = this['IP address']
        if this['IP address'].lower() == 'no ip':
            this_ip = ' ' #'0.0.0.0'
        this_name = this['Name']
        if this['Name'] is None or this['Name'].lower() == 'none':
            this_name = ' '
        if this['notes'] is None:
            this['notes'] = ''
        mac_address = self.regularize_mac_address(this['MAC address'])
        try:
            vendor = maclookup.lookup(mac_address)
        except:
            vendor = ''
            
        return(form.format(duplex = this['Duplex'],
                           speed  = this['Speed'],
                           tag    = this['Tag'],
                           vlan   = this['VLAN'],
                           role   = role,
                           portn  = this['Port number'],
                           ip     = this_ip,
                           name   = this_name,
                           mac    = mac_address,
                           vendor = vendor,
                           notes  = this['notes'],
        ))
        





def main():
    m=Ports()
    m.spreadsheet = '06BM port info.xlsx'
    m.html = 'test.html'
    m.read_spreadsheet()
    m.make_html()

if __name__ == "__main__":
    main()
