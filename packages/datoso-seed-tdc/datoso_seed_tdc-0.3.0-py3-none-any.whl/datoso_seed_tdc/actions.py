from datoso_seed_tdc.dats import TdcDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': TdcDat
        },
        {
            'action': 'DeleteOld'
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}'
        },
        {
            'action': 'SaveToDatabase'
        }
    ]
}

def get_actions():
    return actions