# import typing
import uproot
import numpy as np
import pandas as pd
import rich.progress

from dataclasses import dataclass
from pathlib import Path
from bytechomp.datatypes import U16, U64
from PyQt5 import QtCore
from .. import read_root
reader = read_root.root_reader_v2


def uint64_diff(a: U64, b: U64) -> tuple[U64, int]:
    if a == b:
        return 0, 0
    elif a > b:
        return a - b, 1
    else:
        return b - a, -1
    
#Throughout the rest of the code 0 is considered to be the stop and 1 the start. This means that doing t0-t1 is doing stop-start like normal.
    
@dataclass
class ConsolidatedData:
    timestamp0: U64
    timestamp1: U64
    energy0: U16
    energy1: U16

class Merger(QtCore.QObject):
    """Merger Class.
    The start file is considered #1 and stop file, #0.

    Parameters
    ----------
    stop_file : Path
        Root file containing the stop events
    start_file : Path
        Root file containing the start events
    window : U64, optional
        Maximum time for the events to coincide, by default 0
    tree : str, optional
        TTree key for the root files, by default "Data_R"
    """
    cuts_enabled = False
    unfilter_data = False
    finished = QtCore.pyqtSignal(list)

    def __init__(self, stop_file: Path, start_file: Path, window: U64 = 0, tree: str = "Data_R") -> None:
        super(Merger, self).__init__()
        self.file_ch0__: Path = stop_file
        self.file_ch1__: Path = start_file
        self.window : U64 = window
        self.tree = tree
        self.cuts = {0:[],1:[]}

    def select_cuts(self, start: U16, stop: U16, file: int):
        if self.cuts.get(file) is not None:
            self.cuts[file] = [start, stop]

    def merge(self) -> None:     
        root_file0 = reader(self.file_ch0__, self.tree).open(raw=True)
        root_file1 = reader(self.file_ch1__, self.tree).open(raw=True)

        if self.unfilter_data:
            unfiltered_root_file0 = read_root.get_unfiltered(root_file0)
            unfiltered_root_file1 = read_root.get_unfiltered(root_file1)
        else:
            unfiltered_root_file0 = root_file0
            unfiltered_root_file1 = root_file1

        if self.cuts_enabled:
            filtered_root_file0 = unfiltered_root_file0.iloc[read_root.define_cut(*self.cuts[0],unfiltered_root_file0["Energy"])]
            filtered_root_file1 = unfiltered_root_file1.iloc[read_root.define_cut(*self.cuts[1],unfiltered_root_file1["Energy"])]
        else:
            filtered_root_file0 = unfiltered_root_file0
            filtered_root_file1 = unfiltered_root_file1       
    
        length = len(filtered_root_file0["Energy"])           
        result: list[ConsolidatedData] = []
        
        delta: U64
        threshold: U64 = self.window
        iter_t0 = np.nditer(filtered_root_file0["Timestamp"],flags=["f_index"])
        iter_e0 = np.nditer(filtered_root_file0["Energy"])
        iter_t1 = np.nditer(filtered_root_file1["Timestamp"])
        iter_e1 = np.nditer(filtered_root_file1["Energy"])
       
        t0 = next(iter_t0)
        e0 = next(iter_e0)
        t1 = next(iter_t1) 
        e1 = next(iter_e1)
        
        with rich.progress.Progress(
            "[progress.percentage]{task.percentage:>3.0f}%",
            rich.progress.BarColumn(),
            rich.progress.DownloadColumn(),
            "•",
            rich.progress.TimeRemainingColumn(
                compact=True,
                elapsed_when_finished=True
            ),
            "•",
            rich.progress.TransferSpeedColumn(),
            "•",
            rich.progress.SpinnerColumn(finished_text="✔")
        ) as progress:
            task_id = progress.add_task("", total=length)
            while t0 != 0 and t1 != 0:
                progress.update(task_id, completed=iter_t0.index)
                delta, sign = uint64_diff(t0, t1) # Doing t0-t1
                if delta <= threshold:
                    result.append(ConsolidatedData(t0, t1, e0, e1))
                    
                    t0 = next(iter_t0, 0)
                    e0 = next(iter_e0, 0)
                    
                    t1 = next(iter_t1, 0) 
                    e1 = next(iter_e1, 0)
                elif sign < 0:
                    t0 = next(iter_t0, 0)
                    e0 = next(iter_e0, 0)
                elif sign > 0:
                    t1 = next(iter_t1, 0) 
                    e1 = next(iter_e1, 0)

            progress.update(task_id, completed=length)
                    
        # print("result len:", len(result))
        self.finished.emit(result)
        return result

class Converter:
    compress = True
    def __init__(self, data_set: list[ConsolidatedData]):
        self.data_set: list[ConsolidatedData] = data_set

    def convert(self) -> pd.DataFrame:
        """Converts a list of ConsolidatedData to a tuple containing the different data types.

        Returns
        -------
        output_tuple : pd.DataFrame
            Start timestamps, stop timestamps, start energies and stop energies of the original list.
        """
        start_time_stamps = [item.timestamp1 for item in self.data_set]
        stop_time_stamps = [item.timestamp0 for item in self.data_set]
        start_energies = [item.energy1 for item in self.data_set]
        stop_energies = [item.energy0 for item in self.data_set]
        temp_dict = {"Start Time":start_time_stamps,"Stop Time":stop_time_stamps,"Start Energy":start_energies,"Stop Energy":stop_energies}
        return pd.DataFrame.from_dict(temp_dict)

    def save(self, file_path: str):
        """Saves the data into a csv file compressed with bz2 if compress is set to `True`.

        Parameters
        ----------
        file_path : str
            Path to the file
        """
        df = self.convert()
        df.to_csv(file_path, index=False, compression="bz2") if Converter.compress else df.to_csv(file_path, index=False)

                
if __name__ == '__main__':
    toto: Merger = Merger(Path("./data/DataR_CH0@DT5751_1989_Co60-EQ2611-20-CFD.root"), Path("./data/DataR_CH1@DT5751_1989_Co60-EQ2611-20-CFD.root"))
    
    toto.merge()