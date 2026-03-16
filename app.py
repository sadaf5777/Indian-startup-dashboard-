import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("startup_cleaned.csv")
df['date']=pd.to_datetime(df['date'])
df["years"]=df['date'].dt.year.fillna(method='ffill').astype(int)
df["month"]=df['date'].dt.month.fillna(method='ffill').astype(int)
def load_investor_details(investor_name):
    st.title(investor_name)
    # loads 5 most recently investments
    recently_invested=df[df['investor'].str.contains(investor_name,na=False)].head()[['date', 'startup', 'city', 'round', 'vertical', 'amount']]
    st.subheader(" most Recently Invested")
    st.dataframe(recently_invested)
    col1,col2=st.columns(2)
    with col1:
        st.subheader(" biggest investments")
        most_invested=df[df['investor'].str.contains(investor_name)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(most_invested.index, most_invested.values)
        plt.xlabel('Startups')
        plt.ylabel('amount in Cr')
        st.pyplot(fig)  

    with col2:
        st.subheader(" amount invested in sectors")
        vertical_series=df[df['investor'].str.contains(investor_name)].groupby('vertical')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.pyplot(fig1)

    col1,col2=st.columns(2)
    with col1:
        st.subheader(" cities invested in")
        city_series=df[df['investor'].str.contains(investor_name)].groupby('city')['amount'].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(city_series, labels=city_series.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    with col2:
        st.subheader("YoY invested ")
        year_series = df[df['investor'].str.contains(investor_name)].groupby('years')['amount'].sum()
        fig3, ax3 = plt.subplots()
        ax3.plot(year_series.index,year_series.values)
        st.pyplot(fig3)




def overall_analysis():
    st.title("Overall Analysis")
    total=round(df['amount'].sum())
    max_amount=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=round(df.groupby("startup")['amount'].sum().mean())
    all_startups=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total",f"{total} cr")

    with col2:
        st.metric("maximum amount",f"{max_amount} cr")

    with col3:
        st.metric("avg",f"{avg_funding} cr")
    
    with col4:
        st.metric("allstartups",f"{all_startups}")


    
    
    
    
    st.header('Mom chart')
    selected_option=st.selectbox('select_type',['total','count'])
    if selected_option=='total':
        temp_df=df.groupby(['years','month'])['amount'].sum().reset_index()
        temp_df["x_axis"]=temp_df['month'].astype("str")+'-'+temp_df['years'].astype('str')
        fig4, ax4 = plt.subplots(figsize=(10,5))
        ax4.plot(temp_df["x_axis"],temp_df["amount"])
        plt.xlabel("Month-Year")
        plt.ylabel("Amount")
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(fig4)

    else:
        temp_df=df.groupby(['years','month'])['amount'].count().reset_index()


        temp_df["x_axis"]=temp_df['month'].astype("str")+'-'+temp_df['years'].astype('str')
        fig4, ax4 = plt.subplots(figsize=(10,5))
        ax4.plot(temp_df["x_axis"],temp_df["amount"])
        plt.xlabel("Month-Year")
        plt.ylabel("Starups")
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(fig4)
        
    





option=st.sidebar.selectbox('select one',['overall analysis', 'startup','investor'])
if option == 'overall analysis':
       overall_analysis()

elif option == 'startup':
    st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("find startup details")
    st.title("startup funding analysis")
else:
    selected_investor=st.sidebar.selectbox('select investor', sorted(set(df['investor'].str.split(',').sum())))
    btn2=st.sidebar.button("find investor details")
    if btn2:
        load_investor_details(selected_investor)