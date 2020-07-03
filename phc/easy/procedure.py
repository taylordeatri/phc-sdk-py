from typing import Union
import pandas as pd
from phc.easy.patient_item import PatientItem
from phc.easy.frame import Frame
from phc.easy.auth import Auth


class Procedure:
    @staticmethod
    def transform_results(data_frame: pd.DataFrame, **expand_args):
        args = {
            **expand_args,
            "custom_columns": [
                *expand_args.get("custom_columns", []),
                Frame.codeable_like_column_expander("subject"),
                Frame.codeable_like_column_expander("performedPeriod"),
            ],
        }

        return Frame.expand(data_frame, **args)

    @staticmethod
    def get_data_frame(
        all_results: bool = False,
        raw: bool = False,
        patient_id: Union[None, str] = None,
        query_overrides: dict = {},
        auth_args=Auth.shared(),
        expand_args: dict = {},
    ):
        """Retrieve procedures

        Attributes
        ----------
        all_results : bool = False
            Retrieve sample of results (10) or entire set of procedures

        raw : bool = False
            If raw, then values will not be expanded (useful for manual
            inspection if something goes wrong)

        patient_id : None or str = None
            Find procedures for a given patient_id

        auth_args : Any
            The authenication to use for the account and project (defaults to shared)

        expand_args : Any
            Additional arguments passed to phc.Frame.expand

        Examples
        --------
        >>> import phc.easy as phc
        >>> phc.Auth.set({'account': '<your-account-name>'})
        >>> phc.Project.set_current('My Project Name')
        >>> phc.Procedure.get_data_frame(patient_id='<patient-id>')
        """
        data_frame = PatientItem.retrieve_raw_data_frame(
            "procedure", all_results, patient_id, query_overrides, auth_args
        )

        if raw:
            return data_frame

        return Procedure.transform_results(data_frame, **expand_args)
