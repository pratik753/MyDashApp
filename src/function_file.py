#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import datetime as dt


# In[8]:


def changeP(x):
    if x >= 10e+6:
        x = round(x/10e+6, 1)
        x = str(x)+' Cr.'
    elif x < 10e+6 and x >= 10e+4:
        x = round(x/10e+4, 1)
        x = str(x)+' Lac.'
    elif x < 10e+4 and x >= 10e+2:
        x = round(x/10e+2, 1)
        x = str(x)+' K.'
    else:
        x = str(round(x,1))
    return x


# In[9]:


def merge_file(original, merge1, on1):
    data1 = original.copy()
    data2 = merge1.copy()
    lst_cust = data1[on1].unique()
    customer = []
    for i in lst_cust:
        if i not in list(data2[on1].unique()):
            customer.append(i)
    col = list(merge1.columns)
    Trade = ['New_'+col[-1]+'_Head']*len(customer)
    df1 = pd.DataFrame()
    df1[on1] = customer
    df1[col[-1]] = Trade
    data2 = pd.concat([data2, df1], axis=0)
    data1 = pd.merge(data1, data2, on=on1)
    data1['Date'] = pd.to_datetime(data1['Date'], format="%Y-%m-%d")
    data1.sort_values('Date', ascending=True, inplace=True)
    data1.reset_index(inplace=True, drop=True)
    return data1


# In[10]:


def CUSTOM_MONTH(data_1, axis, initial, final,data_2,no_cust='10',):#df_trade
    no_cust = str(no_cust)
    data1 = data_1.copy()
    data2 = data_2.copy()
    col1 = list(data2.columns)
    data1 = merge_file(data1, data2, col1[0])
    mon_yr = []
    for i in range(len(data1)):
        x1 = data1['Date_Month1'][i]+'-'+str(data1['Date_year'][i])
        mon_yr.append(x1)
    data1['Month_year'] = mon_yr
    ini = list(data1[data1['day'] == initial].index)[0]
    fin = list(data1[data1['day'] == final].index)[-1]
    output = data1.loc[ini:fin]
    sum_c = []
    sum_c_p = []
    sum_c_2 = []
    con = pd.DataFrame()
    for k in list(output[axis].unique()):
        x = round(output[output[axis] == k]['Amount'].sum(), 2)
        sum_c.append(x)
        sum_c_p.append(round(x*100/output['Amount'].sum(), 1))
        sum_c_2.append(changeP(x))
    con[axis] = list(output[axis].unique())
    con['Amount'] = sum_c
    con['Amount (Rs.)'] = sum_c_2
    con['Sale_Amount (%)'] = sum_c_p
    con.sort_values('Amount', ascending=False, inplace=True)
    con.reset_index(drop=True, inplace=True)
    if (no_cust).upper() == 'ALL' or int(no_cust) > len(con):
        con = con
    else:
        con = con.loc[0:int(no_cust)-1]
    output2 = pd.DataFrame()
    for j in list(output['Month_year'].unique()):
        sum_1 = []
        sum_2 = []
        sum_3 = []
        test = output[output['Month_year'] == j]
        for i in list(test[axis].unique()):
            x = round(test[test[axis] == i]['Amount'].sum(), 2)
            sum_1.append(x)
            sum_2.append(round(x*100/test['Amount'].sum(), 1))
            sum_3.append(changeP(x))
        output1 = pd.DataFrame()
        output1[axis] = list(test[axis].unique())
        output1['Amount'] = sum_1
        output1['Amount (Rs.)'] = sum_3
        output1['Sale_Amount (%)'] = sum_2
        output1['Month'] = [j]*len(sum_1)
        if (no_cust).upper() == 'ALL' or len(sum_1) < int(no_cust):
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output2 = pd.concat([output2, output1], axis=0)
        else:
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output1 = output1.loc[0:int(no_cust)-1]
            output2 = pd.concat([output2, output1], axis=0)
    mon = list(output2['Month'].unique())
    iden = list(output2[axis].unique())
    data_1=[]
    for i in mon:
        test = output2[output2['Month'] == i]
        sum1 =[]
        sum2 =[]
        for j in iden:
            x = test[test[axis] == j]['Amount (Rs.)'].values
            if len(x) == 0:
                sum1.append('0')
            else:
                sum1.append(x[0])
            x1 = test[test[axis] == j]['Sale_Amount (%)'].values
            if len(x1) == 0:
                sum2.append(0)
            else:
                sum2.append(x1[0])
        sum1.append(changeP(test['Amount'].sum()))
        sum2.append(round(np.array(sum2).sum(),1))
        data_1.append(sum1)
        data_1.append(sum2)
    data_1 = np.array(data_1)
    data_1 = data_1.transpose()
    mux = pd.MultiIndex.from_product([ mon,['Amount(Rs.)','Amount(%)']])
    new_data = pd.DataFrame(data_1,columns = mux)
    iden.append('TOTAL')
    iden = pd.Series(iden)
    new_data.set_index(iden,inplace = True)
    new_data.reset_index(inplace = True)
    new_data.rename(columns={'index':axis},inplace = True)
    return (new_data,output2, con)


# In[11]:


def MTD(data_1, axis, initial,data_2,no_cust=2):
    no_cust = str(no_cust)
    data1 = data_1.copy()
    data2 = data_2.copy()
    coln = list(data2.columns)
    data1 = merge_file(data1, data2, coln[0])
    mon_yr = []
    for i in range(len(data1)):
        x1 = str(data1['Date_Month1'][i])+'-'+str(data1['Date_year'][i])
        mon_yr.append(x1)
    data1['Month_year'] = mon_yr
    new = data1[data1['Month_year'] == initial]
    sum_c = []
    sum_c_p = []
    sum_c_2 = []
    con = pd.DataFrame()
    for k in list(new[axis].unique()):
        x = round(new[new[axis] == k]['Amount'].sum(), 2)
        sum_c.append(x)
        sum_c_p.append(round(x*100/new['Amount'].sum(), 1))
        sum_c_2.append(changeP(x))
    con[axis] = list(new[axis].unique())
    con['Amount'] = sum_c
    con['Amount (Rs.)'] = sum_c_2
    con['Sale_Amount (%)'] = sum_c_p
    con.sort_values('Amount', ascending=False, inplace=True)
    con.reset_index(drop=True, inplace=True)
    if (no_cust).upper() == 'ALL' or int(no_cust) > len(con):
        con = con
    else:
        con = con.loc[0:int(no_cust)-1]
    lst1 = list(new[axis].unique())
    amount_sum = []
    sum_3 = []
    amount_sum_per = []
    for i in lst1:
        x = round(new[new[axis] == i]['Amount'].sum(), 2)
        amount_sum.append(x)
        sum_3.append(changeP(x))
        amount_sum_per.append(round(x*100/new['Amount'].sum(), 1))
    output = pd.DataFrame()
    output[axis] = lst1
    output['Amount'] = amount_sum
    output['Amount (Rs.)'] = sum_3
    output['Sale_Amount (%)'] = amount_sum_per
    output.sort_values('Amount', ascending=False, inplace=True)
    output.reset_index(drop=True, inplace=True)
    output['Month'] = [initial]*len(lst1)
    if (no_cust).upper() == 'ALL' or len(lst1) < int(no_cust):
        output.sort_values('Amount', ascending=False, inplace=True)
        output.reset_index(drop=True, inplace=True)
    else:
        output.sort_values('Amount', ascending=False, inplace=True)
        output.reset_index(drop=True, inplace=True)
        output = output.loc[0:int(no_cust)-1]
    mon = list(output['Month'].unique())
    iden = list(output[axis].unique())
    data_1=[]
    for i in mon:
        test = output[output['Month'] == i]
        sum1 =[]
        sum2 =[]
        for j in iden:
            x = test[test[axis] == j]['Amount (Rs.)'].values
            if len(x) == 0:
                sum1.append('0')
            else:
                sum1.append(x[0])
            x1 = test[test[axis] == j]['Sale_Amount (%)'].values
            if len(x1) == 0:
                sum2.append(0)
            else:
                sum2.append(x1[0])
        sum1.append(changeP(test['Amount'].sum()))
        sum2.append(round(np.array(sum2).sum(),1))
        data_1.append(sum1)
        data_1.append(sum2)
    data_1 = np.array(data_1)
    data_1 = data_1.transpose()
    mux = pd.MultiIndex.from_product([ mon,['Amount(Rs.)','Amount(%)']])
    new_data = pd.DataFrame(data_1,columns = mux)
    iden.append('TOTAL')
    iden = pd.Series(iden)
    new_data.set_index(iden,inplace = True)
    new_data.reset_index(inplace = True)
    new_data.rename(columns={'index':axis},inplace = True)
    return (new_data,output, con)


# In[12]:


def QUARTER(data_1, axis, Qtr, year,data_2,no_cust=2):
    no_cust = str(no_cust)
    year = int(year)
    data1 = data_1.copy()
    data2 = data_2.copy()
    coln = list(data2.columns)
    data1 = merge_file(data1, data2, coln[0])
    mon_yr = []
    for i in range(len(data1)):
        x = str(data1['Date_Month1'][i])+'-'+str(data1['Date_year'][i])
        mon_yr.append(x)
    data1['Month_year'] = mon_yr
    Qtd = {'Date_month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
           'Quarter': ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q3', 'Q3', 'Q3', 'Q4', 'Q4', 'Q4']}
    Qtd_df = pd.DataFrame(Qtd)
    output = pd.merge(data1, Qtd_df, on='Date_month')
    output2 = pd.DataFrame()
    test1 = output[(output['Quarter'] == Qtr) & (output['Date_year'] == year)]
    sum_c = []
    sum_c_p = []
    sum_c_2 = []
    con = pd.DataFrame()
    for k in list(test1[axis].unique()):
        x = round(test1[test1[axis] == k]['Amount'].sum(), 2)
        sum_c.append(x)
        sum_c_p.append(round(x*100/test1['Amount'].sum(), 1))
        sum_c_2.append(changeP(x))
    con[axis] = list(test1[axis].unique())
    con['Amount'] = sum_c
    con['Amount (Rs.)'] = sum_c_2
    con['Sale_Amount (%)'] = sum_c_p
    con.sort_values('Amount', ascending=False, inplace=True)
    con.reset_index(drop=True, inplace=True)
    if (no_cust).upper() == 'ALL' or int(no_cust) > len(con):
        con = con
    else:
        con = con.loc[0:int(no_cust)-1]
    for j in list(test1['Month_year'].unique()):
        sum_1 = []
        sum_2 = []
        sum_3 = []
        test = test1[test1['Month_year'] == j]
        for k in list(test[axis].unique()):
            x = round(test[test[axis] == k]['Amount'].sum(), 2)
            sum_1.append(x)
            sum_2.append(round(x*100/test['Amount'].sum(), 1))
            sum_3.append(changeP(x))
        output1 = pd.DataFrame()
        output1[axis] = list(test[axis].unique())
        output1['Amount'] = sum_1
        output1['Amount (Rs.)'] = sum_3
        output1['Sale_Amount (%)'] = sum_2
        output1['Month'] = [j]*len(sum_1)
        if (no_cust).upper() == 'ALL' or len(sum_1) < int(no_cust):
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output2 = pd.concat([output2, output1], axis=0)
        else:
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output1 = output1.loc[0:int(no_cust)-1]
            output2 = pd.concat([output2, output1], axis=0)
    mon = list(output2['Month'].unique())
    iden = list(output2[axis].unique())
    data_1=[]
    for i in mon:
        test = output2[output2['Month'] == i]
        sum1 =[]
        sum2 =[]
        for j in iden:
            x = test[test[axis] == j]['Amount (Rs.)'].values
            if len(x) == 0:
                sum1.append('0')
            else:
                sum1.append(x[0])
            x1 = test[test[axis] == j]['Sale_Amount (%)'].values
            if len(x1) == 0:
                sum2.append(0)
            else:
                sum2.append(x1[0])
        sum1.append(changeP(test['Amount'].sum()))
        sum2.append(round(np.array(sum2).sum(),1))
        data_1.append(sum1)
        data_1.append(sum2)
    data_1 = np.array(data_1)
    data_1 = data_1.transpose()
    mux = pd.MultiIndex.from_product([ mon,['Amount(Rs.)','Amount(%)']])
    new_data = pd.DataFrame(data_1,columns = mux)
    iden.append('TOTAL')
    iden = pd.Series(iden)
    new_data.set_index(iden,inplace = True)
    new_data.reset_index(inplace = True)
    new_data.rename(columns={'index':axis},inplace = True)
    return (new_data,output2, con)


# In[13]:


def PAST_6_12_MON(data_1, axis,data_2,step=6,no_cust=2):
    no_cust = str(no_cust)
    data1 = data_1.copy()
    data2 = data_2.copy()
    coln = list(data2.columns)
    data1 = merge_file(data1, data2, coln[0])
    mon_yr = []
    for i in range(len(data1)):
        x = str(data1['Date_month'][i])+'-'+str(data1['Date_year'][i])
        mon_yr.append(x)
    data1['Month_year'] = mon_yr
    month1 = dt.datetime.now().month
    year1 = dt.datetime.now().year
    if (str(month1)+'-'+str(year1)) not in (data1['Month_year'].unique()):
        month1 = data1['Date_month'][len(data1)-1]
        year1 = data1['Date_year'][len(data1)-1]
    month2 = month1 - step + 1
    year2 = dt.datetime.now().year
    if month2 <= 0:
        month2 = 12+month2
        year2 = year1-1
    if ((str(month2)+'-'+str(year2)) not in list(data1['Month_year'].unique())):
        month2 = data1['Date_month'][0]
        year2 = data1['Date_year'][0]
    fin1 = (str(month1)+'-'+str(year1))
    ini1 = (str(month2)+'-'+str(year2))
    mon_yr1 = []
    for i in range(len(data1)):
        x1 = data1['Date_Month1'][i]+'-'+str(data1['Date_year'][i])
        mon_yr1.append(x1)
    data1['Month_year1'] = mon_yr1
    ini = list(data1[data1['Month_year'] == ini1].index)[0]
    fin = list(data1[data1['Month_year'] == fin1].index)[-1]
    data1.drop(['Month_year'], axis=1, inplace=True)
    output = data1.loc[ini:fin]
    sum_c = []
    sum_c_p = []
    sum_c_2 = []
    con = pd.DataFrame()
    for k in list(output[axis].unique()):
        x = round(output[output[axis] == k]['Amount'].sum(), 2)
        sum_c.append(x)
        sum_c_p.append(round(x*100/output['Amount'].sum(), 1))
        sum_c_2.append(changeP(x))
    con[axis] = list(output[axis].unique())
    con['Amount'] = sum_c
    con['Amount (Rs.)'] = sum_c_2
    con['Sale_Amount (%)'] = sum_c_p
    con.sort_values('Amount', ascending=False, inplace=True)
    con.reset_index(drop=True, inplace=True)
    if (no_cust).upper() == 'ALL' or int(no_cust) > len(con):
        con = con
    else:
        con = con.loc[0:int(no_cust)-1]
    output2 = pd.DataFrame()
    for j in list(output['Month_year1'].unique()):
        sum_1 = []
        sum_2 = []
        sum_3 = []
        test = output[output['Month_year1'] == j]
        for i in list(test[axis].unique()):
            x = round(test[test[axis] == i]['Amount'].sum(), 2)
            sum_1.append(x)
            sum_2.append(round(x*100/test['Amount'].sum(), 1))
            sum_3.append(changeP(x))
        output1 = pd.DataFrame()
        output1[axis] = list(test[axis].unique())
        output1['Amount'] = sum_1
        output1['Amount (Rs.)'] = sum_3
        output1['Sale_Amount (%)'] = sum_2
        output1['Month'] = [j]*len(sum_1)
        if (no_cust).upper() == 'ALL' or len(sum_1) < int(no_cust):
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output2 = pd.concat([output2, output1], axis=0)
        else:
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output1 = output1.loc[0:int(no_cust)-1]
            output2 = pd.concat([output2, output1], axis=0)
    mon = list(output2['Month'].unique())
    iden = list(output2[axis].unique())
    data_1=[]
    for i in mon:
        test = output2[output2['Month'] == i]
        sum1 =[]
        sum2 =[]
        for j in iden:
            x = test[test[axis] == j]['Amount (Rs.)'].values
            if len(x) == 0:
                sum1.append('0')
            else:
                sum1.append(x[0])
            x1 = test[test[axis] == j]['Sale_Amount (%)'].values
            if len(x1) == 0:
                sum2.append(0)
            else:
                sum2.append(x1[0])
        sum1.append(changeP(test['Amount'].sum()))
        sum2.append(round(np.array(sum2).sum(),1))
        data_1.append(sum1)
        data_1.append(sum2)
    data_1 = np.array(data_1)
    data_1 = data_1.transpose()
    mux = pd.MultiIndex.from_product([ mon,['Amount(Rs.)','Amount(%)']])
    new_data = pd.DataFrame(data_1,columns = mux)
    iden.append('TOTAL')
    iden = pd.Series(iden)
    new_data.set_index(iden,inplace = True)
    new_data.reset_index(inplace = True)
    new_data.rename(columns={'index':axis},inplace = True)
    return (new_data,output2, con)


# In[ ]:




