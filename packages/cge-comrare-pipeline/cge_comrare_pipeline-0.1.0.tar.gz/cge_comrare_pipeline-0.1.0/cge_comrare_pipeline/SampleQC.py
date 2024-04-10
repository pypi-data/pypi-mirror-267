"""
Module to perform sample quality control
"""

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize
from matplotlib import colormaps

from cge_comrare_pipeline.Helpers import shell_do, delete_temp_files

class SampleQC:

    def __init__(self, input_path:str, input_name:str, output_path:str, output_name:str, config_dict:str, dependables_path:str) -> None:

        """
        Initialize the SampleQC object.

        Parameters:
        -----------
        - input_path (str): Path to the input data.
        - input_name (str): Name of the input data files (without extension).
        - output_path (str): Path to the folder where the output will be saved.
        - output_name (str): Name of the output data.
        - config_dict (str): Dictionary containing configuration settings.
        - dependables_path (str): Path to dependent files.

        Raises:
        ------
        - ValueError: If values for input_path, output_path, and dependables_path are not provided upon initialization.

        Attributes:
        -----------
        - input_path (str): Path to the folder containing the input data files.
        - output_path (str): Path to the folder where the output will be saved.
        - input_name (str): Name of the input data files (without extension).
        - output_name (str): Name for the output files.
        - dependables (str): Path to the folder containing reference data.
        - config_dict (str): Dictionary containing configuration settings.
        - dependables_to_keep (list): List of reference data files to keep.
        - results_to_keep (list): List of result files to keep.
        - results_dir (str): Path to the folder where PCA results will be saved.
        - fails_dir (str): Path to the folder where failed samples will be saved.
        - plots_dir (str): Path to the folder where plots will be saved.
        """

        # check if paths are set
        if input_path is None or output_path is None or dependables_path is None:
            raise ValueError("values for input_path, output_path and dependables_path must be set upon initialization.")

        # Check path validity of input data
        bed_path = os.path.join(input_path, input_name + '.bed')
        fam_path = os.path.join(input_path, input_name + '.fam')
        bim_path = os.path.join(input_path, input_name + '.bim')

        bed_check = os.path.exists(bed_path)
        fam_check = os.path.exists(fam_path)
        bim_check = os.path.exists(bim_path)

        if not os.path.exists(input_path) or not os.path.exists(output_path):
            raise FileNotFoundError("input_path or output_path is not a valid path")
        if not bed_check:
            raise FileNotFoundError(".bed file not found")
        if not fam_check:
            raise FileNotFoundError(".fam file not found")
        if not bim_check:
            raise FileNotFoundError(".bim file not found")
        

        self.input_path = input_path
        self.output_path= output_path
        self.input_name = input_name
        self.output_name= output_name
        self.dependables= dependables_path
        self.config_dict= config_dict

        self.files_to_keep = ['fail_samples']

        # create results folder
        self.results_dir = os.path.join(output_path, 'sample_qc_results')
        if not os.path.exists(self.results_dir):
            os.mkdir(self.results_dir)

        # create fails folder
        self.fails_dir = os.path.join(self.results_dir, 'fail_samples')
        if not os.path.exists(self.fails_dir):
            os.mkdir(self.fails_dir)
        
        # create figures folder
        self.plots_dir = os.path.join(output_path, 'plots')
        if not os.path.exists(self.plots_dir):
            os.mkdir(self.plots_dir)

    def run_sex_check(self)->dict:

        """
        Identify individuals with discordant sex information.

        This function performs a sex check analysis on input data using PLINK to identify individuals with discordant sex information.

        Returns:
        --------
        - dict: A dictionary containing information about the process completion status, the step performed, and the output files generated.

        Raises:
        -------
        - TypeError: If sex_check in config_dict is not a list or if its values are not floats.
        - ValueError: If the length of sex_check is not 2, if the values in sex_check are not between 0 and 1, or if the sum of sex_check values is not equal to 1.
        """

        input_path = self.input_path
        input_name = self.input_name
        output_name= self.output_name
        result_path= self.results_dir
        fails_dir  = self.fails_dir

        sex_check = self.config_dict['sex_check']

        # check type sex_check
        if not isinstance(sex_check, list):
            raise TypeError("sex_check should be a list")
        if len(sex_check)!=2:
            raise ValueError("sex_check must be a list of length 2")
        
        for value in sex_check:
            if not isinstance(value, float):
                raise TypeError("sex_check values should be float")
            if 0 > value or value > 1:
                raise ValueError("sex_check values must be between 0 and 1")
        
        if sum(sex_check) != 1:
            raise ValueError("sex_check values should add to 1")
        
        step = "sex_check"

        # create .sexcheck file
        plink_cmd1 = f"plink --bfile {os.path.join(input_path, input_name)} --check-sex {sex_check[0]} {sex_check[1]} --keep-allele-order --out {os.path.join(result_path, output_name+'_1')}"

        # execute PLINK command
        shell_do(plink_cmd1, log=True)

        # load .sexcheck file
        df = pd.read_csv(
            os.path.join(result_path, output_name+'_1.sexcheck'),
            sep='\s+'
        )

        # filter problematic samples and save file
        df_probs = df[df['STATUS']=='PROBLEM'].reset_index(drop=True)

        # save IDs of samples who failed sex check QC
        df_probs = df_probs.iloc[:,0:2].copy()
        df_probs.to_csv(
            os.path.join(fails_dir, output_name+'.fail-sexcheck-qc.txt'),
            index  =False,
            header =False,
            sep    =' '
        )

        # report
        process_complete = True

        outfiles_dict = {
            'plink_out': result_path
        }

        out_dict = {
            'pass': process_complete,
            'step': step,
            'output': outfiles_dict
        }

        return out_dict

    def run_heterozygosity_rate(self)->dict:

        """
        Identify individuals with elevated missing data rates or outlying heterozygosity rate.

        This function performs a heterozygosity rate analysis on input data using PLINK to identify individuals with elevated missing data rates or outlying heterozygosity rates.

        Returns:
        --------
        - dict: A dictionary containing information about the process completion status, the step performed, and the output files generated.
        """

        input_path = self.input_path
        input_name = self.input_name
        output_name= self.output_name
        result_path= self.results_dir
        plots_path = self.plots_dir
        fails_dir  = self.fails_dir

        step = "heterozygosity_rate"

        # create .imiss and .lmiss files
        plink_cmd1 = f"plink --bfile {os.path.join(input_path, input_name)} --keep-allele-order --missing --out {os.path.join(result_path, output_name+'_1')}"

        # create .het file
        plink_cmd2 = f"plink --bfile {os.path.join(input_path, input_name)} --keep-allele-order --het --autosome --out {os.path.join(result_path, output_name+'_1')}"

        # execute PLINK commands
        cmds = [plink_cmd1, plink_cmd2]
        for cmd in cmds:
            shell_do(cmd, log=True)

        # save samples that failed QC
        fails_path = os.path.join(fails_dir, output_name+'.fail-imisshet-qc.txt')
        logFMISS, meanHET = self.fail_imiss_het(
            result_path, output_name+'_1',
            fails_path
        )

        # generate plot
        self.plot_imiss_het(
            logFMISS, meanHET, plots_path
        )

        # report
        process_complete = True

        outfiles_dict = {
            'plink_out': result_path
        }

        out_dict = {
            'pass': process_complete,
            'step': step,
            'output': outfiles_dict
        }

        return out_dict

    def run_relatedness_prune(self)->dict:

        """
        Identify duplicated or related individuals.

        This function performs a relatedness pruning analysis on input data using PLINK to identify duplicated or related individuals.

        Returns:
        --------
        - dict: A dictionary containing information about the process completion status, the step performed, and the output files generated.
        """

        input_name =self.input_name
        input_path =self.input_path
        results_dir= self.results_dir
        output_name= self.output_name
        fails_dir  = self.fails_dir
        dependables= self.dependables

        maf     = self.config_dict['maf']
        geno    = self.config_dict['geno']
        mind    = self.config_dict['mind']
        ind_pair= self.config_dict['indep-pairwise']

        high_ld_regions_file = os.path.join(dependables, 'high-LD-regions.txt')

        step = "duplicate_relative_prune"

        to_remove = pd.DataFrame(columns=['FID', 'IID'])

        # generates prune.in and prune.out
        plink_cmd1 = f"plink --bfile {os.path.join(input_path, input_name)} --maf {maf} --geno {geno} --mind {mind} --exclude {high_ld_regions_file} --indep-pairwise {ind_pair[0]} {ind_pair[1]} {ind_pair[2]} --out {os.path.join(results_dir, input_name)}"

        # prune and run genome [compute IBD]
        plink_cmd2 = f"plink --bfile {os.path.join(input_path, input_name)} --extract {os.path.join(results_dir, input_name+'.prune.in')} --keep-allele-order --genome --out {os.path.join(results_dir, output_name+'_3')}"

        # generate new .imiss file
        plink_cmd3 = f"plink --bfile {os.path.join(input_path, input_name)} --keep-allele-order --missing --out {os.path.join(results_dir, output_name+'_3')}"

        # execute PLINK commands
        cmds = [plink_cmd1, plink_cmd2, plink_cmd3]
        for cmd in cmds:
            shell_do(cmd, log=True)

        # load .imiss file
        df_imiss = pd.read_csv(
            os.path.join(results_dir, output_name+'_3.imiss'),
            sep='\s+'
        )
        # load .genome file
        df_genome = pd.read_csv(
            os.path.join(results_dir, output_name+'_3.genome'),
            sep='\s+'
        )

        # isolate duplicates or related samples
        df_dup = df_genome[df_genome['PI_HAT']>0.185].reset_index(drop=True)

        df_1 = pd.merge(
            df_dup[['FID1', 'IID1']], 
            df_imiss[['FID', 'IID', 'F_MISS']], 
            left_on =['FID1', 'IID1'],
            right_on=['FID', 'IID']
        ).drop(columns=['FID', 'IID'], inplace=False)

        df_2 = pd.merge(
            df_dup[['FID2', 'IID2']], 
            df_imiss[['FID', 'IID', 'F_MISS']], 
            left_on=['FID2', 'IID2'],
            right_on=['FID', 'IID']
        ).drop(columns=['FID', 'IID'], inplace=False)

        for k in range(len(df_dup)):

            if df_1.iloc[k,2]>df_2.iloc[k,2]:
                to_remove.loc[k] = df_1.iloc[k,0:2].to_list()
            elif df_1.iloc[k,2]<df_2.iloc[k,2]:
                to_remove.loc[k] = df_2.iloc[k,0:2].to_list()
            else:
                to_remove.loc[k] = df_1.iloc[k,0:2].to_list()

        to_remove = to_remove.drop_duplicates(keep='last')
        to_remove.to_csv(
            os.path.join(fails_dir, output_name+'.fail-IBD1-qc.txt'),
            index=False,
            header=False,
            sep=" "
        )

        # report
        process_complete = True

        outfiles_dict = {
            'plink_out': results_dir
        }

        out_dict = {
            'pass': process_complete,
            'step': step,
            'output': outfiles_dict
        }

        return out_dict

    def delete_failing_QC(self)->None:

        """
        Remove samples that failed quality control.

        This function removes samples that failed one or several quality control (QC) steps based on the generated fail files. It generates cleaned binary files without the failing samples using PLINK.

        Returns:
        --------
        - dict: A dictionary containing information about the process completion status, the step performed, and the output files generated.
        """

        input_path = self.input_path
        input_name = self.input_name
        result_path= self.results_dir
        output_name= self.output_name
        fails_dir  = self.fails_dir

        step = "delete_sample_failed_QC"

        # load samples who failed sex check
        sex_path = os.path.join(fails_dir, output_name+'.fail-sexcheck-qc.txt')
        if os.path.getsize(sex_path)==0:
            df_sex = pd.DataFrame()
        else:
            df_sex = pd.read_csv(
                sex_path,
                sep      =' ',
                index_col=False,
                header   =None
            )

        # load samples who failed heterozygosity check
        imiss_path = os.path.join(fails_dir, output_name+'.fail-imisshet-qc.txt')
        if os.path.getsize(imiss_path)==0:
            df_imiss = pd.DataFrame()
        else:
            df_imiss = pd.read_csv(
                imiss_path,
                sep      =' ',
                index_col=False,
                header   =None
            )

        # load samples who failed IBD check
        ibd1_path = os.path.join(fails_dir, output_name+'.fail-IBD1-qc.txt')
        if os.path.getsize(ibd1_path)==0:
            df_ibd1 = pd.DataFrame()
        else:
            df_ibd1 = pd.read_csv(
                ibd1_path,
                sep      =' ',
                index_col=False,
                header   =None
            )

        # concatenate all failings samples
        df = pd.concat([df_sex, df_imiss, df_ibd1], axis=0)

        # sort values by the first column
        df.sort_values(by=df.columns[0], inplace=True)

        # drop duplicates
        df = df.drop_duplicates(keep='first')

        # save file with samples who failed QC
        df.to_csv(
            os.path.join(fails_dir, output_name+'.fail-qc_1-inds.txt'),
            sep   =' ',
            header=False,
            index =False
        )

        # generate cleaned binary files
        plink_cmd = f"plink --bfile {os.path.join(input_path, input_name)} --keep-allele-order --remove {os.path.join(fails_dir, output_name+'.fail-qc_1-inds.txt')} --make-bed --out {os.path.join(self.results_dir, output_name+'.clean')}"

        # execute PLINK command
        shell_do(plink_cmd, log=True)

        # add cleaned files to list with files to keep
        self.files_to_keep.append(output_name+'.clean.bed')
        self.files_to_keep.append(output_name+'.clean.bim')
        self.files_to_keep.append(output_name+'.clean.fam')

        # report
        process_complete = True

        outfiles_dict = {
            'plink_out': result_path
        }

        out_dict = {
            'pass': process_complete,
            'step': step,
            'output': outfiles_dict
        }

        return out_dict

    @staticmethod
    def plot_imiss_het(logFMISS:pd.Series, meanHET:pd.Series, figs_folder:str)->None:

        """
        Plot missing genotypes proportion vs. heterozygosity rate.

        This static method plots the proportion of missing genotypes vs. heterozygosity rate for individuals. It visualizes the relationship between missing data and heterozygosity rate.

        Parameters:
        -----------
        - logFMISS (pd.Series): Pandas Series containing the logarithm of the proportion of missing genotypes for individuals.
        - meanHET (pd.Series): Pandas Series containing the mean heterozygosity rate for individuals.
        - figs_folder (str): Path to the folder where the plot will be saved.

        Returns:
        --------
        - None
        """

        # Calculate colors based on density
        norm = Normalize(vmin=min(logFMISS), vmax=max(logFMISS))
        colors = colormaps['viridis']

        fig_path = os.path.join(figs_folder, "imiss-vs-het.pdf")

        meanHet_low= np.mean(meanHET) - 2*np.std(meanHET)
        meanHet_up = np.mean(meanHET) + 2*np.std(meanHET)

        # Plotting
        plt.figure(figsize=(8, 6))
        plt.scatter(logFMISS, meanHET, cmap=colors, s=50, marker='o', norm=norm)
        plt.xlim(-3, 0)
        plt.ylim(0, 0.5)
        plt.xlabel("Proportion of missing genotypes")
        plt.ylabel("Heterozygosity rate")
        plt.yticks(np.arange(0, 0.51, 0.05))
        plt.xticks([-3, -2, -1, 0], [0.001, 0.01, 0.1, 1])
        plt.axhline(meanHet_low, color='red', linestyle='--')
        plt.axhline(meanHet_up, color='red', linestyle='--')
        plt.axvline(-1.522879, color='red', linestyle='--')
        plt.grid(True)
        plt.savefig(fig_path)

        return None

    @staticmethod
    def fail_imiss_het(folder_path:str, file_name:str, output_file:str)->tuple:

        """
        Identify samples failing imiss-het quality control.

        This static method reads the .het and .imiss files generated by PLINK from the specified folder path and file name. It computes the mean heterozygosity rate and the logarithm of the proportion of missing genotypes for each sample. Then, it filters samples based on specific criteria (proportion of missing genotypes or mean heterozygosity rate). It saves the samples that failed imiss-het quality control to the specified output file.

        Parameters:
        -----------
        - folder_path (str): Path to the folder containing the .het and .imiss files.
        - file_name (str): Name of the PLINK file (without extension).
        - output_file (str): Path to save the samples that failed imiss-het quality control.

        Returns:
        --------
        - Tuple[pd.Series, pd.Series]: A tuple containing the logarithm of the proportion of missing genotypes (logF_MISS) and the mean heterozygosity rate (meanHet) for all samples.
        """

        # load .het and .imiss files
        df_het = pd.read_csv(
            os.path.join(folder_path, file_name+'.het'),
            sep="\s+"
        )
        df_imiss = pd.read_csv(
            os.path.join(folder_path, file_name+'.imiss'),
            sep="\s+"
        )

        # compute Het mean
        df_het['meanHet'] = (df_het['N(NM)']-df_het['O(HOM)'])/df_het['N(NM)']

        df_imiss['logF_MISS'] = np.log10(df_imiss['F_MISS'])
    
        # compute the lower 2 standard deviation bound
        meanHet_lower = df_het['meanHet'].mean() - 2*df_het['meanHet'].std()

        # compute the upper 2 standard deviation bound
        meanHet_upper = df_het['meanHet'].mean() + 2*df_het['meanHet'].std()

        # filter samples
        mask = ((df_imiss['F_MISS']>=0.04) | (df_het['meanHet'] < meanHet_lower) | (df_het['meanHet'] > meanHet_upper))

        df = df_imiss[mask].reset_index(drop=True)
        df = df.iloc[:,0:2].copy()

        # save samples that failed imiss-het QC
        df.to_csv(
            path_or_buf =output_file, 
            sep         =' ', 
            index       =False, 
            header      =False
        )

        return df_imiss['logF_MISS'], df_het['meanHet']
