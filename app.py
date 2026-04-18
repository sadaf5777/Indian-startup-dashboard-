import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df= pd.read_csv("cleaned_startups_unexploded_latest_less_verticals.csv")

df['date'] = pd.to_datetime(df['date'], errors='coerce')

df["years"] = df['date'].dt.year
df["years"] = df["years"].ffill().bfill().astype(int)

df["month"] = df['date'].dt.month
df["month"] = df["month"].ffill().bfill().astype(int)
def load_investor_details(investor_name):
    st.title(investor_name)
    # loads 5 most recently investments
    recently_invested=df[df['investor'].astype(str).str.contains(investor_name,case=False,na=False)].head()[['date', 'startup', 'city', 'round', 'vertical', 'amount']].sort_values("date",ascending=False)
    st.subheader(" most Recently Invested")
    st.dataframe(recently_invested)
    col1,col2=st.columns(2)
    with col1:
        st.subheader(" biggest investments")
        most_invested=df[df['investor'].str.contains(investor_name,na=False,case=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(most_invested.index, most_invested.values)
        plt.xlabel('Startups')
        plt.ylabel('amount in usd')
        st.pyplot(fig)  

    with col2:
        st.subheader(" amount invested in sectors")
        vertical_series=df[df['investor'].str.contains(investor_name,na=False,case=False)].groupby('vertical')['amount'].sum()
        vertical_series_index=vertical_series.index
        vertical_series_percentages=np.round((vertical_series/vertical_series.sum()*100).values,2).astype(str)
        labels_with_percentages=vertical_series_index+"->"+vertical_series_percentages
        fig1, ax1 = plt.subplots(figsize=(10,10))
        wedges,_,_= ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%',radius=1
    )
        plt.subplots_adjust(left=0.1, right=0.65)
        ax1.legend(
        wedges,
        labels_with_percentages,
        title="sectors with percentages",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        
    )
        
        st.pyplot(fig1)




    col1,col2=st.columns(2)
    with col1:
        st.subheader(" cities invested in")
        city_series=df[df['investor'].str.contains(investor_name,na=False,case=False)].groupby('city')['amount'].sum()
        city_series_index=city_series.index.astype(str)
        city_series_percentages=round((city_series/city_series.sum())*100,2).values.astype(str)
        labels_with_percentages_city=city_series_index+"->"+city_series_percentages
        fig2, ax2 = plt.subplots(figsize=(10,10))
        wedges, _,_=ax2.pie(city_series, labels=city_series.index, autopct='%1.1f%%',radius=1,startangle=140)
        plt.subplots_adjust(left=0.1, right=0.65)
        ax2.legend(wedges,
        
        labels_with_percentages_city,
        title="cities with percentages",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        
    )
        
        st.pyplot(fig2)






    with col2:
        st.subheader("YoY invested ")
        year_series = df[df['investor'].str.contains(investor_name,na=False,case=False)].groupby('years')['amount'].sum()
        fig3, ax3 = plt.subplots()
        ax3.plot(year_series.index,year_series.values)
        plt.ylabel("USD")
        plt.xlabel("years")
        st.pyplot(fig3)








# startup analysis
def startup_analysis(selected_startup):
    st.title("Startup funding analysis")
    col1,col2,col3,col4=st.columns(4)
    total_funded_amount=df[df["startup"].str.contains(selected_startup,na=False,case=False)]["amount"].sum()
    with col1:
        st.metric("Total funding", f"{total_funded_amount}")




def overall_analysis():
    st.title("Overall Analysis")
    total=round(df['amount'].sum())
    max_amount=round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0])
    avg_funding=round(df.groupby("startup")['amount'].sum().mean())
    all_startups=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total",f"{total} usd")

    with col2:
        st.metric("maximum amount",f"{max_amount} usd")

    with col3:
        st.metric("avg",f"{avg_funding} usd")
    
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
        plt.ylabel("Amount in usd")
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(fig4)

    else:
        temp_df=df.groupby(['years','month'])['amount'].count().reset_index()


        temp_df["x_axis"]=temp_df['month'].astype("str")+'-'+temp_df['years'].astype('str')
        fig4, ax4 = plt.subplots(figsize=(10,6))
        ax4.plot(temp_df["x_axis"],temp_df["amount"])
        plt.xlabel("Month-Year")
        plt.ylabel("Starups")
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(fig4)



    
    # most invested sectors
    st.header("most invested sectors")
    amount_invested_in_sectors=df.groupby("vertical")["amount"].sum()
    sector_index=(amount_invested_in_sectors/amount_invested_in_sectors.sum()*100).astype(str).index
    percentage=round(amount_invested_in_sectors/amount_invested_in_sectors.sum()*100,2).astype(str).values

    labels_with_percentages=sector_index + "->" +  percentage
    fig, ax = plt.subplots(figsize=(10,6))
    ax.pie(amount_invested_in_sectors, labels=amount_invested_in_sectors.index, autopct='%1.1f%%',
    startangle=90)
    ax.axis('equal') 
    ax.legend(
        
        labels_with_percentages,
        title="Startups",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    st.pyplot(fig)
    



option=st.sidebar.selectbox('select one',['overall analysis', 'startup','investor'])
if option == 'overall analysis':
       overall_analysis()

elif option == 'startup':
    selected_startup=st.sidebar.selectbox('select startup',sorted(df['startup'].str.replace('"', '', regex=False).str.replace("\\", '', regex=False).str.strip().str.lower().str.title().unique().tolist()))
    btn1=st.sidebar.button("find startup details")
    if btn1:
        startup_analysis(selected_startup)
else:
    selected_investor=st.sidebar.selectbox('select investor', sorted(set(df['investor'].astype(str).str.split(',').sum())))
    btn2=st.sidebar.button("find investor details")
    if btn2:
        load_investor_details(selected_investor)