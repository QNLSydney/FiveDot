# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:03:11 2018

@author: Administrator
"""

from qcodes_measurements import pyplot
from qcodes_measurements.plot import plot_tools
from scipy import signal

midas.raster_points(2048)
midas.sw_mode(0)
midas.raster_rate(66)

midas.ch1.frequency(369.7)

midas.ch1.magnitude.shape=(2048,)
midas.ch1.magnitude.setpoints=(np.linspace(0, 1, 2048),)
midas.ch1.magnitude.setpoint_labels = ("Voltage", )
midas.ch1.magnitude.setpoint_units = ("V", )

midas.ch1.I.shape=(2048,)
midas.ch1.I.setpoints=(np.linspace(0, 1, 2048),)
midas.ch1.I.setpoint_labels = ("Voltage", )
midas.ch1.I.setpoint_units = ("V", )

midas.ch1.Q.shape=(2048,)
midas.ch1.Q.setpoints=(np.linspace(0, 1, 2048),)
midas.ch1.Q.setpoint_labels = ("Voltage", )
midas.ch1.Q.setpoint_units = ("V", )

midas.ch1.phase.shape=(2048,)
midas.ch1.phase.setpoints=(np.linspace(0, 1, 2048),)
midas.ch1.phase.setpoint_labels = ("Voltage", )
midas.ch1.phase.setpoint_units = ("V", )


def linear1d_midas(midas, param_set, start, stop, num_points, delay, *param_meas, 
             append=None, save=True, wallcontrol=None, wallcontrol_slope=None,
             differentiate=True):
    """
    """

    # Set up a plotting window
    if append is None or not append:
        win = pyplot.PlotWindow()
        win.win_title = 'ID: '
        win.resize(1000,600)
    elif isinstance(append, pyplot.PlotWindow):
        # Append to the given window
        win = append
    elif isinstance(append, bool):
        # Append to the last trace if true
        win = pyplot.PlotWindow.getWindows()[-1]
    else:
        raise ValueError("Unknown argument to append. Either give a plot window"
                         " or true to append to the last plot")
        
    # Register setpoints
    meas = Measurement()
    meas.register_parameter(param_set)
    param_set.post_delay = delay
    set_points = np.linspace(start, stop, num_points)
    
    # Keep track of data and plots
    output = []
    data = []
    plots = []

    # Register each of the sweep parameters and set up a plot window for them
    for p, parameter in enumerate(param_meas):
        meas.register_parameter(parameter, setpoints=(param_set,))
        output.append([parameter, None])
        
        # Create plot window
        if append is not None and append:
            plot = win.items[0]
        else:
            plot = win.addPlot(title="%s (%s) v.<br>%s (%s)" % 
                               (param_set.full_name, param_set.label, 
                                parameter.full_name, parameter.label))
        
        # Figure out if we have 1d or 2d data
        if getattr(parameter, 'shape', None):
            # If we have 2d data, we need to know its length
            shape = parameter.shape[0]
            set_points_y = parameter.setpoints[0]
            
            # Create data array
            data.append(np.ndarray((num_points, shape)))
        else:
            # Create data arrays
            data.append(np.full(num_points, np.nan))
            set_points_y = None        

        plotdata = plot.plot(setpoint_x=set_points,
                             setpoint_y=set_points_y,
                             pen=(255,0,0), 
                             name=parameter.name)
        
        # Update axes
        if set_points_y is not None:
            plot.update_axes(param_set, parameter, param_y_setpoint=True)
            plotdata.update_histogram_axis(parameter)
        else:
            plot.update_axes(param_set, parameter)
        plots.append(plotdata)

    if wallcontrol is not None:    
        wallcontrol_start = wallcontrol.get()
        step = (stop-start)/num_points
    
    param_set.set(start)
    midas.capture_1d_trace()

    with meas.run() as datasaver:
        # Update plot titles
        win.win_title += "{} ".format(datasaver.run_id)
        for i in range(len(param_meas)):
            plots[p]._parent.plot_title += " (id: %d)" % datasaver.run_id
        
        # Then, run the actual sweep
        for i, set_point in enumerate(set_points):
            if wallcontrol is not None:
                wallcontrol.set(wallcontrol_start + i*step*wallcontrol_slope)
            param_set.set(set_point)
            midas.averaged_1d_trace()
            for p, parameter in enumerate(param_meas):
                midas_data = parameter.get()
                midas_data = signal.savgol_filter(midas_data, 15, 3)
                if differentiate:
                    midas_data = np.gradient(midas_data)
                output[p][1] = midas_data
                if getattr(parameter, 'shape', None) is not None:
                    data[p][i,:] = output[p][1] # Update 2D data
                    if i == 0:
                        data[p][1:] = (np.min(output[p][1]) + 
                                       np.max(output[p][1]))/2
                else:
                    data[p][i] = output[p][1] # Update 1D data
                
                # Update live plots
                plots[p].update(data[p])
            
            # Save data
            datasaver.add_result((param_set, set_point),
                                *output)
    
    if wallcontrol is not None:
        wallcontrol.set(wallcontrol_start)

    if save:
        plot_tools.save_figure(win, datasaver.run_id)
    return (datasaver.run_id, win)  # can use plot_by_id(dataid)