import pandas as pd

def apply_filters(data_df, config):
    # create a mask to filter the data
    mask = pd.Series(True, index=data_df.index)  # Start with all True values

    # if config is not a list, return the original dataframe
    if not isinstance(config, list):
        return data_df

    for filter_item in config:
        filter_type = filter_item.get('type', None)
        column = filter_item.get('column', None)

        # skip if essential information is missing
        if column is None or filter_type is None:
            continue
        if column not in data_df.columns:
            continue

        # cast the column to the specified type
        if filter_type == 'int':
            data_df[column] = pd.to_numeric(data_df[column], errors='coerce').astype('Int64')
        elif filter_type == 'float':
            data_df[column] = pd.to_numeric(data_df[column], errors='coerce')
        elif filter_type == 'bool':
            data_df[column] = data_df[column].astype(bool)
        elif filter_type == 'str':
            data_df[column] = data_df[column].astype(str)
        elif filter_type == 'date':
            data_df[column] = pd.to_datetime(data_df[column], errors='coerce')
        else:
            continue  # unknown type, skip this filter

        # retrieve filter parameters
        min_ = filter_item.get('min', None)
        max_ = filter_item.get('max', None)
        take_only = filter_item.get('take_only', None)
        include = filter_item.get('include', None)
        exclude = filter_item.get('exclude', None)

        # apply min and max for numeric types and dates
        if filter_type in ['int', 'float', 'date']:
            if min_ is not None:
                if filter_type == 'date':
                    min_ = pd.to_datetime(min_)
                mask &= data_df[column] >= min_
            if max_ is not None:
                if filter_type == 'date':
                    max_ = pd.to_datetime(max_)
                mask &= data_df[column] <= max_

        # apply take_only for boolean type
        if filter_type == 'bool' and take_only is not None:
            mask &= data_df[column] == take_only

        # apply include and exclude for any type
        if include is not None:
            mask &= data_df[column].isin(include)
        if exclude is not None:
            mask &= ~data_df[column].isin(exclude)

    # return the filtered dataframe
    return data_df[mask]
