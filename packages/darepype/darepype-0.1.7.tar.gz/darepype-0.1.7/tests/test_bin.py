""" Test_Bin

    Unittest for runnable files
"""

# Imports
import unittest
import logging
import os
from tempfile import mkdtemp
import shutil

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Define folders and files
TESTDATA_FOLDER = os.path.join(os.path.dirname(__file__), 'testdata')
CONFFILE = os.path.join(TESTDATA_FOLDER, 'testconf.txt')
FITSORIG = os.path.join(TESTDATA_FOLDER, 'testfit.fits')
TEMPFOLDER = mkdtemp()
FITSFILE = os.path.join(TEMPFOLDER,'testfits.fits')
DRPATH = os.path.split(os.path.dirname(__file__))[0]
shutil.copyfile(FITSORIG, FITSFILE)

class TestDarePypeRun(unittest.TestCase):
    
    def test_running(self):
        """ Simple test to run a piperun file
        """
        # Prepare piperun file 
        inf = open(os.path.join(TESTDATA_FOLDER,'pyperun.txt'))
        prtext = inf.read()
        inf.close()
        prtext.strip()
        prtext += '\npythonpath = ' + DRPATH
        prtext += '\npipeconf   = ' + CONFFILE
        prtext += '\ninputfiles   = ' + FITSFILE
        prtext += '\noutputfolder = ' + TEMPFOLDER
        prtext += '\nlogfile = ' + os.path.join(TEMPFOLDER, 'log.txt')
        prfile = os.path.join(TEMPFOLDER, 'pyperun.txt')
        outf = open(prfile, 'wt')
        outf.write(prtext+'\n')
        outf.close()
        # Run the test
        cmd = os.path.join(DRPATH,'bin','darepyperun.py')
        cmd += ' ' + prfile
        print(cmd)
        os.system(cmd)
        print('== Files in Temp Folder ==')
        print(os.listdir(TEMPFOLDER))
        # Check if output file exists
        self.assertTrue(os.path.exists(os.path.join(TEMPFOLDER,'log.txt')), 'log.txt was not created')
        self.assertTrue(os.path.exists(FITSFILE.replace('.fits','.UNK.fits')))
        