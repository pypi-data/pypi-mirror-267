import numpy as np
from math import prod as mprod




class Pathway(object):
    """A class handeling a pathway."""


    @classmethod
    def _convert_intset(cls, obj):
        """Convert an object to a set of integers."""
        
        if hasattr(obj, '__iter__'):
            intset = set([int(x) for x in obj])
        else:
            intset = set([int(obj)])

        return intset
    
    
    @classmethod
    def _convert_intlist(cls, obj):
        """Convert an object to a list of integers."""
        
        if hasattr(obj, '__iter__'):
            intlist = [int(x) for x in obj]
        else:
            intlist = [int(obj)]
        
        return intlist
    
    
    @classmethod
    def _convert_inttuple(cls, obj):
        """Convert an object to a tuple of integers."""
        
        if hasattr(obj, '__iter__'):
            inttuple = tuple(int(x) for x in obj)
        else:
            inttuple = (int(obj),)
            
        return inttuple


    @classmethod
    def _convert_unique_intlist(cls, obj):
        """Convert an object to a sorted list of unique integers."""
        
        if hasattr(obj, '__iter__'):
            intlist = [int(x) for x in obj]
        else:
            intlist = [int(obj)]
        
        return sorted(set(intlist))
    
    
    
    def __init__(self, layers):
        """Initialize Pathway object."""
        
        self._layers = []
        self._metadata = []
        self._n_paths = None
        
        if not isinstance(layers, list):
            raise TypeError("Given layers must be list.")
        
        for layer in layers:
            
            nodes = self._convert_unique_intlist(layer)
            if len(nodes) == 0:
                self._layers = [[] for i in range(len(layers))]
                self._metadata = [dict() for i in range(len(layers))]
                break
            self._layers.append(nodes)
            
            connections = dict()
            for node in nodes:
                if layer[node] is None:
                    connections.update({node: [None, 0]})
                else:
                    connections.update({node: [self._convert_unique_intlist(layer[node]), 0]})
            self._metadata.append(connections)
        
        # fix the input (should not be neccassary)
        self._fix()
        
        # check own consistency
        is_valid, msg = self._validate_self()
        if not is_valid:
            raise RuntimeError("Could not set up Pathway object (message: '{}').".format(msg))
        
        # initialize the branch sizes
        self._init_branch_sizes()
    
    
    
    def _norm_layer_idx(self, idx):
        """Normalize a layer index for internal use.
        
        A layer index is an integer between `-n_layers` and `n_layers-1` where
        `n_layers` is the number of layers in the Pathway object.
        
        Parameters
        ----------
        idx : int castable
            Layer index to normalize.
        
        Returns
        -------
        norm_idx : int
            Normalized layer index between 0 and `n_layers-1`.
        """
        
        idx = int(idx)
        n_layers = len(self._layers)
        if idx >= n_layers or idx < -n_layers:
            raise IndexError("layer index {} out of range for Pathway object with {} layers".format(idx,n_layers))
        idx = idx % n_layers
        
        return idx
        
    
    def _norm_given_path(self, path):
        """Normalize and check a given path for internal use.
        
        Parameters
        ----------
        path : list
            Path to normalize.
        
        Returns
        -------
        norm_path : list
            Normalized path.
        """
        
        path = self._convert_intlist(path)
        
        if not len(path) == len(self._layers):
            raise ValueError("Given path is of length {} but Pathway object has {} layers.".format(len(path), len(self._layers)))
        
        return path
        
        
        
    
    
    
    def _validate_self(self):
        """Validate the consisteny of internal data objects.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        is_valid : bool
            Whether self is a valid Pathway object.
        msg : str
            Message giving more information about why the Pathway object was
            considered invalid.
        """
        
        msg = "undefined message"
        
        # check general type and shape of _layers and _metadata
        if not isinstance(self._layers, list):
            msg = "_layers is not a list"
            return False, msg
        if not isinstance(self._metadata, list):
            msg = "_metadata is not a list"
            return False, msg
        if not len(self._layers) == len(self._metadata):
            msg = "_layers and _metadata have different lengths"
            return False, msg
        
        
        # loop over all layers
        reached_nodes = set()
        last_has_none = True
        
        for idx_layer in range(len(self._layers)):
            
            nodes = self._convert_intset(self._layers[idx_layer])
            if not nodes == set(self._layers[idx_layer]):
                msg = "nodes of layer {} are not a sorted list of unique integers".format(idx_layer)
                return False, msg
            if len(nodes) == 0:
                if any(len(layer) != 0 for layer in self._layers):
                    msg = "if one layer is empty, all have do be"
                    return False, msg
            if not isinstance(self._metadata[idx_layer], dict):
                msg = "_metadata[{}] is not a dict".format(idx_layer)
                return False, msg
            if not set(nodes) == self._metadata[idx_layer].keys():
                msg = "nodes of layer {} do not match the ones in _metadata".format(idx_layer)
                return False, msg
            
            if last_has_none:
                if not reached_nodes.issubset(nodes):
                    msg = "nodes reached from previous layer are not a subset of nodes in layer {}".format(idx_layer)
                    return False, msg
            else:
                if not reached_nodes == set(nodes):
                    msg = "nodes reached from previous layer do not match nodes in layer {}".format(idx_layer)
                    return False, msg
            reached_nodes = set()
            last_has_none = False
            
            # loop over all nodes for this layer
            for node in nodes:
                
                # check type and structure of this node in _metadata
                if not isinstance(self._metadata[idx_layer][node], list):
                    msg = "_metadata[{}][{}] is not a list".format(idx_layer, node)
                    return False, msg
                if not len(self._metadata[idx_layer][node]) == 2:
                    msg = "len(_metadata[{}][{}]) != 2".format(idx_layer, node)
                    return False, msg
                if isinstance(self._metadata[idx_layer][node][0], list):
                    next_nodes = self._convert_unique_intlist(self._metadata[idx_layer][node][0])
                    if not next_nodes == self._metadata[idx_layer][node][0]:
                        msg = "_metadata[{}][{}][0] is not a sorted list of unique integers".format(idx_layer, node)
                        return False, msg
                    if len(next_nodes) < 1:
                        msg = "_metadata[{}][{}][0] is an empty list".format(idx_layer, node)
                        return False, msg
                elif not self._metadata[idx_layer][node][0] is None:
                    msg = "_metadata[{}][{}][0] is not None or list".format(idx_layer, node)
                    return False, msg
                if not isinstance(self._metadata[idx_layer][node][1], int):
                    msg = "_metadata[{}][{}][1] is not int".format(idx_layer, node)
                    return False, msg
                
                if idx_layer == len(self._layers) - 1:
                    if not self._metadata[idx_layer][node][0] is None:
                        return False, msg
            
                
                if self._metadata[idx_layer][node][0] is None:
                    last_has_none = True
                else:
                    reached_nodes.update(self._metadata[idx_layer][node][0])
        
        
        msg = "Pathway object is OK"
        return True, msg


    
    def _init_branch_sizes(self):
        """Initialize the branch sizes in the metadata.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        n_layers = len(self._layers)
        
        # iterate over all layers in reversed order
        for idx_layer in reversed(range(n_layers)):
            nodes = self._layers[idx_layer]
            # for final layer, number of reachable nodes is 1
            if idx_layer == n_layers-1:
                for node in nodes:
                    self._metadata[idx_layer][node][1] = 1
            # for all other layers add the number of paths reachable for all reachable nodes
            else:
                for node in nodes:
                    next_nodes = self.get_forward_nodes(idx_layer, node)
                    self._metadata[idx_layer][node][1] = sum(self._metadata[idx_layer+1][n][1] for n in next_nodes)
        
        # total number of paths is just the sum of reachable paths from the nodes in the first layer
        if n_layers == 0:
            self._n_paths = 0
        else:
            self._n_paths = sum(self._metadata[0][n][1] for n in self._layers[0])
            
    
    
    def _fix(self):
        """Try to fix self."""
        # not needed at the moment
        return None
    
    
    
    def get_n_layers(self):
        """Return the number of layers.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        n_layers : int
            Number of layers.
        """
        
        return len(self._layers)
    
    
    
    def get_nodes(self, layer_idx):
        """Get a copy of the nodes of a given layer.
        
        Parameters
        ----------
        layer_idx : int
            Index of the relevant layer.
            
        Returns
        -------
        nodes : list
            Copy of the nodes of this layer.
        """
        
        layer_idx = self._norm_layer_idx(layer_idx)
        return self._layers[layer_idx].copy()
    
    
    
    def get_n_nodes(self, layer_idx):
        """Get the number of nodes of a given layer.
        
        Parameters
        ----------
        layer_idx : int
            Index of the relevant layer.
            
        Returns
        -------
        n_nodes : int
            Number of the nodes of this layer.
        """
        
        layer_idx = self._norm_layer_idx(layer_idx)
        return len(self._layers[layer_idx])
    
    
    
    def get_forward_nodes(self, idx_layer, node):
        """Get the next-layer nodes connecting to a given node of a layer.
        
        Parameters
        ----------
        layer_idx : int
            Index of the relevant layer.
        node : int
            Node to get the forward connected nodes from.
        
        Returns
        -------
        forward_nodes : list
            The nodes of the next layer connected to the given node of the
            given layer.
        """
        
        n_layers = len(self._layers)
        idx_layer = self._norm_layer_idx(idx_layer)
        
        # check for key error
        if node not in self._layers[idx_layer]:
            raise KeyError("'{}' not a node of layer {}".format(node, idx_layer))
        
        # the last layer has no forward nodes, return empty list
        if idx_layer == n_layers - 1:
            return []
        
        else:
            # if None, all nodes of the next layer are reachable
            if self._metadata[idx_layer][node][0] is None:
                return self._layers[idx_layer+1].copy()
            else:
                return self._metadata[idx_layer][node][0].copy()
    
    
    
    def get_backward_nodes(self, idx_layer, node):
        """Get the previous-layer nodes connectung to a given node of a layer.
        
        Parameters
        ----------
        layer_idx : int
            Index of the relevant layer.
        node : int
            Node to get the backward connected nodes from.
        
        Returns
        -------
        backward_nodes : list
            The nodes of the previous layer connected to the given node of the
            given layer.
        """
        
        n_layers = len(self._layers)
        idx_layer = self._norm_layer_idx(idx_layer)
        
        # check for key error
        if node not in self._layers[idx_layer]:
            raise KeyError("'{}' not a node of layer {}".format(node, idx_layer))
        
        # the first layer has no backward nodes
        if idx_layer == 0:
            return []
        
        else:
            # grab all nodes of last layer that lead to the given one
            backward_nodes = []
            for prevnode in self._layers[idx_layer-1]:
                if self._metadata[idx_layer-1][prevnode][0] is None:
                    backward_nodes.append(prevnode)
                elif node in self._metadata[idx_layer-1][prevnode][0]:
                    backward_nodes.append(prevnode)
            
            return backward_nodes
    
    
    
    def get_n_forward_paths(self, idx_layer, node):
        """Get the number of paths followind a given node in a given layer.
        
        Parameters
        ----------
        layer_idx : int
            Index of the relevant layer.
        node : int
            Node to get the number of forward nodes from.
        
        Returns
        -------
        n_paths : int
            Number of paths following the given node of the given index. For
            any node in the final layer this is just 1.
        """
        
        n_layers = len(self._layers)
        idx_layer = self._norm_layer_idx(idx_layer)
        
        # check for key error
        if node not in self._layers[idx_layer]:
            raise KeyError("'{}' not a node of layer {}".format(node, idx_layer))
        
        return self._metadata[idx_layer][node][1]
    
    
    

    
    
    
    def __str__(self):
        """Return str(self)."""
        
        string = "Pathway with {} layers".format(self.get_n_layers())

        return string
    
    
    
    def __len__(self):
        """Return len(self) which is the number of pathways."""
        
        return self._n_paths
    
    
    
    def __getitem__(self, i):
        """Return self[i]."""
        
        if not isinstance(i, int):
            return NotImplemented
        
        # normalize the path index
        if i >= self._n_paths or i < -self._n_paths:
            raise IndexError("path index {} out of range".format(i))
        i = i % self._n_paths
        
        path = []
        
        
        for idx_layer in range(self.get_n_layers()):
            
            if idx_layer == 0:
                nodes = self._layers[idx_layer]
            
            acc = 0
            for node in nodes:
                acc += self._metadata[idx_layer][node][1]
                if i < acc:
                    path.append(node)
                    i = i - acc + self._metadata[idx_layer][node][1]
                    nodes = self.get_forward_nodes(idx_layer, node)
                    break
        
        return path
    
    
    
    def __iter__(self):
        """Return iter(self)."""
        
        self._i = 0
        return self
    
    
    
    def __next__(self):
        """Return next(self)"""
        
        if self._i >= self._n_paths:
            del self._i
            raise StopIteration
        
        i = self._i
        self._i += 1
        return self[i]
    
    
    
    def __contains__(self, other):
        """Return `other in self`."""
        
        n_layers = len(self._layers)
        
        # check the input
        other = self._norm_given_path(other)
        
        # pathway with empty nodes contains nothing
        if len(self._layers) == 0:
            return False
        
        # nodes possible in the first layer are just all the nodes of the first layer
        nodes = self._layers[0]
        for idx_layer in range(n_layers-1):
            
            # check in given node is possible in this layer
            node = other[idx_layer]
            if node not in nodes:
                return False
            
            # possible nodes for the next layer, either all of the next layer or a subset
            if self._metadata[idx_layer][node][0] is None:
                nodes = self._layers[idx_layer+1]
            else:
                nodes = self._metadata[idx_layer][node][0]
                
        # check last node
        node = other[n_layers-1]
        if node not in nodes:
            return False
        
        return True
    
    
    
    def get_path_index(self, path):
        """Get the index of a given path so that `self[index] == path`.
        
        Parameters
        ----------
        path : list
            Path to get the index from.
        
        Returns
        -------
        index : int
            Index of the given path.
        """
        
        n_layers = len(self._layers)
        
        # check the input
        path = self._norm_given_path(path)
        
        # pathway with empty nodes contains nothing
        if len(self._layers) == 0:
            raise KeyError("Empty Pathway does not contain anything.")
        
        idx = 0
        
        # nodes possible in the first layer are just all the nodes of the first layer
        nodes = self._layers[0]
        for idx_layer in range(n_layers-1):
            
            # check in given node is possible in this layer
            path_node = path[idx_layer]
            
            for layer_node in nodes:
                if path_node == layer_node:
                    break
                idx += self._metadata[idx_layer][layer_node][1]
            else:
                raise KeyError("Given path is not an element of this Pathway object.")
            
            # possible nodes for the next layer, either all of the next layer or a subset
            if self._metadata[idx_layer][layer_node][0] is None:
                nodes = self._layers[idx_layer+1]
            else:
                nodes = self._metadata[idx_layer][layer_node][0]
                
        # check last node
        path_node = path[n_layers-1]
        for layer_node in nodes:
            if path_node == layer_node:
                break
            idx += self._metadata[n_layers-1][layer_node][1]
        else:
            raise KeyError("Given path is not an element of this Pathway object.")
        
        return idx
    
    
    
    
    







class CTP(object):
    """
    A class handeling coherence order transfer pathways (CTPs).
    
    A coherence order transfer pathway is a set of coherence orders that
    are present during an NMR experiment. The cohernce order of a spin system
    can only change if pulses are applied for a given channel or nucleus.
    
    Objects worked on:
    
    _orders:
        list of lists of sets
        One list for every channel, in each channel list of sets for coherences
        of every step.
    _changes:
        None
    _desired:
        None
    _pathways:
        None
    """
    
    
    
    
    @classmethod
    def _is_intlist(cls, obj):
        """Check if object is a list of integers.
        
        Returns 'true' if given object is a list and all of its elements
        are instances of the Python int class.
        
        Parameters
        ----------
        obj : object
            Object to check.
        
        Returns
        -------
        is_intlist : bool
            Whether the object is a list of integers or not.
        """
        
        if not isinstance(obj, list):
            return False
        
        return all(isinstance(x, int) for x in obj)
    
    
    
    
    
    @classmethod
    def _is_intset(cls, obj):
        """Check if object is a set containing only integers.
        
        Returns 'true' if given object is a set and all of its elements
        are integer instances. It does not matter if the set is a usual
        set or frozenset.
        
        Parameters
        ----------
        obj : object
            Object to check.
        
        Returns
        -------
        is_intset : bool
            Whether the object is a set of integers or not.
        """
        
        if not isinstance(obj, set) or not isinstance(obj, frozenset):
            return False
        
        return all(isinstance(x, int) for x in obj)
    
    
    
    
    
    @classmethod
    def _convert_intlist(cls, x):
        """Convert an object to a list of integers.
        
        Tries to convert an object to a list of integers. The object can be
        an iterable where every element is castable to an integer or a
        non-iterable object that can be casted to an integers directly.
        
        Parameters
        ----------
        x : obj
            Object to convert to a list of integers.
        
        Returns
        -------
        intlist : list of int
            List of integers generated from `x`.
        """
        
        # if x ist int, return just list with this int
        if hasattr(x, '__iter__'):
            intlist = [int(xi) for xi in x]
        else:
            intlist = [int(x)]
        
        return intlist
    
    
    
    
    
    @classmethod
    def _convert_intset(cls, x):
        """Convert an object to a set of integers.
        
        Tries to convert an object to a set of integers. The object can be
        an iterable where every element is castable to an integer or a
        non-iterable object that can be casted to an integers directly.
        
        Parameters
        ----------
        x : obj
            Object to convert to a set of integers.
        
        Returns
        -------
        intlist : list of int
            Set of integers generated from `x`.
        """
        
        # if x ist int, return just list with this int
        if hasattr(x, '__iter__'):
            intset = {int(xi) for xi in x}
        else:
            intset = set([int(x)])
        
        return intset
    
    
    
    
    
    @classmethod
    def _convert_unique_intlist(cls, x):
        """Convert an object to a list of unique sorted integers.
        
        Tries to convert an object to a list of integers. The object can be
        an iterable where every element is castable to an integer or a
        non-iterable object that can be casted to an integers directly.
        The final list returned is sorted and contains only unique integers.
        
        Parameters
        ----------
        x : obj
            Object to convert to a list of integers.
        
        Returns
        -------
        intlist : list of int
            Sorted list of unique integers generated from `x`.
        """
        
        # return sorted list of unique elements
        return sorted(cls._convert_intset(x))
    
    
    
    
    
    @classmethod
    def _format_nbytes(cls, nbytes):
        """Format an integer representing a number of bytes to a string.
        
        Parameters
        ----------
        nbytes : int
            Number of bytes as integer or castable to integer.
            
        Returns
        -------
        bytes_str : str
            String representing the number of bytes.        
        """
        
        # try to handle error cases, nbytes must be castable to int
        try:
            nbytes = int(nbytes)
        except:
            return "???"
        if nbytes < 0:
            return "???"
        
        rest = 0
        
        prefices = {0: 'Bytes', 1: 'kB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB', 6: 'EB',
                    7: 'ZB', 8: 'YB', 9: 'RB', 10: 'QB'}
        
        for i in range(len(prefices)):
            if nbytes >= 1000:
                nbytes, rest = divmod(nbytes, 1000)
            else:
                if i == 0:
                    return "{} ".format(nbytes) + prefices[i]
                return "{:.2f} ".format(nbytes+rest/1000) + prefices[i]
            
        maxiter = 1000
        pow_of_10 = 15
        divisor = 10**pow_of_10
        for i in range(maxiter):
            if nbytes >= divisor:
                nbytes, rest = divmod(nbytes, divisor)
            else:
                exponent = pow_of_10*i+3
                for j in range(pow_of_10):
                    if nbytes < 10**(j+1):
                        base = (nbytes+rest/10**pow_of_10)/10**j
                        return "{:.2f} x10^{} QB".format(base, exponent)
                    exponent += 1
        
        # huge number, overflow
        return "overflow"
    
    
    
    
    
    def __init__(self, n_blocks):
        """
        Create a new CTP instance.
        
        Parameters
        ----------
        n_blocks : int or list of int
            Number of blocks, that change the coherence order (either as an
            integer for homonuclear experiments or as a list of integers for
            heteronuclear experiments). The number of steps, i.e. the number
            of position in time with fixed coherence orders is the number of
            blocks plus one for each channel as the starting and final
            coherence orders have to be taken into account.
        
        Returns
        -------
        None
        """
        
        # handle the number of blocks
        n_blocks = self._convert_intlist(n_blocks)            
        if len(n_blocks) < 1:
            raise ValueError("Experiment must have at least one channel.")
        for idx, n_block in enumerate(n_blocks):
            if n_block < 1:
                raise ValueError("Number of blocks must be at least "
                                 "one for every channel but is {} for channel {}.".format(n_block, idx))
        
        self._n_channels = len(n_blocks)
        self._n_blocks = n_blocks
        
        # setup the coherence orders, changes and desired pathways
        self._init_orders()
        self._init_changes()
        self._init_desired()
        self._init_pathways()
    
    
    
    
    
    def _init_orders(self):
        """Initialize internal coherence order object.
        
        Initialize self._orders which holds the possible coherence orders
        for every step of every channel. self._coherence orders is a list
        (one element for each channel) of lists (one element for each step)
        of sets containing integers. These sets will be empty initially for
        every step except the first and the final one, where 0 and -1 will
        be set, respectively.        
        """
        
        self._pathways = None
        # orders are list of empty lists
        self._orders = []
        for idx in range(self._n_channels):
            self._orders.append([set() for i in range(self._n_blocks[idx]+1)])
            self._orders[idx][0].update([0])
            self._orders[idx][self._n_blocks[idx]].update([-1])
    
    
    def _init_changes(self):
        """Initialize internal coherence order changes object."""
        
        self._pathways = None
        # a list of empty sets, one for each channel
        self._changes = [dict() for i in range(self._n_channels)]
    
    
    
    def _init_desired(self):
        """Initialize internal desired CTPs object."""
        
        # this is just an empty set
        self._desired = set()
        self._reference = None
    
    
    def _init_pathways(self):
        """Initialize internal pathways object."""
        
        self._pathways = None
        
        
    # some internal utility functions
    
    def _normalize_index(self, index, size):
        """Normalize an index for an object with a given size.
        
        Parameters
        ----------
        index : int castable
            Index to be normalized. Should be int or castable to int
            int the range from `-size` to `size-1`.
        size : int
            Size of the object.
        
        Returns
        -------
        normalized_index : int
            Normalized index in the range from `0` to `size-1`.
        """
        
        size = int(size)
        
        try:
            index = int(index)
        except:
            raise TypeError("Cannot interpret given index as integer.")
        
        if index >= size or index < -size:
            raise KeyError("Index {} is out of range for object with size {}".format(index, size))
        
        return index % size
    
    
    
    def _normalize_channel_index(self, index):
        """Check and normalize one channel index.
        
        Parameters
        ----------
        index : int, None
            Index of the relevant channel. Can be a single index or object
            convertible to an integer. For homonuclear experiments this
            parameter is redundant and will assumed to be just 0. Only in
            this case `None` can also be given.
        
        Returns
        -------
        normalized_index : int
            Normalized channel index from 0 to `n_channels-1`.
        """
        
        n_channels = self._n_channels
        
        # ignore index in homonuclear experiment, just return 0 and don't complain
        if n_channels == 1:
            return 0
        
        if index is None:
            raise ValueError("Channel index must be specified in heteronuclear experiments.")
        
        try:
            index = int(index)
        except:
            raise TypeError("Cannot convert given channel index to integer.")
            
        if index >= self._n_channels or index < -self._n_channels:
            raise ValueError("Channel index ({}) out of range (must be between {} and {}).".format(
                                    index,-self._n_channels,self._n_channels-1)
                            )
        
        return index % self._n_channels
    
    
    
    def _normalize_channel_indices(self, indices):
        """Check an normalize channel one or more indices.
        
        Parameters
        ----------
        indices : int, list of int or str
            Index or indices of the relevant channel. Can be a list of
            valid indices, a single index (or objects convertible to int).
            'all' can be used to chose all possible channel indices from
            0 to `n_channel-1`. For homonuclear experiments this parameter
            is redundant and will assumed to be just 0. Only in this case
            `None` can also be given.
        
        Returns
        -------
        normalized_indices : list of int
            Normalized channel indices from 0 to `n_channels-1`.
        """
        
        n_channels = self._n_channels
        
        # ignore index in homonuclear experiment
        if n_channels == 1:
            return [0]
        
        if indices is None:
            raise ValueError("Channel indices must be specified in heteronuclear experiments.")
            
        elif isinstance(indices, str):
            if indices.lower() == 'all':
                return [i for i in range(n_channels)]
            else:
                raise ValueError("Invalid channel index str argument '{}'.".format(indices))
            
        else:
            # convert to list of integers, delete dublicates and sort later
            indices = self._convert_intlist(indices)
            
            # check if all indices are in correct range
            for i, idx in enumerate(indices):
                if idx >= n_channels or idx < -n_channels:
                    raise ValueError("Channel index ({}) out of range (must be between {} and {}).".format(
                                            idx,-self._n_channels,self._n_channels-1)
                                    )
                indices[i] = idx % self._n_channels
            
            # return sorted list of indices without dublicates
            return sorted(set(indices))
    
    
    
    def _normalize_block_indices(self, block_idxs, channel_idx=None):
        """Normalize given block indices for a given channel.
        
        Parameters
        ----------
        block_idxs : intlist castable, str
            Index or indices of the relevant blocks. Can be a list of valid
            indices, a single index (or objects convertible to int). 'all'
            can be used to chose all possible block indices.
        channel_idx : int, optional
            Index of the relevant channel. Can be a single index or object
            convertible to an integer. For homonuclear experiments this
            parameter is redundant and will assumed to be just 0. Only in
            this case `None` can also be given (default).
        
        Returns
        -------
        normalized_block_idxs : list of int
            Normalized block indices as a sorted list of unique integers.
        """
        
        channel_idx = self._normalize_channel_index(channel_idx)
        n_blocks = self._n_blocks[channel_idx]
        
        if isinstance(block_idxs, str):
            if block_idxs.lower() == 'all':
                return [i for i in range(n_blocks)]
        
        block_idxs = self._convert_intlist(block_idxs)
        
        for i, idx in enumerate(block_idxs):
        
            if idx >= n_blocks or idx < -n_blocks:
                raise ValueError("Invalid changes index {}.".format(idx))
            block_idxs[i] = idx % n_blocks         
            
        return sorted(set(block_idxs))
    
    
    
    def _normalize_block_channel_indices(self, block_idxs, channel_idxs):
        """"""
        
        channel_idxs = self._normalize_channel_indices(channel_idxs)
        
        # clean up all changes indices
        if isinstance(block_idxs, str):
            block_idxs = [block_idxs] * len(channel_idxs)
        if not hasattr(block_idxs, '__iter__'):
            block_idxs = [int(block_idxs)] * len(channel_idxs)
            
        if not len(block_idxs) == len(channel_idxs):
            raise ValueError('Number of lists of changes indices must equal number of channel indices.')
        
        block_idxs_out = []
        
        for i, channel_idx in enumerate(channel_idxs):
            
            n_blocks = self._n_blocks[channel_idx]
            indices = block_idxs[i]
            
            if isinstance(indices, str):
            
                if indices.lower() == 'all':
                    indices = [i for i in range(n_blocks)]
                
                else:
                    raise ValueError("If block indices is a string it should be 'all', 'start' or 'end'.")
                
            else:
                
                # indices must be a list of integers
                indices = self._convert_unique_intlist(indices)
                
                for j, idx in enumerate(indices):
                    if idx >= n_blocks or idx < -n_blocks:
                        raise ValueError('Channel index is out of range.')
                    indices[j] = idx % n_blocks
            
            
            block_idxs_out.append(sorted(set(indices)))
        
        return block_idxs_out, channel_idxs
    
    
    
    def _normalize_step_indices(self, indices, channel_idx=None):
        """Check and normalize a list of block indices for a given channel.
        
        The number of steps for a given channel is the number of blocks plus
        one. The step with index 0 corresponds to the initial coherences and
        the step with index n_steps-1 to the final coherence orders.
        
        Parameters
        ----------
        indices : int, list of int, str
            Index or indices of the relevant steps. Can be a list of valid
            indices, a single index (or objects convertible to int). 'all'
            can be used to chose all possible step indices except the first
            and the last step for the given channel, 'start' or 'init' and
            'end' or 'final' are aliases for the first (index 0) and last
            (index n_steps-1) step, respectively.
        channel_idx : int, optional
            Index of the relevant channel. Can be a single index or object
            convertible to an integer. For homonuclear experiments this
            parameter is redundant and will assumed to be just 0. Only in
            this case `None` can also be given (default).
        
        Returns
        -------
        normalized_indices : list of int
            Normalized block indices.
        """
        
        channel_idx = self._normalize_channel_index(channel_idx)
        n_steps = self._n_blocks[channel_idx] + 1
        
        # handle special str cases
        if isinstance(indices, str):
            
            indices = indices.lower()
            
            if indices == 'all':
                return [i for i in range(1,n_steps-1)]
            elif indices in ['start', 'init']:
                return [0]
            elif indices in ['end', 'final']:
                return [n_steps-1]
            else:
                raise ValueError("If block indices is a string it should be 'all', 'start' or 'end'.")
        
        else:
            # indices must be a list of integers
            indices = self._convert_intlist(indices)
            for i, idx in enumerate(indices):
                if idx >= n_steps or idx < -n_steps:
                    raise ValueError('Block index ({}) is out of range for channel {}.'.format(idx, channel_idx))
                indices[i] = idx % n_steps
                
            # return sorted list of indices without dublicates
            return sorted(set(indices))
    
    
    
    def _normalize_step_channel_indices(self, step_idxs, channel_idxs):
        """Normalize a set of given step an channel indices.
        
        Parameters
        ----------
        step_idxs : int, list of int or str
            Index or indices of the relevant steps. Can be a list of valid
            indices, a single index (or objects convertible to int). 'all'
            can be used to chose all possible step indices except the first
            and the last step for the given channel, 'start' or 'init' and
            'end' or 'final' are aliases for the first (index 0) and last
            (index n_steps-1) step, respectively.
        channel_idxs : int, list of int or str
            Index or indices of the relevant channel. Can be a list of
            valid indices, a single index (or objects convertible to int).
            'all' can be used to chose all possible channel indices from
            0 to `n_channel-1`. For homonuclear experiments this parameter
            is redundant and will assumed to be just 0. Only in this case
            `None` can also be given.
        
        Returns
        -------
        step_idxs_out : list of list of int
        channel_idxs : list of int
        """
        
        channel_idxs = self._normalize_channel_indices(channel_idxs)
        
        # clean up all block indices
        if isinstance(step_idxs, str):
            step_idxs = [step_idxs] * len(channel_idxs)
        if not hasattr(step_idxs, '__iter__'):
            step_idxs = [int(step_idxs)] * len(channel_idxs)
            
        if not len(step_idxs) == len(channel_idxs):
            raise ValueError("Number of lists of block indices must equal number of channel indices.")
        
        step_idxs_out = []
        for i, channel_idx in enumerate(channel_idxs):
            step_idxs_out.append(self._normalize_step_indices(step_idxs[i], channel_idx=channel_idx))
        
        return step_idxs_out, channel_idxs
    
    
    
    def _normalize_changes_mode(self, changes_mode):
        """Normalize a given coherence order changes mode.
        
        Parameters
        ----------
        changes_mode : str, None
            Changes mode to normalize. Can be None or a str like 'allowed',
            'a', 'forbidden' or 'f' where case does not matter.
        
        Returns
        -------
        normalized_mode : str
            Either 'a' or 'f' for allowed and forbidden mode. If None is given
            None is returned.
        """
        
        # if None is given, return None
        if changes_mode is None:
            return None
        
        # convert given value to lowercase str
        try:
            changes_mode = str(changes_mode).lower()
        except:
            raise TypeError("Cannot convert coherence changes mode to str.")
        
        # check the changes_mode
        if changes_mode in ['allowed', 'a']:
            return 'a'
        elif changes_mode in ['forbidden', 'f']:
            return 'f'
        else:
            raise ValueError("Invalid changes mode '{}' for coherence order changes.".format(changes_mode))
    
    
    
    def _normalize_given_ctp(self, given_ctp):
        """Normalize a given CTP."""
        
        if self._n_channels == 1:
            # either list of list of integers or list of integers
            try:
                # maybe a list of integers is given?
                given_ctp = [self._convert_intlist(given_ctp)]
            except:
                # now a list of a list of integers must be given like [[1,2,3]]
                given_ctp = list(given_ctp)
        else:
            try:
                given_ctp = list(given_ctp)
            except:
                raise TypeError("Cannot convert desired CTP to a list of a list of integers.")
        
        # one CTP integer list for every channel
        if not len(given_ctp) == self._n_channels:
            raise ValueError("Number of CTP lists ({}) does not match number of channels ({}).".format(len(given_ctp), self._n_channels))
        
        ctps_out = []
        for idx in range(self._n_channels):
            
            try:
                this_ctp = tuple(self._convert_intlist(given_ctp[idx]))
            except:
                raise TypeError("Cannot convert to tuple of integers for channel {}.".format(idx))
                
            if not len(this_ctp) == self._n_blocks[idx]+1:
                raise ValueError("Wrong number of coherence orders for channel {} (given are {}, expected were {}).".format(idx,len(this_ctp),self._n_blocks[idx]+1))
                
            ctps_out.append(this_ctp)
            
        return tuple(ctps_out)
    
    
    
    # other generators
    
    @classmethod
    def from_compressed(cls, x):
        """Construct CTP object from a compressed intlist object."""
        
        
        x = cls._convert_intlist(x)
        length = len(x)
        
        if length < 1:
            raise ValueError("Compressed CTP element must have at least one element.")
        
        # number of channels
        n_channels = x[0]
        if n_channels < 1:
            raise ValueError("Number of channels must be greater than 1.")
        
        # number of blocks
        if length < n_channels + 1:
            raise ValueError("Compressed CTP element must have at least {} elements.".format(n_channels + 1))
            
        n_blocks = x[1:1+n_channels]
        
        # check index portion
        n_total = sum(n_blocks) + len(n_blocks) # total number of steps in all channels
        n_indices = 2*sum(n_blocks) + len(n_blocks) + 2
        
        for i in range(n_channels+2, n_channels+n_indices+1):
            if x[i-1] > x[i]:
                raise ValueError("Index block of compressed CTP is corrupted.")
        if not x[n_channels+n_indices] == len(x):
            raise ValueError("Index block of compressed CTP is corrupted.")
        
        n_desired, rest = divmod(x[n_channels+n_indices]-x[n_channels+n_indices-1], n_total)
        if not rest == 0:
            raise ValueError("Desired CTPs broken.")
        
        # generate the CTP object
        ctp = CTP(n_blocks)
        
        # set all coherence orders
        idx_pos = 1+n_channels
        
        for idx_channel in range(n_channels):
            for idx_step in range(n_blocks[idx_channel]+1):
                
                orders = x[x[idx_pos]:x[idx_pos+1]]
                
                ctp.set_orders(orders, idx_step, idx_channel)
                
                idx_pos += 1
        
        # set all coherence order changes
        for idx_channel in range(n_channels):
            for idx_block in range(n_blocks[idx_channel]):
                
                changes = x[x[idx_pos]+1:x[idx_pos+1]]
                
                if len(changes) > 0:
                
                    if x[x[idx_pos]] == 1:
                        mode = 'a'
                    elif x[x[idx_pos]] == 2:
                        mode = 'f'
                    else:
                        raise ValueError("Invalid changes mode in compressed CTP.")
                    
                    ctp.set_changes(changes, idx_block, idx_channel, changes_mode=mode)
                    
                idx_pos += 1
        
        # set all desired CTPs
        for idx_desired in range(n_desired):
            
            idx_left = x[idx_pos] + idx_desired*n_total
            
            desired_ctp = []
            for idx_channel in range(n_channels):
                desired_ctp.append(x[idx_left:idx_left+n_blocks[idx_channel]+1])
                idx_left += n_blocks[idx_channel] + 1    
                
            ctp.add_desired_ctp(desired_ctp)
        
        return ctp
    
    
    
    
    
    def export_compressed(self):
        """Export compressed CTP object."""
        
        export = [self._n_channels]
        n_steps = [i+1 for i in self._n_blocks]
        
        export += [i-1 for i in n_steps]
        export += [0] * (2*sum(n_steps) - len(n_steps) + 2)
        
        index1 = len(n_steps) + 1
        index2 = 2*sum(n_steps) + 3
        
        # append coherence orders
        for i in range(len(n_steps)):
            for j in range(n_steps[i]):
                
                orders = sorted(self._orders[i][j])
                
                export += orders
                export[index1] = index2
                index1 += 1
                index2 += len(orders)
        
        # append coherence order changes
        for i in range(len(n_steps)):
            for j in range(n_steps[i]-1):
                
                if j in self._changes[i]:
                    
                    mode = self._changes[i][j]['mode']
                    changes = sorted(self._changes[i][j]['values'])
                    
                    if mode == 'a':
                        mode_int = 1
                    elif mode == 'f':
                        mode_int = 2
                    else:
                        raise ValueError("Invalid changes mode '{}'.".format(mode))
                        
                    export += [mode_int] + changes
                    export[index1] = index2
                    index1 += 1
                    index2 += len(changes) + 1
                
                else:
                    export[index1] = index2
                    index1 += 1
        
        
        # append desired CTPs
        for desired_ctp in sorted(self._desired):
            for desired_ctp_chan in desired_ctp:
                export += list(desired_ctp_chan)
        
        export[index1] = index2
        index1 += 1
        index2 += len(self._desired) * sum(n_steps)
        
        # final value
        export[index1] = index2
        
        return export
    
    
    
    def copy(self):
        """Return a deep copy of self.
        
        This function returns a new CTP instance where all relevant internal
        objects (self._orders, self._changes and self._desired) are copied.
        Changes to the copied CTP instance do not affect this instance.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        ctp : CTP
            New CTP instance with copied parameters.
        """
        
        # channel indices
        channel_idxs = [i for i in range(self._n_channels)]
        
        # generate new CTP object
        ctp = CTP(self._n_blocks)
        
        # copy coherence orders
        ctp._orders = [[set(orders) for orders in self._orders[idx]] for idx in channel_idxs]
        # copy coherence order changes
        ctp._changes = [{o: {'mode': str(v['mode']), 'values': set(v['values'])} for o, v in self._changes[idx].items()} for idx in channel_idxs]
        # copy desired CTPs
        ctp._desired = set(tuple(tuple(wctp[idx]) for idx in channel_idxs) for wctp in self._desired)
        
        return ctp
    
    
    

    
    
    
    def __repr__(self):
        """Convert object to string representation."""
        
        return 'CTP({})'.format(self._n_blocks)
    
    
    
    def __str__(self):
        """Convert object to string as needed by print().
        
        The string representation contains everything there is to know about
        this CTP instance, i.e. number of channels and number of blocks for
        each channel, the possible coherence orders for every step of every
        channel and the allowed (a) or forbidden (f) coherence order changes
        for every block of every channel.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        repr_str : str
            String representation of self.
        """
        
        string = ""
        
        n_channels = self._n_channels
        
        if n_channels == 1:
            string += "Coherence Transfer Pathway with 1 channel"
        else:
            string += "Coherence Transfer Pathway with {} channels".format(n_channels)
        
        
        for idx_channel in range(n_channels):
            
            n_blocks = self._n_blocks[idx_channel]
            
            # header for this channel
            channel_header = "Coherences for channel {} ".format(idx_channel)
            if n_blocks == 1:
                channel_header += "(with 1 block):"
            else:
                channel_header += "(with {} blocks):".format(n_blocks)
            
            string += "\n\n" + channel_header + '\n' + '-'*len(channel_header) + "\n"
            
            # coherences of all intermediate blocks
            for idx_block in range(n_blocks):                    
                
                # print allowed coherences
                if idx_block == 0:
                    string += '\nStart      :'
                else:
                    string += '\nStep {:2}    :'.format(idx_block)
                coherences = sorted(self._orders[idx_channel][idx_block])
                if len(coherences) == 0:
                    string += ' None'
                else:
                    for c in coherences:
                        string += ' {:>+3}'.format(c)
                        
                # print allowed changes from previous block
                if idx_block in self._changes[idx_channel]:
                    changes = self._changes[idx_channel][idx_block]
                    mode = changes['mode']
                    values = sorted(changes['values'])
                    string += "\n({:>2} -> {:<2}) : ({})".format(idx_block, idx_block+1, mode)
                    if len(values) == 0:
                        string += ' None'
                    else:
                        for c in values:
                            string += ' {:>+3}'.format(c)
                
            # final coherences
            string += "\nEnd        :"
            coherences = sorted(self._orders[idx_channel][n_blocks])
            if len(coherences) == 0:
                string += "None"
            else:
                for c in coherences:
                    string += " {:>+3}".format(c)
                    
        # print desired CTPs
        if len(self._desired) == 0:
            string += "\n\nNo desired CTPs defined yet."
        
        else:
            header = "Desired CTPs ({} in total defined):".format(len(self._desired))
            string += "\n\n" + header + "\n" + "-"*len(header)
            for idx, ctp in enumerate(sorted(self._desired)):
                
                # generate the string of attributes for this CTP (if it's valid or the reference CTP)
                attributes = []
                if self._reference is not None and ctp == self._reference:
                    attributes.append("reference")
                if not self.is_ctp_valid(ctp):
                    attributes.append("invalid")
                
                if len(attributes) > 0:
                    info_str = " ("
                    for i in range(len(attributes)-1):
                        info_str += attributes[i] + ", "
                    info_str += attributes[-1]
                    info_str += ")"
                else:
                    info_str = ""
                
                # header for this CTP
                string += "\nDesired CTP #{}{}:".format(idx, info_str)
                # print every channel
                for jdx in range(self._n_channels):
                    string += "\n  Channel {:<2}: ".format(jdx)
                    for kdx in range(self._n_blocks[jdx]):
                        string += "{:>+3} --> ".format(ctp[jdx][kdx])
                    string += "{:>+3}".format(ctp[jdx][-1])
            
        return string
    
    
    
    
    
    def __len__(self):
        """Total number of CTPs possible for this CTP instance.
        
        In order to compute the number of CTPs possible for this experiment
        the Pathway object for every channel has to be generated. The total
        number of CTPs is then the product of the number of pathways for
        every channel.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        length : int
            Total number of CTPs possible.        
        """
        
        # generate pathway objects if not available
        self._generate_pathways()
        
        # total number of CTPs is product of number of pathways for every channel
        n_total = 1
        for idx_channel in range(self._n_channels):
            n_total *= len(self._pathways[idx_channel])
        
        return n_total
    
    
    
    
    
    def __getitem__(self, i):
        """"""
        
        # here, self.__len__() also calls self._generate_pathways()
        self_len = self.__len__()
        
        if not isinstance(i, int):
            return NotImplemented
        
        # normalize the index
        if i >= self_len or i < -self_len:
            raise IndexError("CTP index out of range.")
        i = i % self_len
        
        # number of CTPs for every channel
        n_ctps = [len(p) for p in self._pathways]
        
        # index of CTP for every channel
        i_chan = []
        for n in reversed(n_ctps):
            i, mod = divmod(i, n)
            i_chan.insert(0, mod)
        
        item = []
        for idx_channel in range(self._n_channels):
            item.append(self._pathways[idx_channel][i_chan[idx_channel]])
        
        return item
    
    
    
    
    
    def __contains__(self, other):
        """Returns `other in self`."""
        
        # TODO: replace this also with self.is_ctp_valid(other) to avoid calling self._generate_pwathways?
        # I like to have this as reference because it can be used to show that always `other`in self == self.is_ctp_valid(other)
        
        self._generate_pathways()
        
        other = self._normalize_given_ctp(other)
        
        for idx_channel in range(self._n_channels):
            if other[idx_channel] not in self._pathways[idx_channel]:
                return False
        
        return True
    
    
    
    def get_ctp_index(self, ctp):
        """Return the index of a CTP so that `CTP[idx] == ctp`."""
        
        # generate self._pathways if not already done
        self._generate_pathways()
        
        ctp = self._normalize_given_ctp(ctp)
        n_channels = self._n_channels
        pathways = self._pathways
        
        n = len(self)
        idx_ctp = 0
        for idx_channel in range(n_channels):
            n //= len(pathways[idx_channel])
            try:
                idx_path = pathways[idx_channel].get_path_index(ctp[idx_channel])
            except:
                raise IndexError("Given CTP is not an element of this object "
                                 "(could not find the path index for channel {}).".format(idx_channel))
            idx_ctp += n * idx_path
        
        # sanity check
        if not n == 1:
            RuntimeError("Something went wrong in `get_ctp_index` (n != 1).")
        
        return idx_ctp    
    
    
    
    def get_sub_ctp(self, channel_idxs):
        """Return a deep copy of self of given channels."""
        
        # normalize channel indices but keep order and do not delete dublicates
        if hasattr(channel_idxs, '__iter__'):
            channel_idxs = [self._normalize_channel_index(i) for i in channel_idxs]
        else:
            channel_idxs = [self._normalize_channel_index(channel_idxs)]
        
        # generate new CTP object
        sub_ctp = CTP([self._n_blocks[idx] for idx in channel_idxs])
        
        # copy coherence orders
        sub_ctp._orders = [[set(orders) for orders in self._orders[idx]] for idx in channel_idxs]
        # copy coherence order changes
        sub_ctp._changes = [{o: {'mode': str(v['mode']), 'values': set(v['values'])} for o, v in self._changes[idx].items()} for idx in channel_idxs]
        # copy desired CTPs
        sub_ctp._desired = set(tuple(tuple(wctp[idx]) for idx in channel_idxs) for wctp in self._desired)
        
        return sub_ctp
    
    
    
    def _purge_empty_changes(self):
        """Utility function to purge empty changes entries."""
        
        # iterate over coherence order changes of every channel
        for idx_channel in range(self._n_channels):
            
            this_changes = self._changes[idx_channel]
            # get all keys that have an empty value set
            to_delete = [key for key, value in this_changes.items() if len(value['values']) == 0]
            # delete all keys that have an empty value set
            for key in to_delete:
                this_changes.pop(key)
    
    
    
    # functions for pathway generation
    
    
    def _are_all_orders_initialized(self):
        """Check if orders are set for every channel and step.
        
        This function checks whether at least one coherence order is defined
        for every step of every channel. It this is not the case, the function
        also returns a tuple with the channel index and step index of the
        first channel and step where not even one order is defined.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        all_init : bool
            Whether all orders are initialized or not.
        which : tuple
            Tuple containing the indices of the first channel and step where
            no coherence orders are defined or empty tuple if all orders are
            defined.
        """
        
        # loop over all channel
        n_channels = self._n_channels
        for idx_channel in range(n_channels):
            
            # loop over all steps
            n_steps = self._n_blocks[idx_channel] + 1
            for idx_step in range(n_steps):
                
                if len(self._orders[idx_channel][idx_step]) == 0:
                    return False, (idx_channel, idx_step)
        
        return True, tuple()
    
    
    
    
    
    def _generate_pathways_dicts(self):
        """Generate CTPs from internal cohrence orders and changes.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        all_pathways_dict : list of list of dict
            Todo
        """
        
        # get rid of all changes entries that have no effect
        self._purge_empty_changes()
        
        all_pathways_dict = []
        # loop over all channels
        for idx_channel in range(self._n_channels):
            
            n_blocks = self._n_blocks[idx_channel]   # number of blocks for this channel
            pathways = []                            # dict of coherence orders for every step for this channel
            orders_prev = None                       # orders reachable from last step (`None` means all are reachable)
            
            # loop over all steps except acquisition step (done in else)
            for idx_block in range(n_blocks):
                
                # orders allowed in this step, only keep orders reachable from last step
                orders = set(self._orders[idx_channel][idx_block])
                if not orders_prev is None:
                    orders.intersection_update(orders_prev)
                    
                # orders possible in next step
                orders_next = set(self._orders[idx_channel][idx_block+1])
                
                # no orders are reachable or present in this step, so no possibe CTPs
                if len(orders) == 0 or len(orders_next) == 0:
                    pathways = [dict() for i in range(n_blocks+1)]
                    break
                
                # apply restrictions due to coherence order changes if there are any
                if idx_block in self._changes[idx_channel]:
                    
                    changes_mode = self._changes[idx_channel][idx_block]['mode']
                    changes_vals = set(self._changes[idx_channel][idx_block]['values'])
                    orders_dict = dict()
                    orders_prev = set()
                    
                    # only changes of this magnitude are allowed
                    if changes_mode == 'a':
                        for order in orders:
                            possible_next = set([order+change for change in changes_vals])
                            # only keep orders that lead to possible order in next step
                            possible_next.intersection_update(orders_next)
                            if len(possible_next) > 0:
                                orders_prev.update(possible_next)
                                if len(possible_next) == len(orders_next):
                                    orders_dict.update({order: None})
                                else:
                                    orders_dict.update({order: possible_next})
                    
                    # changes of this magnitude are not allowed
                    elif changes_mode == 'f':
                        for order in orders:
                            forbidden_next = set([order+change for change in changes_vals])
                            # remove forbidden orders from all next orders
                            possible_next = orders_next.difference(forbidden_next)
                            if len(possible_next) > 0:
                                orders_prev.update(possible_next)
                                if len(possible_next) == len(orders_next):
                                    orders_dict.update({order: None})
                                else:
                                    orders_dict.update({order: possible_next})
                        
                    # invalid coherence order change mode
                    else:
                        raise ValueError("Invalid changes mode '{}'.".format(changes_mode))
                    
                    # no coherence orders to go to, so no CTPs possible at all
                    if len(orders_dict) == 0:
                        pathways = [dict() for i in range(n_blocks+1)]
                        break
                    
                    pathways.append(orders_dict)
                
                
                # no restrictions due to changes to apply
                else:
                    # `None` indicates all next orders are reachable that exist
                    pathways.append({order: None for order in orders})
                    orders_prev = None
            
            
            # the coherences in the acquisition step are done extra
            else:
                
                # orders allowed in this step (the final step), only keep orders reachable from last step
                orders = set(self._orders[idx_channel][n_blocks])
                if not orders_prev is None:
                    orders.intersection_update(orders_prev)
                
                if len(orders) == 0:
                    pathways = [dict() for i in range(n_blocks+1)]
                
                else:
                    pathways.append({order: None for order in orders})
                
                    # deletion of lose ends
                    for idx_block in range(n_blocks-1,-1,-1):
                        
                        # orders that are reachable in the next step
                        orders_reachable = set(pathways[idx_block+1].keys())
                        for order in pathways[idx_block]:
                            
                            # skip orders that can lead to anything
                            if pathways[idx_block][order] is None:
                                continue
                            
                            # remove connected orders that are impossible in next step
                            pathways[idx_block][order].intersection_update(orders_reachable)
                            # remove order in this step, that does not lead to anything
                            if len(pathways[idx_block][order]) == 0:
                                pathways[idx_block].pop(order)
                            # replace connected order set if all orders in next step can be reached
                            elif len(pathways[idx_block][order]) == len(orders_reachable):
                                pathways[idx_block][order] = None
            
            
            # append pathways of this channel to object for all channels
            all_pathways_dict.append(pathways)
        
        # validate the generated pathways 
        is_valid, msg = self._validate_pathways_dicts(all_pathways_dict)
        if not is_valid:
            raise RuntimeError("Could not generate pathways in a valid way (message: {}).".format(msg))
        
        return all_pathways_dict
    
    
    
    
    
    def _validate_pathways_dicts(self, pathways):
        """Check if generated pathways are valid.
        
        Parameters
        ----------
        pathways : list of dict
            todo
        
        Returns
        -------
        is_valid : bool
            Whether the given pathways are valid in terms of type, shape, size
            and so on.
        msg : str
            Message giving more information about the validation, i.e. why it
            might have failed.
        """
        
        msg = "undefined error message"
        
        # check general shape of pathways
        if not isinstance(pathways, list):
            msg = "'pathways' object must be a list"
            return False, msg
        if not len(pathways) == self._n_channels:
            msg = "'pathways' object has length {}, but number of channels is {}".format(len(pathways), self._n_channels)
            return False, msg
        
        # loop over all channels
        for idx_channel in range(self._n_channels):
            
            # each element of pathways must be a list of length n_steps = n_blocks+1
            if not isinstance(pathways[idx_channel], list):
                msg = "all elements of 'pathways' object must be a list, but element {} is not".format(idx_channel)
                return False, msg
            n_blocks = self._n_blocks[idx_channel]
            if not len(pathways[idx_channel]) == n_blocks+1:
                msg = ("element {} of 'pathways' object has length {}, but number of"
                    " steps is {} for this channel".format(
                        idx_channel, len(pathways[idx_channel]), n_blocks+1))
                return False, msg
            
            has_none = False
            orders_from_last = set()
            
            # loop over all steps of this channel
            for idx_step in range(n_blocks+1):
                
                # alias for pathways of this step
                p = pathways[idx_channel][idx_step]
                
                # check type of elements of this step
                if not isinstance(p, dict):
                    msg = "pathways not a dict in step {} of channel {}".format(idx_step, idx_channel)
                    return False, msg
                if not all( isinstance(v, (set, frozenset)) or (v is None) for v in p.values() ):
                    msg = "not all elements of pathways dict are set, frozenset or NoneType in step {} of channel {}".format(idx_step, idx_channel)
                    return False, msg
                
                # only orders should appear, that are possible in general
                if not set(p).issubset(self._orders[idx_channel][idx_step]):
                    msg = "coherence order present are not a subset of allowed orders in step {} of channel {}".format(idx_step, idx_channel)
                    return False, msg
                
                # check if orders here are exactly the ones reachable from the last step
                if idx_step > 0:
                    if has_none:
                        if not orders_from_last.issubset(p.keys()):
                            msg = "orders reachable from last step are not a subset of the orders in step {} of channel {}".format(idx_step, idx_channel)
                            return False, msg
                    else:
                        if not orders_from_last == p.keys():
                            msg = "orders reachable from last step do not match the orders in step {} of channel {}".format(idx_step, idx_channel)
                            return False, msg
                
                # orders reachable from this step to next step for next iteration
                if idx_step < n_blocks:
                    has_none = False
                    orders_from_last = set()
                    for order in p:
                        if p[order] is None: has_none = True; continue
                        orders_from_last.update(p[order])
                # special treatment for last step (acquisition step)
                else:
                    for order in p:
                        if not p[order] is None:
                            msg = "reachable orders in final step is not None for order={} in channel {}".format(order, idx_channel)
                            return False, msg    
        
        msg = "pathways are valid"
        return True, msg
    
    
    
    
    
    def _generate_pathways(self, regenerate=False):
        """Generate the pathwys of this CTP object.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        # generate the pathways if not already exist or regenaration is desired explicitly
        if self._pathways is None or regenerate:
        
            pathways_dicts = self._generate_pathways_dicts()
            pathways = []
            for idx_channel in range(self._n_channels):
                pathways.append(Pathway(pathways_dicts[idx_channel]))
            self._pathways = pathways
    
    
    
    
    
    def purge(self):
        """Purge everything.
        
        This function will re-initialize the coherence orders in _orders,
        the changes in _changes and desired CTPs in _desired.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        
        # purge evrything
        self._init_orders()
        self._init_changes()
        self._init_desired()
    
    
    
    
    
    # getters for _n_channels
    
    def is_homonuclear(self):
        """Whether the CTP defines a homonuclear experiment.
        
        An experiment is homonuclear if the number of channels is one.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        is_homonuclear : bool
            Whether the experiment is homonuclear or not.
        """
        
        return self._n_channels == 1
    
    
    
    def is_heteronuclear(self):
        """Whether the CTP defines a heteronuclear experiment.
        
        An experiment is heteronuclear if the number of channels is larger
        then one.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        is_heteronuclear : bool
            Whether the experiment is heteronuclear or not.
        """
        
        return not self.is_homonuclear()
    
    
    
    def get_n_channels(self):
        """Get the number of channels of the experiment.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        n_channels : int
            Number of channels of this experiment.
        """
        
        return self._n_channels
    
    
    
    def get_n_blocks(self, channel_idx):
        """Get the number of blocks for a given channel.
        
        Parameters
        ----------
        channel_idx : int , optional
            Index of the relevant channel. Can be a single index or object
            convertible to an integer. For homonuclear experiments this
            parameter is redundant and will assumed to be just 0. Only in
            this case `None` can also be given.
        
        Returns
        -------
        n_blocks : int
            Number of blocks (where coherence orders change) for the
            given channel.
        """
        
        channel_idx = self._normalize_channel_index(channel_idx)
        return self._n_blocks[channel_idx]
    
    
    
    def get_n_steps(self, channel_idx):
        """Get the number of steps for a given channel.
        
        Parameters
        ----------
        channel_idx : int , optional
            Index of the relevant channel. Can be a single index or object
            convertible to an integer. For homonuclear experiments this
            parameter is redundant and will assumed to be just 0. Only in
            this case `None` can also be given.
        
        Returns
        -------
        n_steps : int
            Number of steps (where coherence orders stay the same) for the
            given channel.
        
        """
        
        channel_idx = self._normalize_channel_index(channel_idx)
        return self._n_blocks[channel_idx]+1
    
    
    
    # setting coherence orders
    
    def set_orders(self, orders, step_idxs, channel_idxs=None):
        """Set the coherence orders for given steps and channels.
        
        Parameters
        ----------
        orders : intlist castable
            Coherence orders to set for the given steps and channels. Only
            unique orders will be kept.
        step_idxs : int, list or str
            todo
        channel_idxs
        
        Returns
        -------
        None
        """
        
        # clear pathways as they are invalid now
        self._pathways = None
        
        # normalize the input
        orders = self._convert_unique_intlist(orders)
        step_idxs, channel_idxs = self._normalize_step_channel_indices(step_idxs, channel_idxs)
        
        for i, idx in enumerate(channel_idxs):
            for jdx in step_idxs[i]:
                self._orders[idx][jdx].clear()
                self._orders[idx][jdx].update(orders)
    
    
    
    def add_orders(self, orders, step_idxs, channel_idxs=None):
        """Add coherence orders to given steps of channels.
        
        Parameters
        ----------
        orders : intlist castable
            Coherence orders to set for the given steps and channels. Only
            unique orders will be kept.
        step_idxs : todo
        channel_idxs : todo
        
        Returns
        -------
        None
        """
        
        # clear pathways as they are invalid now
        self._pathways = None
        
        # normalize the input
        orders = self._convert_unique_intlist(orders)
        step_idxs, channel_idxs = self._normalize_step_channel_indices(step_idxs, channel_idxs)
        
        for i, idx in enumerate(channel_idxs):
            for jdx in step_idxs[i]:
                self._orders[idx][jdx].update(orders)
    
    
    
    def remove_orders(self, orders, step_idxs, channel_idxs=None):
        """Remove coherence orders from given steps of channels.
        
        Parameters
        ----------
        orders : intlist castable
            Coherence orders to set for the given steps and channels. Only
            unique orders will be kept.
        
        Returns
        -------
        None
        """
        
        # delete the pathways as they are invalid now
        self._pathways = None
        
        if isinstance(orders, str):
            if orders.lower() == 'all':
                self.set_orders([], step_idxs, channel_idxs)
            
        else:
            orders = self._convert_unique_intlist(orders)
            step_idxs, channel_idxs = self._normalize_step_channel_indices(step_idxs, channel_idxs)
            
            for idx in channel_idxs:
                for jdx in step_idxs[idx]:
                    intersection = self._orders[idx][jdx].intersection(orders)
                    self._orders[idx][jdx] -= intersection
    
    
    
    # aliases and some convinience functions for set_orders
    
    def set_initial_orders(self, orders, channel_idxs=None):
        """"""
        self.set_orders(orders, 'start', channel_idxs)
    
    def set_final_orders(self, orders, channel_idxs=None):
        """"""
        self.set_orders(orders, 'end', channel_idxs)
    
    def set_orders_frommax(self, max_order, step_idxs, channel_idxs=None):
        """"""
        
        max_order = int(max_order)
        orders = [i for i in range(-max_order, max_order+1)]
        self.set_orders(orders, step_idxs, channel_idxs)
    
    def set_orders_fromrange(self, min_order, max_order, step_idxs, channel_idxs=None):
        """"""
        
        min_order, max_order = int(min_order), int(max_order)
        min_order, max_order = min(min_order, max_order), max(min_order, max_order)
        if min_order > max_order:
            raise ValueError('`min_order` cannot be greater than `max_order`.')
        orders = [i for i in range(min_order, max_order+1)]
        self.set_orders(orders, step_idxs, channel_idxs)
    
    
    
    # aliases and some convinience functions for add_orders
    
    def add_initial_orders(self, orders, channel_idxs=None):
        """Add coherence orders to the initial step of the specified channels.
        
        Parameters
        ----------
        
        Returns
        -------
        None
        """
        
        self.add_orders(orders, 'start', channel_idxs)
    
    def add_final_orders(self, orders, channel_idxs=None):
        """"""
        self.add_orders(orders, 'end', channel_idxs)
    
    def add_orders_frommax(self, max_order, step_idxs, channel_idxs=None):
        """"""
        
        max_order = int(max_order)
        orders = [i for i in range(-max_order, max_order+1)]
        self.add_orders(orders, step_idxs, channel_idxs)
    
    def set_orders_fromrange(self, min_order, max_order, step_idxs, channel_idxs=None):
        """"""
        
        min_order, max_order = int(min_order), int(max_order)
        min_order, max_order = min(min_order, max_order), max(min_order, max_order)
        if min_order > max_order:
            raise ValueError("`min_order` cannot be greater than `max_order`.")
        orders = [i for i in range(min_order, max_order+1)]
        self.add_orders(orders, step_idxs, channel_idxs)
    
    
    
    # setting banned coherence order changes
    
    def remove_initial_orders(self, orders, channel_idxs=None):
        """"""
        
        self.remove_orders(orders, 'start', channel_idxs)
    
    def remove_final_orders(self, orders, channel_idxs=None):
        """"""
        
        self.remove_orders(orders, 'end', channel_idxs)
    
    def remove_orders_frommax(self, max_order, step_idxs, channel_idxs=None):
        """"""
        
        max_order = int(max_order)
        orders = [i for i in range(-max_order, max_order+1)]
        self.remove_orders(orders, step_idxs, channel_idxs)
    
    def remove_orders_fromrange(self, min_order, max_order, step_idxs, channel_idxs=None):
        """"""
        
        min_order, max_order = int(min_order), int(max_order)
        min_order, max_order = min(min_order, max_order), max(min_order, max_order)
        if min_order > max_order:
            raise ValueError('`min_order` cannot be greater than `max_order`.')
        orders = [i for i in range(min_order, max_order+1)]
        self.remove_orders(orders, step_idxs, channel_idxs)
        
        
    
    # setting coherence order changes
    
    def set_changes_mode(self, changes_mode, block_idxs, channel_idxs=None):
        """Set coherence order changes mode."""
        
        self._pathways = None
        
        changes_mode = self._normalize_changes_mode(changes_mode)
        if changes_mode is None:
            raise ValueError("Changes mode must be 'allowed' or 'forbidden'.")
        block_idxs, channel_idxs = self._normalize_block_channel_indices(block_idxs, channel_idxs)
        
        for i, channel_idx in enumerate(channel_idxs):
            for changes_idx in block_idxs[i]:
        
                if not changes_idx in self._changes[channel_idx]:
                    self._changes[channel_idx].update({changes_idx: {'mode': changes_mode, 'values': set()}})
                
                else:
                    self._changes[channel_idx][changes_idx]['mode'] = changes_mode
        
    
    def set_changes(self, changes, block_idxs, channel_idxs=None, changes_mode=None):
        """Set coherene order changes."""
        
        self._pathways = None
        
        # normalize the input
        block_idxs, channel_idxs = self._normalize_block_channel_indices(block_idxs, channel_idxs)
        changes_mode = self._normalize_changes_mode(changes_mode)
        
        changes = self._convert_unique_intlist(changes)
        
        for i, channel_idx in enumerate(channel_idxs):
            for changes_idx in block_idxs[i]:
            
                if not changes_idx in self._changes[channel_idx]:
                    if changes_mode is None:
                        raise ValueError("mode must be given")
                        
                    self._changes[channel_idx].update({changes_idx: {'mode': changes_mode, 'values': set(changes)}})
                 
                else:
                    entry = self._changes[channel_idx][changes_idx]
                    if not changes_mode is None:
                        entry['mode'] = changes_mode
                    
                    entry['values'].clear()
                    entry['values'].update(changes)
                
            
    def add_changes(self, changes, block_idxs, channel_idxs=None, changes_mode=None):
        """Add coherence order changes."""
        
        self._pathways = None
        
        # normalize the input
        block_idxs, channel_idxs = self._normalize_block_channel_indices(block_idxs, channel_idxs)
        changes_mode = self._normalize_changes_mode(changes_mode)
        
        changes = self._convert_unique_intlist(changes)
        
        for i, channel_idx in enumerate(channel_idxs):
            for changes_idx in block_idxs[i]:
        
                if not changes_idx in self._changes[channel_idx]:
                    if changes_mode is None:
                        raise ValueError("mode must be given")
                        
                    self._changes[channel_idx].update({changes_idx: {'mode': changes_mode, 'values': set(changes)}})
                 
                else:
                    entry = self._changes[channel_idx][changes_idx]
                    if not changes_mode is None:
                        entry['mode'] = changes_mode
                    
                    entry['values'].update(changes)
            
            
    def remove_changes(self, changes, block_idxs, channel_idxs=None, changes_mode=None):
        """"""
        
        self._pathways = None
        
        # normalize the input
        block_idxs, channel_idxs = self._normalize_block_channel_indices(block_idxs, channel_idxs)
        changes_mode = self._normalize_changes_mode(changes_mode)
        
        changes = self._convert_unique_intlist(changes)
        
        for i, channel_idx in enumerate(channel_idxs):
            for changes_idx in block_idxs[i]:
        
                if not changes_idx in self._changes[channel_idx]:
                    if changes_mode is None:
                        raise ValueError("mode must be given")
                        
                    self._changes[channel_idx].update({changes_idx: {'mode': changes_mode, 'values': set()}})
                 
                else:
                    entry = self._changes[channel_idx][changes_idx]
                    if not changes_mode is None:
                        entry['mode'] = changes_mode
                    
                    intersection = entry['values'].intersection(changes)
                    entry['values'] -= intersection
            
            
    
    def purge_changes(self, block_idxs, channel_idxs=None):
        """Remove all coherence order changes."""
        
        self._pathways = None
        
        # normalize the input
        block_idxs, channel_idxs = self._normalize_block_channel_indices(block_idxs, channel_idxs)
        
        for i, channel_idx in enumerate(channel_idxs):
            for changes_idx in block_idxs[i]:
        
                self._changes[channel_idx].pop(changes_idx, None)
    
    
    
    # desired CTP handeling
                
    def _are_all_desired_ctps_valid(self):
        """Check if all defined CTPs are valid.
        
        This function also checks, if the reference CTP (if it is defined) is
        actually a desired CTP.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        all_valid : bool
            Whether all desired CTPs are valid and the reference CTP is also
            desired.
        """
        
        for desired_ctp in self._desired:
            for idx_channel in range(self._n_channels):
                if desired_ctp[idx_channel] not in self._pathways[idx_channel]:
                    return False
        
        # check if reference CTP is a desired CTP
        if self._reference is not None and self._reference not in self._desired:
            return False
        
        return True
        
        
        
    
    def add_desired_ctp(self, desired_ctp, set_as_reference=False):
        """Add a desired CTP.
        
        Add a desired CTP to the internal set of desired CTPs. It can also
        be set as the reference CTP.
        
        Parameters
        ----------
        desired_ctp : array_like
            Desired CTP to add.
        set_as_reference : bool
            Set the given CTP as the reference CTP.
        
        Returns
        -------
        None
        """
        
        # normalize the given CTP
        desired_ctp = self._normalize_given_ctp(desired_ctp)
        
        # set CTP as reference CTP
        if set_as_reference:
            # inform user when reference CTP already defined
            if self._reference is not None:
                print("Replacing reference CTP")
            self._reference = desired_ctp
        
        self._desired.update((desired_ctp,))
    
    
    
    
    def remove_desired_ctp(self, desired_ctp):
        """Remove a desired CTP."""
        
        desired_ctp = self._normalize_given_ctp(desired_ctp)
        
        # check if removed CTP is reference CTP
        if self._reference is not None and desired_ctp == self._reference:
            print("Reference CTP was removed.")
            self._reference = None
        
        self._desired.difference_update((desired_ctp,))
        
    
    def forget_reference(self):
        """Forget what desired CTP is the reference CTP."""
        
        self._reference = None
    
    
    
     # other useful functions
    
    def is_ctp_valid(self, ctp):
        """Check if a given CTP is valid.
        
        A given CTP is valid if it does not break any rule specified in this
        CTP object. For every channel, only possible coherence orders are
        present in every step and only allowed changes or not forbidden changes
        of coherence orders occur.
        This function should give the same result as `ctp in self` but does not
        need to generate the Pathways objects and so saves some time.
        
        Parameters
        ----------
        ctp : array_like
            The CTP to check.
        
        Returns
        -------
        is_valid : bool
            Whether the given CTP is valid or not.
        """
        
        ctp = self._normalize_given_ctp(ctp)
        
        n_channels = self._n_channels
        for idx_channel in range(n_channels):
            
            # alias names for this channel
            ctp_channel = ctp[idx_channel]
            orders = self._orders[idx_channel]
            changes = self._changes[idx_channel]
            n_steps = self._n_blocks[idx_channel] + 1
            
            # loop over all blocks of this channel
            for idx_step in range(n_steps):
                
                # check the current order possible
                if ctp_channel[idx_step] not in orders[idx_step]:
                    return False
                
                # check the coherence order changes (idx_step = n_steps-1 can never be in changes)
                if idx_step in changes:
                    
                    changes_mode = changes[idx_step]['mode']
                    changes_vals = changes[idx_step]['values']
                    
                    # get the actual change in the given CTP
                    # won't throw an IndexError because of ctp_channel[idx_step+1] because `n_steps-1 not in changes`
                    change = ctp_channel[idx_step+1] - ctp_channel[idx_step]
                    
                    if changes_mode == 'a':
                        if change not in changes_vals:
                            return False
                    elif changes_mode == 'f':
                        if change in changes_vals:
                            return False
                    else:
                        raise ValueError("Invalid changes mode '{}'.".format(changes_mode))
        
        return True
            
            
    
    
    def check_all_desired_possible(self):
        """Check if all given desired CTPs are possible.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        all_possible : bool
            Whether all desried are possible.
        impossible : list
            List of desired CTPs that are not possible.
        """
        
        impossible = []
        
        for desired_ctp in sorted(self._desired):
            if not self.is_ctp_valid(desired_ctp):
                impossible.append(desired_ctp)
            
        return len(impossible) == 0, impossible
        
    
    
    
    def get_ctp_broken_rules(self, ctp):
        """For a given CTP find all the rules that are broken according to this CTP instance."""
        
        ctp = self._normalize_given_ctp(ctp)
        broken_rules = []
        
        # loop over all channels
        for idx_channel in range(self._n_channels):
            
            # alias names for this channel
            ctp_channel = ctp[idx_channel]
            orders = self._orders[idx_channel]
            changes = self._changes[idx_channel]
            
            # loop over all blocks of this channel
            for idx_block in range(self._n_blocks[idx_channel]+1):
                
                # check the current order
                if ctp_channel[idx_block] not in orders[idx_block]:
                    broken_rules.append("Channel {}, step {}: Order {:>+} not allowed.".format(idx_channel, idx_block, ctp_channel[idx_block]))
                
                if idx_block in changes:
                    
                    changes_mode = changes[idx_block]['mode']
                    changes_vals = changes[idx_block]['values']
                    
                    change = ctp_channel[idx_block+1] - ctp_channel[idx_block]
                    
                    if changes_mode == 'a':
                        if change not in changes_vals:
                            broken_rules.append("Channel {}, block {}: Change {:>+} ({:>+} --> {:>+}) not allowed (only {}).".format(
                                idx_channel, idx_block, change, ctp_channel[idx_block], ctp_channel[idx_block+1], sorted(changes_vals)))
                    elif changes_mode == 'f':
                        if change in changes_vals:
                            broken_rules.append("Channel {}, block {}: Change {:>+} ({:>+} --> {:>+}) not allowed.".format(idx_channel, idx_block, change, ctp_channel[idx_block], ctp_channel[idx_block+1]))
                    else:
                        raise ValueError("Invalid changes mode '{}'.".format(changes_mode))
                    
            
            
        
        return broken_rules
        
        
        
        
        
    def _generate_numpy_array_channel(self, idx_channel, max_MB=100):
        """Generate CTPs for a specified channel.
        
        Parameters
        ----------
        
        Returns
        -------
        """
        
        idx_channel = self._normalize_channel_index(idx_channel)
        
        dtype = np.dtype(np.int64)
        
        self._generate_pathways()
        
        n_blocks = self._n_blocks[idx_channel]
        n_steps = n_blocks + 1
        pathway = self._pathways[idx_channel]
        
        # try to estimate the array size used
        
        array_size = n_steps*len(pathway)
        
        total_size_bytes = array_size * dtype.itemsize
        if total_size_bytes > max_MB * 1000 * 1000:
            raise MemoryError("Output array would be too big.")
        
        
        arr = np.zeros(shape=(len(pathway), n_steps), dtype=dtype)
        nodes = pathway.get_nodes(0)
        
        for idx_step in range(n_steps):
            
            reps = [pathway.get_n_forward_paths(idx_step, node) for node in nodes]
            arr[:,idx_step] = np.repeat(np.array(nodes, dtype=dtype), reps)
            new_nodes = []
            for node in nodes:
                new_nodes += pathway.get_forward_nodes(idx_step, node)
            nodes = new_nodes
            
        return arr
        
        


    def generate_numpy_array(self, what, collapse=True, push_desired_up=False, max_MB=100):
        """ToDo
        
        Parameters
        ----------
        what : ...
            ...
        collapse : bool
            ...
        max_MB : int
            ...
        
        Returns
        -------
        arr : ...
            ...
        metadata : ...
            ...
        """
        
        
        
        # re-generate the pathways
        self._generate_pathways(regenerate=True)
        
        # first entry, whether to perform difference, second entry: whether to give relative to reference
        config = {'ctps'  : (False, False),
                  'ctps0' : (False, True ),
                  'dctps' : (True , False),
                  'dctps0': (True , True )
                  }
        
        # check the input
        what = what.lower()
        if what not in config.keys():
            raise ValueError("Invalid value '{}' for argument `what`.".format(what))
        calc_diff, calc_ref = config[what]
        
        # some general declarations
        n_channels = self._n_channels
        dtype = np.dtype(np.int64)
        metadata = {"type": str(what), "collapsed": bool(collapse)}
        
        # some checks before we start
        
        if calc_ref:
            if self._reference is None:
                raise ValueError("Cannot calculate relative to reference because no reference is defined.")
            ref = [np.array(self._reference[i], dtype=dtype) for i in range(n_channels)]
            metadata.update({"ref_ctps": tuple(tuple(r) for r in ref)})
        
        # check if all desired CTPs are possible
        if not self._are_all_desired_ctps_valid():
            raise ValueError("Cannot generate the CTPs because not all desired CTPs are valid.")
        
        
        n_steps = []
        n_ctps = []
        add = {True: 0, False: 1}[calc_diff]
        for idx_channel in range(n_channels):
            n_steps.append( self._n_blocks[idx_channel] + add )
            n_ctps.append( len(self._pathways[idx_channel]) )
        
        n_ctps_total = mprod(n_ctps)
        metadata.update({"block_sizes": n_steps.copy(), "n_tot": int(n_ctps_total)})
        
        
        if collapse:
            
            arr = np.zeros(shape=(n_ctps_total,sum(n_steps)), dtype=dtype)
            
            cnt_tile = 1
            cnt_reap = n_ctps_total
            cnt_block = 0
            for idx_channel in range(n_channels):
                
                # devide before array is constructed
                cnt_reap //= n_ctps[idx_channel]
                
                a = self._generate_numpy_array_channel(idx_channel)
                
                if calc_ref:
                    a -= ref[idx_channel][None,:]
                if calc_diff:
                    a = np.diff(a, axis=1)
                
                # set the elements for this block
                arr[:,cnt_block:cnt_block+n_steps[idx_channel]] = (
                    np.repeat( np.tile(a,reps=(cnt_tile,1)), repeats=cnt_reap, axis=0 ))
                
                # multiply after array is constructed
                cnt_tile *= n_ctps[idx_channel]
                cnt_block += n_steps[idx_channel]
                
            # sanity check
            if not cnt_reap == 1 or not cnt_tile == n_ctps_total:
                raise RuntimeError("Internal sanity check failed in `generate_numpy_array`.")
            
            
            # push the desired CTPs to the top of the array, if reference CTP is defined it will be first
            if push_desired_up:
                
                # predict indices of desired CTPs
                
                desired_ctps = sorted(self._desired)
                metadata.update({'n_desired': len(desired_ctps)})
                # make reference the first CTP
                if self._reference is not None:
                    desired_ctps.remove(self._reference)
                    desired_ctps.insert(0, self._reference)
                
                desired_indices = [self.get_ctp_index(w) for w in desired_ctps]
                desired_ctps_arr = []
                for idx_channel in range(n_channels):
                    a = np.array([c[idx_channel] for c in desired_ctps], dtype=dtype)
                    if calc_ref:
                        a -= ref[idx_channel][None,:]
                    if calc_diff:
                        a = np.diff(a, axis=1)
                    desired_ctps_arr.append(a)
                desired_ctps_arr = np.concatenate(desired_ctps_arr, axis=1)
                
                # sanity check if the indices found are the real desired CTPs
                if not np.all(arr[desired_indices] == desired_ctps_arr):
                    raise RuntimeError("Internal sanity check failed in `generate_numpy_array`.")
                    
                # copy desired CTPs to the front (although concatenation wir np.delete is not very memory efficient)
                arr = np.concatenate( (arr[desired_indices,:],
                                       np.delete(arr,desired_indices,axis=0)),
                                    axis=0)
                
            return arr, metadata
        
        # if not collapse
        else:
            
            arr = []
            
            for idx_channel in range(n_channels):
                
                a = self._generate_numpy_array_channel(idx_channel)
                if calc_ref:
                    a -= ref[idx_channel][None,:]
                if calc_diff:
                    a = np.diff(a, axis=1)
                    
                # sanity check
                if not a.shape == (n_ctps[idx_channel],n_steps[idx_channel]):
                    raise RuntimeError("Internal sanity check failed in `generate_numpy_array`.")
                
                arr.append(a)
            
            
            return arr, metadata


