from datoso_seed_tdc.dats import TdcDat

rules = [
    {
        'name': 'TDC Dat',
        '_class': TdcDat,
        'seed': 'tdc',
        'priority': 0,
        'rules': [
            {
                'key': 'Homepage',
                'operator': 'contains',
                'value': 'totaldoscollection'
            }
        ]
    }
]

def get_rules():
    return rules