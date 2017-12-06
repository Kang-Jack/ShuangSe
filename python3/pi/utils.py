from pandas import DataFrame

def format_str(rs, type):
    for i in range(0, 4):
        if i == 0:
            top_line = "R:" + str(rs[i])
        else:
            top_line = top_line + "," + str(rs[i])
    for i in range(4, 6):
        if i == 4:
            bottom_line = str(rs[i])
        else:
            bottom_line = bottom_line + "," + str(rs[i])

    bottom_line = bottom_line + " B:" + str(rs[6]) + " " + type
    return top_line, bottom_line


def generate_txt(rs):
    # rs = historical_data.get_all_data()
    # drinks['beer_servings'] = drinks.beer_servings.astype(float)
    # df =df.Series([2:8], dtype='int64')
    df = DataFrame(rs).sort_index(ascending=False)
    df[2] = df[2].astype('int64')
    df[3] = df[3].astype('int64')
    df[4] = df[4].astype('int64')
    df[5] = df[5].astype('int64')
    df[6] = df[6].astype('int64')
    df[7] = df[7].astype('int64')
    df[8] = df[8].astype('int64')
    df.insert(0, 'year', df[0].astype(str).str[:4])

    # print (df.head(5))
    # df.insert(0, 'year', dfi)
    # df = DataFrame(rs)
    df.to_csv(r'./123.txt', header=None, index=True, sep=' ', mode='w', encoding='utf-8')
