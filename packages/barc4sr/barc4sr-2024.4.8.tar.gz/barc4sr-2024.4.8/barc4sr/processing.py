#!/bin/python

"""
This module provides a collection of functions for processing and analyzing data related
 to undulator radiation, power density, and spectra. It includes functions for reading 
 data from XOPPY files (HDF5 format), SPECTRA files (JSON format), and processing the 
 data to calculate various properties such as spectral power, cumulated power, 
 integrated power, and power density. Additionally, it offers functions for selecting 
 specific energy ranges within 3D data sets, spatially trimming data, and generating 
 animated GIFs of energy scans in the 3D data-sets. Overall, this module facilitates 
 the analysis and visualization of data obtained from simulations related to synchrotron 
 radiation sources.
"""

__author__ = ['Rafael Celestre']
__contact__ = 'rafael.celestre@synchrotron-soleil.fr'
__license__ = 'GPL-3.0'
__copyright__ = 'Synchrotron SOLEIL, Saint Aubin, France'
__created__ = '26/JAN/2024'
__changed__ = '10/APR/2024'

import json
import multiprocessing
import pickle
import sys
from typing import Any, Dict, List, Union

import h5py as h5
import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
import xraylib
from PIL import Image, ImageDraw, ImageFont
from scipy.constants import physical_constants
from scipy.interpolate import RegularGridInterpolator

CHARGE = physical_constants["atomic unit of charge"][0]

#***********************************************************************************
# barc4sr.xoppy.undulator_spectrum()
#***********************************************************************************

def read_undulator_spectrum(file_list: List[str], computer_code: str = 'xoppy') -> Dict[str, Any]:
    """
    Reads spectrum data from files and processes it using process_spectrum function.

    This function reads spectrum data from files specified in the 'file_list' and processes
    it using the 'process_spectrum' function to compute spectral power, cumulated power, and integrated power.

    Parameters:
        - file_list (List[str]): A list of file paths containing spectrum data.
        - computer_code (str): The code used to generate the spectrum data ('xoppy', 'srw', or 'spectra').

    Returns:
        Dict[str, Any]: A dictionary containing processed spectrum data with the following keys:
            - 'spectrum': A dictionary containing various properties of the spectrum including:
                - 'energy': Array containing energy values.
                - 'flux': Array containing spectral flux data.
                - 'spectral_power': Array containing computed spectral power.
                - 'cumulated_power': Cumulated power computed using cumulative trapezoid integration.
                - 'integrated_power': Integrated power computed using trapezoid integration.
    """
    energy = []
    flux = []

    if computer_code == 'xoppy' or computer_code == 'srw':
        for sim in file_list:
            f = open(sim, "rb")
            data = np.asarray(pickle.load(f))
            f.close()

            energy = np.concatenate((energy, data[0, :]))
            flux = np.concatenate((flux, data[1, :]))
    elif computer_code == 'spectra':
        for jsonfile in file_list:
            f = open(jsonfile)
            data = json.load(f)
            f.close()

            energy = np.concatenate((energy, data['Output']['data'][0]))
            flux = np.concatenate((flux, data['Output']['data'][1]))
    else:
        raise ValueError("Invalid computer code. Please specify either 'xoppy', 'srw', or 'spectra'.")

    return process_spectrum(flux, energy)


def process_spectrum(flux: np.ndarray, energy: np.ndarray) -> Dict[str, Any]:
    """
    Processes spectrum data to compute spectral power, cumulated power, and integrated power.

    This function processes spectrum data provided as 'flux' and 'energy' arrays to compute spectral power,
    cumulated power, and integrated power.

    Parameters:
        - flux (np.ndarray): Array containing the spectral flux data.
        - energy (np.ndarray): Array containing the energy values corresponding to the spectral flux.

    Returns:
        Dict[str, Any]: A dictionary containing processed spectrum data with the following keys:
            - 'spectrum': A dictionary containing various properties of the spectrum including:
                - 'energy': Array containing energy values.
                - 'flux': Array containing spectral flux data.
                - 'spectral_power': Array containing computed spectral power.
                - 'cumulated_power': Cumulated power computed using cumulative trapezoid integration.
                - 'integrated_power': Integrated power computed using trapezoid integration.
    """

    spectral_power = flux*CHARGE*1E3

    cumulated_power = integrate.cumulative_trapezoid(spectral_power, energy, initial=0)
    integrated_power = integrate.trapezoid(spectral_power, energy)

    spectrumSRdict = {
        "spectrum":{
            "energy":energy,
            "flux": flux,
            "spectral_power": spectral_power,
            "cumulated_power": cumulated_power,
            "integrated_power": integrated_power
        }
    }

    return spectrumSRdict

#***********************************************************************************
# barc4sr.xoppy.undulator_power_density()
#***********************************************************************************

def read_undulator_power(file_name: str, computer_code: str = 'xoppy') -> Dict[str, Any]:
    """
    Reads power density data from an XOPPY HDF5 file or SPECTRA JSON file and processes it.

    This function reads power density data from either an XOPPY HDF5 file or a SPECTRA JSON 
    file specified by 'file_name'. It extracts the power density map along with 
    corresponding x and y axes from the file, and then processes this data using the 
    'process_power_density' function

    Parameters:
        - file_name (str): File path containing power density data.
        - computer_code (str): The code used to generate the power density data ('xoppy', 'srw', or 'spectra').

    Returns:
        Dict[str, Any]: A dictionary containing processed power density data with the following keys:
            - 'axis': A dictionary containing 'x' and 'y' axes arrays.
            - 'power_density': A dictionary containing power density-related data, including the power density map,
              total received power, and peak power density.
    """
    if computer_code == 'xoppy' or computer_code == 'srw':
        f = h5.File(file_name, "r")
        PowDenSR = f["XOPPY_POWERDENSITY"]["PowerDensity"]["image_data"][()]

        x = f["XOPPY_POWERDENSITY"]["PowerDensity"]["axis_x"][()]
        y = f["XOPPY_POWERDENSITY"]["PowerDensity"]["axis_y"][()]

    elif computer_code == 'spectra':
        f = open(file_name)
        data = json.load(f)
        f.close()

        PowDenSR = np.reshape(data['Output']['data'][2],
                            (len(data['Output']['data'][1]), 
                            len(data['Output']['data'][0])))

        if "mrad" in data['Output']['units'][2]:
            dist = data["Input"]["Configurations"]["Distance from the Source (m)"]
            dx = (data["Input"]["Configurations"]["x Range (mm)"][1]-data["Input"]["Configurations"]["x Range (mm)"][0])*1e-3
            dy = (data["Input"]["Configurations"]["y Range (mm)"][1]-data["Input"]["Configurations"]["y Range (mm)"][0])*1e-3

            dtx = 2*np.arctan(dx/dist/2)*1e3    # mrad
            dty = 2*np.arctan(dy/dist/2)*1e3

            PowDenSR *= 1e3 * (dtx*dty)/(dx*dy*1e3*1e3)
            x = data['Output']['data'][0]
            y = data['Output']['data'][1]
        else:
            PowDenSR *= 1e3
    else:
        raise ValueError("Invalid computer code. Please specify either 'xoppy', 'srw', or 'spectra'.")

    return process_power_density(PowDenSR, x, y)


def process_power_density(PowDenSR: np.ndarray, x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """
    Processes the power density data and calculates the total received power and peak power density.

    This function processes the power density data provided in 'PowDenSR' array along with corresponding x and y axes,
    and calculates the total received power and peak power density. The processed data is returned in a dictionary format.

    Parameters:
        - PowDenSR (np.ndarray): An array representing the power density map.
        - x (np.ndarray): Array containing x-axis coordinates.
        - y (np.ndarray): Array containing y-axis coordinates.

    Returns:
        Dict[str, Any]: A dictionary containing the processed power density data with the following keys:
            - 'axis': A dictionary containing 'x' and 'y' axes arrays.
            - 'power_density': A dictionary containing power density-related data, including the power density map,
              total received power, and peak power density.
    """
    dx = x[1]-x[0]
    dy = y[1]-y[0]

    CumPow = PowDenSR.sum()*dx*dy

    print(f"Total received power: {CumPow:.3f} W")
    print(f"Peak power density: {PowDenSR.max():.3f} W/mm^2")

    PowDenSRdict = {
        "axis": {
            "x": x,
            "y": y,
        },
        "power_density": {
            "map":PowDenSR,
            "CumPow": CumPow,
            "PowDenSRmax": PowDenSR.max()
        },
    }

    return PowDenSRdict


def trim_and_resample_power_density(PowDenSRdict: Dict[str, Any], **kwargs: Union[float, bool]) -> Dict[str, Any]:
    """
    Trims and optionally resamples the power density data map.

    This function trims the power density data map based on specified criteria and optionally resamples
    it using interpolation if new axis values are provided. It returns the trimmed and resampled power density map
    along with cumulative power and maximum power density.

    Parameters:
        - PowDenSRdict (Dict[str, Any]): A dictionary containing power density data with the following keys:
            - 'axis': A dictionary containing 'x' and 'y' axes arrays.
            - 'power_density': A dictionary containing the power density map.
        - **kwargs (Union[float, bool]): Additional keyword arguments for optional trimming and resampling:
            - 'dx' (float): Width in the x-direction for trimming.
            - 'dy' (float): Width in the y-direction for trimming.
            - 'xc' (float): Center of the trimming region along the x-axis.
            - 'yc' (float): Center of the trimming region along the y-axis.
            - 'X' (array_like): New x-axis values for resampling.
            - 'Y' (array_like): New y-axis values for resampling.

    Returns:
        Dict[str, Any]: A dictionary containing trimmed and resampled power density data with the following keys:
            - 'axis': A dictionary containing trimmed and resampled 'x' and 'y' axes arrays.
            - 'power_density': A dictionary containing the trimmed and resampled power density map,
              along with cumulative power and maximum power density.

    """

    PowDenSR = PowDenSRdict["power_density"]["map"]

    x, y = PowDenSRdict["axis"]["x"], PowDenSRdict["axis"]["y"]
    xc, yc = 0, 0
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]

    if kwargs:
        dx = kwargs.get("dx", dx)
        dy = kwargs.get("dy", dy)
        xc = kwargs.get("xc", xc)
        yc = kwargs.get("yc", yc)
        X = kwargs.get("X", x)
        Y = kwargs.get("Y", y)
        interpol = "X" in kwargs or "Y" in kwargs

    if interpol:
        print("Interpolation of PowDenSR")
        ygrid, xgrid = np.meshgrid(Y, X, indexing='ij')
        f = RegularGridInterpolator((y, x), PowDenSR, bounds_error=False, fill_value=0)
        PowDenSR = f((ygrid, xgrid))
        x, y = X, Y
    else:
        deltax, deltay = x[1] - x[0], y[1] - y[0]

        bool_x = np.logical_and((x - xc <=  dx / 2 + deltax / 20),
                                (x - xc >= -dx / 2 - deltax / 20))

        bool_y = np.logical_and((y - yc <=  dy / 2 + deltay / 20),
                                (y - yc >= -dy / 2 - deltay / 20)) 

        PowDenSR = PowDenSR[bool_y, :][:, bool_x]
        x = np.delete(x, np.logical_not(bool_x)) - xc
        y = np.delete(y, np.logical_not(bool_y)) - yc

    dx, dy = x[1] - x[0], y[1] - y[0]

    CumPow = PowDenSR.sum() * dx * dy

    print(f"Total received power: {CumPow:.3f} W")
    print(f"Peak received power density (normal incidence): {PowDenSR.max():.3f} W/mm^2")

    return {
        "axis": {"x": x, "y": y},
        "power_density": {"map": PowDenSR, "CumPow": CumPow, "PowDenSRmax": PowDenSR.max()}
    }

#***********************************************************************************
# barc4sr.xoppy.undulator_radiation()
#***********************************************************************************

def read_undulator_radiation(file_list: List[str], computer_code: str = 'srw', parallel_processing: bool = False) -> dict:
    """
    Reads XOPPY undulator radiation data from a list of files and processes it.

    This function reads the XOPPY undulator radiation data from a list of HDF5 files,
    concatenates the spectral flux data, and processes it using either the process_undulator_radiation function
    or the process_undulator_radiation_parallel function based on the value of parallel_processing.

    Parameters:
        - file_list (List[str]): A list of file paths containing the XOPPY undulator radiation data.
        - computer_code (str): The code used to generate the power density data ('xoppy' or 'srw').
        - parallel_processing (bool, optional): Whether to use parallel processing. Defaults to False.

    Returns:
        dict: A dictionary containing processed undulator radiation data.

    Notes:
        - The input HDF5 files should contain the following datasets:
            - 'XOPPY_RADIATION/Radiation/stack_data': 3D array representing the spectral flux data.
            - 'XOPPY_RADIATION/Radiation/axis0': 1D array representing the energy axis.
            - 'XOPPY_RADIATION/Radiation/axis1': 1D array representing the x-axis.
            - 'XOPPY_RADIATION/Radiation/axis2': 1D array representing the y-axis.
        - The spectral flux data from different files will be concatenated along the 0-axis.
        - The x and y axes are assumed to be the same for all files in the file_list.
    """
    energy = []
    spectral_flux_3D = []

    k = 0

    for sim in file_list:
        print(sim)
        f = h5.File(sim, "r")

        if k == 0:
            spectral_flux_3D = f["XOPPY_RADIATION"]["Radiation"]["stack_data"][()]
            k+=1
        else:
            spectral_flux_3D = np.concatenate((spectral_flux_3D, f["XOPPY_RADIATION"]["Radiation"]["stack_data"][()]), 0)
        energy = np.concatenate((energy, f["XOPPY_RADIATION"]["Radiation"]["axis0"][()]))

    print("UR files loaded")
    if computer_code == 'xoppy':
        spectral_flux_3D = spectral_flux_3D.swapaxes(1, 2)

    x = f["XOPPY_RADIATION"]["Radiation"]["axis1"][()]
    y = f["XOPPY_RADIATION"]["Radiation"]["axis2"][()]

    if parallel_processing:
        return process_undulator_radiation_parallel(spectral_flux_3D, energy, x, y)
    else:
        return process_undulator_radiation(spectral_flux_3D, energy, x, y)


def process_undulator_radiation(spectral_flux_3D: np.ndarray, energy: np.ndarray, x: np.ndarray, y: np.ndarray) -> dict:
    """
    Processes the undulator radiation data.

    This function calculates various properties of undulator radiation based on the provided 3D spectral flux data.

    Parameters:
        - spectral_flux_3D (np.ndarray): A 3D numpy array representing the spectral flux data. Shape: (n_slices, ny, nx)
        - energy (np.ndarray): A 1D numpy array containing the energy values.
        - x (np.ndarray): A 1D numpy array containing the x-axis values.
        - y (np.ndarray): A 1D numpy array containing the y-axis values.

    Returns:
        dict: A dictionary containing processed undulator radiation data with the following keys:
            - 'axis': Dictionary containing the x and y axis values.
            - 'spectral_power_3D': 3D numpy array of spectral power.
            - 'power_density': Dictionary containing the power density information with keys:
                - 'map': 2D numpy array representing the power density map.
                - 'CumPow': Cumulative power.
                - 'PowDenSRmax': Maximum power density.
            - 'spectrum': Dictionary containing spectral information with keys:
                - 'energy': 1D numpy array of energy values.
                - 'flux': Flux values.
                - 'spectral_power': Spectral power.
                - 'cumulated_power': Cumulative power.
                - 'integrated_power': Integrated power.

    Notes:
        - The input spectral_flux_3D should have dimensions (n_slices, ny, nx) where:
            - n_slices: Number of sample images.
            - ny: Number of points along the y-axis.
            - nx: Number of points along the x-axis.
        - The energy array should correspond to the energy values for each slice in spectral_flux_3D.
        - The x and y arrays represent the coordinates of the grid on which the data is sampled.

    """
    print("Processing undulator radiation")
    n_slices = spectral_flux_3D.shape[0]
    ny = spectral_flux_3D.shape[1]
    nx = spectral_flux_3D.shape[2]

    print(f"> {n_slices} sample images ({ny} x {nx}) found ({ sys.getsizeof(spectral_flux_3D) / (1024 ** 3):.2f} Gb in memory)")

    dx = (x[1]-x[0])
    dy = (y[1]-y[0])

    flux = dx*dy*np.sum(spectral_flux_3D, axis=(1, 2))
    spectral_power = flux*CHARGE*1E3
    cumulated_power = integrate.cumulative_trapezoid(spectral_power, energy, initial=0)
    integrated_power = integrate.trapezoid(spectral_power, energy)

    PowDenSR = integrate.trapezoid(spectral_flux_3D*CHARGE*1E3, energy, axis=0)

    CumPow = dx*dy*PowDenSR.sum()

    print(f"Puissance totale reçue : {CumPow:.3f} W")
    print(f"Puissance crête reçue (incidence normale): {PowDenSR.max():.3f} W/mm^2")

    URdict = {
        "axis": {
            "x": x,
            "y": y,
        },
        "spectral_power_3D":spectral_flux_3D*CHARGE*1E3,
        "power_density": {
            "map":PowDenSR,
            "CumPow": CumPow,
            "PowDenSRmax": PowDenSR.max()
        },
        "spectrum":{
            "energy":energy,
            "flux": flux,
            "spectral_power": spectral_power,
            "cumulated_power": cumulated_power,
            "integrated_power": integrated_power
        }
    }
    print("Dictionary written")
    return URdict


def process_undulator_radiation_parallel(spectral_flux_3D: np.ndarray, energy: np.ndarray, x: np.ndarray, y: np.ndarray, chunk_size: int = 25) -> dict:
    """
    Process undulator radiation data in parallel.

    This function calculates various properties of undulator radiation based on the provided 3D spectral flux data.

    Parameters:
        - spectral_flux_3D (np.ndarray): A 3D numpy array representing the spectral flux data. Shape: (n_slices, ny, nx)
        - energy (np.ndarray): A 1D numpy array containing the energy values.
        - x (np.ndarray): A 1D numpy array containing the x-axis values.
        - y (np.ndarray): A 1D numpy array containing the y-axis values.
        - chunk_size (int, optional): Size of each chunk of spectral flux data for parallel processing. Default is 25.

    Returns:
        dict: A dictionary containing processed undulator radiation data with the following keys:
            - 'axis': Dictionary containing the x and y axis values.
            - 'spectral_power_3D': 3D numpy array of spectral power.
            - 'power_density': Dictionary containing the power density information with keys:
                - 'map': 2D numpy array representing the power density map.
                - 'CumPow': Cumulative power.
                - 'PowDenSRmax': Maximum power density.
            - 'spectrum': Dictionary containing spectral information with keys:
                - 'energy': 1D numpy array of energy values.
                - 'flux': Flux values.
                - 'spectral_power': Spectral power.
                - 'cumulated_power': Cumulative power.
                - 'integrated_power': Integrated power.

    Notes:
        - The input spectral_flux_3D should have dimensions (n_slices, ny, nx) where:
            - n_slices: Number of sample images.
            - ny: Number of points along the y-axis.
            - nx: Number of points along the x-axis.
        - The energy array should correspond to the energy values for each slice in spectral_flux_3D.
        - The x and y arrays represent the coordinates of the grid on which the data is sampled.

    """
    print("Processing undulator radiation (parallel)")
    n_slices = spectral_flux_3D.shape[0]
    ny = spectral_flux_3D.shape[1]
    nx = spectral_flux_3D.shape[2]

    print(f"> {n_slices} sample images ({ny} x {nx}) found ({ sys.getsizeof(spectral_flux_3D) / (1024 ** 3):.2f} Gb in memory)")

    dx = (x[1]-x[0])
    dy = (y[1]-y[0])

    # Divide the data into chunks
    chunks = [(spectral_flux_3D[i:i + chunk_size+1], energy[i:i + chunk_size+1], x, y) for i in range(0, n_slices, chunk_size)]
    
    # Create a multiprocessing Pool
    with multiprocessing.Pool() as pool:
        # Process each chunk in parallel
        processed_chunks = pool.map(process_chunk, chunks)
    
    # Concatenate the processed chunks
    PowDenSR = np.zeros((ny, nx))
    flux = []

    for i, (PowDenSR_chunk, flux_chunk, energy_chunck) in enumerate(processed_chunks):
        PowDenSR += PowDenSR_chunk
        if i == 0:
            flux.extend(flux_chunk)
            previous_energy_chunck = energy_chunck
        else: 
            if energy_chunck[0] == previous_energy_chunck[-1]:
                flux.extend(flux_chunk[1:])
            else:
                flux.extend(flux_chunk)
        previous_energy_chunck = energy_chunck

    spectral_power = np.asarray(flux)*CHARGE*1E3
    cumulated_power = integrate.cumulative_trapezoid(spectral_power, energy, initial=0)
    integrated_power = integrate.trapezoid(spectral_power, energy)
    CumPow = dx*dy*PowDenSR.sum()

    print(f"Puissance totale reçue : {CumPow:.3f} W")
    print(f"Puissance crête reçue (incidence normale): {PowDenSR.max():.3f} W/mm^2")

    URdict = {
        "axis": {
            "x": x,
            "y": y,
        },
        "spectral_power_3D":spectral_flux_3D*CHARGE*1E3,
        "power_density": {
            "map":PowDenSR,
            "CumPow": CumPow,
            "PowDenSRmax": PowDenSR.max()
        },
        "spectrum":{
            "energy":energy,
            "flux": np.asarray(flux),
            "spectral_power": spectral_power,
            "cumulated_power": cumulated_power,
            "integrated_power": integrated_power
        }
    }
    print("Dictionary written")
    return URdict


def process_chunk(args):
    """
    Process a chunk of spectral flux data.

    This function calculates the power density and flux for a chunk of spectral flux data.

    Parameters:
        args (tuple): A tuple containing the following elements:
            - spectral_flux_3D_chunk (np.ndarray): A chunk of spectral flux data.
            - energy_chunk (np.ndarray): A chunk of energy values.
            - x (np.ndarray): A 1D numpy array containing the x-axis values.
            - y (np.ndarray): A 1D numpy array containing the y-axis values.

    Returns:
        tuple: A tuple containing the calculated power density and flux.
    """
    spectral_flux_3D_chunk, energy_chunk, x, y = args

    dx = x[1] - x[0]
    dy = y[1] - y[0]

    flux = dx * dy * np.sum(spectral_flux_3D_chunk, axis=(1, 2))
    PowDenSR = integrate.trapezoid(spectral_flux_3D_chunk * CHARGE * 1E3, energy_chunk, axis=0)

    return PowDenSR, flux, energy_chunk


def select_energy_range_undulator_radiation(URdict: Dict[str, Any], ei: float, ef: float, **kwargs: Union[float, bool]) -> Dict[str, Any]:
    """
    Selects a specific energy range from the undulator radiation data and returns processed data within that range.

    This function selects a specific energy range from the given undulator radiation data dictionary (URdict)
    and returns processed data within that range. Optionally, it allows trimming the data based on specified criteria.

    Parameters:
        - URdict (Dict[str, Any]): A dictionary containing undulator radiation data with the following keys:
            - 'axis': A dictionary containing 'x' and 'y' axes arrays.
            - 'spectrum': A dictionary containing energy-related data, including 'energy' array.
            - 'spectral_power_3D': A 3D array representing spectral power density.
        - ei (float): The initial energy of the selected range.
        - ef (float): The final energy of the selected range.
        - **kwargs (Union[float, bool]): Additional keyword arguments for optional trimming:
            - 'dx' (float): Width in the x-direction for trimming.
            - 'dy' (float): Width in the y-direction for trimming.
            - 'xc' (float): Center of the trimming region along the x-axis.
            - 'yc' (float): Center of the trimming region along the y-axis.

    Returns:
        Dict[str, Any]: A dictionary containing processed undulator radiation data within the selected energy range,
        trimmed based on the specified criteria (if any).

    Notes:
        - If 'ei' or 'ef' is set to -1, the function selects the minimum or maximum energy from the available data, respectively.
        - If 'ei' is equal to 'ef', the function duplicates the data for that energy and increments the energy values by 1.

    """
    x = URdict["axis"]["x"]
    y = URdict["axis"]["y"]

    dx = kwargs.get("dx", x[-1] - x[0])
    dy = kwargs.get("dy", y[-1] - y[0])
    xc = kwargs.get("xc", 0)
    yc = kwargs.get("yc", 0)

    deltax, deltay = x[1] - x[0], y[1] - y[0]

    bool_x = np.logical_and((x - xc <= dx / 2 + deltax / 20),
                            (x - xc >= -dx / 2 - deltax / 20))

    bool_y = np.logical_and((y - yc <= dy / 2 + deltay / 20),
                            (y - yc >= -dy / 2 - deltay / 20))

    if ei == -1:
        ei = URdict["spectrum"]["energy"][0]
    if ef == -1:
        ef = URdict["spectrum"]["energy"][-1]

    crop_map = np.logical_not(np.logical_and((URdict["spectrum"]["energy"] <= ef),
                                             (URdict["spectrum"]["energy"] >= ei)))
    energy = np.delete(URdict["spectrum"]["energy"], crop_map)
    spectral_flux_3D = np.delete(URdict["spectral_power_3D"], crop_map, axis=0) / (CHARGE * 1E3)

    if ei == ef:
        spectral_flux_3D = np.concatenate((spectral_flux_3D, spectral_flux_3D), axis=0)
        energy = np.concatenate((energy, energy + 1))

    if kwargs:  # Check if trimming is requested
        spectral_flux_3D = spectral_flux_3D[:, bool_y, :][:, :, bool_x]
        x = np.delete(x, np.logical_not(bool_x)) - xc
        y = np.delete(y, np.logical_not(bool_y)) - yc

    return process_undulator_radiation_parallel(spectral_flux_3D, energy, x, y)


def animate_undulator_radiation(URdict: dict, file_name: str, **kwargs: Any) -> None:
    """
    Generate an animated GIF of an energy scan.

    Args:
        URdict (dict): Dictionary containing spectral power data.
        file_name (str): Name of the output GIF file.
        **kwargs: Additional keyword arguments.
            duration_per_frame (float): Duration of each frame in seconds. Defaults to 0.05.
            frame_rate (float): Frame rate in frames per second. Overrides duration_per_frame if provided.
            cmap (str): Colormap for visualization. Defaults to 'plasma'.
            cumSum (bool): If True, generate an additional GIF with cumulative sum. Defaults to False.
            ScaleBar (bool): If True, add a scale bar to the GIF. Defaults to False.
            ScaleBarLength (float): Length of the scale bar in the unit of theScaleBarUnit.
            ScaleBarUnit (str): Unit of measurement for the scale bar.
            group (bool): If True, group the energy scan with the cumulative sum. Defaults to False.

    """
    duration_per_frame = 0.05
    cmap = 'plasma'
    cumSum = False
    ScaleBar = False
    group = False

    if bool(kwargs):

        if "duration_per_frame" in kwargs.keys():
            duration_per_frame = kwargs["duration_per_frame"]
        if "frame_rate" in kwargs.keys():
            duration_per_frame = 1/kwargs["frame_rate"]
        if "cmap" in kwargs.keys():
            cmap = kwargs["cmap"]
        if "cumSum" in kwargs.keys():
            cumSum = kwargs["cumSum"]

        ScaleBarLength = None
        ScaleBarUnit = None
        if "ScaleBar" in kwargs.keys():
            ScaleBar = kwargs["ScaleBar"]
        if "ScaleBarLength" in kwargs.keys():
            ScaleBar = True
            ScaleBarLength = kwargs["ScaleBarLength"]
        if "ScaleBarUnit" in kwargs.keys():
            ScaleBar = True
            ScaleBarUnit = kwargs["ScaleBarUnit"]

        if ScaleBar is True and ScaleBarUnit is None:
            # warnings.warn(">> Scale bar unit nor provided. No scale bar will be displayed", Warning)
            print(">> Warning: Scale bar unit nor provided. No scale bar will be displayed")
            ScaleBar = False

        if ScaleBar:
            if ScaleBarLength is None:
                dh = np.round((URdict["axis"]["x"][-1]-URdict["axis"]["x"][0])/4)
                ScaleBarLength = dh-dh%2
            PixelsPerLengthUnit = len(URdict["axis"]["x"])/(URdict["axis"]["x"][-1]-URdict["axis"]["x"][0])
            ScaleLengthPixels = int(ScaleBarLength * PixelsPerLengthUnit)
        
        if "group" in kwargs.keys():
            group = kwargs["group"]

    global_min = np.min(URdict["spectral_power_3D"])
    global_max = np.max(URdict["spectral_power_3D"])

    if group:
        cumulated_power = np.cumsum(URdict["spectral_power_3D"], axis=0)
        with imageio.get_writer(file_name + ".gif", mode='I', duration=duration_per_frame) as writer:
            for i, frame in enumerate(URdict["spectral_power_3D"]):

                cp_frame_min = np.min(cumulated_power[i, :, :])
                cp_frame_max = np.max(cumulated_power[i, :, :])
                cp_frame_normalized = (cumulated_power[i, :, :] - cp_frame_min) / (cp_frame_max - cp_frame_min)

                dnan = 5
                frame_normalized = (frame - global_min) / (global_max - global_min)
                frame_normalized = np.hstack((frame_normalized, np.full((frame_normalized.shape[0], dnan), np.nan)))
                frame_normalized = np.concatenate((frame_normalized, cp_frame_normalized), axis=1)

                frame_colored = plt.cm.get_cmap(cmap)(frame_normalized)
                # Convert the colormap to uint8 format (0-255)
                frame_colored_uint8 = (frame_colored[:, :, :3] * 255).astype(np.uint8)
                
                # Convert NumPy array to PIL Image
                pil_image = Image.fromarray(frame_colored_uint8)
                
                # Add frame number as text overlay
                draw = ImageDraw.Draw(pil_image)
                font = ImageFont.truetype("arial.ttf", 20)
                draw.text((15, 15), f"E = {URdict['spectrum']['energy'][i]:.2f} eV", fill=(255, 255, 255), font=font)
                draw.text((15+frame.shape[1]+dnan, 15), "cummulated", fill=(255, 255, 255), font=font)

                if ScaleBar:
                    # Add scale bar
                    scale_bar_x0 = pil_image.width - 10 - ScaleLengthPixels
                    scale_bar_y0 = pil_image.height - 20
                    scale_bar_x1 = pil_image.width - 10
                    scale_bar_y1 = pil_image.height - 15
                    draw.rectangle([scale_bar_x0, scale_bar_y0, scale_bar_x1, scale_bar_y1], fill=(255, 255, 255))
                    # Add text for scale bar length
                    scale_text = f"{ScaleBarLength} {ScaleBarUnit}"
                    text_left, text_top, text_right, text_bottom = draw.textbbox(xy=(0,0), text=scale_text, font=font)
                    text_width, text_height = (text_right - text_left, text_bottom - text_top)
                    text_x = scale_bar_x0 + (scale_bar_x1 - scale_bar_x0 - text_width) // 2
                    text_y = scale_bar_y0 - text_height - 10
                    draw.text((text_x, text_y), scale_text, fill=(255, 255, 255), font=font)

                # Convert PIL Image back to NumPy array
                frame_with_tag = np.array(pil_image)
                
                writer.append_data(frame_with_tag)

        print(f"GIF created successfully: {file_name.split('/')[-1]}")
    else:
        with imageio.get_writer(file_name + ".gif", mode='I', duration=duration_per_frame) as writer:
            for i, frame in enumerate(URdict["spectral_power_3D"]):

                frame_normalized = (frame - global_min) / (global_max - global_min)
                frame_colored = plt.cm.get_cmap(cmap)(frame_normalized)

                # Convert the colormap to uint8 format (0-255)
                frame_colored_uint8 = (frame_colored[:, :, :3] * 255).astype(np.uint8)
                
                # Convert NumPy array to PIL Image
                pil_image = Image.fromarray(frame_colored_uint8)
                
                # Add frame number as text overlay
                draw = ImageDraw.Draw(pil_image)
                font = ImageFont.truetype("arial.ttf", 20)
                draw.text((15, 15), f"E = {URdict['spectrum']['energy'][i]:.2f} eV", fill=(255, 255, 255), font=font)
                        
                if ScaleBar:
                    # Add scale bar
                    scale_bar_x0 = pil_image.width - 10 - ScaleLengthPixels
                    scale_bar_y0 = pil_image.height - 20
                    scale_bar_x1 = pil_image.width - 10
                    scale_bar_y1 = pil_image.height - 15
                    draw.rectangle([scale_bar_x0, scale_bar_y0, scale_bar_x1, scale_bar_y1], fill=(255, 255, 255))
                    # Add text for scale bar length
                    scale_text = f"{ScaleBarLength} {ScaleBarUnit}"
                    text_left, text_top, text_right, text_bottom = draw.textbbox(xy=(0,0), text=scale_text, font=font)
                    text_width, text_height = (text_right - text_left, text_bottom - text_top)
                    text_x = scale_bar_x0 + (scale_bar_x1 - scale_bar_x0 - text_width) // 2
                    text_y = scale_bar_y0 - text_height - 10
                    draw.text((text_x, text_y), scale_text, fill=(255, 255, 255), font=font)

                # Convert PIL Image back to NumPy array
                frame_with_tag = np.array(pil_image)
                
                writer.append_data(frame_with_tag)

        print(f"GIF created successfully: {file_name.split('/')[-1]}")

        if cumSum:
            cumulated_power = np.cumsum(URdict["spectral_power_3D"], axis=0)
            with imageio.get_writer(file_name + "_CumSum.gif", mode='I', duration=duration_per_frame) as writer:
                for i, frame in enumerate(cumulated_power):

                    frame_min = np.min(frame)
                    frame_max = np.max(frame)

                    frame_normalized = (frame - frame_min) / (frame_max - frame_min)
                    frame_colored = plt.cm.get_cmap(cmap)(frame_normalized)

                    # Convert the colormap to uint8 format (0-255)
                    frame_colored_uint8 = (frame_colored[:, :, :3] * 255).astype(np.uint8)
                    
                    # Convert NumPy array to PIL Image
                    pil_image = Image.fromarray(frame_colored_uint8)
                    
                    # Add frame number as text overlay
                    draw = ImageDraw.Draw(pil_image)
                    font = ImageFont.truetype("arial.ttf", 20)
                    draw.text((15, 15), f"E = {URdict['spectrum']['energy'][i]:.2f} eV (cummulated)", fill=(255, 255, 255), font=font)
                    if ScaleBar:
                        # Add scale bar
                        scale_bar_x0 = pil_image.width - 10 - ScaleLengthPixels
                        scale_bar_y0 = pil_image.height - 20
                        scale_bar_x1 = pil_image.width - 10
                        scale_bar_y1 = pil_image.height - 15
                        draw.rectangle([scale_bar_x0, scale_bar_y0, scale_bar_x1, scale_bar_y1], fill=(255, 255, 255))
                        # Add text for scale bar length
                        scale_text = f"{ScaleBarLength} {ScaleBarUnit}"
                        text_left, text_top, text_right, text_bottom = draw.textbbox(xy=(0,0), text=scale_text, font=font)
                        text_width, text_height = (text_right - text_left, text_bottom - text_top)
                        text_x = scale_bar_x0 + (scale_bar_x1 - scale_bar_x0 - text_width) // 2
                        text_y = scale_bar_y0 - text_height - 10
                        draw.text((text_x, text_y), scale_text, fill=(255, 255, 255), font=font)
                    # Convert PIL Image back to NumPy array
                    frame_with_tag = np.array(pil_image)
                    
                    writer.append_data(frame_with_tag)

            print(f"GIF created successfully: {file_name.split('/')[-1]+'_CumSum'}")


if __name__ == '__main__':
    print("This is the barc4sr.processing auxiliary lib!")
    print("This module provides functions for processing and analyzing data related to undulator radiation, power density, and spectra.")
