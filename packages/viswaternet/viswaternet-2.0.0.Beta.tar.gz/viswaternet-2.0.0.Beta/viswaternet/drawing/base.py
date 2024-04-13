# -*- coding: utf-8 -*-
"""
The viswaternet.utils.base module contains plotting functions that are 
frequently utilized by other plotting functions. This includes base element
drawing, legend drawing, color map, and label drawing functions.
"""
import numpy as np
import pandas as pd
import networkx.drawing.nx_pylab as nxp
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from viswaternet.utils import save_fig, normalize_parameter
from viswaternet.utils.markers import *


def draw_nodes(
        self,
        ax,
        node_list,
        parameter_results=None,
        vmin=None,
        vmax=None,
        node_size=None,
        node_color="k",
        cmap="tab10",
        node_shape=".",
        node_border_color="k",
        node_border_width=0,
        label=None,
        draw_tanks=True,
        draw_reservoirs=True):
    """Draws continuous nodal data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    node_list : string, array-like
        List of draw_nodes to be drawn.
        
    parameter_results : array-like
        The data associated with each node.
        
    vmin : integer
        The minimum value of the color bar. 
        
    vmax : integer
        The maximum value of the color bar.
        
    node_size : integer, array-like
        Integer representing all node sizes, or array of sizes for each node.
    
    node_color : string
        Color of the draw_nodes.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    node_shape : string
        Shape of the draw_nodes. Refer to matplotlib documentation for available marker types.
    
    node_border_color : string
        Color of the node borders.
    
    node_border_width : integer
        Width of the node borders.
    
    label : string
        Matplotlib label of plotting instance.
        
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
        
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    """
    
    # Initalize parameters
    model = self.model
    if parameter_results is None:
        parameter_results = pd.DataFrame([])
    # Creates default list of node sizes
    if node_size is None:
        node_size = (np.ones(len(node_list)) * 100).tolist()
    # Checks if some data values are given
    if parameter_results.values.tolist():
        # If values is less than this value, we treat it as a negative.
        node_list = [node_list[node_list.index(name)]
                     for name in node_list
                     if ((name not in model["tank_names"]
                          or draw_tanks is False)
                     and (name not in model["reservoir_names"]
                          or draw_reservoirs is False))]
        parameter_results = parameter_results.loc[node_list]
        parameter_results = parameter_results.values.tolist()
        if isinstance(node_size, tuple):
            min_size = node_size[0]
            max_size = node_size[1]
            if min_size is not None and max_size is not None:
                node_size = normalize_parameter(
                    parameter_results, min_size, max_size)
        if np.min(parameter_results) < -1e-5:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, set vmax to the max data
            # value and vmin to the negative of the max data value. This
            # ensures that the colorbar is centered at 0.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    vmax=np.max(parameter_results),
                    vmin=-np.max(parameter_results),
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color,
                    label=label)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    vmax=vmax,
                    vmin=vmin,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color,
                    label=label)
            # Return networkx object
            return g
        else:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, don't pass vmin and vmax,
            # as networkx will handle the limits of the colorbar
            # itself.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_nodes(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    nodelist=node_list,
                    node_size=node_size,
                    node_color=parameter_results,
                    cmap=cmap,
                    node_shape=node_shape,
                    linewidths=node_border_width,
                    edgecolors=node_border_color,
                    vmin=vmin,
                    vmax=vmax)
            # Return networkx object
            return g
    # Draw without any data associated with draw_nodes
    else:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=node_list,
            node_size=node_size,
            node_color=node_color,
            node_shape=node_shape,
            edgecolors=node_border_color,
            linewidths=node_border_width,
            label=label)


def draw_links(
        self,
        ax,
        link_list,
        parameter_results=None,
        edge_color="k",
        cmap="tab10",
        link_width=None,
        vmin=None,
        vmax=None,
        link_style='-',
        link_arrows=False,
        pump_element='node',
        draw_pumps=True,
        valve_element='node',
        draw_valves=True):
    """Draws continuous link data onto the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    link_list : string, array-like
        List of draw_links to be drawn.
    
    parameter_results : array-like
        The data associated with each node.
    
    edge_color : string
        Color of draw_links.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    vmin : integer
        The minimum value of the color bar. 
    
    vmax : integer
        The maximum value of the color bar.    
    
    link_width : integer, array-like
        Integer representing all link widths, or array of widths for each link.
    
    link_style : string
        The style (solid, dashed, dotted, etc.) of the draw_links. Refer to matplotlib documentation for available line styles.
    
    link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
   
    pump_element : string
        Determines if pumps are drawn as links or nodes.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
        
    valve_element : string
        Determines if valves are drawn as links or nodes.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    """
    # Initalize parameters
    model = self.model
    if isinstance(link_list, np.ndarray):
        link_list = link_list.tolist()
    if parameter_results is None:
        parameter_results = pd.DataFrame([])
    # Creates default list of link widths
    if link_width is None:
        link_width = (np.ones(len(link_list)) * 1).tolist()
    # Checks if some data values are given
    if parameter_results.values.tolist():
        link_list = [link_list[link_list.index(name)]
                     for name in link_list
                     if ((name not in model["pump_names"]
                          or pump_element == 'node'
                          or draw_pumps is False)
                     and (name not in model["valve_names"]
                          or valve_element == 'node'
                          or draw_valves is False))]
        edges = [model["pipe_list"][model['G_pipe_name_list'].index(name)]
                 for name in link_list]
        parameter_results = parameter_results.loc[link_list]
        parameter_results = parameter_results.values.tolist()
        if isinstance(link_width, tuple):
            min_size = link_width[0]
            max_size = link_width[1]
            if min_size is not None and max_size is not None:
                link_width = normalize_parameter(
                    parameter_results, min_size, max_size)
        if np.min(parameter_results) < -1e-5:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, set vmax to the max data
            # value and vmin to the negative of the max data value. This
            # ensures that the colorbar is centered at 0.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_vmax=np.max(parameter_results),
                    edge_vmin=-np.max(parameter_results),
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_vmax=vmax,
                    edge_vmin=vmin,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Return networkx object
            return g
        else:
            # Gets the cmap object from matplotlib
            cmap = mpl.colormaps[cmap]
            # If both vmin and vmax are None, don't pass vmin and vmax,
            # as networkx will handle the limits of the colorbar
            # itself.
            if vmin is None and vmax is None:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    node_size=0)
            # Otherwise, just pass the user-given parameters
            else:
                g = nxp.draw_networkx_edges(
                    model["G"],
                    model["pos_dict"],
                    ax=ax,
                    edgelist=edges,
                    edge_color=parameter_results,
                    edge_cmap=cmap,
                    style=link_style,
                    arrows=link_arrows,
                    width=link_width,
                    edge_vmin=vmin,
                    edge_vmax=vmax,
                    node_size=0)
            # Return networkx object
            return g
    # Draw without any data associated with draw_links
    else:
        edges = ([model["pipe_list"][i]
                  for i, name in enumerate(link_list)])
        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            ax=ax,
            edgelist=edges,
            edge_color=edge_color,
            style=link_style,
            arrows=link_arrows,
            width=link_width,
            node_size=0)


def draw_base_elements(
        self,
        ax,
        draw_nodes=True,
        draw_links=True,
        draw_reservoirs=True,
        draw_tanks=True,
        draw_pumps=True,
        draw_valves=True,
        include_pumps=True,
        include_valves=True,
        include_reservoirs=True,
        include_tanks=True,
        element_list=None,
        legend=True,
        reservoir_size=150,
        reservoir_color='k',
        reservoir_shape=epa_res,
        reservoir_border_color='k',
        reservoir_border_width=3,
        tank_size=200,
        tank_color='k',
        tank_shape=epa_tank,
        tank_border_color='k',
        tank_border_width=2,
        valve_element='node',
        valve_size=200,
        valve_color='k',
        valve_shape=epa_valve,
        valve_border_color='k',
        valve_border_width=1,
        valve_width=3,
        valve_line_style='-',
        valve_arrows=False,
        pump_element='node',
        pump_size=200,
        pump_color='k',
        pump_shape=epa_pump,
        pump_border_color='k',
        pump_border_width=1,
        pump_width=3,
        pump_line_style='-',
        pump_arrows=False,
        base_node_color='k',
        base_node_size=30,
        base_link_color='k',
        base_link_width=1,
        base_link_line_style='-',
        base_link_arrows=False):
    """
    Draws base elements (draw_nodes, draw_links, draw_reservoirs, draw_tanks, draw_pumps, and draw_valves)
    without any data associated with the elements.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
        
    draw_nodes : boolean
        Determines if base draw_nodes with no data associated with them are drawn. Set to False for all functions excep plot_basic_elements by default.
    
    draw_links : boolean
        Determines if base draw_links with no data associated with them are drawn. Set to False for all functions that deal with link data plotting.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    legend : boolean
        Determines if the base elements legend will be drawn. 
    
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
    
    reservoir_color : string
        The color of the reservoir marker. Refer to matplotlib documentation for available colors.
    
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for available marker types.
    
    reservoir_border_color : string
        The color of the border around the reservoir marker.
    
    reservoir_border_width : integer
        The width in points of the border around the reservoir marker.
    
    tank_size : integer
        The size of the tank marker on the plot in points^2. 
    
    tank_color : string
        The color of the tank marker.
    
    tank_shape : string
        The shape of the tank marker.
    
    tank_border_color : string
        The color of the border around the tank marker.
    
    tank_border_width : integer
        The width in points of the border around the tank marker.
    
    valve_elememt : string
        Determines whether the valves are drawn as links or nodes.
    
    valve_size : integer
        The size of the valve marker on the plot in points^2. 
    
    valve_color : string
        The color of the valve marker.
    
    valve_shape : string
        The shape of the valve marker.
    
    valve_border_color : string
        The color of the border around the valve marker.
    
    valve_border_width : integer
        The width in points of the border around the valve marker.
    
    valve_width : integer
        The width of the valve line in points
    
    valve_line_style : string
        The line style of valves if they are drawn as links. Refer to matplotlib documentation for available line styles.
    
    valve_arrows : boolean
       Determines if an arrow is drawn in the direction of flow of the valves. 
   
    pump_element : string
       Determines if pumps are drawn as links or nodes. 
        
    pump_size : integer
        The size of the pump marker on the plot in points^2.
        
    pump_color : string
        The color of the pump line.
    
    pump_shape : string
        The shape of the pump marker.
    
    pump_border_color : string
        The color of the border around the pump marker.
    
    pump_border_width : integer
        The width in points of the border around the pump marker.
    
    pump_width : integer
        The width of the pump line in points.
    
    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.
    
    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    base_node_color : string
        The color of the draw_nodes without data associated with them.
    
    base_node_size : integer
        The size of the draw_nodes without data associated with them in points^2.
    
    base_link_color : string
        The color of the draw_links without data associated with them.
    
    base_link_width : integer
        The width of the draw_links without data associated with them in points.
    
    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the draw_links with no data associated with them.
    
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the draw_links with no data associated with them.
    """
    model = self.model
    # If draw_nodes is True, then draw draw_nodes
    if draw_nodes:
        node_list = model['node_names']
        if element_list is None:
            node_list = [node_list[node_list.index(name)]
                         for name in node_list
                         if ((name not in model["tank_names"]
                              or draw_tanks is False)
                         and (name not in model["reservoir_names"]
                              or draw_reservoirs is False))]
        else:
            node_list = [node_list[node_list.index(name)]
                         for name in node_list
                         if ((name not in model["tank_names"]
                              or draw_tanks is False)
                         and (name not in model["reservoir_names"]
                              or draw_reservoirs is False)
                         and (name not in element_list))]
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            node_size=base_node_size,
            nodelist=node_list,
            node_color=base_node_color,
            ax=ax)
    # If draw_reservoirs is True, then draw draw_reservoirs
    if draw_reservoirs:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=model["reservoir_names"],
            node_size=reservoir_size,
            node_color=reservoir_color,
            edgecolors=reservoir_border_color,
            linewidths=reservoir_border_width,
            node_shape=reservoir_shape,
            label="Reservoirs")
    # If draw_tanks is True, then draw draw_tanks
    if draw_tanks:
        nxp.draw_networkx_nodes(
            model["G"],
            model["pos_dict"],
            ax=ax,
            nodelist=model["tank_names"],
            node_size=tank_size,
            node_color=tank_color,
            edgecolors=tank_border_color,
            linewidths=tank_border_width,
            node_shape=tank_shape,
            label="Tanks")
    # If draw_links is True, then draw draw_links
    if draw_links:
        pipe_name_list = model['G_pipe_name_list']
        if element_list is None:
            edgelist = [model['pipe_list'][pipe_name_list.index(name)]
                        for name in pipe_name_list
                        if ((name not in model["pump_names"]
                             or pump_element == 'node'
                             or draw_pumps is False)
                        and (name not in model["valve_names"]
                             or valve_element == 'node'
                             or draw_valves is False))]
        else:
            edgelist = [model['pipe_list'][pipe_name_list.index(name)]
                        for name in pipe_name_list
                        if ((name not in model["pump_names"]
                             or pump_element == 'node'
                             or draw_pumps is False)
                        and (name not in model["valve_names"]
                             or valve_element == 'node'
                             or draw_valves is False)
                        and (name not in element_list))]
        nxp.draw_networkx_edges(
            model["G"],
            model["pos_dict"],
            edgelist=edgelist,
            ax=ax,
            edge_color=base_link_color,
            width=base_link_width,
            style=base_link_line_style,
            arrows=base_link_arrows)
    # If draw_valves is True, then draw draw_valves
    if draw_valves:
        if valve_element == 'node':
            valve_coordinates = {}
            # For each valve, calculate midpoint along link it is located at
            # then store the coordinates of where valve should be drawn
            for i, (point1, point2) in enumerate(model["G_list_valves_only"]):
                midpoint = [(model["wn"].get_node(point1).coordinates[0]
                             + model["wn"].get_node(point2).coordinates[0])/2,
                            (model["wn"].get_node(point1).coordinates[1]
                             + model["wn"].get_node(point2).coordinates[1])/2]
                valve_coordinates[model["valve_names"][i]] = midpoint
            # Draw draw_valves after midpoint calculations
            nxp.draw_networkx_nodes(
                model["G"],
                valve_coordinates,
                ax=ax,
                nodelist=model["valve_names"],
                node_size=valve_size,
                node_color=valve_color,
                edgecolors=valve_border_color,
                linewidths=valve_border_width,
                node_shape=valve_shape,
                label="Valves")
        elif valve_element == 'link':
            nxp.draw_networkx_edges(
                model["G"],
                model["pos_dict"],
                ax=ax,
                edgelist=model["G_list_valves_only"],
                edge_color=valve_color,
                width=valve_width,
                style=valve_line_style,
                arrows=valve_arrows)
    # If draw_pumps is True, then draw draw_pumps
    if draw_pumps:
        if pump_element == 'node':
            pump_coordinates = {}
            # For each valve, calculate midpoint along link it is located at
            # then store the coordinates of where pump should be drawn
            for i, (point1, point2) in enumerate(model["G_list_pumps_only"]):
                midpoint = [(model["wn"].get_node(point1).coordinates[0]
                             + model["wn"].get_node(point2).coordinates[0])/2,
                            (model["wn"].get_node(point1).coordinates[1]
                             + model["wn"].get_node(point2).coordinates[1])/2]
                pump_coordinates[model["pump_names"][i]] = midpoint
            # Draw draw_valves after midpoint calculations
            nxp.draw_networkx_nodes(
                model["G"],
                pump_coordinates,
                ax=ax,
                nodelist=model["pump_names"],
                node_size=pump_size,
                node_color=pump_color,
                edgecolors=pump_border_color,
                linewidths=pump_border_width,
                node_shape=pump_shape,
                label="Pumps")
        elif pump_element == 'link':
            nxp.draw_networkx_edges(
                model["G"],
                model["pos_dict"],
                ax=ax,
                edgelist=model["G_list_pumps_only"],
                edge_color=pump_color,
                width=pump_width,
                style=pump_line_style,
                arrows=pump_arrows)


def plot_basic_elements(
        self,
        ax=None,
        draw_nodes=True,
        draw_links=True,
        draw_reservoirs=True,
        draw_tanks=True,
        draw_pumps=True,
        draw_valves=True,
        savefig=False,
        save_name=None,
        dpi='figure',
        save_format='png',
        legend=True,
        base_legend_loc="upper right",
        base_legend_label_font_size=15,
        base_legend_label_color='k',
        draw_legend_frame=False,
        reservoir_size=150,
        reservoir_color='k',
        reservoir_shape=epa_res,
        reservoir_border_color='k',
        reservoir_border_width=3,
        tank_size=200,
        tank_color='k',
        tank_shape=epa_tank,
        tank_border_color='k',
        tank_border_width=2,
        valve_element='node',
        valve_size=200,
        valve_color='k',
        valve_shape=epa_valve,
        valve_border_color='k',
        valve_border_width=1,
        valve_width=3,
        valve_line_style='-',
        valve_arrows=False,
        pump_element='node',
        pump_size=200,
        pump_color='k',
        pump_shape=epa_pump,
        pump_border_color='k',
        pump_border_width=1,
        pump_width=3,
        pump_line_style='-',
        pump_arrows=False,
        base_node_color='k',
        base_node_size=30,
        base_link_color='k',
        base_link_width=1,
        base_link_line_style='-',
        base_link_arrows=False):
    """User-level function that draws base elements with no data assocaited with
    them, draws a legend, and saves the figure.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
   
    draw_nodes : boolean
        Determines if base draw_nodes with no data associated with them are drawn. Set to False for all functions excep plot_basic_elements by default.
    
    draw_links : boolean
        Determines if base draw_links with no data associated with them are drawn. Set to False for all functions that deal with link data plotting.
    
    draw_reservoirs : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_tanks : boolean
        Determines if draw_reservoirs with no data associated with them are drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
    
    savefig : boolean
        Determines if the figure is saved. 
    
    save_name : string
        The inputted string will be appended to the name of the network.
    
        Example
        -------
        >>>import viswaternet as vis
        >>>model = vis.VisWNModel(r'Networks/Net3.inp')
        ...
        >>>model.save_fig(save_name='_example')
        <Net3_example.png>
    
    dpi : int, string
        The dpi that the figure will be saved with.
    
    save_format : string
        The file format that the figure will be saved as.
    
    legend : boolean
        Determines if the base elements legend will be drawn. 
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_label_font_size : integer
        The font size of the non-title text for legends. 
    
    base_legend_label_color : string
        The color of the legend text. Refer to matplotlib documentation for available colors.

    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
    reservoir_size : integer
        The size of the reservoir marker on the plot in points^2. 
    
    reservoir_color : string
        The color of the reservoir marker.
    
    reservoir_shape : string
        The shape of the reservoir marker. Refer to matplotlib documentation for available marker types.
    
    reservoir_border_color : string
        The color of the border around the reservoir marker.
    
    reservoir_border_width : integer
        The width in points of the border around the reservoir marker.
    
    tank_size : integer
        The size of the tank marker on the plot in points^2. 
    
    tank_color : string
        The color of the tank marker.
    
    tank_shape : string
        The shape of the tank marker.
    
    tank_border_color : string
        The color of the border around the tank marker.
    
    tank_border_width : integer
        The width in points of the border around the tank marker.
    
    valve_elememt : string
        Determines whether the valves are drawn as links or nodes.
    
    valve_size : integer
        The size of the valve marker on the plot in points^2. 
    
    valve_color : string
        The color of the valve marker.
    
    valve_shape : string
        The shape of the valve marker.
    
    valve_border_color : string
        The color of the border around the valve marker.
    
    valve_border_width : integer
        The width in points of the border around the valve marker.
    
    valve_width : integer
        The width of the valve line in points
    
    valve_line_style : string
        The line style of valves if they are drawn as links. Refer to matplotlib documentation for available line styles.
    
    valve_arrows : boolean
       Determines if an arrow is drawn in the direction of flow of the valves. 
   
    pump_element : string
       Determines if pumps are drawn as links or nodes. 
        
    pump_size : integer
        The size of the pump marker on the plot in points^2.
        
    pump_color : string
        The color of the pump line.
    
    pump_shape : string
        The shape of the pump marker.
    
    pump_border_color : string
        The color of the border around the pump marker.
    
    pump_border_width : integer
        The width in points of the border around the pump marker.
    
    pump_width : integer
        The width of the pump line in points.
    
    pump_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles.
    
    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    base_node_color : string
        The color of the draw_nodes without data associated with them.
    
    base_node_size : integer
        The size of the draw_nodes without data associated with them in points^2.
    
    base_link_color : string
        The color of the draw_links without data associated with them.
    
    base_link_width : integer
        The width of the draw_links without data associated with them in points.
    
    base_link_line_style : string
        The style (solid, dashed, dotted, etc) of the draw_links with no data associated with them.
    
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the draw_links with no data associated with them.
    """
    # Checks if there is no draw_pumps
    if not self.model['G_list_pumps_only']:
        draw_pumps = False
    # Checks if an axis as been specified
    if ax is None:
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
            ax.set_frame_on(self.axis_frame)
    # Draw all base elements w/o data associated with them
    draw_base_elements(
        self,
        ax,
        draw_nodes=draw_nodes,
        draw_reservoirs=draw_reservoirs,
        draw_tanks=draw_tanks,
        draw_links=draw_links,
        draw_valves=draw_valves,
        draw_pumps=draw_pumps,
        reservoir_size=reservoir_size,
        reservoir_color=reservoir_color,
        reservoir_shape=reservoir_shape,
        reservoir_border_color=reservoir_border_color,
        reservoir_border_width=reservoir_border_width,
        tank_size=tank_size,
        tank_color=tank_color,
        tank_shape=tank_shape,
        tank_border_color=tank_border_color,
        tank_border_width=tank_border_width,
        valve_element=valve_element,
        valve_size=valve_size,
        valve_color=valve_color,
        valve_shape=valve_shape,
        valve_border_color=valve_border_color,
        valve_border_width=valve_border_width,
        valve_width=valve_width,
        valve_line_style=valve_line_style,
        valve_arrows=valve_arrows,
        pump_element=pump_element,
        pump_size=pump_size,
        pump_color=pump_color,
        pump_shape=pump_shape,
        pump_border_color=pump_border_color,
        pump_border_width=pump_border_width,
        pump_width=pump_width,
        pump_line_style=pump_line_style,
        pump_arrows=pump_arrows,
        base_node_color=base_node_color,
        base_node_size=base_node_size,
        base_link_color=base_link_color,
        base_link_width=base_link_width,
        base_link_line_style=base_link_line_style,
        base_link_arrows=base_link_arrows)
    # Draw legend if legend is True. Only draws base elements legend
    if legend:
        draw_legend(
            ax,
            draw_pumps=draw_pumps,
            base_legend_loc=base_legend_loc,
            base_legend_label_color=base_legend_label_color,
            base_legend_label_font_size=base_legend_label_font_size,
            draw_legend_frame=draw_legend_frame,
            pump_color=pump_color,
            base_link_color=base_link_color,
            pump_line_style=pump_line_style,
            base_link_line_style=base_link_line_style,
            base_link_arrows=base_link_arrows,
            pump_arrows=pump_arrows,
            draw_links=True,
            draw_valves=draw_valves,
            valve_element=valve_element,
            valve_line_style=valve_line_style,
            valve_color=valve_color,
            valve_arrows=valve_arrows,
            pump_element=pump_element)
    # Save figure if savefig is set to True
    if savefig:
        save_fig(self, save_name=save_name, dpi=dpi, save_format=save_format)


def draw_legend(
        ax,
        intervals=None,
        title=None,
        draw_pumps=True,
        pump_element='node',
        draw_valves=True,
        valve_element='node',
        base_legend_loc="upper right",
        discrete_legend_loc="lower right",
        base_legend_label_font_size=15,
        base_legend_label_color="k",
        discrete_legend_label_font_size=15,
        discrete_legend_label_color="k",
        discrete_legend_title_font_size=17,
        discrete_legend_title_color='k',
        cmap=None,
        color_list=None,
        draw_legend_frame=False,
        pump_color='b',
        valve_color='orange',
        valve_line_style='-',
        valve_arrows=False,
        base_link_color='k',
        node_size=None,
        link_width=None,
        element_size_intervals=None,
        element_size_legend_title=None,
        element_size_legend_loc=None,
        element_size_legend_labels=None,
        draw_base_legend=True,
        draw_discrete_legend=True,
        node_border_color='k',
        linewidths=1,
        pump_line_style='-',
        base_link_line_style='-',
        base_link_arrows=False,
        pump_arrows=False,
        draw_links=True):
    """Draws the legends for all other plotting functions. There are two legends that might be drawn. One is the base elements legend with displays what markers are associated with each element type (draw_nodes, draw_links, etc.) The other legend is the intervals legend which is the legend for discrete drawing. Under normal use, draw_legends is not normally called by the user directly, even with more advanced applications. However, some specialized plots may require draw_legend to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
   
    intervals : array-like, string
        If set to 'automatic' then intervals are created automatically on a equal interval basis. Otherwise, it is the edges of the intervals to be created. intervals array length should be num_intervals + 1.
    
    color_list : string, array-like
        The list of node colors for each interval. Both cmap and color_list can not be used at the same time to color draw_nodes. If both are, then color_list takes priority.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    title : string
        The title text of the legend.
    
    draw_discrete_legend : boolean
        Determine if the intervals legend is drawn.
    
    discrete_legend_loc : string
        The location of the intervals legend on the figure.
    
    discrete_legend_label_font_size : integer
        The font size of the intervals legend text.
    
    discrete_legend_label_color : string
        The color of the intervals legend text. Refer to matplotlib documentation for available colors.
    
    discrete_legend_title_font_size : integer
        The font size of the title text for the intervals legend.
    
    discrete_legend_title_color : string
        The color of the title tect for the intervals legend.
    
    draw_base_legend : boolean
        Determine if the base elements legend is drawn.
    
    base_legend_loc : string
        The location of the base elements legend on the figure. Refer to matplotlib documentation for possible inputs.
    
    base_legend_label_font_size : integer
        The font size of the non-title text for the base elements legend. 
    
    base_legend_label_color : string
        The color of the legend text. Refer to matplotlib documentation for available colors.
    
    draw_legend_frame : boolean
        Determines if the frame around the legend is drawn.
    
    draw_pumps : boolean
        Determines if draw_pumps with no data associated with them are drawn.
    
    pump_element : string
        Determines if pumps are drawn as links or nodes. 
    
    pump_color : string
        The color of the pump line.
        
    pump_line_style
       The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles. 
    
    pump_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the pump.
    
    draw_valves : boolean
        Determines if draw_valves with no data associated with them are drawn.
        
    valve_element : string
        Determines if valves are drawn as links or nodes.
        
    valve_color : string
        The color of the valve line.
        
    valve_line_style : string
        The style (solid, dashed, dotted, etc.) of the pump line. Refer to matplotlib documentation for available line styles. 
    
    valve_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the valve.
   
    draw_links : boolean
        Determines if draw_links with no data associated with them are drawn.
    
    base_link_color : string
        The color of the draw_links without data associated with them.
        
    base_link_line_style : string
        The style (solid, dashed, dotted, etc.) of draw_links with no data associated with them.
    
    base_link_arrows : boolean
        Determines if an arrow is drawn in the direction of flow of the draw_links with no data associated with them.
    
    node_size : integer, array-like
        The size of the node elements. Can either be an integer if the node sizes are uniform, or an array-like if variable node sizes are present.
    
    link_width : integer, array-like
        The width of the link elements. Can either be an integer if the link sizes are uniform, or an array-like if variable link sizes are present.
    
    element_size_intervals : integer
        The number of intervals to be used if an element size legend is used.
    
    element_size_legend_title : string
        The title of the element size legend.
    
    element_size_legend_loc : string
        The location of the element size legend on the figure.
    
    element_size_legend_labels : array-like
        The labels of each interval of the element size legend.
    
    node_border_color : string
        The color of the legend draw_nodes edges when plotting element size legend.
    
    linewidths: integer
        The width of the line of the legend draw_nodes when plotting element size legend.
    """
    # If no intervals for data legend are specified, then create empty array
    if intervals is None:
        intervals = []
    # Get handles, labels
    handles, labels = ax.get_legend_handles_labels()

    # Where new handles will be stored
    extensions = []

    # If draw_pumps is True, then add legend element. Note that right now
    # pump_arrows does not affect legend entry, but that it may in the future,
    # hence the if statement
    if draw_pumps and pump_element == 'link':
        if pump_arrows:
            extensions.append(Line2D([0], [0], color=pump_color,
                              linestyle=pump_line_style, lw=4, label='Pumps'))
        else:
            extensions.append(Line2D([0], [0], color=pump_color,
                              linestyle=pump_line_style, lw=4, label='Pumps'))
    if draw_valves and valve_element == 'link':
        if valve_arrows:
            extensions.append(Line2D([0], [0], color=valve_color,
                              linestyle=valve_line_style, lw=4,
                              label='Valves'))
        else:
            extensions.append(Line2D([0], [0], color=valve_color,
                              linestyle=valve_line_style, lw=4,
                              label='Valves'))
    # If draw_base_links is True, then add legend element. Note that right now
    # base_link_arrows does not affect legend entry, but that it may in the
    # future, hence the if statement
    if draw_links:
        if base_link_arrows:
            extensions.append(Line2D([0], [0], color=base_link_color,
                              linestyle=base_link_line_style, lw=4,
                              label='Pipes'))
        else:
            extensions.append(Line2D([0], [0], color=base_link_color,
                              linestyle=base_link_line_style, lw=4,
                              label='Pipes'))
    # Extend handles list
    handles.extend(extensions)

    # If discrete intervals are given
    if intervals:
        # Draws base legend, which includes the legend for draw_reservoirs,
        # draw_tanks, and so on
        if draw_base_legend is True:
            legend = ax.legend(handles=handles[len(intervals):],
                               loc=base_legend_loc,
                               fontsize=base_legend_label_font_size,
                               labelcolor=base_legend_label_color,
                               frameon=draw_legend_frame)
            # Align legend text to the left, add legend to ax
            legend._legend_box.align = "left"
            ax.add_artist(legend)
        # Draws intervals, or data, legend to the ax
        if draw_discrete_legend is True:
            if isinstance(discrete_legend_label_color, str) \
                    and discrete_legend_label_color != 'interval_color':
                legend2 = ax.legend(
                    title=title,
                    handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    labelcolor=discrete_legend_label_color,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)

            if discrete_legend_label_color == 'interval_color':
                legend2 = ax.legend(
                    title=title, handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)
                if color_list:
                    for i, text in enumerate(legend2.get_texts()):
                        text.set_color(color_list[i])
                elif cmap:
                    cmap = mpl.colormaps[cmap]
                    cmap_value = 1 / len(intervals)
                    for i, text in enumerate(legend2.get_texts()):
                        text.set_color(cmap(float(cmap_value)))
                        cmap_value += 1 / len(intervals)
            if isinstance(discrete_legend_label_color, list):
                legend2 = ax.legend(
                    title=title,
                    handles=handles[: len(intervals)],
                    loc=discrete_legend_loc,
                    fontsize=discrete_legend_label_font_size,
                    title_fontsize=discrete_legend_title_font_size,
                    frameon=draw_legend_frame)
                for i, text in enumerate(legend2.get_texts()):
                    text.set_color(discrete_legend_label_color[i])
            # Align legend text to the left, adds title, and adds to ax
            legend2._legend_box.align = "left"
            legend2.get_title().set_color(discrete_legend_title_color)
            ax.add_artist(legend2)
    # If there are no intervals, just draw base legend
    else:
        # Draws base legend, which includes the legend for draw_reservoirs,
        # draw_tanks, and so on
        if draw_base_legend is True:
            legend = ax.legend(handles=handles,
                               loc=base_legend_loc,
                               fontsize=base_legend_label_font_size,
                               labelcolor=base_legend_label_color,
                               frameon=draw_legend_frame)
            # Align legend text to the left, add legend to ax
            legend._legend_box.align = "left"
            ax.add_artist(legend)

    # The following code is for a node/link legend. This adds a 2nd dimension
    # to the data that can be plotted, by allowing for changes in size of
    # a node/link to represent some parameter. For now it is limited to
    # discrete node sizes, which works the same as discrete data for the color
    # of draw_nodes. To use it requires a much more involved process than all
    # other functions that viswaternet performs, and improvements to ease of
    # use will be made in the future.
    if node_size is not None and element_size_intervals is not None:
        if isinstance(node_size, list):
            handles_2 = []
            min_size = np.min(node_size)
            max_size = np.max(node_size)
            marker_sizes = np.linspace(
                min_size, max_size, element_size_intervals)
            for size, label in zip(marker_sizes, element_size_legend_labels):
                handles_2.append(Line2D([], [], marker='.', color='w',
                                 markeredgecolor=node_border_color,
                                 markeredgewidth=linewidths,
                                 label=label, markerfacecolor='k',
                                 markersize=np.sqrt(size)))
            legend3 = ax.legend(
                handles=handles_2,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=discrete_legend_label_font_size,  # Change later!
                title_fontsize=discrete_legend_title_font_size,
                labelcolor=discrete_legend_label_color,
                frameon=draw_legend_frame)
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)
    if link_width is not None and element_size_intervals is not None:
        if isinstance(link_width, list):
            handles_2 = []
            min_size = np.min(link_width)
            max_size = np.max(link_width)
            marker_sizes = np.linspace(
                min_size, max_size, element_size_intervals)
            for size, label in zip(marker_sizes, element_size_legend_labels):
                handles_2.append(Line2D([], [], marker=None, color='k',
                                 linewidth=size, label=label))
            legend3 = ax.legend(
                handles=handles_2,
                title=element_size_legend_title,
                loc=element_size_legend_loc,
                fontsize=discrete_legend_label_font_size,
                title_fontsize=discrete_legend_title_font_size,
                labelcolor=discrete_legend_label_color,
                frameon=draw_legend_frame)
            legend3._legend_box.align = "left"
            ax.add_artist(legend3)


def draw_color_bar(
        ax,
        g,
        cmap,
        color_bar_title=None,
        color_bar_width=0.03,
        color_bar_height=0.8):
    """Draws the color bar for all continuous plotting functions.Like draw_legends, under normal use, draw_color_bar is not normally called by the user directly, even with more advanced applications. However, some specialized plots may require draw_color_bar to be called directly.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    g : NetworkX path collection
        The list of elements drawn by NetworkX function.
    
    cmap : string
        The matplotlib color map to be used for plotting. Refer to matplotlib documentation for possible inputs.
    
    color_bar_title : string
        The title of the color bar.
    
    color_bar_width : integer
        Width of color bar.
        
    color_bar_height : integer
        Height of color bar.
    """
    # Unruly code to make colorbar location nice and symmetrical when dealing
    # with subplots especially.
    divider = make_axes_locatable(ax)
    fig = plt.gcf()
    cax = fig.add_axes([divider.get_position()[0]+divider.get_position()[2]
                        + 0.02, (divider.get_position()[1])
                        + ((divider.get_position()[3]
                            * (1-color_bar_height)))/2,
                        color_bar_width,
                        divider.get_position()[3]*color_bar_height])
    cbar = fig.colorbar(g, cax=cax)
    cbar.set_label(color_bar_title, fontsize=10)


def draw_label(
        self,
        labels,
        x_coords,
        y_coords,
        ax=None,
        draw_nodes=None,
        draw_arrow=True,
        label_font_size=11,
        label_text_color='k',
        label_face_color='white',
        label_edge_color='k',
        label_alpha=0.9,
        label_font_style=None,
        label_edge_width=None
        ):
    """Draws customizable labels on the figure.
    There are two modes of coordinate input: If the 'draw_nodes' argument is not specified, then the label coordinates are processed as absolute coordinates with possible values from 0 to 1. For instance, (0,0) would place the label in the bottom left of the figure, while (1,1) would place the label in the top right of the figure. If the 'draw_nodes' argument IS specified, then the coordinates are processed as coordinates relative to it's associated node. The scale of the coordinates scaling differs between networks. For instance, (50,100) would place the label 50 units to the right, and 100 units above the associated node.
    
    Arguments
    ---------
    ax : axes._subplots.AxesSubplot
        Matplotlib axes object.
    
    labels : string, array-like
        The label(s) textual content.
    
    x_coords : integer, array-like
        The x coordinate(s) of the labels.
    
    y_coords : integer, array-like
        The y coordinate(s) of the labels.
    
    draw_nodes : string, array-like
        A list of the draw_nodes the labels are to be associated with.
    
    draw_arrow : boolean
        Determine if an arrow is drawn from the associated draw_nodes to labels.
    
    label_font_size : integer
        The font size of the labels.
        
    label_text_color : string
        The color of the text of the labels.
        
    label_face_color : string
    
    label_edge_color : string
    
    label_alpha : integer
    
    label_font_style : string
        
    label_edge_width : integer
    """
    model = self.model
    if ax is None:
        ax = self.ax
    if draw_nodes is not None:
        for label, node, xCoord, yCoord in \
                zip(labels, draw_nodes, x_coords, y_coords):
            if draw_arrow:
                edge_list = []
                if label == node:
                    pass
                else:
                    model["G"].add_node(label, pos=(xCoord, yCoord))
                    model["pos_dict"][label] = (
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord)
                    edge_list.append((node, label))
                    nxp.draw_networkx_edges(
                        model["G"], model["pos_dict"], edgelist=edge_list,
                        edge_color="g", width=0.8, arrows=False)
                    model["G"].remove_node(label)
                    model["pos_dict"].pop(label, None)
                    edge_list.append((node, label))
            if draw_arrow is True:
                if xCoord < 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        color=label_text_color,
                        style=label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha,
                                  edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="right",
                        verticalalignment="center",
                        fontsize=label_font_size)
                if xCoord >= 0:
                    ax.text(
                        model["wn"].get_node(node).coordinates[0] + xCoord,
                        model["wn"].get_node(node).coordinates[1] + yCoord,
                        s=label,
                        color=label_text_color,
                        style=label_font_style,
                        bbox=dict(facecolor=label_face_color,
                                  alpha=label_alpha,
                                  edgecolor=label_edge_color,
                                  lw=label_edge_width),
                        horizontalalignment="left",
                        verticalalignment="center",
                        fontsize=label_font_size)
            else:
                ax.text(
                    model["wn"].get_node(node).coordinates[0] + xCoord,
                    model["wn"].get_node(node).coordinates[1] + yCoord,
                    s=label, color=label_text_color, style=label_font_style,
                    bbox=dict(facecolor=label_face_color,
                              alpha=label_alpha, edgecolor=label_edge_color,
                              lw=label_edge_width),
                    horizontalalignment="center",
                    verticalalignment="center", fontsize=label_font_size)
    elif draw_nodes is None:
        for label, xCoord, yCoord in zip(labels, x_coords, y_coords):
            ax.text(
                xCoord,
                yCoord,
                s=label,
                color=label_text_color,
                style=label_font_style,
                bbox=dict(facecolor=label_face_color,
                          alpha=label_alpha,
                          edgecolor=label_edge_color,
                          lw=label_edge_width),
                horizontalalignment="center",
                fontsize=label_font_size,
                transform=ax.transAxes)
