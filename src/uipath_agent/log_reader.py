import pandas as pd

from uipath_agent.models.error import UiPathError


def read_error_logs(file_path: str) -> list[UiPathError]:

    df = pd.read_excel(
        file_path,
        sheet_name="Error_Logs"
    )

    errors = []

    for _, row in df.iterrows():

        error = UiPathError(
            log_id=int(row["Log_ID"]),
            timestamp=str(row["Timestamp"]),
            job_key=str(row["Job_Key"]),
            process_name=str(row["Process_Name"]),
            workflow=str(row["Workflow"]),
            robot=str(row["Robot"]),
            environment=str(row["Environment"]),
            status=str(row["Status"]),
            error_code=str(row["Error_Code"]),
            error_category=str(row["Error_Category"]),
            severity=str(row["Severity"]),
            error_message=str(row["Error_Message"]),
            retry_count=int(row["Retry_Count"]),
            queue_item=(
                str(row["Queue_Item"])
                if pd.notna(row["Queue_Item"])
                else None
            ),
        )

        errors.append(error)

    return errors