
from openpyxl import load_workbook
import json

class Ports():

    def __init__(self):
        self.spreadsheet = '06BM port info.xlsx'
        self.switch_data = {}
        #self.switch = 'net-06bm-agg'
        self.html = 'test.html'
        self.port_roles = {'650' : 'SCI',
                           '651' : 'CAM',
                           '652' : 'INST',
                           '653' : 'EPICS',
                           '659' : 'MGMT',}
        

    def read_spreadsheet(self, spreadsheet=None):
        if spreadsheet is None:
            spreadsheet = self.spreadsheet
        if spreadsheet is None:
            print('You need to specify the path to a spreadsheet')
            return()
        print(f'Reading data from {spreadsheet}')
        workbook = load_workbook(spreadsheet, read_only=True);
        worksheet = workbook.active
        for row in worksheet.rows:
            try:
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
                }
                if row[0].value in self.switch_data:
                    self.switch_data[row[0].value].append(this)
                else:
                    self.switch_data[row[0].value] = [this,]
            except:
                pass

    def to_json(self, filename='ports.json'):
        with open(filename, 'w') as fp:
            json.dump(self.switch_data, fp)

        
    def make_html(self):
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

            page = page + f'\n\n    <h1>{sw}</h1>\n      <div class="wrapper">\n'

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
            
    def oneport(self, this):
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
              <td colspan=3 align=center><span class="name">{mac}</span></td>
            </tr>
          </table>
'''

        role = ''
        if str(this['VLAN']) in self.port_roles:
            role = f'({self.port_roles[str(this["VLAN"])]})'
        return(form.format(duplex = this['Duplex'],
                           speed  = this['Speed'],
                           tag    = this['Tag'],
                           vlan   = this['VLAN'],
                           role   = role,
                           portn  = this['Port number'],
                           ip     = this['IP address'],
                           name   = this['Name'],
                           mac    = this['MAC address'],
        ))
        





def main():
    m=Ports()
    m.spreadsheet = '06BM port info.xlsx'
    m.html = 'test.html'
    m.read_spreadsheet()
    m.make_html()

if __name__ == "__main__":
    main()
