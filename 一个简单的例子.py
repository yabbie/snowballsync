# 例子

def main():
    cookie1 = ('略1')
    u1 = Snowball('6490571482', cookie1)
    u1.get_stocks()
    cookie2 = ('略2')
    u2 = Tonghuashun('89318030', cookie2)
    u2.get_stocks()

    # 删除同花顺所有自选股
    if len(u2.stocks) > 0:
        for i in u2.stocks['code']:
            u2.modify_stock(i, 'del')

    # 把雪球自选股添加到同花顺
    pprint(u1.stocks['code'][::-1])
    for i in u1.stocks['code'][::-1]:
        if bool(re.match(r'(SH|SZ)\d+', i)):
            i = re.sub(r'(SH|SZ)', '', i)
        u2.modify_stock(i, 'add')

if __name__ == '__main__':
    pd.set_option('display.width', 200)
    main()
