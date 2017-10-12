# 一个简单的用例

def main():
    cookie1 = ('略')
    u1 = Snowball('6490571482', cookie1)
    u1.get_stocks()
    pprint(u1.stocks)

    cookie2 = ('略')
    u2 = Tonghuashun(89318030, cookie2)
    u2.get_stocks()
    pprint(u2.stocks)

    # 删除同花顺所有自选股
    if len(u2.stocks) > 0:
        for i in u2.stocks['code']:
            u2.modify_stock(i, 'del')

    # 把雪球自选股添加到同花顺
    def trans_code(row):
        # 雪球code转同花顺code
        if row['exchange'] in ['SH', 'SZ']:
            return re.sub(r'(SH|SZ)', '', row['code'])
        if row['exchange'] == 'HK':
            return 'HK' + row['code'][-4:]
        return row['code']

    u1.stocks['ths_code'] = u1.stocks.apply(trans_code, axis=1)
    pprint(u1.stocks)

    for i in u1.stocks['ths_code'][::-1]:
        u2.modify_stock(i, 'add')

    # 保存csv
    with open('stocks@snowball.csv', 'w') as f:
        u1.stocks.to_csv(f, encoding='gbk')
    with open('stocks@tonghuashun.csv', 'w') as f:
        u2.stocks.to_csv(f, encoding='gbk')

if __name__ == '__main__':
    pd.set_option('display.width', 200)
    main()
