import io
import json
import shutil
import time
import warnings
from importlib.util import find_spec
from json.decoder import JSONDecodeError
from typing import Callable, Dict, Optional, Literal
from urllib.parse import urlparse
from pathlib import Path
from zipfile import ZipFile
import os

import luminesce
import pandas as pd
from fbnsdkutilities import ApiClientFactory
from luminesce.exceptions import ApiException

import lumipy
from lumipy.common import indent_str, table_spec_to_df
from lumipy._config_manager import config
from lumipy.query_job import QueryJob
from tqdm import tqdm

if find_spec('IPython') is not None:
    from IPython.display import clear_output


def _add_lumipy_tag(sql: str):
    if hasattr(lumipy, '__version__'):
        version = lumipy.__version__
    else:
        version = ''
    return f'-- lumipy {version}\n{sql}'


class Client:
    """Higher level client that wraps the low-level luminesce python sdk. This client offers a smaller collection of
    methods for starting, monitoring and retrieving queries as Pandas DataFrames.

    """

    def __init__(self, max_retries: Optional[int] = 5, retry_wait: Optional[float] = 0.5, **kwargs):
        """__init__ method of the lumipy client class. It is recommended that you use the lumipy.get_client() function
        at the top of the library.

        Args:
            max_retries (Optional[int]): number of times to retry a request after receiving an error code.
            code.
            retry_wait (Optional[float]):time in seconds to wait to try again after receiving an error code.
            code.

        Keyword Args:
            token (str): Bearer token used to initialise the API
            api_secrets_filename (str): Name of secrets file (including full path)
            api_url (str): luminesce API url
            app_name (str): Application name (optional)
            certificate_filename (str): Name of the certificate file (.pem, .cer or .crt)
            proxy_url (str): The url of the proxy to use including the port e.g. http://myproxy.com:8888
            proxy_username (str): The username for the proxy to use
            proxy_password (str): The password for the proxy to use
            correlation_id (str): Correlation id for all calls made from the returned finbournesdkclient API instances

        """

        self._factory = ApiClientFactory(luminesce, **kwargs)

        self._catalog_api = self._factory.build(luminesce.api.CurrentTableFieldCatalogApi)
        self._sql_exec_api = self._factory.build(luminesce.api.SqlExecutionApi)
        self._sql_bkg_exec_api = self._factory.build(luminesce.api.SqlBackgroundExecutionApi)
        self._history_api = self._factory.build(luminesce.api.HistoricallyExecutedQueriesApi)
        self._design_api = self._factory.build(luminesce.api.SqlDesignApi)
        self._certs_management = self._factory.build(luminesce.api.CertificateManagementApi)
        self._binary_download = self._factory.build(luminesce.api.BinaryDownloadingApi)

        self.max_retries = max_retries
        self.retry_wait = retry_wait

    def get_token(self):
        return self._factory.api_client.configuration.access_token

    def get_domain(self) -> str:
        url = self._factory.api_client.configuration._base_path
        return str(urlparse(url).netloc.split('.')[0])

    def __repr__(self):
        return f'{type(self).__name__}(domain={self.get_domain()})'

    def _retry_handling(self, action: Callable, label: str, retry=False):
        """Wrap an api call to handle error retries and present more readable information from exceptions.

        Args:
            action (Callable): Parameterless function wrapping method call to luminesce, so it can be called repeatedly.
            label (str): name of the method being called.

        Returns:
            Any: the result of the luminesce python sdk api method call.
        """

        attempts = 0
        while True:
            try:
                return action()
            except ApiException as ae:
                if retry and attempts < self.max_retries:
                    attempts += 1
                    time.sleep(self.retry_wait)
                    print(f"Received {ae.status} status code. Retrying {attempts}/{self.max_retries}...")
                else:
                    if retry:
                        print(f"Max number of retries ({attempts + 1}) exceeded {self.max_retries}.")
                    print(f"Request to {label} failed with status code {ae.status}, reason: '{ae.reason})'.")
                    try:
                        body = json.loads(ae.body)
                        if 'detail' in body.keys():
                            detail = body['detail']
                            print(indent_str(f"Details:\n{indent_str(detail, n=4)}", n=4))
                    except JSONDecodeError:
                        print(indent_str(f"Details:\n{indent_str(str(ae.body), n=4)}", n=4))
                    raise ae

    def table_field_catalog(self) -> pd.DataFrame:
        """Get the table field catalog as a DataFrame.

        The table field catalog contains a row describing each field on each provider you have access to.

        Returns:
            DataFrame: dataframe containing table field catalog information.
        """
        res = self._retry_handling(
            self._catalog_api.get_catalog,
            'table field catalog'
        )
        return pd.DataFrame(json.loads(res))

    def query_and_fetch(
            self,
            sql: str,
            name: Optional[str] = 'query',
            timeout: Optional[int] = 175,
            **read_csv_params
    ) -> pd.DataFrame:
        """Send a query to Luminesce and get it back as a pandas dataframe.

        Args:
            sql (str): query sql to be sent to Luminesce
            name (str): name of the query (defaults to just 'query')
            timeout (int): max time for the query to run in seconds (defaults to 175)
            **read_csv_params (Any): keyword arguments to pass down to pandas read_csv. See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        Returns:
            DataFrame: result of the query as a pandas dataframe.
        """
        res = self._retry_handling(
            lambda: self._sql_exec_api.put_by_query_csv(
                body=_add_lumipy_tag(sql),
                query_name=name,
                timeout_seconds=timeout
            ),
            'query and fetch'
        )
        buffer_result = io.StringIO(res)
        return pd.read_csv(buffer_result, encoding='utf-8', **read_csv_params)

    def pretty(
            self,
            sql: str,
            **pretty_params
    ) -> pd.DataFrame:
        """Make a sql string pretty using Luminesce pretty method.

        Args:
            sql (str): query sql to be made pretty
            **pretty_params (Any): keyword arguments to be passed down to pretty method.

        Returns:
            str: a pretty sql string
        """
        res = self._retry_handling(
            lambda: self._design_api.put_query_to_format(
                body=_add_lumipy_tag(sql),
                **pretty_params
            ),
            'pretty'
        )
        return res

    def start_query(self, sql: str, name: Optional[str] = "query", timeout: Optional[int] = 3600, keep_for: Optional[int] = 7200) -> str:
        """Send an asynchronous query to Luminesce. Starts the query but does not wait and fetch the result.

        Args:
            sql (str): query sql to be sent to Luminesce
            name (str): name of the query (defaults to just 'query')
            timeout (int): max time for the query to run in seconds (defaults to 3600)
            keep_for (int): time to keep the query result for in seconds (defaults to 7200)

        Returns:
            str: string containing the execution ID

        """
        res = self._retry_handling(
            lambda: self._sql_bkg_exec_api.start_query(
                body=_add_lumipy_tag(sql),
                query_name=name,
                timeout_seconds=timeout,
                keep_for_seconds=keep_for
            ),
            'start query'
        )
        return res.execution_id

    def get_status(self, execution_id: str) -> Dict[str, str]:
        """Get the status of a Luminesce query

        Args:
            execution_id (str): unique execution ID of the query.

        Returns:
            Dict[str, str]: dictionary containing information on the query status.
        """
        return self._retry_handling(
            lambda: self._sql_bkg_exec_api.get_progress_of(execution_id).to_dict(),
            'get query status'
        )

    def delete_query(self, execution_id: str) -> Dict[str, str]:
        """Deletes a Luminesce query.

        Args:
            execution_id (str): unique execution ID of the query.

        Returns:
            Dict[str, str]: dictionary containing information on the deletion.

        """
        return self._retry_handling(
            lambda: self._sql_bkg_exec_api.cancel_query(execution_id).to_dict(),
            'delete query'
        )

    def get_result(
            self,
            execution_id: str,
            page_size: Optional[int] = None,
            sort_by: Optional[str] = None,
            filter_str: Optional[str] = None,
            verbose: bool = False,
            **read_csv_params
    ):
        """Gets the result of a completed luminesce query and returns it as a pandas dataframe.

            Args:
                execution_id (str): execution ID of the query.
                page_size (Optional[int]): [DEPRECATED] page size when getting the result via pagination. Default = None.
                sort_by (Optional[str]): string representing a sort to apply to the result before downloading it.
                filter_str (Optional[str]): optional string representing a filter to apply to the result before downloading it.
                verbose (Optional[bool]): whether to print out information while getting the data.
                **read_csv_params (Any): keyword arguments to pass down to pandas read_csv. See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

            Returns:
                DataFrame: result of the query as a pandas dataframe.

            """
        if page_size is not None:
            warnings.warn(
                "page_size is deprecated: this method now gets the results via a file stream. "
                "The page_size parameter will be removed in future.",
                DeprecationWarning,
                stacklevel=2
            )

        status = self.get_status(execution_id)
        n_tries, row_count = 0, int(status['row_count'])

        max_tries = self.max_retries * 10
        while row_count == -1 and n_tries < max_tries:

            status = self.get_status(execution_id)
            row_count = int(status['row_count'])
            if row_count != -1:
                break

            n_tries += 1
            time.sleep(0.1)

        if row_count == -1:
            raise LumiError(execution_id, status)

        fetch_params = {'execution_id': execution_id, 'download': True}
        if sort_by is not None:
            fetch_params['sort_by'] = sort_by
        if filter_str is not None:
            fetch_params['filter'] = filter_str

        if verbose and row_count != -1:
            print(f'Downloading {row_count} row{"" if row_count == 1 else "s"} of data... 📡')

        s = time.time()
        csv = self._retry_handling(
            lambda: self._sql_bkg_exec_api.fetch_query_result_csv(**fetch_params),
            'get result'
        )
        df = table_spec_to_df(status['columns_available'], csv, **read_csv_params)

        if verbose:
            print(f'Done! ({time.time() - s:3.2f}s)')

        return df

    def start_history_query(self):
        """Start a query that get data on queries that have run historically

        Returns:
            str: execution ID of the history query
        """
        res = self._retry_handling(
            lambda: self._history_api.get_history(),
            'start history query'
        )
        return res.execution_id

    def get_history_status(self, execution_id: str):
        """Get the status of a history query

        Args:
            execution_id (str): execution ID to check status for

        Returns:
            Dict[str,str]: dictionary containing the information from the status response json
        """
        return self._retry_handling(
            lambda: self._history_api.get_progress_ot_history(execution_id),
            'get history query status'
        )

    def get_history_result(self, execution_id: str):
        """Get result of history query

        Args:
            execution_id: execution ID to get the result for

        Returns:
            DataFrame: pandas dataframe containing the history query result.
        """
        res = self._retry_handling(
            lambda: self._history_api.fetch_history_result_json(execution_id),
            'get history query result'
        )
        return pd.DataFrame(json.loads(res))

    def delete_view(self, name: str):
        """Deletes a Luminesce view provider with the given name.

        Args:
            name (str): name of the view provider to delete.

        """
        self.query_and_fetch(f"""
            @x = use Sys.Admin.SetupView
                --provider={name}
                --deleteProvider
                --------------
                select 1;
                enduse;
            select * from @x;
            """)

    def run(
            self,
            sql: str,
            page_size: Optional[int] = None,
            timeout: Optional[int] = 3600,
            keep_for: Optional[int] = 7200,
            quiet: Optional[bool] = False,
            return_job: Optional[bool] = False,
            _print_fn: Optional[Callable] = None,
            **read_csv_params
    ) -> pd.DataFrame:
        """Run a sql string in Luminesce. This method can either run synchonously which will print query progress to the
         screen and then return the result or return a QueryJob instance that allows you to manage the query job yourself.

        Args:
            sql (str): the sql to run.
            page_size (Optional[int]): [DEPRECATED] page size when getting the result via pagination. Default = None.
            timeout (Optional[int]): max time for the query to run in seconds (defaults to 3600)
            keep_for (Optional[int]): time to keep the query result for in seconds (defaults to 7200)
            quiet (Optional[bool]): whether to print query progress or not
            return_job (Optional[bool]): whether to return a QueryJob instance or to wait until completion and return
            the result as a pandas dataframe
            _print_fn (Optional[Callable]): alternative print function for showing progress. This is mainly for internal use with
            the streamlit utility functions that show query progress in a cell. Defaults to the normal python print() fn.
            **read_csv_params (Any): keyword arguments to pass down to pandas read_csv. See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        Returns:
            Union[DataFrame, QueryJob]: either a dataframe containing the query result or a query job object that
            represents the running query.

        """
        ex_id = self.start_query(sql, timeout=timeout, keep_for=keep_for)
        job = QueryJob(ex_id, client=self, _print_fn=_print_fn)
        if return_job:
            return job

        job.interactive_monitor(quiet=quiet)
        result = job.get_result(page_size, quiet=quiet, **read_csv_params)
        if find_spec('IPython') is not None and not quiet:
            clear_output(wait=True)

        return result

    def download_binary(self, name: str, version: str):
        """Download a specified Luminesce binary.

        Args:
            name (str): the name of the binary to download (e.g. Python_Providers).
            version (str): the semantic version number to download.

        """

        res = self._retry_handling(
            lambda: self._binary_download.download_binary(type=name, version=version, _preload_content=False),
            'download Python Provider binaries'
        )

        if int(res.status) != 200:
            raise ValueError(f'Error when downloading Python Provider binaries. Status code: {res.status}.')

        total = int(res.headers['content-length'])

        folder = Path.home() / '.lumipy' / name.lower() / version.replace('.', '_')
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)

        zip_path = folder / f'{name}.zip'

        pbar = tqdm(desc=f'  Downloading {name.replace("_", " ")} ({version})', total=total, unit='B', unit_scale=True, ncols=96)
        chunk_size = 1024 * 8

        with open(zip_path, 'wb') as f:
            for data in res.stream(chunk_size):
                f.write(data)
                pbar.update(len(data))

        pbar.close()

        with ZipFile(zip_path, 'r') as zf:
            zf.extractall(folder)

        os.remove(zip_path)

    def download_certs(self, cert_type: Optional[Literal['Domain', 'User']] = 'Domain'):
        """Download the pem files for running providers. This method will download them and move them to the
        expected directory ~/.lumipy/certs/{domain}/

        Args:
            cert_type (Optional[Literal['Domain', 'User']]): the cert type to download pems for. Defaults to 'Domain'
            the certificate for the client domain. For user-level certs specify 'User'.

        """
        print(f'  Downloading {cert_type} Certificates')
        certs_path = Path.home() / '.lumipy' / 'certs' / self.get_domain()
        if certs_path.exists():
            shutil.rmtree(certs_path)

        certs_path.mkdir(parents=True)

        for file_type in ['Private', 'Public']:
            pem = Path(self._certs_management.download_certificate(type=cert_type, file_type=file_type, may_auto_create=True))
            new_pem_path = certs_path / pem.name.strip(';')
            shutil.copy2(pem, new_pem_path)
            os.remove(pem)


def get_client(domain: Optional[str] = None, **kwargs) -> Client:
    """Build a lumipy client by passing any of the following: a token, api_url and app_name; a path to a secrets file
       via api_secrets_filename; or by passing in proxy information. If none of these are provided then lumipy will try
       to find the credentials information as environment variables.

       Args:
           domain (Optional[str]): specify a domain that's in lumipy.config

       Keyword Args:
           token (str): Bearer token used to initialise the API
           api_secrets_filename (str): Name of secrets file (including full path)
           api_url (str): luminesce API url
           app_name (str): Application name (optional)
           certificate_filename (str): Name of the certificate file (.pem, .cer or .crt)
           proxy_url (str): The url of the proxy to use including the port e.g. http://myproxy.com:8888
           proxy_username (str): The username for the proxy to use
           proxy_password (str): The password for the proxy to use
           correlation_id (str): Correlation id for all calls made from the returned finbournesdkclient API instances

    Returns:
        Client: the lumipy client.

    """
    if domain is not None and len(kwargs) > 0:
        raise ValueError(
            f"You can't specify kwargs and a lumipy.config domain at the same time. Please choose one or the other."
        )

    if len(kwargs) == 0:
        return Client(**config.creds(domain))

    return Client(**kwargs)


class LumiError(Exception):

    def __init__(self, ex_id, metadata):
        self.metadata = metadata

        self.ex_id = ex_id
        self.status = metadata['status']

        p = metadata['progress']

        front_substr1 = 'Query Execution failed.'
        front_substr2 = 'has the following error(s):'

        if front_substr1 in p:
            start = p.find(front_substr1) + len(front_substr1)
            end = p.find('Sql:')
        elif front_substr2 in p:
            start = p.find(front_substr2) + len(front_substr2)
            end = -1
        else:
            start, end = 0, -1

        self.details = p[start:end].strip()

        lines = '\n'.join([
            f'ex id: {self.ex_id}',
            f'status: {self.status}',
            f'details:',
            indent_str(self.details)
        ])
        msg = f'Query results are unavailable.\nInfo:\n{indent_str(lines)}'

        super().__init__(msg)
