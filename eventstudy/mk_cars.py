{"payload":{"allShortcutsEnabled":true,"fileTree":{"event_study":{"items":[{"name":"__init__.py","path":"event_study/__init__.py","contentType":"file"},{"name":"_scratch.py","path":"event_study/_scratch.py","contentType":"file"},{"name":"config.py","path":"event_study/config.py","contentType":"file"},{"name":"download.py","path":"event_study/download.py","contentType":"file"},{"name":"main.py","path":"event_study/main.py","contentType":"file"},{"name":"mk_cars.py","path":"event_study/mk_cars.py","contentType":"file"},{"name":"mk_events.py","path":"event_study/mk_events.py","contentType":"file"},{"name":"mk_rets.py","path":"event_study/mk_rets.py","contentType":"file"},{"name":"test_hypo.py","path":"event_study/test_hypo.py","contentType":"file"}],"totalCount":9},"":{"items":[{"name":"event_study","path":"event_study","contentType":"directory"},{"name":"lectures","path":"lectures","contentType":"directory"},{"name":"webinars","path":"webinars","contentType":"directory"},{"name":"main.py","path":"main.py","contentType":"file"},{"name":"toolkit_config.py","path":"toolkit_config.py","contentType":"file"}],"totalCount":5}},"fileTreeProcessingTime":3.1127160000000003,"foldersToFetch":[],"reducedMotionEnabled":"system","repo":{"id":715396917,"defaultBranch":"master","name":"z5416840_lectures","ownerLogin":"lilyyyg","currentUserCanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2023-11-07T14:51:57.000+11:00","ownerAvatar":"https://avatars.githubusercontent.com/u/150103061?v=4","public":true,"private":false,"isOrgOwned":false},"symbolsExpanded":false,"treeExpanded":true,"refInfo":{"name":"master","listCacheKey":"v0:1699329193.0","canEdit":true,"refType":"branch","currentOid":"ed5f9bfb60a8b1fcffcbd5a2550662caf44e8abf"},"path":"event_study/mk_cars.py","currentUser":{"id":150109314,"login":"bran247","userEmail":"brandon7gunawan@gmail.com"},"blob":{"rawLines":["\"\"\" mk_cars.py","","Utilities to create CARs for the events in our study","\"\"\"","import numpy as np","import pandas as pd","","import event_study.config as cfg","","","def mk_cars_df(ret_df, event_df):","    \"\"\" Given a data frame with all events of interest for a given ticker","    (`event_df`) and the corresponding data frame with stock and market","    returns (`ret_df`), calculate the Cumulative Abnormal Return over the","    two-day window surrounding each event.","","    Parameters","    ----------","    ret_df : pandas dataframe","        Dataframe created by the function `mk_rets.mk_ret_df`. It contains the","        following columns:","            ret : float","                Daily stock return","            mkt : float","                Daily market return","        The index is a DatetimeIndex corresponding to each trading day","","    event_df : pandas dataframe","        Dataframe created by the function `mk_events.mk_event_df`. This data","        frame includes all events in our study (uniquely identified by an","        index starting at 1). The columns are:","            firm : str","                The name of the firm issuing the recommendation","            event_date : str","                A string representing the date part of the recommendation,","                formatted as 'YYYY-MM-DD'.","            event_type : str","                A string identifying the event as either an upgrade","                (\"upgrade\") or downgrade (\"downgrade\")","","    Returns","    -------","    Pandas dataframe","        A data frame with the same format as `event_df` but with an additional","        column containing the CARs:","            car : float","                The CAR for the two-day window surrounding the event","","    Notes","    -----","    This function will apply the `mk_cars.calc_car` function to each row of the `event_df`","","    \"\"\"","    cars = event_df.apply(calc_car, axis=1, ret_df=ret_df)","    event_df.loc[:, 'car'] = cars","    return event_df","","","def calc_car(ser, ret_df, window=2):","    \"\"\" For a given row in the dataframe produced by the `mk_event_df` function","    above, compute the cumulative abnormal returns for the event window","    surrounding the event_date by performing the following operations (in this","    order)","","    1. Expand the dates using the `expand_dates` function","    2. Join returns in `ret_df`","    3. Sum the abnormal returns to compute the CAR","","    Parameters","    ----------","    ser : series","       Series corresponding to a row from the dataframe produced by","        `mk_event_df`","","    ret_df : dataframe","        A dataframe with stock and market returns","","    Returns","    -------","    float","        Cumulative abnormal return for this row","","","    \"\"\"","    # --------------------------------------------------------","    #   Step 4.1: Expand dates and set 'ret_date' as the new index","    # --------------------------------------------------------","    dates = expand_dates(ser, window=window)","    dates.set_index('ret_date', inplace=True)","    # --------------------------------------------------------","    #   Step 4.2: Join stock and market returns returns","    # --------------------------------------------------------","    df = dates.join(ret_df, how='inner')","    # --------------------------------------------------------","    #   Step 4.3: Compute abnormal returns","    # --------------------------------------------------------","    df.loc[:, 'aret'] = df.loc[:, 'ret'] - df.loc[:, 'mkt']","    # --------------------------------------------------------","    #   Step 4.4: Sum abnormal returns","    # --------------------------------------------------------","    # If df is empty, return np.nan","    if len(df) == 0:","        return np.nan","    else:","        return df['aret'].sum()","","","def expand_dates(ser, window=2):","    \"\"\" For a given row in the dataframe produced by the `mk_event_df`","    function above, return a dataframe with the dates for the `window` days","    surrounding the event_date by performing the following operations (in this","    order)","","    1. Create a DF with one row for each day in the window ,","        where each row represents a copy of the series in `row`","    2. Create a column called \"event_date\", which the datetime representation","        of the dates in 'event_date'","    3. Create a column called \"event_time\" with values from -`window` to `window`","    4. Create another column called \"ret_date\" with the **datetime**","      representation of the relevant calendar date. The calendar date will be","      the date in \"event_date\" plus the value from \"event_time\".","","    Parameters","    ----------","    ser : series","       Series corresponding to a row from the dataframe produced by","        `mk_event_df`","","    Returns","    -------","    df","        A Pandas dataframe with the following structure:","","        - df.index : Integers representing the ID of this event, that is,","            uniquely identifying a unique combination of values (<event_date>,","            <firm>). The index should start at 1.","","        - df.columns : See Notes section below","","    Notes","    -----","","    For instance, suppose window = 2 and consider the following row (an event):","","","     | event_id | firm       | event_date  |","     |----------+------------+------------|","     | 1        | Wunderlich | 2012-02-16 |","","","     This function would produce the following data:","","","     | firm       | event_date | event_time | ret_date   |","     |------------+------------+------------+------------|","     | Wunderlich | 2012-02-16 | -2         | 2012-02-14 |","     | Wunderlich | 2012-02-16 | -1         | 2012-02-15 |","     | Wunderlich | 2012-02-16 | 0          | 2012-02-16 |","     | Wunderlich | 2012-02-16 | 1          | 2012-02-17 |","     | Wunderlich | 2012-02-16 | 2          | 2012-02-18 |","","     which should be stored in a dataframe with the following characteristics:","","     ----------------------------------------------","     Data columns (total 4 columns):","      #   Column      Non-Null Count  Dtype","     ---  ------      --------------  -----","      0   firm        5 non-null      object","      1   event_date  5 non-null      datetime64[ns]","      2   event_time  5 non-null      int64","      3   ret_date    5 non-null      datetime64[ns]","     ----------------------------------------------","","","    \"\"\"","    # Create a list of series","    row_lst = [ser] * (2 * window + 1)","","    # Create a new dataframe with copies of the single-row dataframe","    df = pd.concat(row_lst, axis=1).transpose()","","    # Create the event date col","    df['event_date'] = pd.to_datetime(df.loc[:, 'event_date'])","    # Create the event time","    df.loc[:, 'event_time'] = [i for i in range(-window, window + 1)]","","    # Create the return date","    df.loc[:, 'ret_date'] = df.event_date + pd.to_timedelta(df.event_time, unit='day')","","    # keep only relevant columns","    cols = ['firm', 'event_date', 'event_time', 'ret_date']","    df = df.loc[:, cols]","","    # rename the index","    df.index.name = 'event_id'","    return df","","","def _test_mk_cars_df(sample_only=False):","    \"\"\"  Will test the function mk_cars_df","    Parameters","    ----------","    sample_only : bool, optional","        If True, will use a single event from the `event_df`","","    Notes","    -----","    if `sample_only` is True, the event df will become:","","        | event_id | event_date | event_type | car       |","        |----------|------------|------------|-----------|","        | 1        | 2020-09-23 | upgrade    | $CAR_{1}$ |","","","    \"\"\"","    from event_study import mk_rets, mk_events","","    def _mk_example_event_df(event_df):","        \"\"\" Creates an event df to be used if sample_only is True","        \"\"\"","        cond = (event_df.event_date == '2020-09-23') & (event_df.firm == 'DEUTSCHE BANK')","        # The slice is so it returns a DF (not a series)","        event_df = event_df.loc[cond]","        event_df.index = [1]","        event_df.index.name = 'event_id'","        return event_df","","    # Create the `ret_df` and the `event_df` data frames","    tic = 'TSLA'","    ret_df = mk_rets.mk_ret_df(tic)","    event_df = mk_events.mk_event_df(tic)","","    # Sample only?","    if sample_only is True:","        event_df = _mk_example_event_df(event_df)","        ret_df = ret_df.loc['2020-09-21':'2020-09-25']","","    print('-----------------------------')","    print(' event_df:')","    print('-----------------------------')","    print(event_df)","    print('')","","    print('-----------------------------')","    print(' ret_df:')","    print('-----------------------------')","    print(ret_df)","    print('')","","    # Create the CAR df","    cars_df = mk_cars_df(ret_df=ret_df, event_df=event_df)","","    print('-----------------------------')","    print(' cars_df:')","    print('-----------------------------')","    print(cars_df)","","","if __name__ == \"__main__\":","    sample_only = True","    _test_mk_cars_df(sample_only)"],"stylingDirectives":[[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":52,"cssClass":"pl-s"}],[{"start":0,"end":3,"cssClass":"pl-s"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":12,"cssClass":"pl-s1"},{"start":13,"end":15,"cssClass":"pl-k"},{"start":16,"end":18,"cssClass":"pl-s1"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":13,"cssClass":"pl-s1"},{"start":14,"end":16,"cssClass":"pl-k"},{"start":17,"end":19,"cssClass":"pl-s1"}],[],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":18,"cssClass":"pl-s1"},{"start":19,"end":25,"cssClass":"pl-s1"},{"start":26,"end":28,"cssClass":"pl-k"},{"start":29,"end":32,"cssClass":"pl-s1"}],[],[],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":14,"cssClass":"pl-en"},{"start":15,"end":21,"cssClass":"pl-s1"},{"start":23,"end":31,"cssClass":"pl-s1"}],[{"start":4,"end":73,"cssClass":"pl-s"}],[{"start":0,"end":71,"cssClass":"pl-s"}],[{"start":0,"end":73,"cssClass":"pl-s"}],[{"start":0,"end":42,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":29,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":26,"cssClass":"pl-s"}],[{"start":0,"end":23,"cssClass":"pl-s"}],[{"start":0,"end":34,"cssClass":"pl-s"}],[{"start":0,"end":23,"cssClass":"pl-s"}],[{"start":0,"end":35,"cssClass":"pl-s"}],[{"start":0,"end":70,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":31,"cssClass":"pl-s"}],[{"start":0,"end":76,"cssClass":"pl-s"}],[{"start":0,"end":73,"cssClass":"pl-s"}],[{"start":0,"end":46,"cssClass":"pl-s"}],[{"start":0,"end":22,"cssClass":"pl-s"}],[{"start":0,"end":63,"cssClass":"pl-s"}],[{"start":0,"end":28,"cssClass":"pl-s"}],[{"start":0,"end":74,"cssClass":"pl-s"}],[{"start":0,"end":42,"cssClass":"pl-s"}],[{"start":0,"end":28,"cssClass":"pl-s"}],[{"start":0,"end":67,"cssClass":"pl-s"}],[{"start":0,"end":54,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":20,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":35,"cssClass":"pl-s"}],[{"start":0,"end":23,"cssClass":"pl-s"}],[{"start":0,"end":68,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":90,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":7,"cssClass":"pl-s"}],[{"start":4,"end":8,"cssClass":"pl-s1"},{"start":9,"end":10,"cssClass":"pl-c1"},{"start":11,"end":19,"cssClass":"pl-s1"},{"start":20,"end":25,"cssClass":"pl-en"},{"start":26,"end":34,"cssClass":"pl-s1"},{"start":36,"end":40,"cssClass":"pl-s1"},{"start":40,"end":41,"cssClass":"pl-c1"},{"start":41,"end":42,"cssClass":"pl-c1"},{"start":44,"end":50,"cssClass":"pl-s1"},{"start":50,"end":51,"cssClass":"pl-c1"},{"start":51,"end":57,"cssClass":"pl-s1"}],[{"start":4,"end":12,"cssClass":"pl-s1"},{"start":13,"end":16,"cssClass":"pl-s1"},{"start":20,"end":25,"cssClass":"pl-s"},{"start":27,"end":28,"cssClass":"pl-c1"},{"start":29,"end":33,"cssClass":"pl-s1"}],[{"start":4,"end":10,"cssClass":"pl-k"},{"start":11,"end":19,"cssClass":"pl-s1"}],[],[],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":12,"cssClass":"pl-en"},{"start":13,"end":16,"cssClass":"pl-s1"},{"start":18,"end":24,"cssClass":"pl-s1"},{"start":26,"end":32,"cssClass":"pl-s1"},{"start":32,"end":33,"cssClass":"pl-c1"},{"start":33,"end":34,"cssClass":"pl-c1"}],[{"start":4,"end":79,"cssClass":"pl-s"}],[{"start":0,"end":71,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":10,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":57,"cssClass":"pl-s"}],[{"start":0,"end":31,"cssClass":"pl-s"}],[{"start":0,"end":50,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":16,"cssClass":"pl-s"}],[{"start":0,"end":67,"cssClass":"pl-s"}],[{"start":0,"end":21,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":22,"cssClass":"pl-s"}],[{"start":0,"end":49,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":47,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":7,"cssClass":"pl-s"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":66,"cssClass":"pl-c"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":9,"cssClass":"pl-s1"},{"start":10,"end":11,"cssClass":"pl-c1"},{"start":12,"end":24,"cssClass":"pl-en"},{"start":25,"end":28,"cssClass":"pl-s1"},{"start":30,"end":36,"cssClass":"pl-s1"},{"start":36,"end":37,"cssClass":"pl-c1"},{"start":37,"end":43,"cssClass":"pl-s1"}],[{"start":4,"end":9,"cssClass":"pl-s1"},{"start":10,"end":19,"cssClass":"pl-en"},{"start":20,"end":30,"cssClass":"pl-s"},{"start":32,"end":39,"cssClass":"pl-s1"},{"start":39,"end":40,"cssClass":"pl-c1"},{"start":40,"end":44,"cssClass":"pl-c1"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":55,"cssClass":"pl-c"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":8,"cssClass":"pl-c1"},{"start":9,"end":14,"cssClass":"pl-s1"},{"start":15,"end":19,"cssClass":"pl-en"},{"start":20,"end":26,"cssClass":"pl-s1"},{"start":28,"end":31,"cssClass":"pl-s1"},{"start":31,"end":32,"cssClass":"pl-c1"},{"start":32,"end":39,"cssClass":"pl-s"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":42,"cssClass":"pl-c"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":10,"cssClass":"pl-s1"},{"start":14,"end":20,"cssClass":"pl-s"},{"start":22,"end":23,"cssClass":"pl-c1"},{"start":24,"end":26,"cssClass":"pl-s1"},{"start":27,"end":30,"cssClass":"pl-s1"},{"start":34,"end":39,"cssClass":"pl-s"},{"start":41,"end":42,"cssClass":"pl-c1"},{"start":43,"end":45,"cssClass":"pl-s1"},{"start":46,"end":49,"cssClass":"pl-s1"},{"start":53,"end":58,"cssClass":"pl-s"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":38,"cssClass":"pl-c"}],[{"start":4,"end":62,"cssClass":"pl-c"}],[{"start":4,"end":35,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-k"},{"start":7,"end":10,"cssClass":"pl-en"},{"start":11,"end":13,"cssClass":"pl-s1"},{"start":15,"end":17,"cssClass":"pl-c1"},{"start":18,"end":19,"cssClass":"pl-c1"}],[{"start":8,"end":14,"cssClass":"pl-k"},{"start":15,"end":17,"cssClass":"pl-s1"},{"start":18,"end":21,"cssClass":"pl-s1"}],[{"start":4,"end":8,"cssClass":"pl-k"}],[{"start":8,"end":14,"cssClass":"pl-k"},{"start":15,"end":17,"cssClass":"pl-s1"},{"start":18,"end":24,"cssClass":"pl-s"},{"start":26,"end":29,"cssClass":"pl-en"}],[],[],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":16,"cssClass":"pl-en"},{"start":17,"end":20,"cssClass":"pl-s1"},{"start":22,"end":28,"cssClass":"pl-s1"},{"start":28,"end":29,"cssClass":"pl-c1"},{"start":29,"end":30,"cssClass":"pl-c1"}],[{"start":4,"end":70,"cssClass":"pl-s"}],[{"start":0,"end":75,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":10,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":60,"cssClass":"pl-s"}],[{"start":0,"end":63,"cssClass":"pl-s"}],[{"start":0,"end":77,"cssClass":"pl-s"}],[{"start":0,"end":36,"cssClass":"pl-s"}],[{"start":0,"end":81,"cssClass":"pl-s"}],[{"start":0,"end":68,"cssClass":"pl-s"}],[{"start":0,"end":77,"cssClass":"pl-s"}],[{"start":0,"end":64,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":16,"cssClass":"pl-s"}],[{"start":0,"end":67,"cssClass":"pl-s"}],[{"start":0,"end":21,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":0,"end":6,"cssClass":"pl-s"}],[{"start":0,"end":56,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":73,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":49,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":46,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":79,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":44,"cssClass":"pl-s"}],[{"start":0,"end":43,"cssClass":"pl-s"}],[{"start":0,"end":43,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":52,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":78,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":51,"cssClass":"pl-s"}],[{"start":0,"end":36,"cssClass":"pl-s"}],[{"start":0,"end":43,"cssClass":"pl-s"}],[{"start":0,"end":43,"cssClass":"pl-s"}],[{"start":0,"end":44,"cssClass":"pl-s"}],[{"start":0,"end":52,"cssClass":"pl-s"}],[{"start":0,"end":43,"cssClass":"pl-s"}],[{"start":0,"end":52,"cssClass":"pl-s"}],[{"start":0,"end":51,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":7,"cssClass":"pl-s"}],[{"start":4,"end":29,"cssClass":"pl-c"}],[{"start":4,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":15,"end":18,"cssClass":"pl-s1"},{"start":20,"end":21,"cssClass":"pl-c1"},{"start":23,"end":24,"cssClass":"pl-c1"},{"start":25,"end":26,"cssClass":"pl-c1"},{"start":27,"end":33,"cssClass":"pl-s1"},{"start":34,"end":35,"cssClass":"pl-c1"},{"start":36,"end":37,"cssClass":"pl-c1"}],[],[{"start":4,"end":68,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":8,"cssClass":"pl-c1"},{"start":9,"end":11,"cssClass":"pl-s1"},{"start":12,"end":18,"cssClass":"pl-en"},{"start":19,"end":26,"cssClass":"pl-s1"},{"start":28,"end":32,"cssClass":"pl-s1"},{"start":32,"end":33,"cssClass":"pl-c1"},{"start":33,"end":34,"cssClass":"pl-c1"},{"start":36,"end":45,"cssClass":"pl-en"}],[],[{"start":4,"end":31,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":19,"cssClass":"pl-s"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":23,"end":25,"cssClass":"pl-s1"},{"start":26,"end":37,"cssClass":"pl-en"},{"start":38,"end":40,"cssClass":"pl-s1"},{"start":41,"end":44,"cssClass":"pl-s1"},{"start":48,"end":60,"cssClass":"pl-s"}],[{"start":4,"end":27,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":10,"cssClass":"pl-s1"},{"start":14,"end":26,"cssClass":"pl-s"},{"start":28,"end":29,"cssClass":"pl-c1"},{"start":31,"end":32,"cssClass":"pl-s1"},{"start":33,"end":36,"cssClass":"pl-k"},{"start":37,"end":38,"cssClass":"pl-s1"},{"start":39,"end":41,"cssClass":"pl-c1"},{"start":42,"end":47,"cssClass":"pl-en"},{"start":48,"end":49,"cssClass":"pl-c1"},{"start":49,"end":55,"cssClass":"pl-s1"},{"start":57,"end":63,"cssClass":"pl-s1"},{"start":64,"end":65,"cssClass":"pl-c1"},{"start":66,"end":67,"cssClass":"pl-c1"}],[],[{"start":4,"end":28,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":10,"cssClass":"pl-s1"},{"start":14,"end":24,"cssClass":"pl-s"},{"start":26,"end":27,"cssClass":"pl-c1"},{"start":28,"end":30,"cssClass":"pl-s1"},{"start":31,"end":41,"cssClass":"pl-s1"},{"start":42,"end":43,"cssClass":"pl-c1"},{"start":44,"end":46,"cssClass":"pl-s1"},{"start":47,"end":59,"cssClass":"pl-en"},{"start":60,"end":62,"cssClass":"pl-s1"},{"start":63,"end":73,"cssClass":"pl-s1"},{"start":75,"end":79,"cssClass":"pl-s1"},{"start":79,"end":80,"cssClass":"pl-c1"},{"start":80,"end":85,"cssClass":"pl-s"}],[],[{"start":4,"end":32,"cssClass":"pl-c"}],[{"start":4,"end":8,"cssClass":"pl-s1"},{"start":9,"end":10,"cssClass":"pl-c1"},{"start":12,"end":18,"cssClass":"pl-s"},{"start":20,"end":32,"cssClass":"pl-s"},{"start":34,"end":46,"cssClass":"pl-s"},{"start":48,"end":58,"cssClass":"pl-s"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":8,"cssClass":"pl-c1"},{"start":9,"end":11,"cssClass":"pl-s1"},{"start":12,"end":15,"cssClass":"pl-s1"},{"start":19,"end":23,"cssClass":"pl-s1"}],[],[{"start":4,"end":22,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":12,"cssClass":"pl-s1"},{"start":13,"end":17,"cssClass":"pl-s1"},{"start":18,"end":19,"cssClass":"pl-c1"},{"start":20,"end":30,"cssClass":"pl-s"}],[{"start":4,"end":10,"cssClass":"pl-k"},{"start":11,"end":13,"cssClass":"pl-s1"}],[],[],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":20,"cssClass":"pl-en"},{"start":21,"end":32,"cssClass":"pl-s1"},{"start":32,"end":33,"cssClass":"pl-c1"},{"start":33,"end":38,"cssClass":"pl-c1"}],[{"start":4,"end":42,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":32,"cssClass":"pl-s"}],[{"start":0,"end":60,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":9,"cssClass":"pl-s"}],[{"start":0,"end":55,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":58,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":7,"cssClass":"pl-s"}],[{"start":4,"end":8,"cssClass":"pl-k"},{"start":9,"end":20,"cssClass":"pl-s1"},{"start":21,"end":27,"cssClass":"pl-k"},{"start":28,"end":35,"cssClass":"pl-s1"},{"start":37,"end":46,"cssClass":"pl-s1"}],[],[{"start":4,"end":7,"cssClass":"pl-k"},{"start":8,"end":28,"cssClass":"pl-en"},{"start":29,"end":37,"cssClass":"pl-s1"}],[{"start":8,"end":65,"cssClass":"pl-s"}],[{"start":0,"end":11,"cssClass":"pl-s"}],[{"start":8,"end":12,"cssClass":"pl-s1"},{"start":13,"end":14,"cssClass":"pl-c1"},{"start":16,"end":24,"cssClass":"pl-s1"},{"start":25,"end":35,"cssClass":"pl-s1"},{"start":36,"end":38,"cssClass":"pl-c1"},{"start":39,"end":51,"cssClass":"pl-s"},{"start":53,"end":54,"cssClass":"pl-c1"},{"start":56,"end":64,"cssClass":"pl-s1"},{"start":65,"end":69,"cssClass":"pl-s1"},{"start":70,"end":72,"cssClass":"pl-c1"},{"start":73,"end":88,"cssClass":"pl-s"}],[{"start":8,"end":56,"cssClass":"pl-c"}],[{"start":8,"end":16,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":19,"end":27,"cssClass":"pl-s1"},{"start":28,"end":31,"cssClass":"pl-s1"},{"start":32,"end":36,"cssClass":"pl-s1"}],[{"start":8,"end":16,"cssClass":"pl-s1"},{"start":17,"end":22,"cssClass":"pl-s1"},{"start":23,"end":24,"cssClass":"pl-c1"},{"start":26,"end":27,"cssClass":"pl-c1"}],[{"start":8,"end":16,"cssClass":"pl-s1"},{"start":17,"end":22,"cssClass":"pl-s1"},{"start":23,"end":27,"cssClass":"pl-s1"},{"start":28,"end":29,"cssClass":"pl-c1"},{"start":30,"end":40,"cssClass":"pl-s"}],[{"start":8,"end":14,"cssClass":"pl-k"},{"start":15,"end":23,"cssClass":"pl-s1"}],[],[{"start":4,"end":56,"cssClass":"pl-c"}],[{"start":4,"end":7,"cssClass":"pl-s1"},{"start":8,"end":9,"cssClass":"pl-c1"},{"start":10,"end":16,"cssClass":"pl-s"}],[{"start":4,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":20,"cssClass":"pl-s1"},{"start":21,"end":30,"cssClass":"pl-en"},{"start":31,"end":34,"cssClass":"pl-s1"}],[{"start":4,"end":12,"cssClass":"pl-s1"},{"start":13,"end":14,"cssClass":"pl-c1"},{"start":15,"end":24,"cssClass":"pl-s1"},{"start":25,"end":36,"cssClass":"pl-en"},{"start":37,"end":40,"cssClass":"pl-s1"}],[],[{"start":4,"end":18,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-k"},{"start":7,"end":18,"cssClass":"pl-s1"},{"start":19,"end":21,"cssClass":"pl-c1"},{"start":22,"end":26,"cssClass":"pl-c1"}],[{"start":8,"end":16,"cssClass":"pl-s1"},{"start":17,"end":18,"cssClass":"pl-c1"},{"start":19,"end":39,"cssClass":"pl-en"},{"start":40,"end":48,"cssClass":"pl-s1"}],[{"start":8,"end":14,"cssClass":"pl-s1"},{"start":15,"end":16,"cssClass":"pl-c1"},{"start":17,"end":23,"cssClass":"pl-s1"},{"start":24,"end":27,"cssClass":"pl-s1"},{"start":28,"end":40,"cssClass":"pl-s"},{"start":41,"end":53,"cssClass":"pl-s"}],[],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":22,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":18,"cssClass":"pl-s1"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":12,"cssClass":"pl-s"}],[],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":20,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":16,"cssClass":"pl-s1"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":12,"cssClass":"pl-s"}],[],[{"start":4,"end":23,"cssClass":"pl-c"}],[{"start":4,"end":11,"cssClass":"pl-s1"},{"start":12,"end":13,"cssClass":"pl-c1"},{"start":14,"end":24,"cssClass":"pl-en"},{"start":25,"end":31,"cssClass":"pl-s1"},{"start":31,"end":32,"cssClass":"pl-c1"},{"start":32,"end":38,"cssClass":"pl-s1"},{"start":40,"end":48,"cssClass":"pl-s1"},{"start":48,"end":49,"cssClass":"pl-c1"},{"start":49,"end":57,"cssClass":"pl-s1"}],[],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":21,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":41,"cssClass":"pl-s"}],[{"start":4,"end":9,"cssClass":"pl-en"},{"start":10,"end":17,"cssClass":"pl-s1"}],[],[],[{"start":0,"end":2,"cssClass":"pl-k"},{"start":3,"end":11,"cssClass":"pl-s1"},{"start":12,"end":14,"cssClass":"pl-c1"},{"start":15,"end":25,"cssClass":"pl-s"}],[{"start":4,"end":15,"cssClass":"pl-s1"},{"start":16,"end":17,"cssClass":"pl-c1"},{"start":18,"end":22,"cssClass":"pl-c1"}],[{"start":4,"end":20,"cssClass":"pl-en"},{"start":21,"end":32,"cssClass":"pl-s1"}]],"csv":null,"csvError":null,"dependabotInfo":{"showConfigurationBanner":false,"configFilePath":null,"networkDependabotPath":"/lilyyyg/z5416840_lectures/network/updates","dismissConfigurationNoticePath":"/settings/dismiss-notice/dependabot_configuration_notice","configurationNoticeDismissed":false,"repoAlertsPath":"/lilyyyg/z5416840_lectures/security/dependabot","repoSecurityAndAnalysisPath":"/lilyyyg/z5416840_lectures/settings/security_analysis","repoOwnerIsOrg":false,"currentUserCanAdminRepo":false},"displayName":"mk_cars.py","displayUrl":"https://github.com/lilyyyg/z5416840_lectures/blob/master/event_study/mk_cars.py?raw=true","headerInfo":{"blobSize":"8.46 KB","deleteInfo":{"deleteTooltip":"Fork this repository and delete the file"},"editInfo":{"editTooltip":"Fork this repository and edit the file"},"ghDesktopPath":"https://desktop.github.com","gitLfsPath":null,"onBranch":true,"shortPath":"aab181b","siteNavLoginPath":"/login?return_to=https%3A%2F%2Fgithub.com%2Flilyyyg%2Fz5416840_lectures%2Fblob%2Fmaster%2Fevent_study%2Fmk_cars.py","isCSV":false,"isRichtext":false,"toc":null,"lineInfo":{"truncatedLoc":"261","truncatedSloc":"205"},"mode":"file"},"image":false,"isCodeownersFile":null,"isPlain":false,"isValidLegacyIssueTemplate":false,"issueTemplateHelpUrl":"https://docs.github.com/articles/about-issue-and-pull-request-templates","issueTemplate":null,"discussionTemplate":null,"language":"Python","languageID":303,"large":false,"loggedIn":true,"newDiscussionPath":"/lilyyyg/z5416840_lectures/discussions/new","newIssuePath":"/lilyyyg/z5416840_lectures/issues/new","planSupportInfo":{"repoIsFork":null,"repoOwnedByCurrentUser":null,"requestFullPath":"/lilyyyg/z5416840_lectures/blob/master/event_study/mk_cars.py","showFreeOrgGatedFeatureMessage":null,"showPlanSupportBanner":null,"upgradeDataAttributes":null,"upgradePath":null},"publishBannersInfo":{"dismissActionNoticePath":"/settings/dismiss-notice/publish_action_from_dockerfile","dismissStackNoticePath":"/settings/dismiss-notice/publish_stack_from_file","releasePath":"/lilyyyg/z5416840_lectures/releases/new?marketplace=true","showPublishActionBanner":false,"showPublishStackBanner":false},"rawBlobUrl":"https://github.com/lilyyyg/z5416840_lectures/raw/master/event_study/mk_cars.py","renderImageOrRaw":false,"richText":null,"renderedFileInfo":null,"shortPath":null,"tabSize":8,"topBannersInfo":{"overridingGlobalFundingFile":false,"globalPreferredFundingPath":null,"repoOwner":"lilyyyg","repoName":"z5416840_lectures","showInvalidCitationWarning":false,"citationHelpUrl":"https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files","showDependabotConfigurationBanner":false,"actionsOnboardingTip":null},"truncated":false,"viewable":true,"workflowRedirectUrl":null,"symbols":{"timedOut":false,"notAnalyzed":false,"symbols":[{"name":"mk_cars_df","kind":"function","identStart":152,"identEnd":162,"extentStart":148,"extentEnd":1906,"fullyQualifiedName":"mk_cars_df","identUtf16":{"start":{"lineNumber":10,"utf16Col":4},"end":{"lineNumber":10,"utf16Col":14}},"extentUtf16":{"start":{"lineNumber":10,"utf16Col":0},"end":{"lineNumber":55,"utf16Col":19}}},{"name":"calc_car","kind":"function","identStart":1913,"identEnd":1921,"extentStart":1909,"extentEnd":3656,"fullyQualifiedName":"calc_car","identUtf16":{"start":{"lineNumber":58,"utf16Col":4},"end":{"lineNumber":58,"utf16Col":12}},"extentUtf16":{"start":{"lineNumber":58,"utf16Col":0},"end":{"lineNumber":104,"utf16Col":31}}},{"name":"expand_dates","kind":"function","identStart":3663,"identEnd":3675,"extentStart":3659,"extentEnd":6850,"fullyQualifiedName":"expand_dates","identUtf16":{"start":{"lineNumber":107,"utf16Col":4},"end":{"lineNumber":107,"utf16Col":16}},"extentUtf16":{"start":{"lineNumber":107,"utf16Col":0},"end":{"lineNumber":195,"utf16Col":13}}},{"name":"_test_mk_cars_df","kind":"function","identStart":6857,"identEnd":6873,"extentStart":6853,"extentEnd":8575,"fullyQualifiedName":"_test_mk_cars_df","identUtf16":{"start":{"lineNumber":198,"utf16Col":4},"end":{"lineNumber":198,"utf16Col":20}},"extentUtf16":{"start":{"lineNumber":198,"utf16Col":0},"end":{"lineNumber":255,"utf16Col":18}}},{"name":"_mk_example_event_df","kind":"function","identStart":7382,"identEnd":7402,"extentStart":7378,"extentEnd":7770,"fullyQualifiedName":"_mk_example_event_df","identUtf16":{"start":{"lineNumber":217,"utf16Col":8},"end":{"lineNumber":217,"utf16Col":28}},"extentUtf16":{"start":{"lineNumber":217,"utf16Col":4},"end":{"lineNumber":225,"utf16Col":23}}}]}},"copilotInfo":{"documentationUrl":"https://docs.github.com/copilot/overview-of-github-copilot/about-github-copilot-for-individuals","notices":{"codeViewPopover":{"dismissed":false,"dismissPath":"/settings/dismiss-notice/code_view_copilot_popover"}},"userAccess":{"accessAllowed":false,"hasSubscriptionEnded":false,"orgHasCFBAccess":false,"userHasCFIAccess":false,"userHasOrgs":false,"userIsOrgAdmin":false,"userIsOrgMember":false,"business":null,"featureRequestInfo":null}},"copilotAccessAllowed":false,"csrf_tokens":{"/lilyyyg/z5416840_lectures/branches":{"post":"DuyF1Xrs7WKJWDmPw_djIu2ZoFvqsaZdr0UbspTumB6idNqqtm8mfG0DRV7nLjCaNyDpLP4Ljkf3P7DeLCm4Jw"},"/repos/preferences":{"post":"fGUl_GcGU3MBnHcK16G7vYR31YyOaC7vOXcd5e_f4lswXAv-NXi75rL0ZAdHDQTbOhw5C8vPIPfkxss3vfcktw"}}},"title":"z5416840_lectures/event_study/mk_cars.py at master · lilyyyg/z5416840_lectures"}