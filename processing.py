import pandas as pd
import smtplib

df = pd.read_csv("amazon_web_scrapper_dataset.csv")

# Remove duplicate rows
df.drop_duplicates(subset="Description",keep='first',inplace=True)


# Creates column '"Rating_Handle" with a cleaner rating (only with the first three characters)
df["Rating_handle"]=df["Rating"].str[:3]

# Filter only items with reviews higher than 3rd quantile
df["Rating_handle"]=df["Rating_handle"].astype(float)#Convert the type of column Rating_Handle to float
quant3=df.Rating_handle.quantile(0.75) #Compute the 3rd quantile of the ratings for the item searched
a = df.loc[(df['Rating_handle']).apply(lambda x: x>=quant3)] #filters only items with reviews higher than 3rd quantile
df=a.loc[:, a.columns != 'Rating_handle']

#Sort by price (ascending), followed by a sort by "Number of reviews" (descending)
df2 = df.sort_values(["Price", "Number of Reviews"],
ascending = [True, False])

def send_email():
        server=smtplib.SMTP_SSL('smtp.gmail.com',587)
        server.ehlo('0.0.0.0')
        server.login('best.amazon.items.email@gmail.com','lwnkridyjdedoijc')
        subject ="Hi"
        body="Tania"
        msg=f"subject: {subject}\n\n{body}"
        server.sendmail('tania.mcosta.silva.a@gmail.com',msg)
smtp = smtplib.SMTP("localhost",25)
smtp.send_email()
#Enviar e-mail
df.to_csv('results.csv')



