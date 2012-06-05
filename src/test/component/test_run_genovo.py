"""
Created on Mar 20, 2012

@author: Steven Wu
"""
import unittest
import os
from core.component.run_genovo import RunGenovo
from core import run_ext_prog
from core.utils import path_utils


class TestRunGenovo(unittest.TestCase):

    platform = run_ext_prog.get_platform()

    def setUp(self):
        self.long_message = True
        self.data_dir = path_utils.get_data_dir() + "Genovo/"
        self.working_dir = path_utils.get_data_dir() + "Genovo/test_data/"

    def tearDown(self):
        pass

    def test_RunGenovo_init(self):
        infile_var = "wdir_all_reads.fa"
        expected_infile = self.working_dir + infile_var

        genovo = RunGenovo(infile_var, pdir=self.data_dir,
                           wdir=self.working_dir, no_iter=1, thresh=10)
        expected = ["10", self.working_dir + "wdir_all_reads_out.fasta",
                    expected_infile + ".dump.best"]
        self.assertEqual(genovo.assemble.get_switch()[0], expected_infile)
        self.assertEqual(genovo.assemble.get_switch(), [expected_infile, "1"])
        self.assertEqual(genovo.finalize.get_switch(), expected)

    def test_RunGenovo_simple_assemble(self):
        infile_var = "all_read.fa"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir,
                           wdir=self.working_dir, no_iter=3, thresh=250,
                           check_exist=False)
        expected = [self.working_dir + infile_var, "3"]
        self.assertEqual(genovo.assemble.get_switch(), expected)

        genovo.set_number_of_iter(10)
        expected = [self.working_dir + infile_var, "10"]
        self.assertEqual(genovo.assemble.get_switch(), expected)

        infile_var = "test_infile.fasta"
        genovo.set_infile_name(infile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "10"])

    def test_RunGenovo_simple_finalise(self):
        infile_var = "test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=3,
                           thresh=250, check_exist=False)
        self.assertEqual(3, len(genovo.finalize._switch))
        expected = ["250", self.data_dir + "test_infile_out.fasta",
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

        genovo.set_cutoff(300)
        expected = ["300", self.data_dir + "test_infile_out.fasta",
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

        infile_var = "VICTORY!!!.fasta"
        genovo.set_infile_name(infile_var)
        expected = ["300", self.data_dir + "test_infile_out.fasta",
                    infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

    def test_RunGenovo_finalise_outfile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "testOutfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile=outfile_var,
                           pdir=self.data_dir, wdir=self.working_dir, no_iter=3,
                           thresh=250, check_exist=False)
        self.assertEqual(3, len(genovo.finalize._switch))
        expected = ["250", self.working_dir + outfile_var,
                    self.working_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(),
                             expected)

        genovo = RunGenovo(infile=infile_var, outfile=outfile_var,
                           pdir=self.data_dir, no_iter=3, thresh=250,
                           check_exist=False)
        self.assertEqual(3, len(genovo.finalize._switch))
        expected = ["250", self.data_dir + outfile_var,
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

        genovo2 = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=3,
                            thresh=250, check_exist=False)   # outfile == None
        expected = ["250", self.data_dir + "test_infile_out.fasta",
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo2.finalize.get_switch(), expected)

        infile_var = "test_infile.xyz.fasta.abc"
        genovo2 = RunGenovo(infile=infile_var, pdir=self.data_dir,
                            wdir=self.working_dir, no_iter=3, thresh=250,
                            check_exist=False)   # outfile == None
        expected = ["250", self.working_dir + "test_infile.xyz.fasta_out.fasta",
                    self.working_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo2.finalize.get_switch(), expected)

        infile_var = "test_infile"
        genovo2 = RunGenovo(infile=infile_var, pdir=self.data_dir,
                            wdir=self.data_dir, no_iter=3, thresh=250,
                            check_exist=False)   # outfile == None
        expected = ["250", self.data_dir + "test_infile_out.fasta",
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo2.finalize.get_switch(), expected)

    def test_RunGenovo_set_infile_outfile(self):

        infile_var = "test_infile.fasta"
        outfile_var = "test_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile=outfile_var,
                           pdir=self.data_dir, no_iter=3, thresh=250,
                           check_exist=False)
        expected = [self.data_dir + infile_var, "3"]
        self.assertEqual(genovo.assemble.get_switch(), expected)
        expected = ["250", self.data_dir + outfile_var,
                    self.data_dir + infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

        infile_var = "test_infile2.fasta"
        genovo.set_infile_name(infile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        expected = ["250", self.data_dir + outfile_var,
                    infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

        outfile_var = "test_outfile2.fasta"
        genovo.set_outfile(outfile_var)
        self.assertEqual(genovo.assemble.get_switch(), [infile_var, "3"])
        expected = ["250", outfile_var, infile_var + ".dump.best"]
        self.assertEqual(genovo.finalize.get_switch(), expected)

    def test_RunGenovo_set_number_of_iter(self):
        infile_var = "test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=3,
                           thresh=250, check_exist=False)
        self.assertRaises(TypeError, genovo.set_number_of_iter, 1.1)
        self.assertRaises(TypeError, genovo.set_number_of_iter, -1)
        self.assertRaises(TypeError, genovo.set_number_of_iter, "string")
        self.assertRaises(TypeError, genovo.set_number_of_iter, "5")

    def test_RunGenovo_set_cutoff(self):
        """
        Note: There are different type of Errors
        Feel free to change/swap/move between ValueError and TypeError
        """
        infile_var = "test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=3,
                           thresh=250, check_exist=False)
        self.assertRaises(ValueError, genovo.set_cutoff, 1.1)
        self.assertRaises(ValueError, genovo.set_cutoff, -1)
        self.assertRaises(ValueError, genovo.set_cutoff, -2.5)
        self.assertRaises(TypeError, genovo.set_cutoff, "string")
        self.assertRaises(TypeError, genovo.set_cutoff, "3")

    def test_RunGenovo_check_directory_name(self):
        """
        check if directory name is valid
        """
        infile_var = "test_infile.fasta"
        wrong_dir = self.data_dir[:-1]
        genovo = RunGenovo(infile=infile_var, pdir=wrong_dir, no_iter=3,
                           thresh=250, check_exist=False)
        self.assertEqual(genovo.pdir, self.data_dir)

    def test_RunGenovo_infile_not_exist(self):
        """
        check if infile and/or file directory exist
        """

        infile_var = "fileDoesNotExist"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=3,
                      thresh=250, check_exist=True)

        infile_var = "anyFile"
        invalid_dir = "/RandomDirThatDoesNotExist/"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, pdir=invalid_dir, no_iter=3,
                      thresh=250, check_exist=True)

    def test_RunGenovo_outfile_already_exist(self):
        """
        check if out file already exists,
        maybe should not raise error, should
        TODO: maybe it should be handle it at different way, auto rename?
        """
        infile_var = self.data_dir + "test_infile.fasta"
        outfile_var = self.data_dir + "testOutFileAlreadyExist.fasta"
        with self.assertRaises(IOError):
            RunGenovo(infile=infile_var, outfile=outfile_var,
                      pdir=self.data_dir, no_iter=3, thresh=250, check_exist=True)

    def test_RunGenovo_check_assemble_result_exist(self):
        """
        check if ./assemble finished running, should produce 3 output files
        only pass if all 3 exist
        """
        infile_var = "test_infile.fasta"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=10,
                           thresh=250, check_exist=False)
#        print genovo.checkAssembleOutfilesExist("test_infile.fasta")
        self.assertTrue(genovo.check_outfiles_exist(self.data_dir +
                                                    "test_infile.fasta"))

        # negative test, outfiles are not suppose to exist
        infile_var = "fileNotExist.fasta"
        genovo = RunGenovo(infile=infile_var, pdir=self.data_dir, no_iter=10,
                           thresh=250, check_exist=False)
#        print genovo.checkAssembleOutfilesExist("fileNotExist_out")
        self.assertFalse(genovo.check_outfiles_exist(self.data_dir + "fileNotExist_out"))

    def test_RunGenovo_read_finalize_outfile(self):
        """
        check if it can "read" assembled contig
        TODO: have check what happen in the file format is invalid,
        assuming its the correct fasta now
        """
        infile_var = "test_infile.fasta"
        outfile_var = "test_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile=outfile_var,
                           pdir=self.data_dir, no_iter=10, thresh=250,
                           check_exist=False)
        result = genovo.read_outfile()
        self.assertEqual(len(result), 2)
        self.assertEqual(result.keys(), ["1", "2"])

        expected = [170, 60]
        for i, key in enumerate(result):
#            print key, i, type(result[key]), result[key]
            self.assertEqual(len(result[key]), expected[i])

    def test_RunGenovo_run(self):
        infile_var = "test_infile.fasta"
        outfile_var = "test_run_outfile.fasta"
        genovo = RunGenovo(infile=infile_var, outfile=outfile_var,
                           pdir=self.data_dir, no_iter=10, thresh=100,
                           check_exist=True)
        genovo.run()
        self.assertTrue(genovo.check_outfiles_exist(self.data_dir + infile_var))
        self.assertTrue(genovo.is_file_exist(self.data_dir + "test_run_outfile", ".fasta", True))
        os.remove(self.data_dir + outfile_var)