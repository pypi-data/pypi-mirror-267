"""
dlg_example_cmpts appComponent module.

This is the module of dlg_example_cmpts containing DALiuGE
application components.
Here you put your main application classes and objects.

Typically a component project will contain multiple components and will
then result in a single EAGLE palette.

Be creative! do whatever you need to do!
"""

__version__ = "0.1.19"
import json
import logging
import os
import pickle
from glob import glob
from urllib.request import url2pathname

import numpy as np
import requests  # type: ignore
from dlg import droputils
from dlg.meta import dlg_int_param, dlg_string_param

try:
    from dlg.drop import BarrierAppDROP
except ImportError:
    from dlg.apps.app_base import BarrierAppDROP

try:
    from dlg.drop import BranchAppDrop
except ImportError:
    from dlg.apps.branch import BranchAppDrop


logger = logging.getLogger(__name__)


##
# @brief MyBranch
# @details Simple app to demonstrate how to write a branch actually making a
# decision and passing data on.
# Most of the code is boilerplate and can be copied verbatim. Note that a
# branch app is allowed
# to have multiple inputs, but just exactly two outputs. This example is using
# just a single input. There is an associated logical graph available on
# github:
#
#    https://github.com//EAGLE-graph-repo/examples/branchDemo.graph
#
# The application assumes to receive a random floating point array with values
# in the range [0,1] on input. It will calculate the mean of that array and
# then branch depending on whether the mean is smaller or larger than 0.5.
#
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.MyBranch/String/ComponentParameter/readonly//False/False/Application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param array array//Object.Array/InputPort/readwrite//False/False/Port receiving the input array # noqa: E501
# @param yes yes//float/OutputPort/readwrite//False/False/English Port carrying the mean value of the array if mean < 0.5 # noqa: E501
# @param no no//float/OutputPort/readwrite//False/False/English Port carrying the mean value of the array if mean >= 0.5 # noqa: E501
# @par EAGLE_END


class MyBranch(BranchAppDrop):
    def run(self):
        """
        Just reading the input array and calculating the mean.
        """
        input = self.inputs[0]
        data = pickle.loads(droputils.allDropContents(input))
        self.value = data.mean()

    def writeData(self):
        """
        Prepare the data and write to port (self.ind) identified by condition.
        """
        output = self.outputs[self.ind]
        d = pickle.dumps(self.value)
        output.len = len(d)
        output.write(d)

    def condition(self):
        """
        Check value, call write method and return boolean.
        """
        if self.value < 0.5:
            self.ind = 0
            result = True
        else:
            self.ind = 1
            result = False
        self.writeData()
        return result


##
# @brief LengthCheck
#
# This branch returns true if the length of the input array is > 0. It also
# passes the array on to the output ports (will be an empty array in the case
# of N==0).
#
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.MyBranch/String/ComponentParameter/readonly//False/False/Application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param array array//Object.Array/InputPort/readwrite//False/False/Port receiving the input array # noqa: E501
# @param yes yes//float/OutputPort/readwrite//False/False/English Port carrying the mean value of the array if mean < 0.5 # noqa: E501
# @param no no//float/OutputPort/readwrite//False/False/English Port carrying the mean value of the array if mean >= 0.5 # noqa: E501
# @par EAGLE_END


class LengthCheck(BranchAppDrop):
    def initialize(self, **kwargs):
        BranchAppDrop.initialize(self, **kwargs)

    def readData(self):
        """
        Just reading the inoput array and determining the size
        """
        input = self.inputs[0]
        self.raw = droputils.allDropContents(input)
        data = pickle.loads(self.raw)
        # make sure we always have a ndarray with at least 1dim.
        if isinstance(data, np.ndarray):
            # that's what we want..
            if data.size == 0:
                # fix this strange case
                data = np.array([data])
                self.raw = pickle.dumps(data)
        elif not isinstance(data, np.ndarray) and type(data) not in (
            list,
            tuple,
        ):
            raise TypeError
        else:
            # can only be list or tuple. convert those.
            data = np.array(data)
            self.raw = pickle.dumps(data)

        self.value = data.size

    def writeData(self):
        """
        Write unmodified data to port (self.ind) identified by condition.
        """
        output = self.outputs[self.ind]
        output.len = self.value
        output.write(self.raw)

    def condition(self):
        """
        Check value, call write method and return boolean.
        """
        self.readData()
        if self.value > 0:
            self.ind = 0
            result = True
        else:
            self.ind = 1
            result = False
        self.writeData()
        return result

    def run(self):
        self.readData()


##
# @brief FileGlob
# @details An App that uses glob to find all files matching a
# template given by a filepath and a wildcard string
#
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.FileGlob/String/ComponentParameter/readonly//False/False/Application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param wildcard wildcard/"*"/String/InputPort/readwrite//False/False/Port receiving the search pattern # noqa: E501
# @param filepath filepath/"."/String/InputPort/readwrite//False/False/Port receiving the path to search # noqa: E501
# @param file_list file_list//Object.array/OutputPort/readwrite//False/False/Port carrying the resulting file_list # noqa: E501
# @par EAGLE_END


class FileGlob(BarrierAppDROP):
    """
    Simple app collecting file names in a directory
    based on a wild-card pattern
    """

    wildcard = dlg_string_param("wildcard", None)
    filepath = dlg_string_param("filepath", None)

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        for output in self.outputs:
            d = pickle.dumps(self.value)
            output.len = len(d)
            output.write(d)

    def run(self):
        filetmpl = f"{self.filepath}/{self.wildcard}"
        filetmpl = os.path.expandvars(filetmpl)
        logger.debug(f"Looking for files matching {filetmpl}")
        files = glob(filetmpl)
        self.value = [f for f in files if os.path.isfile(f)]
        if len(self.value) == 0:
            logger.warning(f"No matching files found for {filetmpl}")
        else:
            logger.info(f"Number of files found matching {filetmpl}: {len(self.value)}")
        self.writeData()


##
# @brief ExtractColumn
# @details App that extracts one column of an table-like ndarray. The array is
# assumed to be row major, i.e. the second index refers to columns.
# The column is # selected by index counting from 0. If the array is 1-D the
# result is a 1 element array. The component is passing whatever type is in
# the selected column.
#
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.ExtractColumn/String/ComponentParameter/readonly//False/False/Import path for application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param index index/0/Integer/ApplicationArgument/readwrite//False/False/0-base index of column to extract # noqa: E501
# @param table_array table_array//array/InputPort/readwrite//False/False/List of elements # noqa: E501
# @param column column//Object.1Darray/OutputPort/readwrite//False/False/Port carrying the first element of input array # noqa: E501
#               the type is dependent on the list element type.
# @par EAGLE_END
class ExtractColumn(BarrierAppDROP):
    """
    Simple app extracting a column from a 2D ndarray.
    """

    index = dlg_int_param("index", None)

    def readData(self):
        input = self.inputs[0]
        table_array = pickle.loads(droputils.allDropContents(input))

        # make sure we always have a ndarray with 2dim.
        if not isinstance(table_array, (np.ndarray)) or table_array.ndim != 2:
            raise TypeError
        self.column = table_array[:, self.index]

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            if output.name == "column":
                d = pickle.dumps(self.column)
                output.len = len(d)
            output.write(d)

    def run(self):
        self.readData()
        self.writeData()


class LocalFileAdapter(requests.adapters.BaseAdapter):
    """Helper protocol Adapter to allow Requests to GET file:// URLs"""

    @staticmethod
    def _chkpath(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ("put", "delete"):
            return 501, "Not Implemented"  # TODO
        elif method.lower() not in ("get", "head"):
            return 405, "Method Not Allowed"
        elif os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):  # pylint: disable=unused-argument
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        @todo: Should I bother filling `response.headers` and processing
               If-Modified-Since and friends using `os.stat`?
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)
        if response.status_code == 200 and req.method.lower() != "head":
            try:
                response.raw = open(path, "rb")
            except (OSError, IOError) as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


##
# @brief AdvUrlRetrieve
# @details An APP that retrieves the content of a URL and writes
# it to all outputs. The URL can be specified either completely or
# partially through the inputs. In that case the urlTempl parameter can
# use placeholders to construct the final URL.
# @par EAGLE_START
# @param category PythonApp
# @param dropclass droplass/dlg_example_cmpts.apps.AdvUrlRetrieve/String/ComponentParameter/readonly//False/False/Application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param urlTempl urlTempl/"https://eagle.icrar.org"/String/ApplicationArgument/readwrite//False/False/The URL to retrieve # noqa: E501
# @param urlPart urlPart//String/InputPort/readwrite//False/False/The port carrying the content read from the URL. # noqa: E501
# @param content content//String/OutputPort/readwrite//False/False/The port carrying the content read from the URL. # noqa: E501
# @par EAGLE_END
class AdvUrlRetrieve(BarrierAppDROP):
    """
    An App that retrieves the content of a URL and allows to construct the URL
    through input placeholders.

    Keywords:
    URL:   string, URL to retrieve.
    """

    urlTempl = dlg_string_param("urlTempl", None)

    def constructUrl(self):
        url = self.urlTempl
        # this will ignore inputs not referenced in template
        # if isinstance(self.urlParts, list):
        #     for x, v in enumerate(self.urlParts):
        #         pathRef = "%%i%d" % (x,)
        #         if pathRef in url:
        #             url = url.replace(pathRef, v)
        i = 0
        if isinstance(self.urlParts, dict):
            # named ports support
            for n, v in self.urlParts.items():
                nRef = "{%s}" % n
                if nRef in url:
                    url = url.replace(nRef, v)
                # fallback to %iX format
                pathRef = "%%i%d" % (i,)
                if pathRef in url:
                    url = url.replace(pathRef, v)
                i += 1
        else:
            raise TypeError
        logger.info(f"Constructed URL: {url}")
        return url

    def readData(self):
        # for this app we are expecting URL fractions on the inputs
        urlParts = {}
        named_inputs = self._generateNamedPorts("inputs")
        idict = named_inputs
        if len(named_inputs) > 0:
            idict = named_inputs
        else:
            idict = dict(enumerate(self.inputs))
            # idict = {y: x for x, y in idict.items()}
        # elif isinstance(named_inputs, dict):
        #     idict = self.inputs
        logger.debug("Inputs identified: %s", idict)
        for name, input in idict.items():
            part = pickle.loads(droputils.allDropContents(input))
            # make sure the placeholders are strings
            logger.info(f"URL part: {name}:{part}")
            if not isinstance(part, str):
                raise TypeError
            urlParts.update({name: part})
        self.urlParts = urlParts
        self.url = self.constructUrl()
        requests_session = requests.session()
        if "file://" == self.url[:7]:
            requests_session.mount("file://", LocalFileAdapter())
        logger.info("Reading from %s", self.url)
        try:
            u = requests_session.get(self.url)
        except Exception as e:
            raise e
        # finally read the content of the URL
        self.content = u.content

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        outs = self.outputs
        written = False
        if len(outs) < 1:
            raise Exception("At least one output required for %r" % self)
        for output in outs:
            if output.name.lower() == "content":
                # we are not pickling here, but just pass on the data.
                output.len = len(self.content)
                output.write(self.content)
                written = True
            else:
                logger.warning(f"Output with name {output.name} ignored!")

        if not written:
            raise TypeError("No matching output drop found." + "Nothing written")

    def run(self):
        self.readData()
        self.writeData()


##
# @brief String2JSON
# @details App that reads a string from a single input and tries
# to convert that to JSON. If port is converted into an argument the
# JSON value is taken from there.
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.String2JSON/String/ComponentParameter/readonly//False/False/Application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param string string//String/InputPort/readwrite//False/False/String to be converted # noqa: E501
# @param element element//Object.json/OutputPort/readwrite//False/False/Port carrying the JSON structure # noqa: E501
# @par EAGLE_END
class String2JSON(BarrierAppDROP):
    string = dlg_string_param("string", None)

    def readData(self):
        input = self.inputs[0]  # ignore all but the first
        try:
            data = json.loads(droputils.allDropContents(input))
        except json.decoder.JSONDecodeError:
            raise TypeError
        return data

    def writeData(self, data):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            d = pickle.dumps(data)
            output.len = len(d)
            output.write(d)

    def run(self):
        if len(self.inputs) == 0:  # if there is no input use the argument value
            try:
                logger.debug("Input found: %s", self.string)
                data = json.loads(self.string)
            except TypeError:
                raise
        else:
            data = self.readData()
        self.writeData(data)
        del data  # make sure this is cleaned up


##
# @brief GenericGather
# @details App that reads all its inputs and simply writes them in
# concatenated to all its outputs. This can be used stand-alone or
# as part of a Gather. It does not do anything to the data, just
# passing it on.
#
# @par EAGLE_START
# @param category PythonApp
# @param dropclass dropclass/dlg_example_cmpts.apps.GenericGather/String/ComponentParameter/readonly//False/False/Import path for application class # noqa: E501
# @param execution_time execution_time/5/Float/ComponentParameter/readonly//False/False/Estimated execution time # noqa: E501
# @param num_cpus num_cpus/1/Integer/ComponentParameter/readonly//False/False/Number of cores used # noqa: E501
# @param input input//Object/InputPort/readwrite//False/False/0-base placeholder port for inputs # noqa: E501
# @param output output//Object/OutputPort/readwrite//False/False/Placeholder port for outputs # noqa: E501
# @par EAGLE_END
class GenericGather(BarrierAppDROP):
    def readWriteData(self):
        inputs = self.inputs
        outputs = self.outputs
        total_len = 0
        for input in inputs:
            total_len += input.len
        for output in outputs:
            output.len = total_len
            for input in inputs:
                d = droputils.allDropContents(input)
                output.write(d)

    def run(self):
        self.readWriteData()
