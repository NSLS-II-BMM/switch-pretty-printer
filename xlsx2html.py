
import json

class make_ports():

    def __init__(self):
        self.ports_json = json.load(open('ports.json'))
        self.switch = 'net-06bm-agg'

    def full_switch(self):
        page = '''
<html>
  <head>
    <link rel="stylesheet" href="ports.css" />
  </head>

  <body>
    <h1>{switch}</h1>
    <div class="wrapper">
'''.format(switch=self.switch)
        for i,this in enumerate(self.ports_json[self.switch]):
            if i == 0:
                text = '<div class="box box1">' + self.oneport(this) + '</div>'
                #print(text, '\n')
            elif i == 1:
                text = '<div class="box box2">' + self.oneport(this) + '</div>'
                #print(text, '\n')
            else:
                text = '<div class="box">' + self.oneport(this) + '</div>'
                #print(text, '\n')
            page = page + text
        page = page + '''
    </div>
  </body>
</html>

'''
        with open('test.html', 'w') as fh:
            fh.write(page)
            
    def oneport(self, this):
        form = '''
  <table style="width: 160px">
    <tr>
      <td rowspan= 4><span class="port">{portn}</span></td>
      <td><span class="minor">Duplex:</span></td>
      <td><span class="minor">{duplex}</span></td>
    </tr>
    <tr>
      <td><span class="minor">Speed:</span></td>
      <td><span class="minor">{speed}</span></td>
    </tr>
    <tr>
      <td><span class="minor">Tag:</span></td>
      <td><span class="minor">{tag}</span></td>
    </tr>
    <tr>
      <td><span class="minor">VLAN:</span></td>
      <td><span class="minor">{vlan}</span></td>
    </tr>
    <tr>
      <td colspan=3 align=center><span class="major">{ip}</span></td>
    </tr>
    <tr>
      <td colspan=3 align=center><span class="name">{name}</span></td>
    </tr>
    <tr>
      <td colspan=3 align=center><span class="major">{mac}</span></td>
    </tr>
  </table>
'''

        return(form.format(duplex = this['Duplex'],
                          speed  = this['Speed'],
                          tag    = this['Tag'],
                          vlan   = this['VLAN'],
                          portn  = this['Port number'],
                          ip     = this['IP address'],
                          name   = this['Name'],
                          mac    = this['MAC address'],
        ))
        
