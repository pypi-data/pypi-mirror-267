
def error_handling(data):
    from openai import AzureOpenAI
    import pandas as pd
    import numpy as np

    # Define ANSI escape codes for different colors
    class Color:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    # data = pd.read_csv("output_test9.csv")

    completeness_scores = (1 - data.isnull().mean()) * 100
    cell_quality_scores = (100 - completeness_scores) / 100
    column_quality_scores = []

    for col in data.columns:
        weighted_sum = (cell_quality_scores * (1 - data[col].isnull().astype(int))).sum()
        sum_completeness = (1 - data[col].isnull().astype(int)).sum()
        col_quality_score = weighted_sum / sum_completeness
        column_quality_scores.append(col_quality_score)

    column_quality_scores = pd.Series(column_quality_scores, index=data.columns)
    row_confidences = 1 - data.isnull().sum(axis=1) / data.shape[1]
    row_quality_scores = row_confidences
    dataset_quality_score = np.mean(cell_quality_scores)

    print(Color.HEADER + "Completeness Scores:" + Color.ENDC)
    print(completeness_scores)
    print(Color.BLUE + "\nCell Quality Scores:" + Color.ENDC)
    print(cell_quality_scores)
    print(Color.GREEN + "\nColumn Quality Scores:" + Color.ENDC)
    print(column_quality_scores)
    print(Color.WARNING + "\nDataset error Score:" + Color.ENDC, dataset_quality_score)

    # time_columns = [col for col in data.columns if "date" in col.lower() or "time" in col.lower()]

    # for col in time_columns:
    #     data[col] = pd.to_datetime(data[col], errors='coerce')

    # time_variations = {}
    # for col in time_columns:
    #     if data[col].dtype == 'datetime64[ns]':
    #         time_variations[col] = data[col].diff().fillna(pd.Timedelta(seconds=0))

    # for col, time_variation in time_variations.items():
    #     print(Color.HEADER + "Time variations for column:" + Color.ENDC, col)
    #     print(time_variation)
    #     print("\n")

    # reference_point = pd.Timestamp.now()

    # time_differences = {}

    # for col in data.columns:
    #     if 'date' in col.lower() or 'time' in col.lower():  
    #         data[col] = pd.to_datetime(data[col], errors='coerce')
            
    #         latest_entry = data[col].max()
    #         if pd.notnull(latest_entry): 
    #             time_difference = (reference_point - latest_entry).days 
    #             time_differences[col] = time_difference

    # # Normalize time differences to a common scale (e.g., days)
    # max_time_difference = max(time_differences.values())
    # min_time_difference = min(time_differences.values())
    # if max_time_difference != min_time_difference:  
    #     normalized_time_differences = {col: (max_time_difference - time_diff) / (max_time_difference - min_time_difference)
    #                                     for col, time_diff in time_differences.items()}
    # else:
    #     normalized_time_differences = {col: 1.0 for col in time_differences}

    # timeliness_score = sum(normalized_time_differences.values()) / len(normalized_time_differences)

    # print(Color.BLUE + "Timeliness Score:" + Color.ENDC, timeliness_score)

    # Remaining code remains the same


    # def calculate_data_dirtiness_score(data):

    #     completeness_score = data.isnull().mean() * 100    
    #     accuracy_score = pd.Series(0, index=data.columns)   
    #     consistency_score = pd.Series(0, index=data.columns)    
    #     timeliness_score = pd.Series(0, index=data.columns)   
    #     validity_score = pd.Series(0, index=data.columns)
    #     total_score = completeness_score + accuracy_score + consistency_score + timeliness_score + validity_score    
    #     data_dirtiness_score = total_score.mean()
        
    #     return data_dirtiness_score

    # completeness_score = calculate_data_dirtiness_score(data)
    # accuracy_score = calculate_data_dirtiness_score(data)
    # consistency_score = calculate_data_dirtiness_score(data)
    # timeliness_score = calculate_data_dirtiness_score(data)
    # validity_score = calculate_data_dirtiness_score(data)
    # total_score = calculate_data_dirtiness_score(data)

    def find_missing_value_positions(data):

        missing_value_positions = data.isnull()
        rows_with_missing_values = missing_value_positions.any(axis=0)
        cols_with_missing_values = missing_value_positions.any(axis=1)  # Fix: Changed axis=0 to axis=1
        rows = rows_with_missing_values.index[rows_with_missing_values].tolist()
        cols = cols_with_missing_values.index[cols_with_missing_values].tolist()

        return rows, cols

    missing_rows, missing_cols = find_missing_value_positions(data)

    def coerce_to_correct_dtype(data):

        for col in data.columns:
            col_data = data[col]
            numeric_count = pd.to_numeric(col_data, errors='coerce').notna().sum()
            total_count = col_data.count()
            if numeric_count > total_count / 2:
                try:
                    data[col] = pd.to_numeric(col_data, errors='coerce')
                except ValueError:
                    pass

    def data_quality_check(data):
        coerce_to_correct_dtype(data)
        missing_values = data.isnull().sum()
        nan_values = data.isna().sum()
        none_values = data.isin([None]).sum()
        zero_missing_values = ((data == 0) | (data == 0.0) | (data.isnull()) | (data == None) | (data == np.nan)).sum()
        total_missing_values = missing_values + zero_missing_values - nan_values - none_values
        data.replace('', np.nan, inplace=True)
        empty_columns = data.columns[data.isnull().all()]
        empty_rows = data[data.isnull().all(axis=1)]
        empty_rows = pd.concat([empty_rows, data[data.eq('').all(axis=1)]])
        empty_rows.drop_duplicates(inplace=True)
        duplicate_rows = data.duplicated().sum()
        data_types = data.dtypes
        missing_value_positions = [(row + 2, col + 1) for row, col in zip(*np.where(data.isnull()))]

        results = {}
        results["Missing_Values"] = total_missing_values
        results["Empty_Columns"] = empty_columns
        results["Empty_Rows"] = empty_rows
        results["Duplicate_Rows"] = duplicate_rows
        results["Data_Types"] = data_types
        results["Missing_Value_Positions"] = missing_value_positions

        columns_with_missing_values = {}
        for column, count in total_missing_values.items():
            if count > 0:
                columns_with_missing_values[column] = count
        results["Columns_with_missing_values"] = columns_with_missing_values
        return results

    results = data_quality_check(data)

    missing_values = results["Missing_Values"]
    empty_columns = results["Empty_Columns"]
    empty_rows = results["Empty_Rows"]
    duplicate_rows = results["Duplicate_Rows"]
    data_types = results["Data_Types"]
    missing_value_positions = results["Missing_Value_Positions"]
    columns_with_missing_values = results["Columns_with_missing_values"]

    print(Color.HEADER + "Data Quality Check Results:" + Color.ENDC)
    for check, result in results.items():
        print(Color.GREEN + f"{check}:" + Color.ENDC)
        print(result)
        print("\n")


    # dirtiness_score = calculate_data_dirtiness_score(data)
    # print("Data Dirtiness Score:", dirtiness_score)

    azure_client = AzureOpenAI(
        api_version="2023-07-01-preview",
        azure_endpoint="https://covalenseopenaieastus2.openai.azure.com/",
        api_key="17b15c9c0c3643368bb8e9e2c5ada06f",
    )

    messages = [
        {
            "role": "system",
            "content": f"Analyse the provided financial dataset to identify and document data quality issues."
                        f"Below are common data quality issues to guide your analysis. However, you may also identify other relevant issues:"
                        "- Ingestion errors"
                        "- Typecasting issues"
                        "- Duplicates"
                        "- Date parsing issues"
                        "- Character encoding problems"
                        "- Missing values"
                        "- Typos/spelling mistakes"
                        "- Anomalies/outliers"
                        "- Conversion errors and inconsistent units"
                        "- Privacy concerns (e.g., exposed PII)"
                        "- Domain-specific errors (e.g., invalid formats for addresses, phone numbers, emails)"
                        "- Inconsistent formatting"
                        "- Data integrity"
                        "- Data cell quality scores: {cell_quality_scores}"
                        "- Data completeness score: {completeness_score}"
                        "- Data timeliness score: {timeliness_score}"
                        "- Data column quality scores: {column_quality_scores}"
                        "- Data Time variations for column: {time_variation}"
                        "- Data security"
                        "- Data governance"
                        "- Preventive measures"
                        "Instructions:"
                        "1. Examine silently the table and its metadata."
                        "2. Line by line, identify potential data quality issues without coding."
                        "3. Document each issue, including:"
                        "- Nature and description of the issue"
                        "- Expected correct state"
                        "- Violated constraint"
                        "- Confidence level in your assessment using ordinal categories: `low`, `medium`, `high`, and `certain`."
                        "- Specific location of the issue in the table (use 'None' for table-wide issues): Index and Column names."
                        f"Provided complete Dataset data: {data}"
                        f"provided Data dirtiness score percentage of the data: {dataset_quality_score}"
                        f"provided Data results having the missing value positions of the data: {missing_values}"
                        f"provided Data results having the data types of the data: {data_types}"
                        f"provided Data results having the columns with missing values of the data: {columns_with_missing_values}"
                        f"provided Data results having the empty columns of the data: {empty_columns}"
                        f"provided Data results having the empty rows of the data: {empty_rows}"
                        f"provided Data results having the duplicate rows of the data: {duplicate_rows}"

        },
    ]
    
    response = azure_client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages,
        max_tokens=1000
    )

    final_output = response.choices[0].message.content 
    print(final_output)
    return dataset_quality_score