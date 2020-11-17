# switch-pretty-printer
Generate a useful HTML page showing how switch ports are configured

```python
m=Ports()
m.spreadsheet = '06BM port info.xlsx'
m.html = 'test.html'
m.read_spreadsheet()
m.make_html()
```


Here's an example:

![example output](./example.png)
