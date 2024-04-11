from datoso.repositories.dat import DOSCenterDatFile
from pprint import pprint

class TdcDat(DOSCenterDatFile):
    seed: str = 'tdc'

    def initial_parse(self) -> list:
        """ Parse the dat file. """
        # pylint: disable=R0801
        self.company = 'IBM'
        self.system = 'PC and Compatibles'
        self.suffix = 'Total DOS Collection'
        self.date = self.get_date()
        self.full_name = self.name + ' - ' + self.full_name
        self.preffix = 'Computer'
        self.system_type = 'Computer'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self) -> str:
        """ Get the date from the dat file. """
        return self.header["date"]