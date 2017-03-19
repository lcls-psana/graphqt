#------------------------------
"""IMVConfigParameters - class supporting configuration parameters for application.

@see class :py:class:`graphqt.IMVConfigParameters`

@see project modules
    * :py:class:`graphqt.IMVConfigParameters`
    * :py:class:`CalibManager.ConfigParameters`
    * :py:class:`graphqt.Logger`
    * :py:class:`CalibManager.Logger`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id:IMVConfigParameters.py 11923 2016-11-22 14:28:00Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
#------------------------------

# import os
from expmon.PSConfigParameters import PSConfigParameters
from expmon.PSNameManager import nm # It is here for initialization

#------------------------------

class IMVConfigParameters(PSConfigParameters) :
    """A storage of configuration parameters for Image Vievier (imvi)
    """
    _name = 'IMVConfigParameters'

    def __init__(self, fname=None) :
        """fname : str - the file name with configuration parameters, if not specified then use default.
        """
        #log.debug('In c-tor', self._name)
        print 'In %s c-tor' % self._name

        PSConfigParameters.__init__(self)

        #self.fname_cp = '%s/%s' % (os.path.expanduser('~'), '.confpars-montool.txt') # Default config file name
        self.fname_cp = './confpars-imvi.txt' # Default config file name

        self.declareParameters()
        self.readParametersFromFile()

        self.list_of_sources = None # if None - updated in the ThreadWorker

        nm.set_config_pars(self)

#------------------------------
        
    def declareParameters(self) :
        # Possible typs for declaration : 'str', 'int', 'long', 'float', 'bool'
        self.log_level = self.declareParameter(name='LOG_LEVEL_OF_MSGS', val_def='info', type='str')
        #self.log_file  = self.declareParameter(name='LOG_FILE_NAME', val_def='/reg/g/psdm/logs/montool/log.txt', type='str')
        self.log_file  = self.declareParameter(name='LOG_FILE_NAME', val_def='log.txt', type='str')

        self.save_log_at_exit = self.declareParameter( name='SAVE_LOG_AT_EXIT', val_def=True,  type='bool')
        #self.dir_log_cpo      = self.declareParameter( name='DIR_FOR_LOG_FILE_CPO', val_def='/reg/g/psdm/logs/calibman', type='str')

        self.main_win_pos_x  = self.declareParameter(name='MAIN_WIN_POS_X',  val_def=5,   type='int')
        self.main_win_pos_y  = self.declareParameter(name='MAIN_WIN_POS_Y',  val_def=5,   type='int')
        self.main_win_width  = self.declareParameter(name='MAIN_WIN_WIDTH',  val_def=420, type='int')
        self.main_win_height = self.declareParameter(name='MAIN_WIN_HEIGHT', val_def=530, type='int')

#------------------------------

cp = IMVConfigParameters()

#------------------------------

def test_IMVConfigParameters() :
    from expmon.Logger import log

    log.setPrintBits(0377)
    cp.readParametersFromFile()
    cp.printParameters()
    cp.log_level.setValue('debug')
    cp.saveParametersInFile()

#------------------------------

if __name__ == "__main__" :
    import sys
    test_IMVConfigParameters()
    sys.exit(0)

#------------------------------
