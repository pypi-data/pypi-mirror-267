""" Test_Objects

    Unittest for darepype objects. Creates an instance of every object.
    Runs specific tests for each type of object.
"""

import unittest
# setup logging
import logging
logging.basicConfig(level=logging.DEBUG)
# Get testdata_folder
import os
testdir = os.path.dirname(__file__)
TESTDATA_FOLDER = os.path.join(testdir, 'testdata')
# Make sure new code version is in path (can also do venv)
#import sys
#sys.path.insert(0,os.path.split(testdir)[0])

class TestDataParent(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import dataparent
        dp = dataparent.DataParent()
        self.assertIsInstance(dp, dataparent.DataParent)
        from darepype.drp import DataParent
        dp = DataParent()
        self.assertIsInstance(dp, DataParent)
        
    def test_config(self):
        """ Tests loading the configuration
        """
        from darepype.drp import DataParent
        conf = os.path.join(TESTDATA_FOLDER,'testconf.txt')
        dp = DataParent(config = conf)
        self.assertIn('general', dp.config)

class TestDataFits(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import datafits
        df = datafits.DataFits()
        self.assertIsInstance(df,datafits.DataFits)
        
    def test_load(self):
        """ Test to load a fits file.
            Also tests if DataParent.load correctly finds
            data object for file
        """
        from darepype.drp import DataParent
        from darepype.drp import DataFits
        dp = DataParent(config = os.path.join(TESTDATA_FOLDER, 'testconf.txt'))
        df = dp.load(os.path.join(TESTDATA_FOLDER, 'testfit.fits'))
        self.assertIsInstance(df, DataFits)
        self.assertGreater(sum(df.image.shape), 0)
        
    def test_imageHDUs(self):
        """ Test image, imageindex, imageget, imageset, imagedel
        """
        # Load test file
        from darepype.drp import DataParent
        dp = DataParent(config = os.path.join(TESTDATA_FOLDER, 'testconf.txt'))
        df = dp.load(os.path.join(TESTDATA_FOLDER, 'testfit.fits'))
        # Name the hdu
        df.imgnames[0] = "FIRST IMAGE"
        # Make copy first image to second hdu
        df.imageset(df.image, "Second Image", df.header)
        # Check imageindex for second image
        self.assertEqual(1, df.imageindex("Second Image"), 'check imageindex on 2 images')
        # Check imageget
        self.assertEqual(df.image.sum(), df.imageget("Second Image").sum())
        # Check imaagedel
        df.imagedel('First Image')
        self.assertEqual(3, len(df.imgdata)+len(df.imgnames)+len(df.imgheads))
        self.assertEqual(0, df.imageindex("Second Image"), 'check imagedelete')
    
    def test_getheader(self):
        """ Test header functions: Set and get header keywords
        """
        # Load test file
        from darepype.drp import DataParent
        dp = DataParent(config = os.path.join(TESTDATA_FOLDER, 'testconf.txt'))
        df = dp.load(os.path.join(TESTDATA_FOLDER, 'testfit.fits'))        
        # Name the hdu
        df.imgnames[0] = "FIRST IMAGE"
        # Make copy first image to second hdu
        df.imageset(df.image, "Second Image", df.header)
        # Get getting values
        self.assertEqual(2,df.getheadval('NAXIS'), 'getheadval from header')
        self.assertEqual(3,df.getheadval('TESTVAL'), 'getheadval from config[header]')
        # Set value in each header
        df.setheadval('AVALUE',10)
        df.setheadval('BVALUE',20,None,'Second Image')
        # Check values
        self.assertEqual(10, df.getheadval('AVALUE'), 'check setheadval primary header')
        self.assertEqual(20, df.getheadval('BVALUE', 'allheaders'), 'check setheadval second header')
        
class TestDataText(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import datatext
        dt = datatext.DataText()
        self.assertIsInstance(dt, datatext.DataText)
        
    def test_load(self):
        """ Test to laod a text file.
            Also tests if DataParent.load correctly finds
            data object for file
        """
        from darepype.drp import DataParent
        from darepype.drp import DataText
        dp = DataParent(config = os.path.join(TESTDATA_FOLDER, 'testconf.txt'))
        dt = dp.load(os.path.join(TESTDATA_FOLDER, 'testtext.txt'))
        self.assertIsInstance(dt, DataText)
        self.assertGreater(len(dt.data), 0)

class TestStepParent(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import stepparent
        sp = stepparent.StepParent()
        self.assertIsInstance(sp,stepparent.StepParent)
        
class TestPipeLine(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import pipeline
        pl = pipeline.PipeLine()
        self.assertIsInstance(pl,pipeline.PipeLine)
        
class TestStepMIParent(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import stepmiparent
        sp = stepmiparent.StepMIParent()
        self.assertIsInstance(sp,stepmiparent.StepMIParent)
        
class TestStepMOParent(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import stepmiparent
        sp = stepmiparent.StepMIParent()
        self.assertIsInstance(sp,stepmiparent.StepMIParent)
        
class TestStepNIParent(unittest.TestCase):
    def test_init(self):
        """ Test make an object
        """
        from darepype.drp import stepniparent
        sp = stepniparent.StepNIParent()
        self.assertIsInstance(sp,stepniparent.StepNIParent)
