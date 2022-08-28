import locale
print(locale.setlocale(locale.LC_ALL, ''))

def m(x):
    return locale.currency(x, grouping=True)

print(m(5.4))

print(int(5.7))