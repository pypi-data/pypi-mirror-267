""" Test_Piping

    Unittest for running pipesteps and the entire pipeline.
"""

# Imports
import unittest
import logging
import numpy as np
import os
from tempfile import mkstemp
import shutil
from darepype.drp import DataParent

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Define folders and files
TESTDATA_FOLDER = os.path.join(os.path.dirname(__file__), 'testdata')
CONFFILE = os.path.join(TESTDATA_FOLDER, 'testconf.txt')
FITSORIG = os.path.join(TESTDATA_FOLDER, 'testfit.fits')
_hand, FITSFILE = mkstemp('.fits')
shutil.copyfile(FITSORIG, FITSFILE)

class TestSingleSteps(unittest.TestCase):
     
    def test_siso(self):
        """ Test siso step. Runs the step and makes sure
            that the data is the same but that the header
            has changed.
        """
        dp = DataParent(config = CONFFILE)
        df = dp.load(FITSFILE)
        head = df.header.copy()
        img = df.image.copy()
        step = dp.getobject('StepParent')
        do = step(df)
        self.assertEqual(np.sum(img-do.image), 0)
        self.assertNotEqual(head, do.header)
         
    def test_miso(self):
        """ Test a miso step. Runs the step and makes sure
            that the output data is as expected.
        """
        dp = DataParent(config = CONFFILE)
        df1 = dp.load(FITSFILE)
        df2 = dp.load(FITSFILE)
        step = dp.getobject('StepMIParent')
        head = df1.header.copy()
        img = df1.image.copy()
        do = step([df1, df2])
        self.assertEqual(np.sum(img-do.image), 0)
        self.assertNotEqual(head, do.header)
         
    def test_mimo(self):
        """ Test a mimo step. Runs the step and makes sure
            that the output data is as expected.
        """
        dp = DataParent(config = CONFFILE)
        df1 = dp.load(FITSFILE)
        df2 = dp.load(FITSFILE)
        step = dp.getobject('StepMOParent')
        head = df1.header.copy()
        img = df1.image.copy()
        do1, _do2 = step([df1, df2])
        self.assertEqual(np.sum(img-do1.image), 0)
        self.assertNotEqual(head, do1.header)
 
    def test_nimo(self):
        """ Test nimo step. Runs the step and makes sure
            that there is output data.
        """
        dp = DataParent(config = CONFFILE)
        dp.config['parentni']['filloutput'] = True
        step = dp.getobject('StepNIParent')
        step.config = dp.config
        do = step()
        self.assertIsInstance(do[0], DataParent)

class TestPipeLine(unittest.TestCase):
    
    def test_single(self):
        """ Test pipeline with siso step only
        """
        dp = DataParent(config = CONFFILE)
        pipe = dp.getobject('PipeLine')
        dp.log.info('  ==== START SISO PIPE ====')
        do = pipe([FITSFILE,FITSFILE],dp.config,pipemode='single', force=True)
        dp.log.info('  ==== END SISO PIPE ====')
        self.assertIsInstance(do, DataParent)
        
    def test_multi(self):
        """ Test pipeline with mimo and miso steps
        """
        dp = DataParent(config = CONFFILE)
        pipe = dp.getobject('PipeLine')
        dp.log.info('  ==== START MISO/MIMO PIPE ====')
        do = pipe([FITSFILE,FITSFILE],dp.config,pipemode='multi', force=True)
        dp.log.info('  ==== END MISO/MIMO PIPE ====')
        self.assertIsInstance(do, DataParent)
        
    def test_noconfig(self):
        """ Test pipeline with no config file
        """
        from darepype.drp import PipeLine
        pipe = PipeLine()
        pipe.addfiles(FITSFILE)
        self.assertRaises(RuntimeError,pipe)

