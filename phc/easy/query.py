from phc import Session
from phc.services import Accounts, Projects, Fhir
from phc.easy.auth import Auth
from typing import List


def query_allows_scrolling(query):
    limit = iter(query.get("limit", []))

    lower = next(limit, {}).get("value")
    upper = next(limit, {}).get("value")

    return type(lower) == int and type(upper) == int


class Query:
    @staticmethod
    def execute_dsl(
        query: dict,
        scroll: bool = False,
        auth_args: Auth = Auth.shared(),
        _scroll_id: str = "true",
        _prev_hits: List = [],
    ):
        """Execute a FHIR query with the DSL

        See https://docs.us.lifeomic.com/development/fhir-service/dsl/

        Attributes
        ----------
        query : dict
            The FHIR query to run (is a superset of elasticsearch)

        scroll : bool
            Scroll through mutliple pages of data; (Limit is required and defines
            the size of the sliding window.)

        auth : Auth
            The authenication to use for the account and project (defaults to shared)

        NOTE: All other attributes are private and should not be supplied

        Examples
        --------
        >>> import phc.easy as phc
        >>> phc.Auth.set({ 'account': '<your-account-name>' })
        >>> phc.Project.set_current('My Project Name')
        >>> phc.Query.execute_dsl({
          "type": "select",
          "columns": "*",
          "from": [
              {
                  "table": "observation"
              }
          ],
          "limit": [
              {
                  "type": "number",
                  "value": 0
              },
              {
                  "type": "number",
                  "value": 1000
              }
          ]
        }, scroll=True)
        """
        auth = Auth(auth_args)
        fhir = Fhir(auth.session())

        response = fhir.execute_es(
            auth.project_id,
            query,
            _scroll_id if query_allows_scrolling(query) and scroll else "",
        )

        current_results = response.data.get("hits").get("hits")
        results = [*_prev_hits, *current_results]
        _scroll_id = response.data.get("_scroll_id", "")

        if len(current_results) == 0 or scroll is False:
            return results

        # TODO: Revisit private parameters being exposed in public method
        return Query.execute_dsl(
            query,
            scroll=True,
            auth_args=auth,
            _scroll_id=_scroll_id,
            _prev_hits=results,
        )
